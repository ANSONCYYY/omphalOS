select
  shipment_id,
  exporter_name,
  importer_name,
  exporter_country,
  importer_country,
  hs_code,
  value_usd,
  ship_date
from trade_feed
where value_usd >= :min_value_usd
order by value_usd desc, shipment_id asc
limit :limit;
