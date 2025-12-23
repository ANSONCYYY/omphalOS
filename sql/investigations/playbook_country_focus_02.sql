-- Country focus playbook 02
--
-- Inputs
-- :country, :start_date, :end_date, :limit

with t as (
  select
    shipment_id,
    exporter_name,
    importer_name,
    exporter_country,
    importer_country,
    hs_code,
    substr(hs_code, 1, 2) as hs2,
    value_usd,
    ship_date
  from trade_feed
  where coalesce(exporter_country, country) = :country
    and ship_date between :start_date and :end_date
),
hs as (
  select
    hs2,
    count(*) as shipment_count,
    sum(value_usd) as total_value_usd
  from t
  group by 1
),
pairs as (
  select
    importer_country,
    count(*) as shipment_count,
    sum(value_usd) as total_value_usd
  from t
  group by 1
),
ship as (
  select *
  from t
  order by value_usd desc, shipment_id asc
  limit :limit
)
select
  'hs' as section,
  hs2 as k1,
  null as k2,
  shipment_count,
  total_value_usd
from hs
union all
select
  'pairs',
  importer_country,
  null,
  shipment_count,
  total_value_usd
from pairs
union all
select
  'shipments',
  shipment_id,
  hs2,
  1,
  value_usd
from ship
order by section asc, total_value_usd desc;
