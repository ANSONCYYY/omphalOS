select
  entity_id,
  matched_entity_name as entity_name,
  matched_entity_country as country,
  count(*) as shipment_count,
  sum(value_usd) as total_value_usd,
  avg(match_score) as mean_match_score
from {{ ref('int_trade_with_entity') }}
where entity_id is not null
group by 1,2,3
