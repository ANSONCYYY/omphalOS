select m.*
from entity_matches m
left join trade_feed t on t.shipment_id = m.shipment_id
where t.shipment_id is null;
