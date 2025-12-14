# ADR: Lineage transport and replay

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Lineage is most powerful when it can be moved and replayed: reconstructing derived artifacts or validating provenance claims.
Transport requires a stable event format; replay requires idempotent semantics.
Replay must not depend on hidden state outside the run directory.

    ## Decision

    Lineage is emitted as an append-only JSONL stream with stable event ids.
Replay tooling consumes lineage to:
- reconstruct step-level inputs/outputs
- validate completeness claims (ADR 0028)
- support backfill auditing (ADR 0017)
Replay is designed to be idempotent: re-emitting lineage from the same run yields identical bytes (modulo ordering guarantees already enforced).

    ## Alternatives considered

    - Store lineage in a proprietary format — rejected (transport friction).
- Replay by re-running the whole pipeline — rejected (not always possible or desired for audit).
- Rely on mutable external stores — rejected (breaks portability and auditability).

    ## Consequences

    - Lineage can be archived and audited independently.
- Replay enables lightweight verification and reconstruction of claims.
- The workbench becomes a substrate for external tooling without coupling.

    ## Verification hooks

    - Schema validation on lineage events under strict mode.
- Integration tests confirm deterministic ordering and stable fingerprints of lineage stream.
- `omphalos verify` checks lineage file fingerprint in manifest.

    ## Migration and evolution

    - New lineage event fields are additive; old consumers ignore unknown fields.
- Replay tooling is versioned and must maintain backward compatibility with prior event schemas for a defined window.
- If event ordering constraints change, they are treated as a breaking change (affects payload bytes).
