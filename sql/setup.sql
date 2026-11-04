-- Execute no SQL Editor de um projeto Supabase novo. Os prêmios são fictícios.
create extension if not exists pgcrypto;

create table if not exists public.jogos (
  id uuid primary key default gen_random_uuid(),
  nome text not null unique
);
create table if not exists public.perguntas (
  id uuid primary key default gen_random_uuid(),
  enunciado text not null unique,
  alternativa_a text not null,
  alternativa_b text not null,
  alternativa_c text not null,
  alternativa_d text not null,
  correta text not null check (correta in ('A','B','C','D')),
  dificuldade text not null check (dificuldade in ('facil','media','dificil'))
);
create table if not exists public.partidas (
  id uuid primary key,
  jogo_id uuid not null references public.jogos(id),
  apelido text not null check (length(trim(apelido)) between 1 and 30),
  valor_ganho integer not null check (valor_ganho in (0,1000,5000,10000,25000,50000,100000,200000,500000,1000000)),
  tempo_segundos numeric(12,3) not null check (tempo_segundos >= 0),
  acertos integer not null check (acertos between 0 and 9),
  motivo_encerramento text not null check (motivo_encerramento in ('erro','desistencia','concluiu')),
  data_hora timestamptz not null default now(),
  constraint premio_corresponde_acertos check (valor_ganho = (array[0,1000,5000,10000,25000,50000,100000,200000,500000,1000000])[acertos + 1]),
  constraint conclusao_corresponde_acertos check ((motivo_encerramento = 'concluiu') = (acertos = 9))
);
create index if not exists partidas_ranking_idx on public.partidas (jogo_id, valor_ganho desc, tempo_segundos, data_hora, id);

alter table public.jogos enable row level security;
alter table public.perguntas enable row level security;
alter table public.partidas enable row level security;
revoke all on public.perguntas, public.partidas from anon, authenticated;
grant select on public.jogos to anon;
grant select on public.jogos, public.perguntas to service_role;
grant select, insert on public.partidas to service_role;
drop policy if exists jogos_leitura on public.jogos;
create policy jogos_leitura on public.jogos for select to anon using (true);

-- A página só recebe os campos públicos, sem acesso direto a partidas ou gabaritos.
create or replace function public.ranking_public(p_jogo_id uuid)
returns table (posicao bigint, nome_jogo text, apelido text, valor_ganho integer, tempo_segundos numeric, data_hora timestamptz)
language sql stable security definer set search_path = public
as $$
  with melhores as (
    select p.*, row_number() over (
      partition by p.jogo_id, lower(p.apelido)
      order by p.valor_ganho desc, p.tempo_segundos asc, p.data_hora asc, p.id asc
    ) as escolha
    from public.partidas p where p.jogo_id = p_jogo_id
  ), classificados as (
    select m.*, row_number() over (
      order by m.valor_ganho desc, m.tempo_segundos asc, m.data_hora asc, m.id asc
    ) as posicao
    from melhores m where m.escolha = 1
  )
  select c.posicao, j.nome, c.apelido, c.valor_ganho, c.tempo_segundos, c.data_hora
  from classificados c join public.jogos j on j.id = c.jogo_id
  where c.posicao <= 10 order by c.posicao;
$$;
revoke all on function public.ranking_public(uuid) from public;
revoke all on function public.ranking_public(uuid) from authenticated;
grant execute on function public.ranking_public(uuid) to anon;
grant execute on function public.ranking_public(uuid) to service_role;

insert into public.jogos(nome) values ('Desafio Python') on conflict (nome) do nothing;

