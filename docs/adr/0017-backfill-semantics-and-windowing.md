# ADR: Backfill semantics and windowing

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Backfills reprocess historical windows to correct bugs or apply new logic.
Backfills must be defined precisely to avoid gaps, overlaps, and inconsistent partial updates.
Window semantics must be deterministic and recorded in manifests.

    ## Decision

    Backfills are expressed as a sequence of runs with explicit windows (start/end) and stable parameters.
Backfill driver (`scripts/backfill_driver.sh`) invokes `omphalos run` with windowed configs.
Each windowed run records window bounds in the run manifest and in lineage event metadata.

    ## Alternatives considered

    - Backfill by mutating existing runs — rejected (breaks immutability).
- Backfill with implicit windowing — rejected (un-auditable).
- Only store windowing in external scheduler config — rejected (window semantics must travel with artifacts).

    ## Consequences

    - Backfills are auditable and can be replayed/verified per window.
- Window boundaries become part of the run’s declared configuration (but not host-dependent).
- Downstream systems can reason about coverage and completeness.

    ## Verification hooks

    - Integration tests run two-window backfill and assert window metadata exists and is schema-valid.
- Lineage stream includes window bounds for step-level attribution.
- Quality gates can enforce expected record counts per window when configured.

    ## Migration and evolution

    - Window semantics additions are captured in `contracts/schemas/config.schema.json`.
- If changing window interpretation (inclusive/exclusive), treat as breaking and document migration.
- Allow multiple window strategies (time-based, id-range) as explicit schema choices, never implicit.
