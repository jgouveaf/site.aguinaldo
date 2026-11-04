# 🎓 Guia de Avaliação — AC04 Show do Milhão

**Desafio Python: Jogo de Perguntas com Banco Online e Ranking Web**  
*Documento preparado especialmente para facilitar a correção pelo professor.*

---

## 📌 Identificação do Grupo

* **Turma:** 1F
* **Integrantes (Trio):**
  1. João Gouvêa Ferreira
  2. Henrique
  3. João Vitor
* **Nome do Jogo:** Desafio Python
* **Repositório GitHub:** [https://github.com/jgouveaf/site.aguinaldo](https://github.com/jgouveaf/site.aguinaldo)
* **Site Publicado (Ranking Web):** [https://jgouveaf.github.io/site.aguinaldo/](https://jgouveaf.github.io/site.aguinaldo/)

---

## ⚡ Como Testar Rapidamente (1 Clique)

No Windows, todos os scripts foram preparados para execução direta na raiz da pasta:

1. **Jogar a Partida no Terminal:**  
   Execute `JOGAR.bat` (ou `python game.py`).  
   *Interface rica em cores ANSI, caixas informativas, escada de prêmios e efeitos visuais sem nenhuma dependência externa.*
2. **Executar a Suíte de Testes Automatizados:**  
   Execute `TESTAR.bat` (ou `python -m unittest discover -s tests -v`).  
   *10 testes cobrindo todas as regras da especificação em 0.03s.*
3. **Abrir o Ranking no Navegador:**  
   Abra `ABRIR_SITE.url` (ou acesse o link do GitHub Pages).

---

## 🗺️ Mapa de Atendimento aos Critérios da AC04

| Critério (Valor) | Onde está implementado | Como comprovar |
| :--- | :--- | :--- |
| **1. Jogo em Python (3,0)** | `game.py` | Executar `JOGAR.bat`. Validação de apelido, 9 perguntas (3 fáceis, 3 médias, 3 difíceis), escada até R$ 1 milhão, parada no 1º erro/desistência. |
| **2. Banco e Integração (2,0)** | `sql/setup.sql`, `sql/ampliar_60_perguntas.sql` e Supabase | 60 perguntas reais cadastradas (20 fáceis, 20 médias, 20 difíceis). Partidas salvas com `session_id` persistente, sem duplicação no reenvio. |
| **3. Ranking Web (1,0)** | `site/index.html`, `site/app.js`, `site/style.css` | Acesso online com consulta em tempo real. Ordenação: Maior Prêmio ➔ Menor Tempo ➔ Data ➔ ID. Melhor partida por jogador. |
| **4. Organização e Entrega (1,0)** | `requirements.txt`, `.env.example`, `README.md`, `LEIA_PRIMEIRO.md` | Código limpo, sem bibliotecas pesadas desnecessárias, sem exposição de credenciais privadas. |
| **5. IA e Testes (1,0)** | `prompts.md`, `TESTES.md` e pasta `evidencias/` | 27 prompts completos e cronológicos registrados, análise crítica, logs de teste, JSONs de auditoria e capturas. |
| **6. Domínio Individual (2,0)** | Código modular em `game.py` | Funções divididas claramente para arguição de cada integrante (veja abaixo). |

---

## 🔍 Estrutura das Funções no Python (`game.py`)

As funções exigidas pelo documento da atividade foram implementadas com total clareza e separação de responsabilidades:

1. **`fetch_questions(client, nickname, game_id)`:**  
   Inicia a partida no banco Supabase e obtém o identificador da sessão e a primeira questão. Não recebe gabaritos (segurança contra trapaça no cliente).
2. **`play(client, pending, ...)`:**  
   Controla o fluxo do jogo, apresentação da pergunta, leitura e validação da resposta (`A`, `B`, `C`, `D` ou `S`).
   * **Cronômetro:** Usa `time.perf_counter()` medindo **exclusivamente** o tempo em que a questão está visível na tela até a digitação da resposta. Menus, telas de retomada e tempo de rede HTTP são estritamente excluídos do tempo da partida.
3. **`calculate_prize(correct_count, prizes)`:**  
   Aplica a escada de prêmios da tabela da AC04. O valor substitui o anterior e **nunca é somado**.
4. **`save_answer(client, pending)`:**  
   Envia a resposta e o tempo medido para a API do Supabase. Utiliza o mesmo identificador de sessão (`session_id`) para garantir idempotência (evitando partidas duplicadas em caso de reenvio por instabilidade de rede).
5. **`show_ranking(client, ...)`:**  
   Consulta a função segura `ranking_public` no banco de dados e renderiza o Top 10 formatado em tabela com medalhas, valores em R$ e duração em `mm:ss`.

---

## 🎯 Divisão para a Apresentação Oral (Trio)

* **João Gouvêa:** Explica a arquitetura geral, conexão com a API Supabase e as funções `fetch_questions` e `calculate_prize`.
* **Henrique:** Explica a função `play`, a validação de entradas do usuário e a medição de tempo ativo com `time.perf_counter()`.
* **João Vitor:** Explica a função `save_answer`, a política de idempotência/tratamento de falhas de conexão e a exibição de `show_ranking`.
