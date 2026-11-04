"""Jogo do milhão no terminal, conectado ao mesmo Supabase do site."""
from __future__ import annotations

import json
import http.client
import os
import ssl
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass

# Garante suporte a UTF-8 sem erros em qualquer terminal Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DEFAULT_URL = "https://yserkieipgjqjciouole.supabase.co"
# Chave pública: também aparece no site. Nunca use uma chave secreta aqui.
DEFAULT_PUBLIC_KEY = "sb_publishable_VE02WYLJhwREVcuLdI1DUw_o37Ixx7m"
PRIZES = [1000, 5000, 10000, 25000, 50000, 100000, 200000, 500000, 1000000]
LEVEL_NAMES = {"facil": "Fácil", "media": "Média", "dificil": "Difícil"}

# Cores ANSI para enriquecimento visual do terminal
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
BLUE = "\033[1;34m"
MAGENTA = "\033[1;35m"
WHITE = "\033[1;37m"
GOLD = "\033[38;5;220m"


def setup_terminal():
    """Ativa sequências ANSI no Windows Terminal / prompt."""
    if os.name == "nt":
        os.system("")


def play_sound(effect: str):
    """Efeito sonoro sutil opcional no Windows (sem dependências externas)."""
    try:
        import winsound
        if effect == "correct":
            winsound.Beep(880, 100)
            winsound.Beep(1174, 150)
        elif effect == "wrong":
            winsound.Beep(330, 250)
        elif effect == "win":
            for freq in (587, 740, 880, 1174):
                winsound.Beep(freq, 120)
    except Exception:
        pass


class GameError(Exception):
    """Falha de rede ou resposta inválida do serviço de jogo."""


class GameClient:
    def __init__(self, url: str = DEFAULT_URL, public_key: str = DEFAULT_PUBLIC_KEY):
        self.url = url.rstrip("/")
        self.key = public_key
        if not self.url.startswith("https://") or not self.key:
            raise ValueError("Configure SUPABASE_URL e SUPABASE_PUBLIC_KEY.")
        self.tls_context = ssl.create_default_context()
        # Compatibilidade com cadeias Windows sem Authority Key Identifier.
        # CA e nome do servidor continuam sendo verificados.
        self.tls_context.verify_flags &= ~ssl.VERIFY_X509_STRICT

    def request(self, path: str, data=None):
        body = None if data is None else json.dumps(data).encode("utf-8")
        request = urllib.request.Request(
            self.url + path,
            data=body,
            method="POST" if body is not None else "GET",
            headers={"apikey": self.key, "Content-Type": "application/json", "Accept": "application/json"},
        )
        for attempt in range(3):
            try:
                with urllib.request.urlopen(request, timeout=15, context=self.tls_context) as response:
                    return json.loads(response.read())
            except urllib.error.HTTPError as exc:
                try:
                    message = json.loads(exc.read()).get("error", f"HTTP {exc.code}")
                except (ValueError, OSError):
                    message = f"HTTP {exc.code}"
                raise GameError(message) from exc
            except (urllib.error.URLError, TimeoutError, ConnectionError, OSError,
                    http.client.HTTPException, ValueError) as exc:
                if attempt == 2:
                    raise GameError("Falha de conexão com o Supabase. Verifique a internet e tente novamente.") from exc
                time.sleep(0.4 * (attempt + 1))

    def games(self):
        return self.request("/rest/v1/jogos?select=id,nome&order=nome.asc")

    def ranking(self, game_id):
        return self.request("/rest/v1/rpc/ranking_public", {"p_jogo_id": game_id})

    def start(self, nickname, game_id):
        return self.request("/functions/v1/web-game", {"action": "start", "nickname": nickname, "game_id": game_id})

    def answer(self, session_id, index, choice, elapsed):
        return self.request("/functions/v1/web-game", {
            "action": "answer", "session_id": session_id, "index": index, "choice": choice,
            "elapsed_seconds": elapsed,
        })


@dataclass
class PendingGame:
    nickname: str
    game_id: str
    state: dict
    elapsed_seconds: float = 0.0
    answer: str | None = None


def calculate_prize(correct_count, prizes=None):
    """O prêmio substitui o anterior; nunca somamos as etapas."""
    ladder = prizes if prizes is not None else [0, *PRIZES]
    if not 0 <= correct_count < len(ladder):
        raise ValueError("Quantidade de acertos inválida.")
    return ladder[correct_count]


def fetch_questions(client, nickname, game_id):
    """Inicia o sorteio online. A API entrega uma pergunta por vez, sem gabarito."""
    return client.start(nickname, game_id)


