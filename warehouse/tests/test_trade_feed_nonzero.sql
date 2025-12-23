select
  case when count(*) > 0 then 0 else 1 end as fail
from {{ ref('stg_trade_feed') }}
having fail = 1
