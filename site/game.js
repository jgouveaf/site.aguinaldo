const startForm = document.querySelector('#start-form');
const playGame = document.querySelector('#play-game');
const startButton = document.querySelector('#start-button');
const questionStage = document.querySelector('#question-stage');
const resultStage = document.querySelector('#result-stage');
const gameStatus = document.querySelector('#game-status');
const optionButtons = [...document.querySelectorAll('#options button')];
const quitButton = document.querySelector('#quit-button');
const playAgain = document.querySelector('#play-again');
const modeOptions = document.querySelector('#mode-options');
const ladder = document.querySelector('#prize-ladder');
const modeLabels = {
  'Desafio Python': {name:'Clássico', icon:'✦', detail:'9 perguntas · 3 por nível', tag:'O desafio original', prizes:[0,1000,5000,10000,25000,50000,100000,200000,500000,1000000]},
  'Desafio Rápido': {name:'Rápido', icon:'ϟ', detail:'6 perguntas · 2 por nível', tag:'Direto ao milhão', prizes:[0,2000,10000,50000,200000,500000,1000000]},
  'Maratona do Milhão': {name:'Maratona', icon:'★', detail:'15 perguntas · 5 por nível', tag:'Para quem sabe tudo', prizes:[0,500,1000,2500,5000,10000,20000,40000,75000,125000,200000,300000,450000,600000,800000,1000000]},
};
let selectedMode = modeLabels['Desafio Python'];
let current = null;
let playingGameId = '';
let busy = false;

const reais = value => new Intl.NumberFormat('pt-BR', {style:'currency', currency:'BRL'}).format(value);
const tempo = seconds => {
  const total = Math.floor(Number(seconds));
  return `${String(Math.floor(total / 60)).padStart(2, '0')}:${String(total % 60).padStart(2, '0')}`;
};

