# Methodology

omphalOS is method-agnostic about analysis. It enforces discipline around how an analysis run is recorded.

The reference pipeline demonstrates a common pattern:

- ingest synthetic records
- normalize identifiers into canonical form
- resolve entities deterministically with explainability
- compute analytic summaries
- emit exports intended for review and handoff
- record lineage, reports, and manifests

Methodological changes are encoded as:

- contract changes (schemas/specs)
- rule pack changes (quality/publishability)
- versioned pipeline step changes with tests
