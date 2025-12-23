# ADR: Warehouse layer and marts

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Exports are convenient for downstream consumers, but analytical correctness benefits from a normalized warehouse layer.
A warehouse layer provides:
- Repeatable transformations (staging → intermediate → marts)
- A single source of truth for metrics used by reports and exports
- A testable contract boundary for derived tables
The reference implementation must remain self-contained while still demonstrating warehouse discipline.

    ## Decision

    The repository includes a minimal dbt project under `warehouse/` with models grouped by:
- `models/staging/` for lightly cleaned source tables
- `models/marts/` for consumer-facing views (scores, entity summaries)
The reference pipeline also writes a local file-backed warehouse artifact under `warehouse/warehouse.sqlite` to keep execution self-contained.
Warehouse outputs are treated as **payload** artifacts.

    ## Alternatives considered

    - No warehouse, only CSV/JSON exports — rejected (hard to validate derived relationships at scale).
- Require a hosted warehouse service — rejected (breaks self-contained execution).
- Use only dbt and no runtime warehouse file — rejected (reference pipeline needs a real artifact to hash/verify).

    ## Consequences

    - Users can adopt the dbt layer as-is or swap the storage backend while keeping contracts stable.
- The warehouse artifact enables deterministic verification and portable distribution of derived tables.
- Model organization provides a clear path for extension without breaking interfaces.

    ## Verification hooks

    - Strict pack requires warehouse artifact to exist and be non-empty.
- dbt project includes schema declarations in `warehouse/models/schema.yml` and is linted in CI.
- Integration tests check warehouse artifact fingerprinting and presence in manifest.

    ## Migration and evolution

    - New marts are additive and must be reflected in schema.yml.
- Breaking model renames require a migration note and (when possible) transitional views.
- Warehouse backends can change if the warehouse artifact contract remains satisfied.
