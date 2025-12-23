select shipment_id, entity_id, count(*) as c
from entity_matches
group by 1,2
having count(*) > 1;
