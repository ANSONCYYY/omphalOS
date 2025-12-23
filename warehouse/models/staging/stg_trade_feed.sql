select
  shipment_id,
  upper(trim(exporter_name)) as exporter_name,
  upper(trim(importer_name)) as importer_name,
  upper(trim(exporter_country)) as exporter_country,
  upper(trim(importer_country)) as importer_country,
  hs_code,
  substr(hs_code, 1, 2) as hs2,
  substr(hs_code, 1, 4) as hs4,
  substr(hs_code, 1, 6) as hs6,
  cast(value_usd as double) as value_usd,
  ship_date,
  {{ month_bucket('ship_date') }} as ship_month
from {{ source('omphalos', 'trade_feed') }}
