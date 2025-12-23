select
  reason,
  count(*) as items
from review_queue
group by 1
order by items desc, reason asc;
