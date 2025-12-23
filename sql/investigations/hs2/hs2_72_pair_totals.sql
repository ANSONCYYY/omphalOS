select
  hs2,
  exporter_country,
  importer_country,
  sum(value_usd) as total_value_usd,
  count(*) as shipment_count
from v_trade_enriched
where hs2 = '72'
group by 1,2,3
order by total_value_usd desc;
