-- Review worklist playbook
--
-- Inputs
-- :limit

with rq as (
  select
    shipment_id,
    exporter_name,
    reason,
    candidates_json
  from review_queue
),
t as (
  select
    shipment_id,
    importer_name,
    exporter_country,
    importer_country,
    hs_code,
    substr(hs_code, 1, 2) as hs2,
    value_usd,
    ship_date
  from trade_feed
),
joined as (
  select
    rq.shipment_id,
    rq.exporter_name,
    rq.reason,
    rq.candidates_json,
    t.importer_name,
    t.exporter_country,
    t.importer_country,
    t.hs2,
    t.hs_code,
    t.value_usd,
    t.ship_date
  from rq
  join t on t.shipment_id = rq.shipment_id
)
select *
from joined
order by value_usd desc, ship_date desc, shipment_id asc
limit :limit;
