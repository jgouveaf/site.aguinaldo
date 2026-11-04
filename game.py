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

DEFAULT_URL = "https://yserkieipgjqjciouole.supabase.co"
# Chave pública: também aparece no site. Nunca use uma chave secreta aqui.
DEFAULT_PUBLIC_KEY = "sb_publishable_VE02WYLJhwREVcuLdI1DUw_o37Ixx7m"
PRIZES = [1000, 5000, 10000, 25000, 50000, 100000, 200000, 500000, 1000000]
LEVEL_NAMES = {"facil": "Fácil", "media": "Média", "dificil": "Difícil"}


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

    def answer(self, session_id, index, choice):
        return self.request("/functions/v1/web-game", {
            "action": "answer", "session_id": session_id, "index": index, "choice": choice,
        })


@dataclass
class PendingGame:
    nickname: str
    game_id: str
    state: dict
    start_time: float
    network_seconds: float = 0.0
    answer: str | None = None


def money(amount: int) -> str:
    return "R$ " + f"{amount:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")


def duration(seconds: float) -> str:
    total = int(seconds)
    return f"{total // 60:02d}:{total % 60:02d}"


def ask_nickname(input_fn=input, print_fn=print):
    while True:
        name = input_fn("Apelido: ").strip()
        if 1 <= len(name) <= 30:
            return name
        print_fn("Digite um apelido de 1 a 30 caracteres.")


def choose_game(games, input_fn=input, print_fn=print):
    if not games:
        raise GameError("Nenhum jogo cadastrado no banco.")
    if len(games) == 1:
        print_fn(f"Jogo: {games[0]['nome']}")
        return games[0]
    for i, item in enumerate(games, 1):
        print_fn(f"{i}) {item['nome']}")
    while True:
        choice = input_fn("Número do jogo: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(games):
            return games[int(choice) - 1]
        print_fn("Escolha um número da lista.")


def show_question(state, print_fn=print):
    index = state["index"]
    question = state["question"]
    total = state.get("total", 9)
    prizes = state.get("prizes", [0, *PRIZES])
    print_fn(f"\nQuestão {index + 1}/{total} — {LEVEL_NAMES[state['difficulty']]} — vale {money(prizes[index + 1])}")
    print_fn(question["enunciado"])
    for letter in "abcd":
        print_fn(f"{letter.upper()}) {question['alternativa_' + letter]}")


def ask_answer(input_fn=input, print_fn=print):
    while True:
        answer = input_fn("Resposta (A, B, C, D ou S para desistir): ").strip().upper()
        if answer in ("A", "B", "C", "D", "S"):
            return answer
        print_fn("Entrada inválida. Digite A, B, C, D ou S.")


def play(client, pending=None, input_fn=input, print_fn=print, clock=time.perf_counter):
    if pending is None:
        nickname = ask_nickname(input_fn, print_fn)
        game = choose_game(client.games(), input_fn, print_fn)
        state = client.start(nickname, game["id"])
        pending = PendingGame(nickname, game["id"], state, clock())
        print_fn("Responda A, B, C ou D. Digite S para desistir.")
    while True:
        state = pending.state
        if pending.answer is None:
            show_question(state, print_fn)
            pending.answer = ask_answer(input_fn, print_fn)
        submitted_at = clock()
        try:
            response = client.answer(state["session_id"], state["index"], pending.answer)
            request_seconds = max(0, clock() - submitted_at)
            pending.network_seconds += request_seconds
        except GameError as exc:
            pending.network_seconds += max(0, clock() - submitted_at)
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
            local_elapsed = max(0, submitted_at - pending.start_time - (pending.network_seconds - request_seconds))
            print_fn(f"\nResultado: {pending.nickname} | {result['acertos']} acerto(s) | {money(result['valor_ganho'])} fictícios")
            print_fn(f"Tempo local (perf_counter): {duration(local_elapsed)} | Tempo registrado no banco: {duration(result['tempo_segundos'])}")
            if response.get("correct_answer"):
                print_fn(f"Resposta correta: {response['correct_answer']}.")
            print_fn("Partida salva no Supabase e disponível no ranking.")
            return None
        print_fn(f"Acertou! Prêmio atual: {money(response['prize'])}")


def show_ranking(client, input_fn=input, print_fn=print):
    game = choose_game(client.games(), input_fn, print_fn)
    rows = client.ranking(game["id"])
    if not rows:
        print_fn("Ainda não há resultados para este jogo.")
    for row in rows:
        print_fn(f"{row['posicao']:2}. {row['apelido']:<30} {money(row['valor_ganho']):>16}  {duration(row['tempo_segundos'])}")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    client = GameClient(
        os.getenv("SUPABASE_URL", DEFAULT_URL),
        os.getenv("SUPABASE_PUBLIC_KEY", DEFAULT_PUBLIC_KEY),
    )
    pending_games = []
    while True:
        print("\n1) Iniciar partida  2) Ranking  3) Retomar partida pendente  0) Sair")
        choice = input("Escolha: ").strip()
        try:
            if choice == "1":
                pending = play(client)
                if pending:
                    pending_games.append(pending)
            elif choice == "2":
                show_ranking(client)
            elif choice == "3":
                if not pending_games:
                    print("Nenhuma partida pendente.")
                else:
                    pending = pending_games.pop(0)
                    if play(client, pending):
                        pending_games.append(pending)
            elif choice == "0":
                if pending_games:
                    print(f"Atenção: {len(pending_games)} partida(s) pendente(s) serão perdidas ao sair.")
                break
            else:
                print("Opção inválida.")
        except GameError as exc:
            print(f"Falha ao consultar o Supabase: {exc}")


if __name__ == "__main__":
    main()
