const gameSelect = document.querySelector('#game');
const refreshButton = document.querySelector('#refresh');
const status = document.querySelector('#status');
const table = document.querySelector('#ranking');
const tbody = table.querySelector('tbody');
const feedback = document.querySelector('#feedback');
const stats = document.querySelector('#stats');
const playersCount = document.querySelector('#players-count');
const topPrize = document.querySelector('#top-prize');
const updatedAt = document.querySelector('#updated-at');
const podium = document.querySelector('#podium');

const money = value => new Intl.NumberFormat('pt-BR', {style:'currency', currency:'BRL'}).format(value);
const duration = value => {
  const total = Math.floor(Number(value));
  return `${String(Math.floor(total / 60)).padStart(2,'0')}:${String(total % 60).padStart(2,'0')}`;
};
const date = value => new Intl.DateTimeFormat('pt-BR', {dateStyle:'short', timeStyle:'short'}).format(new Date(value));

async function api(path, options = {}) {
  const url = window.SUPABASE_URL;
  const key = window.SUPABASE_PUBLIC_KEY;
  if (!url || url.includes('SEU-PROJETO') || !key || key === 'SUA_CHAVE_PUBLICA') {
    throw new Error('Configure site/config.js com a URL e a chave pública do Supabase.');
  }
  const response = await fetch(`${url.replace(/\/$/,'')}/rest/v1/${path}`, {
    ...options,
    headers: {'apikey':key, 'Content-Type':'application/json', ...(options.headers || {})},
  });
  if (!response.ok) throw new Error(`Consulta indisponível (HTTP ${response.status}).`);
  return response.json();
}

async function loadGames() {
  status.textContent = 'Carregando jogos do banco de dados…';
  const games = await api('jogos?select=id,nome&order=nome.asc');
  const order = {'Desafio Python':0, 'Desafio Rápido':1, 'Maratona do Milhão':2};
  games.sort((a,b) => (order[a.nome] ?? 99) - (order[b.nome] ?? 99));
  gameSelect.replaceChildren();
  for (const game of games) {
    const option = document.createElement('option');
    option.value = game.id;
    option.textContent = game.nome;
    gameSelect.append(option);
  }
  gameSelect.disabled = !games.length;
  refreshButton.disabled = !games.length;
  window.dispatchEvent(new CustomEvent('games-loaded', {detail: games}));
  if (!games.length) status.textContent = 'Nenhum jogo cadastrado no banco.';
  else await loadRanking();
}

async function loadRanking() {
  tbody.replaceChildren();
  podium.replaceChildren();
  podium.hidden = true;
  table.hidden = true;
  stats.hidden = true;
  feedback.hidden = false;
  if (!gameSelect.value) return;
  status.textContent = 'Atualizando ranking…';
  try {
    const rows = await api('rpc/ranking_public', {method:'POST', body:JSON.stringify({p_jogo_id:gameSelect.value})});
    if (!rows.length) { status.textContent = 'Ainda não há resultados para este jogo.'; return; }
    for (const row of rows.slice(0, 3)) {
      const card = document.createElement('article');
      card.className = `podium-card position-${row.posicao}`;
      const medal = document.createElement('span'); medal.className = 'podium-medal'; medal.textContent = ['✦','Ⅱ','Ⅲ'][row.posicao - 1];
      const place = document.createElement('small'); place.textContent = `${row.posicao}º LUGAR`;
      const name = document.createElement('strong'); name.textContent = row.apelido;
      const prize = document.createElement('b'); prize.textContent = money(row.valor_ganho);
      const time = document.createElement('span'); time.className = 'podium-time'; time.textContent = `◷ ${duration(row.tempo_segundos)}`;
      card.append(medal, place, name, prize, time);
      podium.append(card);
    }
    podium.hidden = false;
    for (const row of rows) {
      const tr = document.createElement('tr');
      for (const value of [`#${String(row.posicao).padStart(2,'0')}`, row.apelido, money(row.valor_ganho), duration(row.tempo_segundos), date(row.data_hora)]) {
        const td = document.createElement('td');
        td.textContent = value;
        tr.append(td);
      }
      tbody.append(tr);
    }
    playersCount.textContent = rows.length;
    topPrize.textContent = money(rows[0].valor_ganho);
    updatedAt.textContent = new Intl.DateTimeFormat('pt-BR', {hour:'2-digit', minute:'2-digit'}).format(new Date());
    stats.hidden = false;
    table.hidden = false;
    feedback.hidden = true;
    status.textContent = `${rows.length} jogador(es) exibido(s).`;
  } catch (error) { status.textContent = `Falha ao consultar ranking: ${error.message}`; }
}

gameSelect.addEventListener('change', loadRanking);
refreshButton.addEventListener('click', loadRanking);
window.addEventListener('ranking-refresh', event => {
  if (event.detail?.gameId) gameSelect.value = event.detail.gameId;
  loadRanking();
});
loadGames().catch(error => { status.textContent = `Falha ao carregar jogos: ${error.message}`; });
