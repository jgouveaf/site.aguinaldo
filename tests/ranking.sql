-- Testa a função real dentro de uma transação; não deixa dados de teste.
begin;
do $$
declare
  g uuid := gen_random_uuid();
  g2 uuid := gen_random_uuid();
  first_name text;
  n integer;
begin
  insert into public.jogos(id,nome) values(g,'QA temporario '||g),(g2,'QA vazio '||g2);
  insert into public.partidas(id,jogo_id,apelido,valor_ganho,tempo_segundos,acertos,motivo_encerramento,data_hora) values
    ('00000000-0000-4000-8000-000000000001',g,'Mesmo',1000,20,1,'erro','2026-01-01'),
    ('00000000-0000-4000-8000-000000000002',g,'Mesmo',1000,10,1,'erro','2026-01-02'),
    ('00000000-0000-4000-8000-000000000003',g,'Antigo',1000,10,1,'erro','2026-01-01'),
    ('00000000-0000-4000-8000-000000000004',g,'Novo',1000,10,1,'erro','2026-01-01'),
    ('00000000-0000-4000-8000-000000000005',g,'Rico',5000,100,2,'erro','2026-01-01');
  select apelido into first_name from public.ranking_public(g) where posicao=1;
  if first_name <> 'Rico' then raise exception 'Prioridade do premio falhou'; end if;
  select apelido into first_name from public.ranking_public(g) where posicao=2;
  if first_name <> 'Antigo' then raise exception 'Desempate data/ID falhou'; end if;
  select count(*) into n from public.ranking_public(g) where apelido='Mesmo' and tempo_segundos=10;
  if n<>1 then raise exception 'Melhor partida do apelido falhou'; end if;
  select count(*) into n from public.partidas where jogo_id=g;
  if n<>5 then raise exception 'Historico perdido'; end if;
  select count(*) into n from public.ranking_public(g2);
  if n<>0 then raise exception 'Ranking vazio/separacao falhou'; end if;
  insert into public.partidas(id,jogo_id,apelido,valor_ganho,tempo_segundos,acertos,motivo_encerramento)
    select gen_random_uuid(),g,'Extra '||i,0,100+i,0,'erro' from generate_series(1,12) i;
  select count(*) into n from public.ranking_public(g);
  if n<>10 then raise exception 'Limite top 10 falhou'; end if;
end $$;
select 'PASS: premio, tempo, data, ID, melhor apelido, historico, separacao, vazio, top 10' as resultado;
rollback;
