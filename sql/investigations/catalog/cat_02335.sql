with matches as (
  select shipment_id, entity_id, score, status
  from entity_matches
  where status in ('REVIEW','AMBIGUOUS','NO_MATCH')
),
joined as (
  select m.entity_id, t.hs2, count(*) as flagged_shipments, sum(t.value_usd) as flagged_value_usd
  from matches m
  join v_trade_enriched t on t.shipment_id = m.shipment_id
  group by 1,2
)
select *
from joined
order by flagged_value_usd desc, flagged_shipments desc
limit 500;
