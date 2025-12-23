select
  cast((score * 10) as integer) / 10.0 as score_bucket,
  count(*) as shipment_count
from entity_matches
group by 1
order by score_bucket asc;
