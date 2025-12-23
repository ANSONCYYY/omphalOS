-- Entity casefile playbook
--
-- Inputs
-- :entity_id, :start_date, :end_date, :limit

with s as (
  select
    entity_id,
    entity_name,
    country,
    shipment_count,
    total_value_usd,
    chokepoint_score
  from entity_scores
  where entity_id = :entity_id
),
shipments as (
  select
    t.shipment_id,
    t.exporter_name,
    t.importer_name,
    t.exporter_country,
    t.importer_country,
    t.hs_code,
    substr(t.hs_code, 1, 2) as hs2,
    t.value_usd,
    t.ship_date,
    m.score as match_score,
    m.status as match_status,
    m.explanation
  from entity_matches m
  join trade_feed t on t.shipment_id = m.shipment_id
  where m.entity_id = :entity_id
    and t.ship_date between :start_date and :end_date
),
hs_mix as (
  select
    hs2,
    count(*) as shipment_count,
    sum(value_usd) as total_value_usd,
    avg(match_score) as mean_match_score
  from shipments
  group by 1
),
counterparties as (
  select
    importer_name,
    count(*) as shipment_count,
    sum(value_usd) as total_value_usd
  from shipments
  group by 1
)
select
  'summary' as section,
  s.entity_id as k1,
  s.entity_name as k2,
  s.country as k3,
  s.shipment_count as n1,
  s.total_value_usd as n2,
  s.chokepoint_score as n3,
  null as n4
from s
union all
select
  'hs_mix',
  hs2,
  null,
  null,
  shipment_count,
  total_value_usd,
  mean_match_score,
  null
from hs_mix
union all
select
  'counterparties',
  importer_name,
  null,
  null,
  shipment_count,
  total_value_usd,
  null,
  null
from counterparties
order by section asc, n2 desc
limit :limit;
