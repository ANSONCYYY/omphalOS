select
  hs2,
  ship_month,
  exporter_country,
  sum(value_usd) as total_value_usd,
  count(*) as shipment_count
from {"{ ref('stg_trade_feed') }" }
where hs2 = '60'
group by 1,2,3
