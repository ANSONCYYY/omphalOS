select importer_country, sum(value_usd) as total_value_usd, count(*) as shipment_count
from v_trade_enriched
where importer_country = 'CN'
group by 1
order by total_value_usd desc
limit 100;
