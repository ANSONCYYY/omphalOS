select
  entity_id,
  upper(trim(entity_name)) as entity_name,
  upper(trim(country)) as country
from {{ source('raw', 'registry') }}
