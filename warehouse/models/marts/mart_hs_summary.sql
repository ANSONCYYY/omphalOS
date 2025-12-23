select
  hs2,
  hs4,
  count(*) as shipment_count,
  sum(value_usd) as total_value_usd,
  avg(value_usd) as mean_value_usd
from {{ ref('int_trade_hs_slices') }}
group by 1,2
