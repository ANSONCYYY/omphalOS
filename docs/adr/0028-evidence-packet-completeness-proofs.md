# ADR: Evidence packet completeness proofs

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Evidence packets are only useful if they are complete with respect to their declared scope.
Completeness means: claims are supported by evidence, evidence is traceable to lineage, and the packet includes required context.
We need a deterministic way to check completeness without relying on external systems.

    ## Decision

    Completeness is operationalized as a set of deterministic checks:
- Each claim field references a computed source (warehouse table or lineage event).
- Each evidence row carries a fingerprint and a lineage pointer.
- Packet contains required sections (claims, evidence, explanation, review metadata).
Strict pack enforces packet schema validation and can be extended to enforce claim-to-lineage linkage checks.

    ## Alternatives considered

    - Assume completeness by convention — rejected.
- Manual packet review only — rejected (does not scale).
- Store completeness logic only in narratives — rejected (must be machine-checkable).

    ## Consequences

    - Packets become defensible artifacts that can be validated automatically.
- Completeness checks reduce risk of “orphan claims” with no provenance.
- Downstream systems can trust packet structure and provenance mechanics.

    ## Verification hooks

    - Schema validation under strict pack is the baseline completeness check.
- Integration tests assert that sample packets contain required fields and valid lineage pointers.
- Future tests can enforce claim-to-warehouse references as an additional rule kind.

    ## Migration and evolution

    - Completeness checks can be tightened by pack without breaking packet schema.
- If claims evolve, their provenance requirements must be updated in lockstep.
- New packet types require explicit completeness definitions.
