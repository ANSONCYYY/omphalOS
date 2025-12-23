select
  rq.shipment_id,
  rq.exporter_name,
  rq.reason,
  t.importer_name,
  t.exporter_country,
  t.importer_country,
  t.hs_code,
  t.value_usd,
  t.ship_date
from review_queue rq
join trade_feed t on t.shipment_id = rq.shipment_id
order by t.value_usd desc, rq.shipment_id asc
limit :limit;
