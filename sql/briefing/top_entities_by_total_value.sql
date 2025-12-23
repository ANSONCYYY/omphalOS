select
  entity_id,
  entity_name,
  country,
  shipment_count,
  total_value_usd,
  chokepoint_score
from entity_scores
order by total_value_usd desc, entity_id asc
limit :limit;
