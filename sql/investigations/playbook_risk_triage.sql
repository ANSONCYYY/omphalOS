-- Risk triage playbook
--
-- Inputs
-- :start_date, :end_date, :min_value_usd, :min_chokepoint_score, :limit

with scored as (
  select
    es.entity_id,
    es.entity_name,
    es.country,
    es.shipment_count,
    es.total_value_usd,
    es.chokepoint_score
  from entity_scores es
  where es.chokepoint_score >= :min_chokepoint_score
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
    m.entity_id,
    m.score as match_score,
    m.status as match_status
  from trade_feed t
  join entity_matches m on m.shipment_id = t.shipment_id
  where t.ship_date between :start_date and :end_date
),
joined as (
  select
    s.entity_id,
    s.entity_name,
    s.country,
    s.shipment_count,
    s.total_value_usd,
    s.chokepoint_score,
    sh.shipment_id,
    sh.importer_name,
    sh.exporter_country,
    sh.importer_country,
    sh.hs_code,
    sh.hs2,
    sh.value_usd,
    sh.ship_date,
    sh.match_score,
    sh.match_status
  from scored s
  join shipments sh on sh.entity_id = s.entity_id
),
ranked as (
  select
    *,
    dense_rank() over (order by chokepoint_score desc) as risk_rank,
    dense_rank() over (partition by hs2 order by sum(value_usd) over (partition by hs2) desc) as hs2_rank
  from joined
)
select
  entity_id,
  entity_name,
  country,
  chokepoint_score,
  risk_rank,
  shipment_id,
  ship_date,
  hs2,
  hs_code,
  value_usd,
  match_score,
  match_status,
  exporter_country,
  importer_country,
  importer_name
from ranked
where value_usd >= :min_value_usd
order by chokepoint_score desc, value_usd desc, shipment_id asc
limit :limit;
