select
  substr(hs_code, 1, 6) as hs_slice,
  count(*) as shipment_count,
  sum(value_usd) as total_value_usd
from trade_feed
group by 1
order by shipment_count desc, hs_slice asc
limit :limit;
