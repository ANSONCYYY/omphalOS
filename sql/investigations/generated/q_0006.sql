select ship_date, sum(value_usd) as total_value_usd
from v_trade_enriched
where hs2 = '48'
group by 1
order by ship_date asc;
