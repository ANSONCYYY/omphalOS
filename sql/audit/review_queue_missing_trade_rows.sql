select rq.*
from review_queue rq
left join trade_feed t on t.shipment_id = rq.shipment_id
where t.shipment_id is null;
