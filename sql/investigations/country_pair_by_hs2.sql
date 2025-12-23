select
  exporter_country,
  importer_country,
  count(*) as shipment_count,
  sum(value_usd) as total_value_usd
from trade_feed
where substr(hs_code, 1, 2) = :hs2
  and ship_date between :start_date and :end_date
group by 1,2
order by total_value_usd desc;
