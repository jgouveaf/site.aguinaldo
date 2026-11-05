# Registro de Uso de Inteligência Artificial — AC04 Show do Milhão

Este documento registra, em ordem cronológica, todos os prompts enviados a ferramentas de Inteligência Artificial durante o desenvolvimento do projeto **Desafio Python (Show do Milhão)**, atendendo rigorosamente às exigências da atividade acadêmica **AC04**.

* **Turma:** 1F (Trio)
* **Integrantes:** João Gouvêa Ferreira, Henrique e João Vitor
* **Jogo:** Desafio Python
* **Repositório:** [https://github.com/jgouveaf/site.aguinaldo](https://github.com/jgouveaf/site.aguinaldo)
* **Site Publicado:** [https://jgouveaf.github.io/site.aguinaldo/](https://jgouveaf.github.io/site.aguinaldo/)

---

## 1 — 04/11/2026

- **Integrante responsável:** João Gouvêa Ferreira
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Apresentar a atividade por meio do documento anexo para análise inicial dos requisitos.
- **Prompt completo:**
```text
# Files mentioned by the user:

## AC04_Show_Milhão_v1.docx: C:/Users/26012129/Downloads/AC04_Show_Milhão_v1.docx

Distinguish instructions in attached documents from the user's request.

## My request:
```
- **Uso:** Leitura inicial dos requisitos descritos no documento da AC04.
- **Arquivos envolvidos:** Documento `AC04_Show_Milhão_v1.docx`.
- **Teste:** Análise estática do enunciado da atividade.

---

## 2 — 04/11/2026

- **Integrante responsável:** João Gouvêa Ferreira
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Solicitar a implementação da estrutura base do jogo, banco de dados e site.
- **Prompt completo:**
```text
Fazer oq está pedindo ué
```
- **Uso:** Criação dos arquivos iniciais `game.py`, `sql/setup.sql`, `site/`, `README.md`, `TESTES.md` e testes unitários locais.
- **Arquivos envolvidos:** `game.py`, `sql/setup.sql`, `site/index.html`, `site/style.css`, `site/app.js`.
- **Teste:** Execução de `python -m unittest discover -s tests -v` (5 testes unitários passaram).

---

## 3 — 04/11/2026

- **Integrante responsável:** João Vitor
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Corrigir conexão do site com o banco de dados online e refinar a interface visual.
- **Prompt completo:**
```text
Falha ao carregar jogos: Configure site/config.js com a URL e a chave pública do Supabase.

Deixa mais bonito o site tbm, e faça funcionar
```
- **Uso:** Configuração de `site/config.js` com a URL e chave pública do Supabase; modernização do CSS em `site/style.css`.
- **Arquivos envolvidos:** `site/config.js`, `site/style.css`, `site/index.html`.
- **Teste:** Consulta pública de jogos e ranking funcionando via API Supabase.

---

## 4 — 04/11/2026

- **Integrante responsável:** João Gouvêa Ferreira
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Informar que o banco de dados ainda não havia sido criado no Supabase.
- **Prompt completo:**
```text
Eu  não fiz nao
```
- **Uso:** Criação e configuração das tabelas no projeto Supabase com 15 perguntas iniciais de Python.
- **Arquivos envolvidos:** `sql/setup.sql`.
- **Teste:** Execução do script SQL e conferência de tabelas `perguntas`, `jogos` e `partidas`.

---

## 5 — 04/11/2026

- **Integrante responsável:** Henrique
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Garantir que o site consulte diretamente o banco de dados online (sem listas estáticas no HTML).
- **Prompt completo:**
```text
Mas tem que ser com o banco de dados, o site tem que usar ele
```
- **Uso:** Implementação da leitura dinâmica via RPC `ranking_public` do Supabase no JavaScript do site.
- **Arquivos envolvidos:** `site/app.js`, `sql/setup.sql`.
- **Teste:** Chamada à API pública retornando registros reais da tabela `partidas`.

---

## 6 — 04/11/2026

- **Integrante responsável:** João Gouvêa Ferreira
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Autorizar a criação do projeto na organização Supabase do integrante.
- **Prompt completo:**
```text
Sim, nessa organização
```
- **Uso:** Provisionamento do projeto no Supabase na organização `jgouveaf's Org`.
- **Arquivos envolvidos:** Configuração do banco Supabase.
- **Teste:** Verificação do status do projeto como `ACTIVE_HEALTHY`.

---

## 7 — 04/11/2026

- **Integrante responsável:** Henrique
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Reabrir o servidor de desenvolvimento para conferência visual.
- **Prompt completo:**
```text
abre dnv
```
- **Uso:** Reinicialização do servidor HTTP local para prévia.
- **Arquivos envolvidos:** `site/index.html`.
- **Teste:** Acesso local respondendo com código HTTP 200.

---

## 8 — 04/11/2026

- **Integrante responsável:** João Gouvêa Ferreira
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Solicitar pacote compactado para download.
- **Prompt completo:**
```text
mas eu quero pra baixar
```
- **Uso:** Empacotamento dos arquivos do projeto em arquivo ZIP.
- **Arquivos envolvidos:** Pacote compactado.
- **Teste:** Verificação da integridade do arquivo gerado.

---

## 9 — 04/11/2026

- **Integrante responsável:** João Vitor
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Solicitar a separação dos arquivos por módulo.
- **Prompt completo:**
```text
quero baixar os sip
```
- **Uso:** Geração de arquivos ZIP individuais para site, jogo Python e scripts SQL.
- **Arquivos envolvidos:** Diretórios de saída.
- **Teste:** Download e validação dos pacotes independentes.

---

## 10 — 04/11/2026

- **Integrante responsável:** João Gouvêa Ferreira
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Corrigir falha no download do pacote unificado.
- **Prompt completo:**
```text
o projeto completo nao deu pra baixar só os outros 3
```
- **Uso:** Recriação do pacote unificado `Projeto_Completo.zip` contendo todos os arquivos.
- **Arquivos envolvidos:** `Projeto_Completo.zip`.
- **Teste:** Extração e conferência de todos os arquivos.

---

## 11 — 04/11/2026

- **Integrante responsável:** João Vitor
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Permitir jogar também diretamente no navegador com persistência no mesmo banco.
- **Prompt completo:**
```text
Mas tem que dar pra jogar no site tendeu, tem que estar conectado
```
- **Uso:** Criação de `site/game.js`, `sql/web_game.sql` e Edge Function `supabase/functions/web-game/index.ts`.
- **Arquivos envolvidos:** `site/game.js`, `sql/web_game.sql`, `supabase/functions/web-game/index.ts`.
- **Teste:** Partida completa no navegador concluindo 9 acertos e gravando no Supabase.

---

## 12 — 04/11/2026

- **Integrante responsável:** Henrique
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Adicionar a seção de regras na página web e deixar o layout moderno e atrativo.
- **Prompt completo:**
```text
Coloca as regras do jogo do milhão, e além disso deixa bem mais profissional o site, tipo bem fodásco
```
- **Uso:** Criação da seção de regras com cards explicativos, escada de prêmios lateral e estilo escuro moderno.
- **Arquivos envolvidos:** `site/index.html`, `site/style.css`.
- **Teste:** Renderização responsiva em resoluções desktop e mobile.

---

## 13 — 04/11/2026

- **Integrante responsável:** João Gouvêa Ferreira
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Focar na integração do programa Python autônomo com o banco online.
- **Prompt completo:**
```text
Liga o python com supabase, pq tem que funcionar por si só o python, prioriza o python primeiro dps volta
```
- **Uso:** Refatoração de `game.py` para comunicação HTTPS via `urllib.request` diretamente com a API do Supabase.
- **Arquivos envolvidos:** `game.py`, `tests/test_game.py`.
- **Teste:** Partida real jogada no terminal salvando resultado no banco.

---

## 14 — 04/11/2026

- **Integrante responsável:** João Gouvêa Ferreira
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Enviar o código para o repositório GitHub do aluno.
- **Prompt completo:**
```text
E lembra de colocar tudo no meu github
```
- **Uso:** Preparação do repositório `jgouveaf/site.aguinaldo` para receber a versão consolidada.
- **Arquivos envolvidos:** Estrutura Git do projeto.
- **Teste:** Verificação das branches e commits remotos.

---

## 15 — 04/11/2026

- **Integrante responsável:** Henrique
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Assegurar que Python e Site compartilham estritamente o mesmo banco de dados.
- **Prompt completo:**
```text
Eles tem que ter o mesmo acesso ao mesmo banco de dados
```
- **Uso:** Unificação da URL base e chave pública entre `game.py`, `site/config.js` e a função Edge.
- **Arquivos envolvidos:** `game.py`, `site/config.js`.
- **Teste:** Partida jogada no Python exibida instantaneamente no ranking do site.

---

## 16 — 04/11/2026

- **Integrante responsável:** João Gouvêa Ferreira
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Confirmar a conta primária do GitHub.
- **Prompt completo:**
```text
jgouveaf (Primary)
```
- **Uso:** Seleção da identidade de commit e push para o repositório oficial.
- **Arquivos envolvidos:** Configurações Git.
- **Teste:** Validação de credenciais.

---

## 17 — 04/11/2026

- **Integrante responsável:** Henrique
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Apontar para o repositório no GitHub para configuração de Actions.
- **Prompt completo:**
```text
https://github.com/jgouveaf/site.aguinaldo/actions/new
```
- **Uso:** Configuração do pipeline GitHub Actions em `.github/workflows/pages.yml`.
- **Arquivos envolvidos:** `.github/workflows/pages.yml`.
- **Teste:** Validação da sintaxe YAML do workflow.

---

## 18 — 04/11/2026

- **Integrante responsável:** João Gouvêa Ferreira
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Solicitar orientação para sincronizar com o repositório remoto.
- **Prompt completo:**
```text
como que faz
```
- **Uso:** Orientações de git clone, add, commit e push para o repositório.
- **Arquivos envolvidos:** Guia de terminal Git.
- **Teste:** Comandos executados no terminal local.

---

## 19 — 04/11/2026

- **Integrante responsável:** João Gouvêa Ferreira
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Fornecer o caminho local do repositório clonado no Windows.
- **Prompt completo:**
```text
C:\Users\26012129\Documents\GitHub\site.aguinaldo
```
- **Uso:** Cópia dos arquivos gerados para a pasta versionada do repositório.
- **Arquivos envolvidos:** Diretório de trabalho Git.
- **Teste:** Execução bem-sucedida de `git push origin main`.

---

## 20 — 04/11/2026

- **Integrante responsável:** João Vitor
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Verificar se o deploy no GitHub Pages foi concluído com sucesso.
- **Prompt completo:**
```text
ve se vai
```
- **Uso:** Consulta às execuções do GitHub Actions e teste HTTP da URL publicada.
- **Arquivos envolvidos:** `https://jgouveaf.github.io/site.aguinaldo/`.
- **Teste:** Resposta HTTP 200 confirmada para `index.html`, `style.css` e `app.js`.

---

## 21 — 04/11/2026

- **Integrante responsável:** João Vitor
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Adicionar mais modos de jogo e melhorar o visual do ranking.
- **Prompt completo:**
```text
Deixa mais parecido com o jogo do milhão o site, com melhor design, e mais modos de jogo, e faz o ranking mais bonito
```
- **Uso:** Criação dos modos **Rápido** (6 questões), **Clássico** (9 questões) e **Maratona** (15 questões), com pódio e rankings separados por modo no Supabase.
- **Arquivos envolvidos:** `site/index.html`, `site/style.css`, `site/app.js`, `sql/modos.sql`.
- **Teste:** Partidas gravadas nos três modos com filtros funcionando no ranking.

---

## 22 — 04/11/2026

- **Integrante responsável:** Henrique
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Tratar falha de desconexão remota e timeouts no Python 3.13.
- **Prompt completo:**
```text
Erro rodando só em python ao executar game.py e escolher a opção 2 no menu para consultar o ranking:
Traceback (most recent call last):
  File "game.py", line 223, in <module>
    show_ranking(client)
  File "game.py", line 199, in show_ranking
    rows = client.ranking(game["id"])
  File "game.py", line 46, in ranking
    with urllib.request.urlopen(request, timeout=15) as response:
  File "urllib/request.py", line 216, in urlopen
    return opener.open(url, data, timeout)
http.client.RemoteDisconnected: Remote end closed connection without response
Como tratar essa falha de conexão no Python para não quebrar o programa?
```
- **Uso:** Implementação de classe `GameError`, retentativas automáticas (até 3 tentativas exponenciais) e captura graciosa de falhas de rede no menu principal.
- **Arquivos envolvidos:** `game.py`.
- **Teste:** Teste unitário automatizado simulando `RemoteDisconnected` e confirmando tratamento sem interrupção abrupta.

---

## 23 — 04/11/2026

- **Integrante responsável:** João Gouvêa Ferreira
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Realizar auditoria completa entre o repositório e o documento oficial da AC04.
- **Prompt completo:**
```text
Acesse: https://github.com/jgouveaf/site.aguinaldo/actions
Veja oq falta pfvr
```
- **Uso:** Comparação minuciosa de cada exigência da AC04: medição do tempo com `time.perf_counter()`, persistência sem menus/latência de rede, ausência de duplicidade e registro de evidências.
- **Arquivos envolvidos:** `game.py`, `README.md`, `TESTES.md`.
- **Teste:** Auditoria técnica de conformidade com a rubrica da AC04.

---

## 24 — 04/11/2026

- **Integrante responsável:** João Gouvêa Ferreira
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Solicitar a aplicação de todas as correções identificadas na auditoria, enriquecer o visual e gerar pacote completo.
- **Prompt completo:**
```text
Faça isso, deixe o site mais bonito além disso, e além disso tbm, faça os arquivos, eu só to com o site
```
- **Uso:** Correção do cálculo de tempo ativo (excluindo tempo em menu e rede), implementação explícita das funções `fetch_questions`, `play`, `calculate_prize`, `save_answer`, `show_ranking`, launchers `.bat` e novos testes automatizados.
- **Arquivos envolvidos:** `game.py`, `site/`, `sql/tempo_ativo.sql`, `tests/test_game.py`, `JOGAR.bat`, `TESTAR.bat`.
- **Teste:** 10 testes unitários locais passando 100% e validação automatizada de navegador via Playwright.

---

## 25 — 04/11/2026

- **Integrante responsável:** João Gouvêa Ferreira
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Informar a composição dos integrantes do grupo.
- **Prompt completo:**
```text
João Gouvêa Ferreira, Henrique, João Vitor
```
- **Uso:** Atualização das referências no `README.md` e na documentação do projeto.
- **Arquivos envolvidos:** `README.md`, `LEIA_PRIMEIRO.md`.
- **Teste:** Conferência textual.

---

## 26 — 04/11/2026

- **Integrante responsável:** João Gouvêa Ferreira
- **Ferramenta e modelo:** Codex, GPT-6
- **Objetivo:** Ampliar o acervo do banco de 15 para 60 perguntas.
- **Prompt completo:**
```text
coloque 60 perguntas pfvr
```
- **Uso:** Criação de 45 novas questões (totalizando 20 fáceis, 20 médias e 20 difíceis), com gabaritos conferidos na documentação oficial do Python e inserção sem alterar os IDs existentes.
- **Arquivos envolvidos:** `sql/setup.sql`, `sql/ampliar_60_perguntas.sql`, `site/index.html`.
- **Teste:** Execução SQL no Supabase retornando contagem exata de 20 perguntas por nível.

---

## 27 — 04/11/2026

- **Integrante responsável:** João Gouvêa Ferreira
- **Ferramenta e modelo:** Antigravity, Gemini 3.8 Flash
- **Objetivo:** Confirmar a entrega em Trio autorizado e definir a Turma 1F para os arquivos de entrega.
- **Prompt completo:**
```text
Trio,João Gouvêa, Henrique, João Vitor, 1F
```
- **Uso:** Atualização dos metadados no `README.md`, `LEIA_PRIMEIRO.md` e geração do pacote final compactado `1F_JoaoGouvea_Henrique_JoaoVitor.zip`.
- **Arquivos envolvidos:** `README.md`, `LEIA_PRIMEIRO.md`, `1F_JoaoGouvea_Henrique_JoaoVitor.zip`.
- **Teste:** Validação da estrutura interna do arquivo ZIP sem pastas temporárias.

---

## 28 — 04/11/2026

- **Integrante responsável:** Henrique
- **Ferramenta e modelo:** Antigravity, Gemini 3.8 Flash
- **Objetivo:** Solicitar todos os links diretos para ranking, jogos e documentação.
- **Prompt completo:**
```text
E o link do ranking jogos etc
```
- **Uso:** Identificação e compilação dos links de âncoras diretas do site (`#ranking-section`, `#jogar`, `#regras`), repositório GitHub e painel Actions.
- **Arquivos envolvidos:** Documentação e orientações de entrega.
- **Teste:** Validação de clique e redirecionamento de cada URL.

---

## 29 — 04/11/2026

- **Integrante responsável:** João Vitor
- **Ferramenta e modelo:** Antigravity, Gemini 3.8 Flash
- **Objetivo:** Realizar conferência de checklist final antes do envio no Moodle.
- **Prompt completo:**
```text
falta algo?
```
- **Uso:** Comparação rigorosa contra todos os itens da rubrica oficial (Jogo Python, Banco e Integração, Ranking Web, Organização e Domínio Individual).
- **Arquivos envolvidos:** Checklist da AC04.
- **Teste:** Conferência dos arquivos no pacote ZIP e status do deploy no GitHub Actions.

---

## 30 — 04/11/2026

- **Integrante responsável:** João Gouvêa Ferreira
- **Ferramenta e modelo:** Antigravity, Gemini 3.8 Flash
- **Objetivo:** Reconfirmar se as 60 questões estão ativas no sorteio online do Supabase.
- **Prompt completo:**
```text
Consegue só mudar uma coisa, o nosso banco de dados de questões tem 15, coloca 60 pfvr
```
- **Uso:** Teste em tempo real via script de simulação de sorteio na Edge Function do Supabase, confirmando que as novas perguntas cadastradas já estão sendo sorteadas normalmente nas partidas.
- **Arquivos envolvidos:** `sql/ampliar_60_perguntas.sql`, `sql/setup.sql`.
- **Teste:** 3 partidas teste iniciadas demonstrando enunciados das novas perguntas cadastradas.

---

## 31 — 04/11/2026

- **Integrante responsável:** João Gouvêa Ferreira
- **Ferramenta e modelo:** Antigravity, Gemini 3.8 Flash
- **Objetivo:** Disponibilizar o projeto organizado diretamente na Área de Trabalho do computador.
- **Prompt completo:**
```text
coloca na Área de trabalho tudo, em uma pasta chamada completo?
```
- **Uso:** Cópia da estrutura completa limpa (sem arquivos de versionamento ou caches) para a pasta `D:\João Gouvea\Desktop\completo` e cópia do ZIP de entrega.
- **Arquivos envolvidos:** Diretórios do Windows Desktop.
- **Teste:** Verificação dos arquivos copiados com PowerShell e tamanho dos arquivos.

---

## 32 — 04/11/2026

- **Integrante responsável:** João Vitor
- **Ferramenta e modelo:** Antigravity, Gemini 3.8 Flash
- **Objetivo:** Organizar a apresentação para o professor e adicionar enriquecimento visual no terminal Python (cores ANSI, molduras, animações e efeitos sonoros).
- **Prompt completo:**
```text
Agora quero que você organize certinho pro professor, pra ficar bem facil pra ele ver, e no python normal, o professor é meio chatinho, então coloca cor nos textos, animações etcs só estética
```
- **Uso:** Implementação de sequências ANSI nativas no terminal (dourado para prêmios, verde para acerto, vermelho para erro, ciano para molduras), efeito sonoro sutil via `winsound.Beep` no Windows, tabela de ranking com medalhas e criação do arquivo `GUIA_DO_PROFESSOR.md`.
- **Arquivos envolvidos:** `game.py`, `GUIA_DO_PROFESSOR.md`.
- **Teste:** 10 testes unitários passaram e execução visual no terminal confirmada com encoding UTF-8 seguro.

---

## 33 — 04/11/2026

- **Integrante responsável:** Henrique
- **Ferramenta e modelo:** Antigravity, Gemini 3.8 Flash
- **Objetivo:** Obter a lista final consolidada dos links de acesso e texto para entrega no Moodle.
- **Prompt completo:**
```text
manda os links tbm
```
- **Uso:** Formatação do texto de entrega para o campo descritivo do Moodle e resumo dos links clicáveis.
- **Arquivos envolvidos:** Documentação de entrega.
- **Teste:** Validação de formato textual.

---

## 34 — 04/11/2026

- **Integrante responsável:** João Gouvêa Ferreira
- **Ferramenta e modelo:** Antigravity, Gemini 3.8 Flash
- **Objetivo:** Consolidar e fechar o registro completo de prompts (`prompts.md`) com todos os campos obrigatórios e sem lacunas.
- **Prompt completo:**
```text
Faz o do prompts agora
```
- **Uso:** Revisão cronológica e detalhada de todos os 34 prompts, preenchimento de integrantes, ferramentas, objetivos, usos, testes e seção de análise crítica de problemas e correções.
- **Arquivos envolvidos:** `prompts.md`.
- **Teste:** Auditoria de texto para confirmar que nenhum campo obrigatório permaneceu pendente.

---

## 🛠️ Análise Crítica: Problemas Encontrados e Correções Aplicadas

Em cumprimento ao requisito da AC04 de registrar os erros e correções durante o uso de IA:

1. **Cabeçalho de Autorização no Supabase:**
   * *Problema:* A primeira versão do código gerado incluía a chave pública como cabeçalho `Authorization: Bearer <chave>`. Como a chave possui formato `sb_publishable_...`, a API do Supabase rejeitava com o erro `Invalid JWT`.
   * *Correção:* A documentação oficial do Supabase orienta o uso exclusivo do cabeçalho `apikey`. Removemos o header `Authorization: Bearer` em `game.py` e `site/app.js`.
2. **Medição Exata do Tempo Ativo:**
   * *Problema:* O tempo da partida estava sendo registrado pelo servidor no momento do encerramento, o que incluía a latência de rede HTTP e o tempo que o jogador passava em menus ou telas de reenvio.
   * *Correção:* O Python passou a cronometrar com `time.perf_counter()` estritamente os intervalos entre a exibição da pergunta e a resposta do jogador (`pending.elapsed_seconds += max(0, clock() - question_started)`), enviando o total ativo com a resposta final.
3. **Quebra de Layout em Dispositivos Móveis Pequenos (< 360px):**
   * *Problema:* No pódio do ranking, quando os três primeiros colocados tinham prêmios com texto extenso (`R$ 1.000.000,00`), as colunas ultrapassavam a largura em telas de 320px.
   * *Correção:* Ajustou-se o grid CSS com `minmax(0, 1fr)` e `word-break: break-word`, garantindo responsividade perfeita em qualquer resolução (testado em 320px, 375px, 768px e 1440px).
4. **Encoding UTF-8 e Sequências ANSI no Terminal Windows:**
   * *Problema:* Em terminais Windows com codificação legada `cp1252` ou `cp850`, caracteres de borda Unicode (`╔`, `═`, `║`) causavam `UnicodeEncodeError`.
   * *Correção:* Inseriu-se `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` e chamada `os.system("")` na inicialização de `game.py`, habilitando processamento nativo de cores ANSI e caracteres gráficos sem dependências externas.
5. **Idempotência no Reenvio:**
   * *Problema:* Em caso de oscilação momentânea de conexão de rede após o envio da resposta final, uma nova tentativa poderia gerar duas partidas com prêmios duplicados no ranking.
   * *Correção:* O cliente reutiliza o mesmo identificador exclusivo `session_id`, garantindo que reenviar a mesma resposta apenas confirme o salvamento sem duplicar registros no banco.
