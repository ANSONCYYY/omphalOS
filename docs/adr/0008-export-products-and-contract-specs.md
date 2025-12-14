# ADR: Export products and contract specs

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Downstream consumers expect stable products: tables, packets, and narratives with consistent meaning.
Exports must be both machine-validated (schemas) and human-reviewable (formatting, ordering).
A contract spec describes the expected shape and required fields for each export type.

    ## Decision

    Exports are organized under `exports/` as:
- `exports/briefing_tables/…` (CSV) — stable columns, stable sort order
- `exports/packets/…` (JSON) — evidence packets validated against schema
- `exports/narratives/…` (Markdown) — human-readable summaries
Export specs live in `contracts/export_specs/*.yaml` and are referenced by quality checks.
Implementation: `omphalos.reference.products` + validation via `omphalos.core.contracts`.

    ## Alternatives considered

    - Only JSON exports — rejected (tables are easier for many consumers).
- Only CSV exports — rejected (packets need nested structure and explicit provenance).
- Let each pipeline define its own export layout — rejected (defeats stable interfaces).

    ## Consequences

    - Exports are easy to diff, validate, and consume.
- Export layout stability enables automation and reduces integration friction.
- Strict pack can tighten export requirements without changing code.

    ## Verification hooks

    - Schema validation of packets under strict pack (`schema_validate_glob`).
- Row-count and non-emptiness checks for tables under strict pack.
- Golden fixtures include representative packets and tables.

    ## Migration and evolution

    - New export types are additive and must include: spec entry, schema (if JSON), and quality rules.
- Deprecations require dual-writing for a migration window if consumers exist.
- Narratives remain informational and can evolve, but strict pack requires their presence.