async function gameRequest(body) {
  const url = window.SUPABASE_URL.replace(/\/$/, '') + '/functions/v1/web-game';
  const response = await fetch(url, {
    method: 'POST',
    headers: {'apikey': window.SUPABASE_PUBLIC_KEY, 'Content-Type': 'application/json'},
    body: JSON.stringify(body),
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || `Falha de conexão (HTTP ${response.status}).`);
  return data;
}

function setBusy(value) {
  busy = value;
  startButton.disabled = value || !playGame.value;
  optionButtons.forEach(button => { button.disabled = value; });
  modeOptions.querySelectorAll('button').forEach(button => {button.disabled = value;});
  quitButton.disabled = value;
}

function updateLadder(acertos, finished = false) {
  for (const item of document.querySelectorAll('#prize-ladder li')) {
    const step = Number(item.dataset.step);
    item.classList.toggle('done', step <= acertos);
    item.classList.toggle('current', !finished && step === acertos + 1);
  }
}

function renderLadder(prizes, name) {
  ladder.replaceChildren();
  for (let step = prizes.length - 1; step >= 1; step--) {
    const item = document.createElement('li');
    item.dataset.step = step;
    const label = document.createElement('span');
    label.textContent = `${String(step).padStart(2,'0')}  •  ${step}º acerto`;
    const value = document.createElement('strong');
    value.textContent = reais(prizes[step]);
    item.append(label, value);
    ladder.append(item);
  }
  document.querySelector('#ladder-mode').textContent = name.toUpperCase();
  updateLadder(0);
}

function showState(data) {
  current = data;
  renderLadder(data.prizes, selectedMode.name);
  gameStatus.textContent = '';
  startForm.hidden = true;
  if (data.finished) {
    questionStage.hidden = true;
    resultStage.hidden = false;
    const result = data.result;
    const message = result.motivo_encerramento === 'concluiu'
      ? `Parabéns! Você acertou as ${data.total} perguntas.`
      : result.motivo_encerramento === 'desistencia'
        ? 'Você decidiu encerrar a partida.'
        : `A partida terminou em uma resposta incorreta${data.correct_answer ? `. A resposta certa era ${data.correct_answer}.` : '.'}`;
    document.querySelector('#result-title').textContent = message;
    document.querySelector('#result-detail').textContent = `${result.acertos} acerto(s) · prêmio fictício`;
    document.querySelector('#result-prize').textContent = reais(result.valor_ganho);
    document.querySelector('#result-time').textContent = `Tempo da partida: ${tempo(result.tempo_segundos)}`;
    updateLadder(result.acertos, true);
    window.dispatchEvent(new CustomEvent('ranking-refresh', {detail: {gameId: playingGameId}}));
    return;
  }
  resultStage.hidden = true;
  questionStage.hidden = false;
  document.querySelector('#question-count').textContent = `Questão ${data.index + 1} de ${data.total}`;
  document.querySelector('#question-level').textContent = ({facil:'Fácil',media:'Média',dificil:'Difícil'})[data.difficulty];
  document.querySelector('#progress-fill').style.width = `${(data.index / data.total) * 100}%`;
  document.querySelector('#question-prize').textContent = reais(data.prizes[data.index + 1]);
  document.querySelector('#question-text').textContent = data.question.enunciado;
  for (const button of optionButtons) {
    button.querySelector('span').textContent = data.question[`alternativa_${button.dataset.answer.toLowerCase()}`];
  }
  updateLadder(data.index);
}

window.addEventListener('games-loaded', event => {
  playGame.replaceChildren();
  modeOptions.replaceChildren();
  for (const game of event.detail) {
    const mode = modeLabels[game.nome];
    if (!mode) continue;
    const option = document.createElement('option');
    option.value = game.id;
    option.textContent = game.nome;
    playGame.append(option);
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'mode-choice';
    button.dataset.gameId = game.id;
    button.setAttribute('aria-pressed', 'false');
    const icon = document.createElement('span'); icon.className = 'mode-icon'; icon.textContent = mode.icon;
    const body = document.createElement('span'); body.className = 'mode-copy';
    const title = document.createElement('strong'); title.textContent = mode.name;
    const detail = document.createElement('small'); detail.textContent = mode.detail;
    const tag = document.createElement('em'); tag.textContent = mode.tag;
    body.append(title, detail, tag);
    button.append(icon, body);
    button.addEventListener('click', () => {
      playGame.value = game.id;
      selectedMode = mode;
      modeOptions.querySelectorAll('button').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
      renderLadder(mode.prizes, mode.name);
    });
    modeOptions.append(button);
  }
  const first = modeOptions.querySelector('button');
  if (first) first.click();
  playGame.disabled = !first;
  startButton.disabled = !first;
});

startForm.addEventListener('submit', async event => {
  event.preventDefault();
  if (busy) return;
  const nickname = document.querySelector('#nickname').value.trim();
  if (!nickname || !playGame.value) { gameStatus.textContent = 'Informe um apelido e escolha o jogo.'; return; }
  playingGameId = playGame.value;
  setBusy(true);
  gameStatus.textContent = 'Preparando as perguntas…';
  try {
    showState(await gameRequest({action:'start', nickname, game_id:playingGameId}));
  } catch (error) { gameStatus.textContent = error.message; }
  finally { setBusy(false); }
});

async function sendAnswer(choice) {
  if (busy || !current || current.finished) return;
  setBusy(true);
  gameStatus.textContent = 'Conferindo resposta…';
  try {
    showState(await gameRequest({action:'answer', session_id:current.session_id, index:current.index, choice}));
  } catch (error) { gameStatus.textContent = error.message; }
  finally { setBusy(false); }
}

optionButtons.forEach(button => button.addEventListener('click', () => sendAnswer(button.dataset.answer)));
quitButton.addEventListener('click', () => sendAnswer('S'));
playAgain.addEventListener('click', () => {
  current = null;
  resultStage.hidden = true;
  questionStage.hidden = true;
  startForm.hidden = false;
  gameStatus.textContent = '';
  renderLadder(selectedMode.prizes, selectedMode.name);
  document.querySelector('#nickname').focus();
});
renderLadder(selectedMode.prizes, selectedMode.name);
