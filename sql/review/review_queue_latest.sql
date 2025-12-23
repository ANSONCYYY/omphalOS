select
  shipment_id,
  exporter_name,
  reason,
  candidates_json
from review_queue
order by shipment_id desc
limit :limit;
