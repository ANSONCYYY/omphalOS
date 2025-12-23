select
  shipment_id,
  entity_id,
  cast(score as {{ dbt.type_numeric() }}) as score,
  status,
  explanation
from {{ source('raw', 'entity_matches') }}