def save_answer(client, pending):
    """Reutiliza sessão, índice, resposta e tempo; a última resposta salva a partida."""
    state = pending.state
    return client.answer(state['session_id'], state['index'], pending.answer,
                         round(pending.elapsed_seconds, 3))


def money(amount: int) -> str:
    return "R$ " + f"{amount:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")


def duration(seconds: float) -> str:
    total = int(seconds)
    return f"{total // 60:02d}:{total % 60:02d}"


def ask_nickname(input_fn=input, print_fn=print):
    while True:
        prompt_text = f"{CYAN}➜ Digite seu apelido:{RESET} " if print_fn is print else "Apelido: "
        name = input_fn(prompt_text).strip()
        if 1 <= len(name) <= 30:
            return name
        print_fn(f"{YELLOW}Digite um apelido de 1 a 30 caracteres.{RESET}" if print_fn is print else "Digite um apelido de 1 a 30 caracteres.")


def choose_game(games, input_fn=input, print_fn=print):
    if not games:
        raise GameError("Nenhum jogo cadastrado no banco.")
    if len(games) == 1:
        print_fn(f"Jogo: {games[0]['nome']}")
        return games[0]
    
    if print_fn is print:
        print_fn(f"\n{CYAN}┌──────────────────────────────────────────────┐{RESET}")
        print_fn(f"{CYAN}│             MODOS DE JOGO DISPONÍVEIS        │{RESET}")
        print_fn(f"{CYAN}└──────────────────────────────────────────────┘{RESET}")
        for i, item in enumerate(games, 1):
            print_fn(f"  {YELLOW}{i}){RESET} {WHITE}{item['nome']}{RESET}")
    else:
        for i, item in enumerate(games, 1):
            print_fn(f"{i}) {item['nome']}")

    while True:
        choice = input_fn("Número do jogo: " if print_fn is not print else f"{CYAN}Escolha o modo (número):{RESET} ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(games):
            return games[int(choice) - 1]
        print_fn("Escolha um número da lista.")


def show_question(state, print_fn=print):
    index = state["index"]
    question = state["question"]
    total = state.get("total", 9)
    prizes = state.get("prizes", [0, *PRIZES])
    prize_val = money(prizes[index + 1])
    diff_key = state.get("difficulty", "facil")
    diff_name = LEVEL_NAMES.get(diff_key, "Fácil")

    if print_fn is print:
        diff_color = GREEN if diff_key == "facil" else (YELLOW if diff_key == "media" else RED)
        banner_border = "─" * 60
        print_fn(f"\n{CYAN}┌{banner_border}┐{RESET}")
        print_fn(f"{CYAN}│{RESET}  {BOLD}Questão {index + 1}/{total}{RESET}  •  {diff_color}[{diff_name.upper()}]{RESET}  •  {GOLD}Valendo: {prize_val}{RESET}")
        print_fn(f"{CYAN}├{banner_border}┤{RESET}")
        print_fn(f"{CYAN}│{RESET}  {WHITE}{BOLD}{question['enunciado']}{RESET}")
        print_fn(f"{CYAN}└{banner_border}┘{RESET}")
        for letter in "abcd":
            alt_text = question['alternativa_' + letter]
            print_fn(f"   {CYAN}[{letter.upper()}]{RESET} {alt_text}")
    else:
        print_fn(f"\nQuestão {index + 1}/{total} — {diff_name} — vale {prize_val}")
        print_fn(question["enunciado"])
        for letter in "abcd":
            print_fn(f"{letter.upper()}) {question['alternativa_' + letter]}")


def ask_answer(input_fn=input, print_fn=print):
    while True:
        prompt_str = f"\n{YELLOW}➜ Sua resposta (A, B, C, D ou S para desistir):{RESET} " if print_fn is print else "Resposta (A, B, C, D ou S para desistir): "
        answer = input_fn(prompt_str).strip().upper()
        if answer in ("A", "B", "C", "D", "S"):
            return answer
        print_fn("Entrada inválida. Digite A, B, C, D ou S.")


def play(client, pending=None, input_fn=input, print_fn=print, clock=time.perf_counter):
    if pending is None:
        nickname = ask_nickname(input_fn, print_fn)
        game = choose_game(client.games(), input_fn, print_fn)
        state = fetch_questions(client, nickname, game["id"])
        pending = PendingGame(nickname, game["id"], state)
        if print_fn is print:
            print_fn(f"\n{GREEN}✔ Partida iniciada com sucesso!{RESET}")
            print_fn(f"Jogo: {BOLD}{game['nome']}{RESET} | Jogador: {BOLD}{nickname}{RESET}")
            print_fn(f"{DIM}Responda A, B, C ou D. Digite S para desistir e garantir seu prêmio.{RESET}")
        else:
            print_fn(f"Jogo: {game['nome']} | Jogador: {nickname}")
            print_fn("Responda A, B, C ou D. Digite S para desistir.")
    while True:
        state = pending.state
        if pending.answer is None:
            question_started = clock()
            show_question(state, print_fn)
            pending.answer = ask_answer(input_fn, print_fn)
            pending.elapsed_seconds += max(0, clock() - question_started)
        try:
            if print_fn is print and sys.stdout.isatty():
                sys.stdout.write(f"{DIM}Consultando o Supabase...{RESET}\r")
                sys.stdout.flush()
            response = save_answer(client, pending)
        except GameError as exc:
            print_fn(f"Não foi possível enviar a resposta: {exc}")
            action = input_fn("Enter para tentar novamente ou M para voltar ao menu: ").strip().upper()
            if action == "M":
                print_fn("Partida mantida na memória. Use a opção 3 para retomar.")
                return pending
            continue
        pending.state = response
        pending.answer = None
        if response["finished"]:
            result = response["result"]
            expected_prize = calculate_prize(result['acertos'], state.get('prizes'))
            if expected_prize != result['valor_ganho']:
                print_fn("Aviso: prêmio retornado diverge da escada do jogo. Confira o registro.")
            
            prize_formatted = money(result['valor_ganho'])
            
            if print_fn is print:
                if result['acertos'] == state.get("total", 9):
                    play_sound("win")
                    print_fn(f"\n{GOLD}╔══════════════════════════════════════════════════════════════╗{RESET}")
                    print_fn(f"{GOLD}║     ★★★ PARABÉNS! VOCÊ CONQUISTOU R$ 1 MILHÃO! ★★★           ║{RESET}")
                    print_fn(f"{GOLD}╚══════════════════════════════════════════════════════════════╝{RESET}")
                elif result['motivo_encerramento'] == "desistencia":
                    play_sound("wrong")
                    print_fn(f"\n{YELLOW}➜ Você optou por parar e garantir seu prêmio!{RESET}")
                else:
                    play_sound("wrong")
                    print_fn(f"\n{RED}✗ Que pena! Resposta incorreta.{RESET}")

                print_fn(f"\n{CYAN}┌─────────────────── RESUMO DA PARTIDA ────────────────────────┐{RESET}")
                print_fn(f"{CYAN}│{RESET} Jogador:        {BOLD}{pending.nickname:<45}{RESET}{CYAN}│{RESET}")
                print_fn(f"{CYAN}│{RESET} Acertos:        {GREEN}{result['acertos']} acerto(s){RESET}{' ' * (36 - len(str(result['acertos'])))}{CYAN}│{RESET}")
                print_fn(f"{CYAN}│{RESET} Prêmio Ganho:   {GOLD}{prize_formatted} fictícios{RESET}{' ' * max(0, 31 - len(prize_formatted))}{CYAN}│{RESET}")
                tempo_str = f"{duration(result['tempo_segundos'])} ({result['tempo_segundos']:.3f} segundos)"
                print_fn(f"{CYAN}│{RESET} Tempo de jogo:  {WHITE}{tempo_str:<45}{RESET}{CYAN}│{RESET}")
                print_fn(f"{CYAN}│{RESET} ID da partida:  {DIM}{state['session_id']:<45}{RESET}{CYAN}│{RESET}")
                print_fn(f"{CYAN}└──────────────────────────────────────────────────────────────┘{RESET}")
            else:
                print_fn(f"\nResultado: {pending.nickname} | {result['acertos']} acerto(s) | {prize_formatted} fictícios")
                print_fn(f"Tempo de jogo: {duration(result['tempo_segundos'])} ({result['tempo_segundos']:.3f} segundos)")
                print_fn(f"ID da partida: {state['session_id']}")
                
            if response.get("correct_answer"):
                print_fn(f"Resposta correta: {response['correct_answer']}." if print_fn is not print else f"{YELLOW}A alternativa correta era: {BOLD}{response['correct_answer']}{RESET}")
            
            print_fn(f"{GREEN}✔ Partida salva no Supabase e disponível no ranking.{RESET}" if print_fn is print else "Partida salva no Supabase e disponível no ranking.")
            return None
        
        # Acertou a questão intermediária
        if print_fn is print:
            play_sound("correct")
            print_fn(f"\n{GREEN}✔ Resposta Correta!{RESET} Prêmio atual acumulado: {GOLD}{BOLD}{money(response['prize'])}{RESET}\n")
        else:
            print_fn(f"Acertou! Prêmio atual: {money(response['prize'])}")


def show_ranking(client, input_fn=input, print_fn=print):
    game = choose_game(client.games(), input_fn, print_fn)
    rows = client.ranking(game["id"])
    if not rows:
        print_fn("Ainda não há resultados para este jogo.")
        return

    if print_fn is print:
        medals = {1: "🥇", 2: "🥈", 3: "🥉"}
        print_fn(f"\n{CYAN}╔══════════════════════════════════════════════════════════════════════════╗{RESET}")
        print_fn(f"{CYAN}║{RESET}                 {BOLD}CLASSIFICAÇÃO GERAL — {game['nome'].upper():<25}{RESET}      {CYAN}║{RESET}")
        print_fn(f"{CYAN}╠════╦══════════════════════════════════╦══════════════════╦═══════════════╣{RESET}")
        print_fn(f"{CYAN}║{RESET} {BOLD}POS{RESET}{CYAN}║{RESET} {BOLD}JOGADOR{RESET}                        {CYAN}║{RESET}   {BOLD}PRÊMIO FICTÍCIO{RESET} {CYAN}║{RESET}  {BOLD}TEMPO TOTAL{RESET}  {CYAN}║{RESET}")
        print_fn(f"{CYAN}╠════╬══════════════════════════════════╬══════════════════╬═══════════════╣{RESET}")
        for row in rows:
            pos = row['posicao']
            medal = medals.get(pos, f"{pos:2}º")
            nick = row['apelido'][:30]
            val = money(row['valor_ganho'])
            tempo = duration(row['tempo_segundos'])
            print_fn(f"{CYAN}║{RESET} {medal:<2} {CYAN}║{RESET} {WHITE}{nick:<32}{RESET} {CYAN}║{RESET} {GOLD}{val:>16}{RESET} {CYAN}║{RESET}   {WHITE}{tempo:>7}{RESET}     {CYAN}║{RESET}")
        print_fn(f"{CYAN}╚════╩══════════════════════════════════╩══════════════════╩═══════════════╝{RESET}")
    else:
        for row in rows:
            print_fn(f"{row['posicao']:2}. {row['apelido']:<30} {money(row['valor_ganho']):>16}  {duration(row['tempo_segundos'])}")


def print_banner():
    """Exibe o cabeçalho estilizado do jogo."""
    banner = f"""
{CYAN}╔════════════════════════════════════════════════════════════════════════╗
║                   {GOLD}★ SHOW DO MILHÃO — DESAFIO PYTHON ★{CYAN}                  ║
║           {WHITE}Persistência Supabase • Ranking Web • Turma 1F{CYAN}               ║
║    {DIM}Integrantes: João Gouvêa Ferreira • Henrique • João Vitor{CYAN}           ║
╚════════════════════════════════════════════════════════════════════════╝{RESET}
"""
    print(banner)


def main():
    setup_terminal()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    client = GameClient(
        os.getenv("SUPABASE_URL", DEFAULT_URL),
        os.getenv("SUPABASE_PUBLIC_KEY", DEFAULT_PUBLIC_KEY),
    )
    pending_games = []
    print_banner()

    while True:
        print(f"\n{CYAN}┌────────────────────── MENU PRINCIPAL ──────────────────────┐{RESET}")
        print(f"{CYAN}│{RESET}  {YELLOW}1){RESET} Iniciar partida                                         {CYAN}│{RESET}")
        print(f"{CYAN}│{RESET}  {YELLOW}2){RESET} Consultar Ranking                                       {CYAN}│{RESET}")
        print(f"{CYAN}│{RESET}  {YELLOW}3){RESET} Retomar partida pendente                                {CYAN}│{RESET}")
        print(f"{CYAN}│{RESET}  {RED}0){RESET} Sair                                                    {CYAN}│{RESET}")
        print(f"{CYAN}└────────────────────────────────────────────────────────────┘{RESET}")
        
        choice = input(f"{CYAN}Escolha uma opção:{RESET} ").strip()
        try:
            if choice == "1":
                pending = play(client)
                if pending:
                    pending_games.append(pending)
            elif choice == "2":
                show_ranking(client)
            elif choice == "3":
                if not pending_games:
                    print(f"\n{YELLOW}Nenhuma partida pendente na memória.{RESET}")
                else:
                    pending = pending_games.pop(0)
                    if play(client, pending):
                        pending_games.append(pending)
            elif choice == "0":
                if pending_games:
                    print(f"{YELLOW}Atenção: {len(pending_games)} partida(s) pendente(s) serão perdidas ao sair.{RESET}")
                print(f"\n{GREEN}Obrigado por jogar o Desafio Python! Até logo! 👋{RESET}")
                break
            else:
                print(f"{RED}Opção inválida. Digite 1, 2, 3 ou 0.{RESET}")
        except GameError as exc:
            print(f"\n{RED}Falha ao consultar o Supabase:{RESET} {exc}")


if __name__ == "__main__":
    main()
