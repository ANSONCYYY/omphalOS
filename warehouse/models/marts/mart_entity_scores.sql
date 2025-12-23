with s as (
  select * from {{ ref('stg_entity_scores') }}
),
ranked as (
  select
    *,
    dense_rank() over (order by chokepoint_score desc) as risk_rank,
    ntile(4) over (order by chokepoint_score desc) as risk_quartile
  from s
)
select
  entity_id,
  entity_name,
  country,
  shipment_count,
  total_value_usd,
  chokepoint_score,
  risk_rank,
  case risk_quartile
    when 1 then 'highest'
    when 2 then 'high'
    when 3 then 'medium'
    else 'low'
  end as risk_tier
from ranked
