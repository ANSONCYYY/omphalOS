select exporter_country, importer_country, count(*) as n, sum(value_usd) as total_value_usd
from v_trade_enriched
where hs2 = '86' and value_usd >= 1000
group by 1,2
order by total_value_usd desc
limit 100;
