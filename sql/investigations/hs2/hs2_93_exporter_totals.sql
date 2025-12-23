select
  hs2,
  exporter_country,
  sum(value_usd) as total_value_usd,
  count(*) as shipment_count
from v_trade_enriched
where hs2 = '93'
group by 1,2
order by total_value_usd desc;
