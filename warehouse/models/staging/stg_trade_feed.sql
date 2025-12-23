with base as (
  select * from {{ source('raw', 'trade_feed') }}
)
select
  shipment_id,
  upper(trim(exporter_name)) as exporter_name,
  upper(trim(importer_name)) as importer_name,
  exporter_country,
  importer_country,
  coalesce(exporter_country, country) as country,
  hs_code,
  cast(value_usd as {{ dbt.type_numeric() }}) as value_usd,
  ship_date
from base
