const startForm = document.querySelector('#start-form');
const playGame = document.querySelector('#play-game');
const startButton = document.querySelector('#start-button');
const questionStage = document.querySelector('#question-stage');
const resultStage = document.querySelector('#result-stage');
const gameStatus = document.querySelector('#game-status');
const optionButtons = [...document.querySelectorAll('#options button')];
const quitButton = document.querySelector('#quit-button');
const playAgain = document.querySelector('#play-again');
const prizeSteps = [1000, 5000, 10000, 25000, 50000, 100000, 200000, 500000, 1000000];
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
  quitButton.disabled = value;
}

function updateLadder(acertos, finished = false) {
  for (const item of document.querySelectorAll('#prize-ladder li')) {
    const step = Number(item.dataset.step);
    item.classList.toggle('done', step <= acertos);
    item.classList.toggle('current', !finished && step === acertos + 1);
  }
}

function showState(data) {
  current = data;
  gameStatus.textContent = '';
  startForm.hidden = true;
  if (data.finished) {
    questionStage.hidden = true;
    resultStage.hidden = false;
    const result = data.result;
    const message = result.motivo_encerramento === 'concluiu'
      ? 'Parabéns! Você acertou as nove perguntas.'
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
  document.querySelector('#question-count').textContent = `Questão ${data.index + 1} de 9`;
  document.querySelector('#question-level').textContent = ({facil:'Fácil',media:'Média',dificil:'Difícil'})[data.difficulty];
  document.querySelector('#progress-fill').style.width = `${(data.index / 9) * 100}%`;
  document.querySelector('#question-prize').textContent = reais(prizeSteps[data.index]);
  document.querySelector('#question-text').textContent = data.question.enunciado;
  for (const button of optionButtons) {
    button.querySelector('span').textContent = data.question[`alternativa_${button.dataset.answer.toLowerCase()}`];
  }
  updateLadder(data.index);
}

window.addEventListener('games-loaded', event => {
  playGame.replaceChildren();
  for (const game of event.detail) {
    const option = document.createElement('option');
    option.value = game.id;
    option.textContent = game.nome;
    playGame.append(option);
  }
  playGame.disabled = !event.detail.length;
  startButton.disabled = !event.detail.length;
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
  updateLadder(0);
  document.querySelector('#nickname').focus();
});
updateLadder(0);
