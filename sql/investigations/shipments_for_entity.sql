select
  t.shipment_id,
  t.exporter_name,
  t.importer_name,
  t.exporter_country,
  t.importer_country,
  t.hs_code,
  t.value_usd,
  t.ship_date,
  m.score as match_score,
  m.status as match_status
from entity_matches m
join trade_feed t on t.shipment_id = m.shipment_id
where m.entity_id = :entity_id
order by t.ship_date asc, t.value_usd desc;
