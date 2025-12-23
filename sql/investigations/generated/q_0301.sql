select exporter_country, sum(value_usd) as total_value_usd, count(*) as shipment_count
from v_trade_enriched
where exporter_country = 'US'
group by 1
order by total_value_usd desc
limit 100;
