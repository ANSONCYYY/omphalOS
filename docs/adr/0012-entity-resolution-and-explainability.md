# ADR: Entity resolution and explainability

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Resolution links noisy identifiers (names, aliases) to canonical entities.
Resolution must be deterministic and explainable to support review and downstream use.
Explainability requires recording features, scores, and decision thresholds in a stable structure.

    ## Decision

    Resolution operates on canonicalized token features and produces decisions with explanations:
- candidate set construction is deterministic
- scoring uses stable token overlap and deterministic tie-breaking
- decisions produce `match`, `review`, or `no_match` outcomes with a justification payload
Explanations are embedded in evidence packets and are also written to the warehouse layer.
Implementation: `omphalos.reference.resolve.*`.

    ## Alternatives considered

    - Opaque learned model with no explanation — rejected (review friction and weak auditability).
- Interactive-only resolution — rejected (pipeline must run unattended).
- Store only final ids without rationale — rejected (cannot be reviewed or debugged).

    ## Consequences

    - Resolution outputs are defensible and testable.
- Review queues can target ambiguity rather than random sampling.
- Determinism certification meaningfully covers resolution outcomes.

    ## Verification hooks

    - Unit tests for canonicalization and match scoring determinism.
- Integration tests assert match-rate and review-fraction gates pass under baseline and strict packs.
- Evidence packets validated under strict pack include resolution explanations.

    ## Migration and evolution

    - New features (phonetics, embeddings) must remain deterministic under hermetic mode or be explicitly excluded.
- Threshold changes are treated as policy changes and recorded via pack updates.
- Explain payload structure is versioned via `evidence_packet_contract.schema.json` changes.
