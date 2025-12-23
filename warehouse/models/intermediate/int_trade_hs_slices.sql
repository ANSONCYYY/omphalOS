select
  shipment_id,
  exporter_name,
  importer_name,
  exporter_country,
  importer_country,
  country,
  hs_code,
  substr(hs_code, 1, 2) as hs2,
  substr(hs_code, 1, 4) as hs4,
  substr(hs_code, 1, 6) as hs6,
  value_usd,
  ship_date
from {{ ref('stg_trade_feed') }}
