with scoped as (
  select * from v_trade_enriched
  where hs2 = '92'
),
by_pair as (
  select exporter_country, importer_country, count(*) as shipments, sum(value_usd) as total_value_usd
  from scoped
  group by 1,2
),
ranked as (
  select *, row_number() over (order by total_value_usd desc, shipments desc) as r
  from by_pair
)
select * from ranked where r <= 200;
