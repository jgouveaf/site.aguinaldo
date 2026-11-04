# Testes e evidências — 04/11/2026

## Resultado desta revisão

Dez testes unitários passaram no Python 3.12. A validação online concluiu partidas nos três modos, confirmou tempos persistidos iguais aos medidos pelo Python, verificou o ranking real e repetiu o envio final. O navegador concluiu nove acertos, simulou perda da resposta final depois da gravação no servidor e reenviou exatamente o mesmo conteúdo com sucesso.

## Python local

Comando executado: `python -m unittest discover -s tests -v`.
Saída em `evidencias/testes-python.txt`.

- Nove acertos: R$ 1.000.000,00, sem somar etapas — PASSOU.
- Erro na primeira: R$ 0,00; alternativa inválida permite corrigir — PASSOU.
- Erro após acertos e desistência: conserva o último prêmio — PASSOU.
- Apelido vazio: solicita nova entrada — PASSOU no fluxo dos testes.
- Falha de rede: resposta e sessão mantidas; retomada sem nova partida — PASSOU.
- Resposta final perdida após salvamento: mesmo ID, resposta e tempo reenviados; uma confirmação — PASSOU.
- Cronômetro: exclui rede, reenvio e tempo no menu; soma só os intervalos de resposta — PASSOU.
- Ranking vazio e desconexão HTTP transitória — PASSOU.

## Integração real

Execução automatizada de `game.play` com `GameClient` real, sem substituir a conexão nem o relógio. Entradas foram fornecidas por um roteiro que conhece os gabaritos, com espera de 150 ms por resposta. São testes de software, não recordes humanos.

Apelido: **QA Python 04-11**.

- Clássico: 9 acertos; R$ 1.000.000,00; **1,354 s**; ID `cb6fa0fb-b19e-423f-9799-900d56941fba`.
- Rápido: 6 acertos; R$ 1.000.000,00; **0,903 s**; ID `2992ded0-56d2-4091-b941-d134c4efd8a4`.
- Maratona: 15 acertos; R$ 1.000.000,00; **2,258 s**; ID `ad1ee3c3-306e-48b2-aa2b-bd8c7d700557`.

A leitura SQL confirmou tempo_ativo_segundos igual a tempo_segundos para as três partidas. Confirmou também 9/6/15 perguntas únicas e as dificuldades na ordem correta. A leitura pública do ranking retornou os mesmos valores. Uma nova execução do Python encontrou os três resultados, comprovando persistência fora da execução original. O reenvio final retornou o mesmo registro.

Arquivos: `evidencias/python-execucao.txt`, `partidas-verificadas.json`, `ranking-python.png` e `permissoes-persistencia.json`. A saída do Python é transcrição real em texto; não foi apresentada como captura nativa do terminal.

## Ranking SQL

`tests/ranking.sql` executado no banco real dentro de BEGIN/ROLLBACK. Todos os registros temporários foram revertidos.

Resultado: PASS para prioridade do prêmio; menor tempo; data mais antiga; ID como desempate; melhor partida por apelido; preservação do histórico; separação entre jogos; ranking vazio e limite de dez resultados.

## Navegador

`python tests/browser_checks.py` executado com Chromium, contra prévia local ligada à função e banco reais.

- Conclusão de nove perguntas sem repetição; ordem 3 fáceis, 3 médias, 3 difíceis — PASSOU.
- Interceptação da última resposta: o servidor recebeu e salvou, mas o navegador recebeu falha. Botões de resposta foram bloqueados, o botão de reenvio apareceu e o corpo reenviado foi idêntico — PASSOU.
- Resultado de R$ 1.000.000,00 mostrado e ranking atualizado — PASSOU.
- Ranking vazio e falha HTTP 503: mensagens correspondentes — PASSOU com respostas de transporte simuladas.
- Após restaurar a rede e atualizar: ranking voltou — PASSOU.
- Recarregar a página: resultado Python persistente visível — PASSOU.
- Larguras 320, 375, 390, 768 e 1440: sem vazamento horizontal da página — PASSOU após corrigir o pódio com três prêmios grandes.
- Preferência por movimento reduzido — PASSOU.
- Erros JavaScript não tratados: nenhum observado.

Capturas: `site-desktop.png`, `site-celular.png`, `partida-navegador.png`, `resultado-navegador.png`. Detalhes em `browser-tests.json`. Os testes podem gerar mais de uma partida QA quando repetidos; isso não é duplicação de um mesmo ID.

## Permissões

GET público direto em perguntas, partidas e sessoes_web retornou HTTP 401. O ranking público permaneceu acessível. Os avisos do advisor sobre RLS sem política de leitura nas tabelas privadas e SECURITY DEFINER no ranking correspondem ao desenho existente: tabelas privadas e função pública restrita de leitura, sem escrita de partidas.

## Limites e próximos passos humanos

O teste visual não substitui a demonstração dos integrantes. Falta captura nativa do terminal durante a própria apresentação, além dos dados de turma/sobrenomes e do prompt histórico 22 completo. Não houve envio no Moodle. O tempo fornecido pelo cliente atende ao exercício, mas pode ser manipulado em um cliente modificado; o projeto não é adequado a competição pública com prêmio real.
