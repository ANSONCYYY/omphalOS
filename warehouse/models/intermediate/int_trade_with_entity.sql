with t as (
  select * from {{ ref('int_trade_hs_slices') }}
),
m as (
  select * from {{ ref('stg_entity_matches') }}
),
r as (
  select * from {{ ref('stg_registry') }}
)
select
  t.shipment_id,
  t.exporter_name,
  t.importer_name,
  t.exporter_country,
  t.importer_country,
  t.country,
  t.hs_code,
  t.hs2,
  t.hs4,
  t.hs6,
  t.value_usd,
  t.ship_date,
  m.entity_id,
  m.score as match_score,
  m.status as match_status,
  r.entity_name as matched_entity_name,
  r.country as matched_entity_country
from t
left join m on m.shipment_id = t.shipment_id
left join r on r.entity_id = m.entity_id
