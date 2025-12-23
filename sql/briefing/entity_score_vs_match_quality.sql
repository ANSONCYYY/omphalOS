select
  es.entity_id,
  es.entity_name,
  es.chokepoint_score,
  avg(em.score) as mean_match_score,
  sum(case when em.status = 'REVIEW' then 1 else 0 end) as review_shipments,
  count(*) as total_shipments
from entity_scores es
join entity_matches em on em.entity_id = es.entity_id
group by 1,2,3
order by es.chokepoint_score desc;
