select hs2, sum(value_usd) as total_value_usd
from v_trade_enriched
where exporter_country = 'MX' and importer_country = 'AE'
group by 1
order by total_value_usd desc
limit 50;
