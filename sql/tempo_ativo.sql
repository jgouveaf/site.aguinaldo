-- Execute após modos.sql. Compatível com clientes antigos (tempo do servidor).
alter table public.sessoes_web add column if not exists tempo_ativo_segundos numeric(12,3)
  check (tempo_ativo_segundos >= 0);

create or replace function public.registrar_partida_web()
returns trigger language plpgsql security definer set search_path = public
as $$
begin
  if new.motivo is not null and old.motivo is null then
    insert into public.partidas
      (id, jogo_id, apelido, modo, valor_ganho, tempo_segundos, acertos, motivo_encerramento, data_hora)
    values
      (new.id, new.jogo_id, new.apelido, new.modo, new.valor_ganho,
       coalesce(new.tempo_ativo_segundos,
         round(greatest(0, extract(epoch from (new.encerrada_em - new.iniciada_em)))::numeric, 3)),
       new.indice, new.motivo, new.encerrada_em)
    on conflict (id) do nothing;
  end if;
  return new;
end;
$$;
revoke all on function public.registrar_partida_web() from public, anon, authenticated;
