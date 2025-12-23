select
  entity_id,
  entity_name,
  country,
  shipment_count,
  total_value_usd,
  chokepoint_score,
  rank() over (order by chokepoint_score desc, total_value_usd desc) as risk_rank
from {{ ref('stg_entity_scores') }}
