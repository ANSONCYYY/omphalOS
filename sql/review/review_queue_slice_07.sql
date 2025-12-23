select
  rq.shipment_id,
  rq.exporter_name,
  rq.reason,
  rq.candidates_json
from review_queue rq
where rq.shipment_id like 'S07%'
order by rq.shipment_id asc
limit :limit;
