# Data dictionary (reference pipeline)

The reference pipeline uses synthetic fields to demonstrate contracts and gates.

## Trade feed (synthetic)

- `record_id`: stable synthetic identifier
- `exporter_name`: noisy string identifier
- `hs_code`: category code (synthetic)
- `quantity`: numeric quantity
- `value_usd`: numeric value
- `date`: ISO date

## Registry (synthetic)

- `entity_id`: stable synthetic canonical id
- `canonical_name`: canonical entity name
- `aliases`: list of alias strings
- `country`: two-letter code (synthetic set)
