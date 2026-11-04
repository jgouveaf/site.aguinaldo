-- Execute após setup.sql. Sessões do jogo no navegador não são públicas.
create table if not exists public.sessoes_web (
  id uuid primary key default gen_random_uuid(),
  jogo_id uuid not null references public.jogos(id),
  apelido text not null check (length(trim(apelido)) between 1 and 30),
  pergunta_ids uuid[] not null check (array_length(pergunta_ids, 1) = 9),
  indice integer not null default 0 check (indice between 0 and 9),
  valor_ganho integer not null default 0 check (valor_ganho in (0,1000,5000,10000,25000,50000,100000,200000,500000,1000000)),
  iniciada_em timestamptz not null default now(),
  encerrada_em timestamptz,
  motivo text check (motivo in ('erro','desistencia','concluiu')),
  check ((motivo is null and encerrada_em is null) or (motivo is not null and encerrada_em is not null)),
  check (valor_ganho = (array[0,1000,5000,10000,25000,50000,100000,200000,500000,1000000])[indice + 1])
);

alter table public.sessoes_web enable row level security;
revoke all on public.sessoes_web from anon, authenticated;
grant select, insert, update on public.sessoes_web to service_role;

-- A gravação da partida acontece na mesma transação que encerra a sessão.
create or replace function public.registrar_partida_web()
returns trigger language plpgsql security definer set search_path = public
as $$
begin
  if new.motivo is not null and old.motivo is null then
    insert into public.partidas
      (id, jogo_id, apelido, valor_ganho, tempo_segundos, acertos, motivo_encerramento, data_hora)
    values
      (new.id, new.jogo_id, new.apelido, new.valor_ganho,
       round(greatest(0, extract(epoch from (new.encerrada_em - new.iniciada_em)))::numeric, 3),
       new.indice, new.motivo, new.encerrada_em)
    on conflict (id) do nothing;
  end if;
  return new;
end;
$$;
revoke all on function public.registrar_partida_web() from public, anon, authenticated;
drop trigger if exists ao_encerrar_sessao_web on public.sessoes_web;
create trigger ao_encerrar_sessao_web
after update of motivo on public.sessoes_web
for each row execute function public.registrar_partida_web();
