select
  m.entity_id,
  r.entity_name,
  t.hs2,
  count(*) as matched_shipments,
  sum(t.value_usd) as matched_value_usd
from {{ ref('stg_entity_matches') }} m
join {{ ref('stg_trade_feed') }} t on t.shipment_id = m.shipment_id
join {{ ref('stg_registry') }} r on r.entity_id = m.entity_id
where m.status = 'MATCH'
group by 1,2,3
