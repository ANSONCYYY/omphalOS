-- HS drilldown playbook
--
-- Inputs
-- :hs2, :start_date, :end_date, :limit

with base as (
  select
    t.shipment_id,
    t.exporter_name,
    t.importer_name,
    t.exporter_country,
    t.importer_country,
    t.hs_code,
    substr(t.hs_code, 1, 2) as hs2,
    substr(t.hs_code, 1, 4) as hs4,
    substr(t.hs_code, 1, 6) as hs6,
    t.value_usd,
    t.ship_date
  from trade_feed t
  where substr(t.hs_code, 1, 2) = :hs2
    and t.ship_date between :start_date and :end_date
),
flows as (
  select
    exporter_country,
    importer_country,
    count(*) as shipment_count,
    sum(value_usd) as total_value_usd
  from base
  group by 1,2
),
entities as (
  select
    m.entity_id,
    r.entity_name,
    r.country,
    count(*) as shipment_count,
    sum(b.value_usd) as total_value_usd,
    avg(m.score) as mean_match_score
  from entity_matches m
  join base b on b.shipment_id = m.shipment_id
  join registry r on r.entity_id = m.entity_id
  group by 1,2,3
)
select
  'flows' as section,
  exporter_country as k1,
  importer_country as k2,
  shipment_count,
  total_value_usd,
  null as mean_match_score
from flows
union all
select
  'entities' as section,
  entity_id as k1,
  entity_name as k2,
  shipment_count,
  total_value_usd,
  mean_match_score
from entities
order by section asc, total_value_usd desc
limit :limit;
