select
  status as match_status,
  count(*) as shipment_count
from entity_matches
group by 1
order by shipment_count desc;
