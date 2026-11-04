# Testes e evidências

## Testes locais automatizados

Comando: `python -m unittest discover -s tests -v`. Os testes cobrem nove acertos e R$ 1.000.000,00, erro na primeira e após acertos, desistência, entradas inválidas, ranking vazio e retomada após falha de conexão. Resultado observado nesta preparação: **5 testes passaram em 04/11/2026**.

## Validação do banco online

Projeto criado em 04/11/2026: `https://yserkieipgjqjciouole.supabase.co`. A consulta SQL confirmou 5 perguntas por dificuldade. A API pública retornou o jogo e as linhas de teste do ranking; as tabelas `perguntas` e `partidas` recusaram leitura direta com a chave pública (HTTP 401). A função `web-game` forneceu uma pergunta sem o campo `correta`, registrou um erro na primeira questão e registrou nove acertos com prêmio de R$ 1.000.000,00. O reenvio da última resposta manteve uma única partida no banco. O programa Python realizou uma partida real com o apelido `Teste Python`, salvou R$ 0,00 e apareceu no ranking consultado pelo site. O site ainda não foi publicado no GitHub Pages. A dupla deve completar os itens abaixo com resultados e capturas reais:

Na primeira execução online do Python, a cadeia TLS apresentada nesta máquina foi rejeitada pelo modo estrito do Python 3.13 por falta do campo Authority Key Identifier. O cliente passou a desligar apenas a checagem estrita de formato do certificado; a validação da autoridade certificadora e do nome do servidor continua ativa. A partida foi repetida com sucesso.

| Caso | Esperado | Observado e evidência |
| --- | --- | --- |
| Salvar partida pelo navegador | Uma linha em `partidas` com jogo, apelido, valor e duração | CONFIRMADO pela função `web-game` |
| Concluir nove acertos no navegador | R$ 1.000.000,00 e uma linha no banco | CONFIRMADO via API; teste visual pendente |
| Atualizar site publicado | Mesma partida visível com R$ e mm:ss | PENDENTE |
| Dois tempos com mesmo valor | Menor tempo primeiro | PENDENTE |
| Mesmo apelido com várias partidas | Só a melhor aparece; todas permanecem no banco | PENDENTE |
| Dois jogos | Rankings separados | PENDENTE |
| Reenvio da última resposta no navegador | Uma única linha por ID | CONFIRMADO via API |
| Partida no Python e leitura pelo site | Mesmo apelido, prêmio e tempo no ranking | CONFIRMADO via API (`Teste Python`); captura visual pendente |
| Falha de conexão no programa Python | Não confirmar antes do sucesso; uma única linha por ID | PENDENTE |
| Reiniciar programa | Resultado permanece no site | PENDENTE |
| Jogo sem partidas | Mensagem de ranking vazio | PENDENTE |
| Falha de consulta | Mensagem de erro no site | PENDENTE |

Adicionem capturas reais do terminal, site e banco mostrando a mesma partida. Não fabriquem evidências. Guardem as capturas nesta pasta antes de montar o ZIP final.
