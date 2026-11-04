const url = Deno.env.get('SUPABASE_URL') ?? '';
const secret = JSON.parse(Deno.env.get('SUPABASE_SECRET_KEYS') ?? '{}').default;
const publicKeys = Object.values(JSON.parse(Deno.env.get('SUPABASE_PUBLISHABLE_KEYS') ?? '{}'));
const modes = {
  'Desafio Python': {id: 'classico', perLevel: 3, prizes: [0, 1000, 5000, 10000, 25000, 50000, 100000, 200000, 500000, 1000000]},
  'Desafio Rápido': {id: 'rapido', perLevel: 2, prizes: [0, 2000, 10000, 50000, 200000, 500000, 1000000]},
  'Maratona do Milhão': {id: 'maratona', perLevel: 5, prizes: [0, 500, 1000, 2500, 5000, 10000, 20000, 40000, 75000, 125000, 200000, 300000, 450000, 600000, 800000, 1000000]},
} as const;
const levels = ['facil', 'media', 'dificil'];
const uuidPattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'apikey, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};

function reply(body, status = 200) {
  return new Response(JSON.stringify(body), {status, headers: {...cors, 'Content-Type': 'application/json'}});
}

async function db(path, method = 'GET', data) {
  const response = await fetch(`${url}/rest/v1/${path}`, {
    method,
    headers: {
      apikey: secret,
      'Content-Type': 'application/json',
      Prefer: 'return=representation',
    },
    body: data === undefined ? undefined : JSON.stringify(data),
  });
  if (!response.ok) {
    console.error('Database request failed', response.status, await response.text());
    throw new Error('Falha na consulta ao banco de dados.');
  }
  return response.json();
}

function pickQuestions(items, count) {
  const copy = [...items];
  for (let i = copy.length - 1; i > 0; i--) {
    const random = new Uint32Array(1);
    crypto.getRandomValues(random);
    const j = random[0] % (i + 1);
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy.slice(0, count);
}

function modeForName(name: string) {
  return modes[name as keyof typeof modes];
}

function modeForId(id: string) {
  return Object.values(modes).find(mode => mode.id === id);
}

async function question(id) {
  const rows = await db(`perguntas?select=id,enunciado,alternativa_a,alternativa_b,alternativa_c,alternativa_d&id=eq.${id}&limit=1`);
  if (!rows.length) throw new Error('Pergunta não encontrada.');
  return rows[0];
}

async function state(session, correctAnswer) {
  const mode = modeForId(session.modo);
  if (!mode) throw new Error('Modo não encontrado.');
  const common = {mode: mode.id, total: mode.prizes.length - 1, prizes: mode.prizes};
  if (session.motivo) {
    const rows = await db(`partidas?select=id,apelido,valor_ganho,tempo_segundos,acertos,motivo_encerramento&id=eq.${session.id}&limit=1`);
    return {...common, finished: true, result: rows[0], correct_answer: correctAnswer ?? null};
  }
  return {
    finished: false,
    session_id: session.id,
    index: session.indice,
    prize: session.valor_ganho,
    difficulty: levels[Math.floor(session.indice / mode.perLevel)],
    ...common,
    question: await question(session.pergunta_ids[session.indice]),
  };
}

async function start(body) {
  const nickname = String(body.nickname ?? '').trim();
  const gameId = String(body.game_id ?? '');
  if (!nickname || nickname.length > 30 || !uuidPattern.test(gameId)) {
    return reply({error: 'Informe um apelido de 1 a 30 caracteres e escolha um jogo.'}, 400);
  }
  const games = await db(`jogos?select=id,nome&id=eq.${gameId}&limit=1`);
  if (!games.length) return reply({error: 'Jogo não encontrado.'}, 404);
  const mode = modeForName(games[0].nome);
  if (!mode) return reply({error: 'Modo não configurado.'}, 400);
  const ids = [];
  for (const level of levels) {
    const pool = await db(`perguntas?select=id&dificuldade=eq.${level}`);
    if (pool.length < mode.perLevel) return reply({error: `Faltam perguntas de dificuldade ${level}.`}, 503);
    ids.push(...pickQuestions(pool, mode.perLevel).map(item => item.id));
  }
  const rows = await db('sessoes_web', 'POST', [{jogo_id: gameId, apelido: nickname, modo: mode.id, pergunta_ids: ids}]);
  return reply(await state(rows[0]));
}

async function answer(body) {
  const id = String(body.session_id ?? '');
  const index = Number(body.index);
  const choice = String(body.choice ?? '').toUpperCase();
  if (!uuidPattern.test(id) || !Number.isInteger(index) || index < 0 || index > 14 || !['A','B','C','D','S'].includes(choice)) {
    return reply({error: 'Resposta inválida.'}, 400);
  }
  const sessions = await db(`sessoes_web?select=*&id=eq.${id}&limit=1`);
  if (!sessions.length) return reply({error: 'Partida não encontrada.'}, 404);
  const session = sessions[0];
  const mode = modeForId(session.modo);
  if (!mode) return reply({error: 'Modo não encontrado.'}, 400);
  if (session.motivo || session.indice !== index) return reply(await state(session));
  const elapsed = body.elapsed_seconds;
  if (elapsed !== undefined && (typeof elapsed !== 'number' || !Number.isFinite(elapsed)
      || elapsed < (session.tempo_ativo_segundos ?? 0) || elapsed > 999999999)) {
    return reply({error: 'Tempo de jogo inválido.'}, 400);
  }
  let patch;
  let correctAnswer = null;
  if (choice === 'S') {
    patch = {motivo: 'desistencia', encerrada_em: new Date().toISOString()};
  } else {
    const rows = await db(`perguntas?select=correta&id=eq.${session.pergunta_ids[index]}&limit=1`);
    if (!rows.length) throw new Error('Pergunta não encontrada.');
    if (choice !== rows[0].correta) {
      correctAnswer = rows[0].correta;
      patch = {motivo: 'erro', encerrada_em: new Date().toISOString()};
    } else {
      const next = index + 1;
      patch = {indice: next, valor_ganho: mode.prizes[next]};
      if (next === mode.prizes.length - 1) Object.assign(patch, {motivo: 'concluiu', encerrada_em: new Date().toISOString()});
    }
  }
  if (elapsed !== undefined) Object.assign(patch, {tempo_ativo_segundos: elapsed});
  const updated = await db(`sessoes_web?id=eq.${id}&indice=eq.${index}&motivo=is.null`, 'PATCH', patch);
  if (!updated.length) {
    const fresh = await db(`sessoes_web?select=*&id=eq.${id}&limit=1`);
    return reply(await state(fresh[0]));
  }
  return reply(await state(updated[0], correctAnswer));
}

Deno.serve(async request => {
  if (request.method === 'OPTIONS') return new Response(null, {status: 204, headers: cors});
  if (request.method !== 'POST') return reply({error: 'Método não permitido.'}, 405);
  if (!publicKeys.includes(request.headers.get('apikey'))) return reply({error: 'Chave pública inválida.'}, 401);
  try {
    const body = await request.json();
    if (body.action === 'start') return await start(body);
    if (body.action === 'answer') return await answer(body);
    return reply({error: 'Ação inválida.'}, 400);
  } catch (error) {
    console.error(error);
    return reply({error: 'Não foi possível processar a partida. Tente novamente.'}, 503);
  }
});
