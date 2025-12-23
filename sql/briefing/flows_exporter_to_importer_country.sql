select
  exporter_country,
  importer_country,
  substr(hs_code, 1, 2) as hs2,
  count(*) as shipment_count,
  sum(value_usd) as total_value_usd
from trade_feed
where ship_date between :start_date and :end_date
group by 1,2,3
order by total_value_usd desc, shipment_count desc;
