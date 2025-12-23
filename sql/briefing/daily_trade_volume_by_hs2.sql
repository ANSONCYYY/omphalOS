select
  ship_date,
  substr(hs_code, 1, 2) as hs2,
  count(*) as shipment_count,
  sum(value_usd) as total_value_usd
from trade_feed
where ship_date between :start_date and :end_date
group by 1,2
order by ship_date asc, hs2 asc;
