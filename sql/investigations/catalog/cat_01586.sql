with scoped as (
  select * from v_trade_enriched
  where exporter_country = 'FR' and ship_date between :start_date and :end_date
),
by_hs2 as (
  select hs2, count(*) as shipments, sum(value_usd) as total_value_usd
  from scoped
  group by 1
),
ranked as (
  select *, dense_rank() over (order by total_value_usd desc) as r
  from by_hs2
)
select * from ranked where r <= 50;
