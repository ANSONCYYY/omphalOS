select 'step1_candidates' as step, m.entity_id, r.entity_name, count(*) as flags
from entity_matches m
join registry r on r.entity_id = m.entity_id
where m.status != 'MATCH'
group by 1,2,3
order by flags desc
limit 50;

select 'step2_trace_hs2' as step, t.*
from v_trade_enriched t
where t.hs2 = '16'
order by t.value_usd desc
limit 200;
