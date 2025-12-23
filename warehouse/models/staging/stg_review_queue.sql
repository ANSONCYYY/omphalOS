select
  shipment_id,
  upper(trim(exporter_name)) as exporter_name,
  reason,
  candidates_json
from {{ source('raw', 'review_queue') }}
