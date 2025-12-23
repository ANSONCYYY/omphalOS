select
  hs2,
  exporter_country,
  sum(total_value_usd) as total_value_usd,
  sum(shipment_count) as shipment_count,
  { safe_divide('sum(total_value_usd)', 'sum(shipment_count)') } as avg_value_usd
from {"{ ref('int_hs2_"+hs2+"_monthly') }" }
group by 1,2
order by total_value_usd desc
