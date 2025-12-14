# ADR: Dependency policy and allow/deny lists

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    A dependency graph is part of the security and reproducibility posture.
Some deployments require constraining dependencies based on license, provenance, or risk assessment.
The workbench needs a place for explicit dependency policy without embedding it in code.

    ## Decision

    Dependency policy is encoded as allow/deny lists (by distribution name) with rationales.
Policy is evaluated in CI against the resolved environment and recorded in SBOM reports when enabled.
Policy configuration is expressed in repo configuration and documented in `docs/governance.md`.

    ## Alternatives considered

    - No dependency policy — rejected (cannot meet stricter supply-chain requirements).
- Policy hard-coded in Python — rejected (difficult to review and extend).
- Rely on upstream package ecosystems alone — rejected (risk is contextual).

    ## Consequences

    - Dependencies become reviewable and constrainable.
- Policy changes become explicit diffs rather than hidden drift.
- SBOM outputs become actionable for compliance and scanning.

    ## Verification hooks

    - CI job checks resolved distributions against deny list.
- Unit tests validate policy parser and matching behavior.
- SBOM schema remains stable regardless of policy choices.

    ## Migration and evolution

    - Allow/deny rules are additive; removals documented and justified.
- If policy becomes pack-specific, packs can include policy references explicitly.
- Any automated enforcement failures must include a machine-readable report for triage.
