select
  t.shipment_id,
  t.exporter_name,
  t.importer_name,
  t.exporter_country,
  t.importer_country,
  t.hs_code,
  t.value_usd,
  t.ship_date,
  m.entity_id,
  m.score as match_score,
  m.status as match_status
from trade_feed t
left join entity_matches m on m.shipment_id = t.shipment_id
where t.ship_date between :start_date and :end_date
order by t.value_usd desc, t.shipment_id asc
limit 32;
