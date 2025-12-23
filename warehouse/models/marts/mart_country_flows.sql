select
  exporter_country,
  importer_country,
  hs2,
  count(*) as shipment_count,
  sum(value_usd) as total_value_usd
from {{ ref('int_trade_hs_slices') }}
group by 1,2,3
