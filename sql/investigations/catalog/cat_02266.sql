with s as (
  select * from v_entity_scores_ranked
),
bands as (
  select
    case
      when risk_rank <= 10 then 'top_10'
      when risk_rank <= 50 then 'top_50'
      when risk_rank <= 200 then 'top_200'
      else 'tail'
    end as band,
    count(*) as entities,
    sum(total_value_usd) as total_value_usd
  from s
  group by 1
)
select * from bands order by entities desc;
