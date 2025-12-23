# ADR: Evidence packets and review queues

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Many workflows require a compact object that can be handed off for review and decision-making.
Packets must include provenance, claims, and evidence; review queues must be trackable and replayable.
Packets are the primary human-facing product and must be stable.

    ## Decision

    Evidence packets are JSON documents validated by `evidence_packet_contract.schema.json` and written under `exports/packets/`.
Packets include:
- a canonical entity id
- a set of claims (derived metrics and key facts)
- evidence rows (sources, fields, fingerprints)
- resolution explanation (why this entity linkage was chosen)
- review metadata (queue state, required actions)
Review queue states are deterministic and derived from confidence thresholds and margin logic.

    ## Alternatives considered

    - Store evidence only in the warehouse — rejected (reviewers need portable, bounded payloads).
- Use free-form narratives only — rejected (automation requires structured packets).
- Put review state only in logs — rejected (logs are control artifacts and can be redacted).

    ## Consequences

    - Packets enable consistent review and downstream automation.
- Queue semantics can be tested and tuned without changing core primitives.
- Packets serve as a stable unit for export and archival.

    ## Verification hooks

    - Strict pack validates packet schema for every JSON under `exports/packets/`.
- Integration tests assert review fraction stays under thresholds.
- Golden packet fixtures document canonical structure and field expectations.

    ## Migration and evolution

    - Packet schema changes are versioned; additive changes preferred.
- Queue state enumeration is treated as an interface surface (ADR 0000).
- New packet types require new schema/spec entries and quality gates.