-- Fontes usadas para revisar os gabaritos: Python Tutorial e Library Reference,
-- https://docs.python.org/3/tutorial/ e https://docs.python.org/3/library/
insert into public.perguntas(enunciado, alternativa_a, alternativa_b, alternativa_c, alternativa_d, correta, dificuldade) values
('Qual função mostra texto no terminal em Python?', 'print()', 'input()', 'len()', 'range()', 'A', 'facil'),
('Qual tipo representa True e False?', 'str', 'int', 'bool', 'list', 'C', 'facil'),
('Qual símbolo inicia um comentário de uma linha em Python?', '#', '//', '<!--', '%', 'A', 'facil'),
('Qual função lê uma entrada digitada no terminal?', 'print()', 'input()', 'open()', 'type()', 'B', 'facil'),
('Qual estrutura guarda elementos em ordem e pode ser alterada?', 'tupla', 'string', 'lista', 'inteiro', 'C', 'facil'),
('Qual palavra inicia uma função em Python?', 'function', 'def', 'func', 'lambda', 'B', 'media'),
('O que retorna len([10, 20, 30])?', '2', '3', '30', 'Erro', 'B', 'media'),
('Qual expressão acessa o valor da chave nome no dicionário pessoa?', 'pessoa.nome', 'pessoa[nome]', 'pessoa["nome"]', 'pessoa->nome', 'C', 'media'),
('Qual comando interrompe um laço imediatamente?', 'stop', 'break', 'pass', 'continue', 'B', 'media'),
('Qual bloco captura uma exceção gerada em try?', 'else', 'finally', 'except', 'raise', 'C', 'media'),
('Qual é o resultado de list(range(2, 6, 2))?', '[2, 4]', '[2, 4, 6]', '[2, 3, 4, 5]', '[4, 6]', 'A', 'dificil'),
('Qual método atualiza um dicionário com as chaves e valores de outro?', 'merge()', 'update()', 'append()', 'extend()', 'B', 'dificil'),
('O que ocorre com o bloco finally após try e except?', 'Executa apenas se houver erro', 'Nunca executa com return', 'Executa normalmente ao sair do bloco', 'Executa apenas sem erro', 'C', 'dificil'),
('Qual expressão produz pares (índice, valor) ao percorrer uma lista?', 'zip(lista)', 'enumerate(lista)', 'range(lista)', 'items(lista)', 'B', 'dificil'),
('Qual operador testa identidade entre dois objetos?', '==', 'in', 'is', '!=', 'C', 'dificil')
on conflict (enunciado) do nothing;

