import sys
import http.client
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import game


class FakeClient:
    def __init__(self):
        self.index = 0
        self.fail_once = False
        self.saved = []

    def games(self):
        return [{"id": "game-1", "nome": "Desafio Python"}]

    def state(self):
        level = ["facil"] * 3 + ["media"] * 3 + ["dificil"] * 3
        return {"finished": False, "session_id": "session-1", "index": self.index,
                "difficulty": level[self.index], "prize": game.PRIZES[self.index - 1] if self.index else 0,
                "question": {"enunciado": "Pergunta?", "alternativa_a": "Certa",
                             "alternativa_b": "Errada", "alternativa_c": "Errada", "alternativa_d": "Errada"}}

    def start(self, nickname, game_id):
        return self.state()

    def answer(self, session_id, index, choice):
        if self.fail_once:
            self.fail_once = False
            raise game.GameError("Falha simulada")
        if self.saved:
            return self.saved[0]
        assert index == self.index
        if choice == "A":
            self.index += 1
            if self.index < 9:
                return self.state()
            reason = "concluiu"
        else:
            reason = "desistencia" if choice == "S" else "erro"
        result = {"finished": True, "result": {"acertos": self.index,
                  "valor_ganho": game.PRIZES[self.index - 1] if self.index else 0,
                  "tempo_segundos": 63.2, "motivo_encerramento": reason}}
        self.saved.append(result)
        return result

    def ranking(self, game_id):
        return []


def inputs(values):
    iterator = iter(values)
    return lambda _: next(iterator)


class Clock:
    def __init__(self):
        self.value = 0

    def __call__(self):
        self.value += 1
        return float(self.value)


class GameTests(unittest.TestCase):
    def run_game(self, answers):
        client = FakeClient()
        output = []
        pending = game.play(client, input_fn=inputs(["", "Ana", *answers]), print_fn=output.append, clock=Clock())
        self.assertIsNone(pending)
        return client, "\n".join(output)

    def test_nine_correct(self):
        client, output = self.run_game(["A"] * 9)
        self.assertEqual(client.index, 9)
        self.assertIn("R$ 1.000.000,00", output)
        self.assertEqual(len(client.saved), 1)

    def test_first_error_and_invalid_input(self):
        client, output = self.run_game(["X", "B"])
        self.assertEqual(client.saved[0]["result"]["valor_ganho"], 0)
        self.assertIn("Entrada inválida", output)
        self.assertIn("R$ 0,00", output)

    def test_later_error_and_quit(self):
        client, output = self.run_game(["A", "A", "B"])
        self.assertEqual(client.saved[0]["result"]["valor_ganho"], 5000)
        self.assertIn("R$ 5.000,00", output)
        client, _ = self.run_game(["A", "S"])
        self.assertEqual(client.saved[0]["result"]["motivo_encerramento"], "desistencia")

    def test_failure_keeps_pending_answer(self):
        client = FakeClient()
        client.fail_once = True
        output = []
        pending = game.play(client, input_fn=inputs(["Ana", "B", "M"]), print_fn=output.append, clock=Clock())
        self.assertIsNotNone(pending)
        self.assertEqual(pending.answer, "B")
        self.assertEqual(len(client.saved), 0)
        resumed = game.play(client, pending, input_fn=inputs([]), print_fn=output.append, clock=Clock())
        self.assertIsNone(resumed)
        self.assertEqual(len(client.saved), 1)

    def test_empty_ranking(self):
        output = []
        game.show_ranking(FakeClient(), print_fn=output.append)
        self.assertIn("Ainda não há resultados", "\n".join(output))

    def test_remote_disconnect_becomes_game_error(self):
        client = game.GameClient()
        with patch("game.time.sleep"), patch("game.urllib.request.urlopen", side_effect=http.client.RemoteDisconnected("closed")) as call:
            with self.assertRaisesRegex(game.GameError, "Falha de conexão"):
                client.games()
        self.assertEqual(call.call_count, 3)


if __name__ == "__main__":
    unittest.main()
