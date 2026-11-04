# Seu projeto completo

O pacote inclui o jogo Python, o site, o banco SQL, os testes e as evidências.

## Jogar

Extraia tudo. No Windows, dê dois cliques em **JOGAR.bat**. É necessário Python 3.10 ou superior instalado e internet. Não há pacotes extras para o jogo. O menu permite jogar, consultar ranking e retomar uma partida cujo envio falhou.

O atalho **ABRIR_SITE.url** abre https://jgouveaf.github.io/site.aguinaldo/.
**TESTAR.bat** executa os dez testes locais sem mexer no banco.

## Onde estão os arquivos

- game.py: programa principal.
- site/: HTML, CSS e JavaScript publicados.
- sql/: scripts para recriar o banco e as perguntas.
- supabase/: função do servidor e configuração.
- evidencias/: execução real do Python em texto, registros JSON e capturas do site.
- tests/: testes do Python, navegador e ranking SQL.
- README.md: instalação, arquitetura e explicação das funções.
- prompts.md: histórico de uso de IA e lacunas identificadas.
- TESTES.md: o que foi executado e seus resultados.

## Conferir antes de enviar no Moodle

Participantes informados: João Gouvêa Ferreira, Henrique e João Vitor.
Preencher turma e sobrenomes de Henrique e João Vitor. Confirmar com o professor os três integrantes, pois o documento pede dupla.
Recuperar o texto completo do prompt histórico 22 e identificar autores dos prompts antigos. Essa informação não estava disponível nesta conversa.
As evidências do Python incluem a saída real em texto. Para cumprir literalmente a captura do terminal solicitada no enunciado, executem JOGAR.bat e tirem uma captura de sua própria apresentação, junto do ranking da mesma partida.

Renomeie o ZIP conforme a orientação do professor (o padrão do enunciado é Turma_Nome1_Nome2.zip). Abra o ZIP para conferir. Envie no Moodle com os links abaixo. O envio não foi realizado por este assistente.

## Texto para o Moodle

Integrantes: João Gouvêa Ferreira, Henrique [sobrenome], João Vitor [sobrenome]
Turma: [preencher]
Nome do jogo: Desafio Python
Repositório: https://github.com/jgouveaf/site.aguinaldo
Site: https://jgouveaf.github.io/site.aguinaldo/

## Apresentação

Demonstrem o modo Clássico. Expliquem calculate_prize, play e save_answer; mostrem a chamada da API e a partida no ranking. Os outros modos são extras. Todos precisam entender e conseguir alterar o Python.
