select
  m.entity_id,
  r.entity_name,
  substr(t.hs_code, 1, 2) as hs2,
  count(*) as shipment_count,
  sum(t.value_usd) as total_value_usd
from entity_matches m
join trade_feed t on t.shipment_id = m.shipment_id
join registry r on r.entity_id = m.entity_id
where substr(t.hs_code, 1, 2) = :hs2
group by 1,2,3
order by total_value_usd desc, shipment_count desc
limit :limit;
