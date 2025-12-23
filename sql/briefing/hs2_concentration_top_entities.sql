with top_entities as (
  select entity_id
  from entity_scores
  order by chokepoint_score desc
  limit :top_n
)
select
  substr(t.hs_code, 1, 2) as hs2,
  count(*) as shipment_count,
  sum(t.value_usd) as total_value_usd
from entity_matches m
join trade_feed t on t.shipment_id = m.shipment_id
where m.entity_id in (select entity_id from top_entities)
group by 1
order by total_value_usd desc, shipment_count desc;
