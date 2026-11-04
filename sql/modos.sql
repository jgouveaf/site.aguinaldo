-- Execute após setup.sql e web_game.sql. Cada modo tem ranking separado.
alter table public.sessoes_web add column if not exists modo text not null default 'classico';
alter table public.partidas add column if not exists modo text not null default 'classico';

alter table public.sessoes_web
  drop constraint if exists sessoes_web_pergunta_ids_check,
  drop constraint if exists sessoes_web_indice_check,
  drop constraint if exists sessoes_web_valor_ganho_check,
  drop constraint if exists sessoes_web_check1;
alter table public.partidas
  drop constraint if exists partidas_acertos_check,
  drop constraint if exists partidas_valor_ganho_check,
  drop constraint if exists premio_corresponde_acertos,
  drop constraint if exists conclusao_corresponde_acertos;

alter table public.sessoes_web
  add constraint sessoes_modo_check check (modo in ('classico','rapido','maratona')),
  add constraint sessoes_perguntas_modo_check check (array_length(pergunta_ids, 1) = case modo when 'rapido' then 6 when 'maratona' then 15 else 9 end),
  add constraint sessoes_indice_modo_check check (indice between 0 and case modo when 'rapido' then 6 when 'maratona' then 15 else 9 end),
  add constraint sessoes_premio_modo_check check (valor_ganho = case modo
    when 'rapido' then (array[0,2000,10000,50000,200000,500000,1000000])[indice + 1]
    when 'maratona' then (array[0,500,1000,2500,5000,10000,20000,40000,75000,125000,200000,300000,450000,600000,800000,1000000])[indice + 1]
    else (array[0,1000,5000,10000,25000,50000,100000,200000,500000,1000000])[indice + 1] end);

alter table public.partidas
  add constraint partidas_modo_check check (modo in ('classico','rapido','maratona')),
  add constraint partidas_acertos_modo_check check (acertos between 0 and case modo when 'rapido' then 6 when 'maratona' then 15 else 9 end),
  add constraint partidas_premio_modo_check check (valor_ganho = case modo
    when 'rapido' then (array[0,2000,10000,50000,200000,500000,1000000])[acertos + 1]
    when 'maratona' then (array[0,500,1000,2500,5000,10000,20000,40000,75000,125000,200000,300000,450000,600000,800000,1000000])[acertos + 1]
    else (array[0,1000,5000,10000,25000,50000,100000,200000,500000,1000000])[acertos + 1] end),
  add constraint partidas_conclusao_modo_check check ((motivo_encerramento = 'concluiu') = (acertos = case modo when 'rapido' then 6 when 'maratona' then 15 else 9 end));

create or replace function public.registrar_partida_web()
returns trigger language plpgsql security definer set search_path = public
as $$
begin
  if new.motivo is not null and old.motivo is null then
    insert into public.partidas
      (id, jogo_id, apelido, modo, valor_ganho, tempo_segundos, acertos, motivo_encerramento, data_hora)
    values
      (new.id, new.jogo_id, new.apelido, new.modo, new.valor_ganho,
       round(greatest(0, extract(epoch from (new.encerrada_em - new.iniciada_em)))::numeric, 3),
       new.indice, new.motivo, new.encerrada_em)
    on conflict (id) do nothing;
  end if;
  return new;
end;
$$;
revoke all on function public.registrar_partida_web() from public, anon, authenticated;

insert into public.jogos(nome) values ('Desafio Rápido'), ('Maratona do Milhão') on conflict (nome) do nothing;
