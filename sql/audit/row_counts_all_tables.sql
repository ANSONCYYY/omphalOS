select 'trade_feed' as table_name, count(*) as rows from trade_feed
union all select 'registry', count(*) from registry
union all select 'entity_matches', count(*) from entity_matches
union all select 'review_queue', count(*) from review_queue
union all select 'entity_scores', count(*) from entity_scores
order by table_name asc;
