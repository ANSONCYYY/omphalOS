select hs2, sum(value_usd) as total_value_usd
from v_trade_enriched
where exporter_country = 'GB' and importer_country = 'BR'
group by 1
order by total_value_usd desc
limit 50;
