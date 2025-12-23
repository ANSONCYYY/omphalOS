select
  entity_id,
  upper(trim(entity_name)) as entity_name,
  upper(trim(country)) as country,
  cast(shipment_count as integer) as shipment_count,
  cast(total_value_usd as {{ dbt.type_numeric() }}) as total_value_usd,
  cast(chokepoint_score as {{ dbt.type_numeric() }}) as chokepoint_score
from {{ source('raw', 'entity_scores') }}