-- Ampliação de 15 para 60 perguntas. Reexecutável, sem alterar perguntas existentes.
-- Fontes: https://docs.python.org/3/tutorial/ e https://docs.python.org/3/library/stdtypes.html
insert into public.perguntas(enunciado, alternativa_a, alternativa_b, alternativa_c, alternativa_d, correta, dificuldade) values
('Qual é o resultado de 2 + 3?', '4', '5', '6', '23', 'B', 'facil'),
('Qual é o resultado de 10 - 4?', '14', '4', '6', '40', 'C', 'facil'),
('Qual é o resultado de 3 * 4?', '12', '7', '34', '1', 'A', 'facil'),
('Qual operador calcula uma potência em Python?', '^', '//', '%', '**', 'D', 'facil'),
('Qual é o resultado de 7 % 3?', '2', '3', '1', '0', 'C', 'facil'),
('Qual símbolo atribui um valor a uma variável?', '=', '==', '!=', '<=', 'A', 'facil'),
('Qual operador compara se dois valores são iguais?', '=', '==', '=>', '+=', 'B', 'facil'),
('Qual palavra-chave inicia uma condição em Python?', 'when', 'caseif', 'test', 'if', 'D', 'facil'),
('Qual palavra-chave introduz a alternativa de um if quando a condição é falsa?', 'else', 'then', 'otherwise', 'end', 'A', 'facil'),
('Qual tipo representa o número inteiro 42?', 'float', 'str', 'int', 'bool', 'C', 'facil'),
('Qual tipo representa o número 3.5?', 'int', 'float', 'list', 'str', 'B', 'facil'),
('Qual é o primeiro índice de uma lista não vazia?', '1', '-1', '2', '0', 'D', 'facil'),
('Qual é o valor de len("casa")?', '4', '3', '5', '0', 'A', 'facil'),
('Qual expressão cria uma lista vazia?', '{}', '()', '[]', '""', 'C', 'facil'),
('Qual palavra-chave importa um módulo?', 'include', 'import', 'using', 'require', 'B', 'facil'),
('Qual é o resultado de 17 // 3?', '5.666', '6', '2', '5', 'D', 'media'),
('Qual é o resultado de "Python"[1]?', '''y''', '''P''', '''t''', '''n''', 'A', 'media'),
('Qual é o resultado de [10, 20, 30][-1]?', '10', '20', '30', '-1', 'C', 'media'),
('Qual é o resultado de [0, 1, 2, 3][1:3]?', '[0, 1, 2]', '[1, 2]', '[1, 2, 3]', '[2, 3]', 'B', 'media'),
('Qual método adiciona um único elemento ao final de uma lista?', 'add()', 'push()', 'put()', 'append()', 'D', 'media'),
('Qual é o resultado de sorted([3, 1, 2])?', '[1, 2, 3]', '[3, 2, 1]', '[3, 1, 2]', 'None', 'A', 'media'),
('Qual é o resultado de sum([2, 3, 4])?', '24', '3', '9', '5', 'C', 'media'),
('Qual é o resultado de "  oi  ".strip()?', '''  oi''', '''oi''', '''oi  ''', '''  oi  ''', 'B', 'media'),
('Qual é o resultado de "a,b,c".split(",")?', '''abc''', '[''a,b,c'']', '(''a'', ''b'', ''c'')', '[''a'', ''b'', ''c'']', 'D', 'media'),
('Qual é o resultado de bool([])?', 'False', 'True', 'None', '0', 'A', 'media'),
('Qual comando pula para a próxima iteração de um laço?', 'break', 'pass', 'continue', 'return', 'C', 'media'),
('Qual palavra-chave devolve um valor e encerra uma chamada de função?', 'yieldall', 'return', 'send', 'exitdef', 'B', 'media'),
('Qual é o resultado de {"a": 1}.get("b", 0)?', 'None', '1', 'KeyError', '0', 'D', 'media'),
('Qual é o resultado de [x * 2 for x in range(3)]?', '[0, 2, 4]', '[2, 4, 6]', '[0, 1, 2]', '[0, 2, 4, 6]', 'A', 'media'),
('Qual modo de open cria um arquivo novo e falha se ele já existir?', 'w', 'a', 'x', 'r', 'C', 'media'),
('Qual é o resultado de -7 // 3?', '-2', '-3', '2', '3', 'B', 'dificil'),
('Qual é o resultado de "abcd"[::-1]?', '''abcd''', '''abc''', '''d''', '''dcba''', 'D', 'dificil'),
('Qual é o resultado de list(zip([1, 2], ["a"]))?', '[(1, ''a'')]', '[(1, ''a''), (2, None)]', '[(2, ''a'')]', '[]', 'A', 'dificil'),
('Qual é o resultado de all([])?', 'False', 'None', 'True', '[]', 'C', 'dificil'),
('Qual é o resultado de any([])?', 'True', 'False', 'None', '[]', 'B', 'dificil'),
('Qual é o resultado de 0 or 7?', 'True', '0', 'False', '7', 'D', 'dificil'),
('Qual é o resultado de 3 and 8?', '8', 'True', '3', 'False', 'A', 'dificil'),
('Após a = [1]; b = a; b.append(2), qual é o valor de a?', '[1]', '[2]', '[1, 2]', 'None', 'C', 'dificil'),
('Após a = [1]; b = a.copy(); b.append(2), qual é o valor de a?', '[1, 2]', '[1]', '[2]', '[]', 'B', 'dificil'),
('Qual é o resultado de len({1, 1, 2, 2, 3})?', '5', '2', '1', '3', 'D', 'dificil'),
('Qual expressão cria uma tupla com um único elemento inteiro?', '(1,)', '(1)', '[1]', '{1}', 'A', 'dificil'),
('Em def f(*args), qual tipo recebe os argumentos posicionais extras?', 'list', 'dict', 'tuple', 'set', 'C', 'dificil'),
('Em def f(**kwargs), qual tipo recebe os argumentos nomeados extras?', 'tuple', 'dict', 'list', 'str', 'B', 'dificil'),
('Em um laço for, quando o bloco else é executado?', 'Sempre que houver break', 'Somente na primeira iteração', 'Apenas se ocorrer exceção', 'Quando o laço termina sem break', 'D', 'dificil'),
('Qual é o resultado de (lambda x: x + 1)(4)?', '5', '4', '1', 'None', 'A', 'dificil')
on conflict (enunciado) do nothing;
