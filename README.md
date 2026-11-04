# Desafio Python — jogo do milhão

Jogo Python no terminal e jogo no navegador, com perguntas e ranking no mesmo banco online. Prêmios fictícios, sem pagamento real.

## Integrantes

- João Gouvêa Ferreira
- Henrique
- João Vitor
- Turma: **PREENCHER**

Os três nomes foram informados pelo responsável. O enunciado fala em dupla: confirmar com o professor a participação de três integrantes. Sobrenomes de Henrique e João Vitor ainda não foram informados.

Repositório: https://github.com/jgouveaf/site.aguinaldo
Site: https://jgouveaf.github.io/site.aguinaldo/

## Começar no Windows

1. Extraia o ZIP inteiro em uma pasta. Não execute de dentro do ZIP.
2. Instale Python 3.10 ou superior, caso ainda não tenha: https://www.python.org/downloads/
3. Abra `JOGAR.bat` ou execute `python game.py` nessa pasta.
4. Informe um apelido, escolha o modo e responda A, B, C ou D. S encerra a partida.
5. Abra `ABRIR_SITE.url` e atualize o ranking do mesmo jogo.

O jogo usa apenas a biblioteca padrão do Python; não é necessário instalar pacotes. Requer internet. URL e chave pública já estão configuradas. Não precisa de senha administrativa nem arquivo `.env`. As variáveis de ambiente opcionais estão em `.env.example`; esse arquivo não é carregado automaticamente.

## Regras

Clássico: 9 perguntas, 3 fáceis, 3 médias, 3 difíceis. Escada: R$ 1.000, 5.000, 10.000, 25.000, 50.000, 100.000, 200.000, 500.000 e 1.000.000. Rápido: 6 perguntas. Maratona: 15. Cada modo tem ranking separado. As perguntas não se repetem na partida.

O primeiro erro, a desistência ou o último acerto encerra a partida. O prêmio substitui o anterior, nunca é somado. Sem acertos, R$ 0. Entrada inválida permite corrigir.

## Como funciona o Python

- `fetch_questions`: inicia o sorteio no banco e recebe a primeira pergunta. As seguintes chegam após cada resposta; o gabarito permanece no servidor.
- `play`: controla entrada, partida, cronômetro e retomada.
- `calculate_prize`: calcula o valor da etapa e confere o prêmio final retornado.
- `save_answer`: envia a resposta; a resposta final grava o resultado na mesma transação do encerramento.
- `show_ranking`: consulta os dez melhores do jogo selecionado.
- `GameClient`: comunicação HTTPS e tratamento de falhas.

O servidor TypeScript sorteia e valida respostas. A atividade permite usar uma API pronta; essa divisão preserva o gabarito e impede gravar um prêmio arbitrário. A lógica de entrada, fluxo, cálculo da escada, tempo e recuperação fica explícita no Python. Cada integrante deve saber explicar as duas partes da integração, sem apresentar o servidor como código Python.

O Python soma intervalos medidos por `time.perf_counter()` enquanto a pergunta é apresentada e respondida, incluindo tentativas inválidas. A contagem para antes do envio. Rede, reenvios e menu de retomada não entram. O navegador usa `performance.now()` com a mesma regra. O tempo acumulado é enviado junto com a resposta e salvo no banco. Sessão, índice, resposta e tempo são preservados no reenvio. Clientes antigos continuam usando tempo do servidor.

Se uma resposta falhar, tente novamente ou volte ao menu e use a opção 3. Não precisa repetir a partida. O resultado só é anunciado como salvo após confirmação. Pendências são mantidas em memória e se perdem ao fechar o programa; há aviso ao sair.

## Banco e reprodução

O projeto atual é `yserkieipgjqjciouole`. Para recriar em outro Supabase, execute no SQL Editor, nesta ordem:

1. `sql/setup.sql`: tabelas, permissões, ranking e 15 perguntas.
2. `sql/web_game.sql`: sessões e gravação transacional.
3. `sql/modos.sql`: modos adicionais.
4. `sql/tempo_ativo.sql`: tempo ativo sem rede/menu.

Publique `supabase/functions/web-game/index.ts` como função `web-game`, com `verify_jwt=false`, conforme `supabase/config.toml`. A função valida a chave pública no cabeçalho `apikey`; usa a chave secreta apenas dentro do ambiente do servidor. Atualize `site/config.js`, a cópia da raiz e as variáveis do Python para o novo projeto.

O ranking ordena por prêmio decrescente, tempo crescente, data mais antiga e ID. Seleciona antes a melhor partida por apelido (sem diferenciar maiúsculas) e jogo; as outras partidas permanecem no banco. As tabelas de perguntas, sessões e partidas não aceitam leitura direta anônima. `ranking_public` é uma função pública de leitura restrita aos campos do ranking. Seu uso de `SECURITY DEFINER` é deliberado; não concede escrita.

Este é um protótipo didático sem autenticação. O tempo é declarado pelo cliente, validado como finito, não negativo e crescente, mas não é uma proteção contra fraude. Não serve como competição com prêmios reais. O site não recebe o banco de gabaritos; após um erro, pode mostrar a alternativa correta daquela pergunta.

## Testes

Abra `TESTAR.bat` ou execute `python -m unittest discover -s tests -v`.
Os testes não dependem da internet e não gravam resultados reais.
Para o teste de navegador opcional: instale as dependências de `requirements-dev.txt`, execute `python -m playwright install chromium`, sirva `site/` com `python -m http.server 8765 --directory site` e execute `python tests/browser_checks.py`. Esse teste cria uma partida identificada como QA no banco.
`tests/ranking.sql` testa a ordenação real em transação revertida; execute no SQL Editor.

Leia `TESTES.md` e `evidencias/`. As partidas QA foram automatizadas, não representam desempenho humano.

## Site e publicação

O GitHub Actions publica `site/` após os testes locais do Python. As cópias HTML/CSS/JS na raiz são mantidas iguais para compatibilidade com a origem padrão do Pages. Modifique a pasta `site/` e sincronize as cópias antes de publicar.

## Entrega

Leia `LEIA_PRIMEIRO.md`. Preencha a turma e os sobrenomes restantes. Confirme o tamanho do grupo. O registro histórico de IA contém um prompt antigo resumido, identificado em `prompts.md`; é necessário recuperar o original para atender integralmente ao enunciado. Não invente esse texto.
O envio ao Moodle e a apresentação individual precisam ser feitos pelos integrantes.
