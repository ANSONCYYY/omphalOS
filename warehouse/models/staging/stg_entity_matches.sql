select
  shipment_id,
  entity_id,
  cast(score as double) as score,
  status,
  explanation
from {{ source('omphalos', 'entity_matches') }}
