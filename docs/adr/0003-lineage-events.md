# ADR: Lineage events

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Deterministic outputs are more useful when they are explainable: what inputs contributed to what outputs and how.
Lineage should be append-only and easy to transport between systems.
Lineage must remain stable under hermetic execution and be safe to store as a run artifact.

    ## Decision

    Lineage is emitted as JSON Lines (`lineage/lineage.jsonl`) using `contracts/schemas/lineage_event.schema.json`.
Each event includes:
- A stable event id derived from content fingerprinting
- A type (`ingest`, `normalize`, `resolve`, `analyze`, `export`, `warehouse`)
- Input and output artifact pointers (relative paths) and their fingerprints
- A deterministic timestamp derived from the run clock
Lineage is treated as a **payload artifact** and contributes to payload root hash.
Implementation lives in `omphalos.core.lineage` and is invoked by pipeline steps.

    ## Alternatives considered

    - Store lineage only in logs — rejected (logs are control artifacts and may be redacted).
- Use a database for lineage — rejected (adds a running service and weakens portability).
- Emit a single huge lineage JSON — rejected (hard to stream, hard to merge, hard to validate incrementally).

    ## Consequences

    - Lineage is streamable, compressible, and trivially diffable across runs.
- Replay and audit tooling can consume lineage without needing the full runtime environment.
- Lineage becomes a stable substrate for completeness checks (see ADR 0028).

    ## Verification hooks

    - Schema validation of each event during emit in strict mode.
- Integration tests assert lineage presence and non-empty stream under strict pack.
- `omphalos verify` checks lineage fingerprint against manifest.

    ## Migration and evolution

    - Adding new event types is additive and requires schema extension.
- New fields must be optional or gated by major version if breaking.
- Replay consumers must tolerate unknown event types by ignoring them.
