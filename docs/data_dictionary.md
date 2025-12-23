# Data dictionary (reference pipeline)

This repository’s **reference pipeline** uses fully synthetic data to demonstrate:
- contracts and schema validation,
- reproducible run manifests,
- deterministic entity resolution + explainability,
- export products (briefing tables + evidence packets),
- and a local SQLite “warehouse” written per-run.

All fields are generated deterministically from a run seed (_i.e._, nothing here is operational or source-derived).

---

## Inputs

### `trade_feed` (synthetic shipments)

One row per synthetic shipment.

| Field | Type | Meaning | Example |
|---|---|---|---|
| `shipment_id` | string | Stable shipment identifier (deterministic). | `S000123` |
| `exporter_name` | string | Noisy exporter name string (intentionally varied with punctuation/spacing/suffixes). | `ASTER-BOREAL LLC.` |
| `importer_name` | string | Synthetic importer organization label. | `NORTH HARBOR` |
| `country` | string | Two-letter country code associated with the shipment. | `DE` |
| `hs_code` | string | **4-digit** synthetic HS-like category code used for illustrative scoring. | `8542` |
| `value_usd` | number | Shipment value in USD (float). | `48215.50` |
| `ship_date` | string | ISO-8601 date (YYYY-MM-DD). | `2024-07-19` |

Notes:
- `exporter_name` is designed to sometimes create **ambiguity** that routes records to review.
- `hs_code` is intentionally short (HS-4 style) for demo simplicity.

### `registry` (synthetic entities)

One row per synthetic canonical entity.

| Field | Type | Meaning | Example |
|---|---|---|---|
| `entity_id` | string | Stable entity identifier (deterministic). | `E0007` |
| `entity_name` | string | Canonical entity name (may include corporate suffixes like `CO`, `INC`, `LLC` to induce controlled ambiguity). | `COBALT DORIAN CO` |
| `country` | string | Two-letter country code for the entity. | `US` |

Notes:
- A small subset of base names intentionally appears with multiple suffix variants (e.g., `LLC` vs `INC`) to exercise the review queue.

---

## Normalized views (canonicalization)

The reference pipeline canonicalizes text fields before resolution:

### `trade_feed_norm`
Same schema as `trade_feed`, but:
- `exporter_name` and `importer_name` are normalized to **uppercase** and **single-spaced** (whitespace collapsed).
- `country` is uppercased.
- `value_usd` is coerced to float.

### `registry_norm`
Same schema as `registry`, but:
- `entity_name` is normalized to **uppercase** and **single-spaced**.
- `country` is uppercased.

---

## Resolution outputs

### `entity_matches`
One row per shipment, linking it to the best-scoring entity candidate.

| Field | Type | Meaning |
|---|---|---|
| `shipment_id` | string | Shipment identifier from `trade_feed_norm`. |
| `entity_id` | string | Best candidate entity identifier from `registry_norm`. |
| `score` | number | Deterministic similarity score (Jaccard over canonical tokens). |
| `status` | string | `MATCH` if confident; otherwise `REVIEW`. |
| `explanation` | string | JSON-encoded explainability payload (see below). |

`explanation` JSON keys (encoded as a string in the table):
- `exporter_name` (string)
- `entity_name` (string)
- `score` (number)
- `common_tokens` (array[string])
- `exporter_tokens` (array[string])
- `entity_tokens` (array[string])

### `review_queue`
Only rows requiring review. Designed to be bounded and deterministic.

| Field | Type | Meaning |
|---|---|---|
| `shipment_id` | string | Shipment identifier. |
| `exporter_name` | string | Exporter string that triggered review. |
| `reason` | string | Reason code (e.g., `ambiguous_or_low_score`). |
| `candidates` | array[object] | Top candidate entities (bounded list). |

Each candidate object contains:
- `entity_id` (string)
- `entity_name` (string)
- `score` (number)

---

## Analytics outputs

### `entity_scores`
One row per entity with aggregated trade exposure and a demo “chokepoint” score.

| Field | Type | Meaning |
|---|---|---|
| `entity_id` | string | Entity identifier. |
| `entity_name` | string | Entity name from registry. |
| `country` | string | Entity country code. |
| `shipment_count` | integer | Count of shipments attributed to the entity. |
| `total_value_usd` | number | Total attributed shipment value (USD). |
| `chokepoint_score` | number | Demo score combining “chokepoint HS share” and magnitude (log-scaled). |

### `sensitivity` (summary stats)
A small set of distribution statistics over `chokepoint_score`:
- `count`
- `p50`
- `p90`
- `max`

---

## Warehouse (SQLite)

Each run writes `warehouse/warehouse.sqlite` containing (at minimum) these tables:
- `trade_feed` (normalized)
- `registry` (normalized)
- `entity_matches`
- `entity_scores`

Column names match the corresponding sections above.

---

## Export products

### Briefing table CSV
`exports/briefing_tables/briefing_table_entities.csv`

Columns:
- `entity_id`, `entity_name`, `country`, `shipment_count`, `total_value_usd`, `chokepoint_score`

### Evidence packets (JSON)
`exports/packets/packet_<ENTITY_ID>.json` (bounded set for demo determinism)

Top-level fields:
- `schema_version` (`"1.0"`)
- `run_id`
- `packet_id`
- `created_at` (deterministic timestamp, UTC `Z`)
- `claim`
- `entity` (object; includes entity summary fields)
- `evidence` (array; each item includes shipment evidence fields)
- `lineage` (array of stage labels)
- `review` (object: `status` + `reason`)
- `hashes` (object: `packet` sha256)

### Narrative
`exports/narratives/deltas.md`

Contains run metadata, sensitivity stats, and a short list of top entities.
