with rq as (
  select * from {{ ref('stg_review_queue') }}
),
t as (
  select * from {{ ref('int_trade_hs_slices') }}
)
select
  rq.shipment_id,
  rq.exporter_name,
  rq.reason,
  rq.candidates_json,
  t.importer_name,
  t.exporter_country,
  t.importer_country,
  t.country,
  t.hs_code,
  t.hs2,
  t.hs4,
  t.value_usd,
  t.ship_date
from rq
left join t on t.shipment_id = rq.shipment_id
