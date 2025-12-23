select
  hs2,
  ship_date,
  exporter_country,
  importer_country,
  value_usd
from v_trade_enriched
where hs2 = '81' and ship_date between :start_date and :end_date
order by ship_date asc, value_usd desc
limit :limit;
