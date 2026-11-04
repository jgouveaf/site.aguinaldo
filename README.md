# Desafio Python

Projeto didático de perguntas em Python e no navegador, com ranking online. Os prêmios são fictícios. O site e o programa de terminal usam o mesmo projeto Supabase.

## Identificação da dupla

- Integrante 1: **PREENCHER**
- Integrante 2: **PREENCHER**
- Turma: **PREENCHER**
- Repositório GitHub: https://github.com/jgouveaf/site.aguinaldo
- Site GitHub Pages: https://jgouveaf.github.io/site.aguinaldo/

## Regras

O jogador informa um apelido e escolhe um modo: **Clássico** (9 perguntas, 3 por nível), **Rápido** (6 perguntas, 2 por nível) ou **Maratona** (15 perguntas, 5 por nível). As perguntas não se repetem na partida. É possível desistir com `S`; o primeiro erro também encerra a partida. O prêmio é o valor da última etapa vencida, de R$ 0,00 a R$ 1.000.000,00 fictícios. O tempo vai da primeira questão ao encerramento. Cada modo tem ranking próprio, que mostra a melhor partida por apelido, ordenada por prêmio, menor tempo, data mais antiga e ID.

## Instalação e execução

1. O projeto Supabase deste pacote já foi criado em `https://yserkieipgjqjciouole.supabase.co`, com o esquema de [sql/setup.sql](sql/setup.sql), [sql/web_game.sql](sql/web_game.sql), [sql/modos.sql](sql/modos.sql), 15 perguntas e os três modos. A função `web-game` já está publicada no Supabase. Para usar outro projeto, execute os três scripts SQL nessa ordem, publique a função em `supabase/functions/web-game/index.ts` com `verify_jwt = false` e atualize `site/config.js`.
2. Use Python 3.10 ou superior. Não há dependências externas; `requirements.txt` documenta isso.
3. Execute `python game.py`. A URL e a chave **pública** do projeto já estão configuradas; não é necessário criar `.env` nem informar uma chave secreta. Para trocar de projeto, use as variáveis opcionais `SUPABASE_URL` e `SUPABASE_PUBLIC_KEY` indicadas em `.env.example`.
4. Para testar a lógica do terminal sem rede, execute `python -m unittest discover -s tests -v`.
5. `site/config.js` já aponta para o projeto acima com a **chave pública**. O site foi publicado em https://jgouveaf.github.io/site.aguinaldo/ pelo workflow incluído, que publica a pasta `site/`. Os arquivos da página também estão na raiz do repositório para a origem padrão do GitHub Pages.
6. A página permite escolher o modo, iniciar uma partida com apelido, responder, desistir e ver o resultado. Ao encerrar, o ranking do modo é atualizado do banco. O jogo no navegador funciona com o programa Python fechado.

O programa Python e o site chamam a mesma função `web-game`, que consulta as perguntas, valida as respostas e salva o resultado no mesmo banco. O Python mede o tempo local da partida com `time.perf_counter()`; o banco registra a duração medida pelo servidor para que o ranking use um relógio comum aos dois clientes.

## Estrutura e permissões

- `game.py`: jogo de terminal conectado ao Supabase, com menu, partida, reenvio após falha e ranking.
- `sql/setup.sql`: tabelas, 15 perguntas, consulta ordenada e permissões.
- `sql/web_game.sql`: sessões do navegador e gravação da partida na mesma transação.
- `sql/modos.sql`: três modos, regras de prêmio e rankings separados.
- `supabase/functions/web-game/index.ts`: servidor que sorteia perguntas e confere respostas sem enviar o gabarito ao site.
- `site/`: página do jogo e ranking.
- `.github/workflows/pages.yml`: publicação da página pelo GitHub Actions.
- `tests/`: testes locais com banco simulado.
- `prompts.md`: registro de uso da IA; completem com quaisquer prompts enviados depois desta entrega.
- `TESTES.md`: resultados dos testes locais e roteiro de validação online.

O SQL nega leitura direta das perguntas, sessões e partidas à chave pública. O site e o Python leem jogos, chamam `ranking_public` e enviam jogadas à função `web-game`. A função consulta o gabarito e valida as respostas no servidor, usando uma chave secreta que não aparece no código distribuído. Este protótipo usa apelidos sem autenticação de jogadores.

O banco contém linhas de teste com apelidos que começam por `Teste`, criadas para confirmar a leitura pública e o jogo no navegador. Elas não são partidas da dupla. A dupla pode removê-las no painel antes da apresentação.

## Antes da entrega no Moodle

Preencham nomes e turma acima, completem os testes de `TESTES.md` e adicionem capturas reais. Incluam no ZIP o código da versão publicada, SQL, README, `prompts.md` e evidências. O nome final solicitado é `Turma_Nome1_Nome2.zip`. Confiram o ZIP e preencham o campo de texto da tarefa no Moodle com integrantes, turma, nome do jogo, repositório e site.
