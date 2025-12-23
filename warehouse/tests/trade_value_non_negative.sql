select *
from {{ ref('stg_trade_feed') }}
where value_usd < 0
