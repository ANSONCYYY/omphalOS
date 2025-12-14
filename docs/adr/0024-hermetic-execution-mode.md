# ADR: Hermetic execution mode

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Hermetic execution eliminates hidden dependencies (network, system time, locale) that break reproducibility.
Hermetic mode is especially valuable for certification and release workflows.
The workbench must support hermetic mode without requiring specialized runtime environments.

    ## Decision

    Hermetic mode enforces:
- No network access (by convention; connectors must be local or simulated).
- Deterministic clock derived from run configuration fingerprint.
- Deterministic randomness seeded from run id.
- Stable locale and sorting semantics for exports.
Hermetic mode is activated by config and recorded in the run manifest.

    ## Alternatives considered

    - Always-hermetic — rejected (some connectors are inherently remote in real deployments).
- Hermetic by best-effort — rejected (ambiguous guarantees).
- Hermetic by container only — rejected (hermetic should be semantic, not just packaging).

    ## Consequences

    - Certification becomes reliable and portable.
- Bugs due to hidden dependencies are easier to detect.
- Runs remain reproducible even when executed on different machines.

    ## Verification hooks

    - Integration tests run hermetic config and assert deterministic payload root across runs.
- Unit tests ensure deterministic clock outputs given a fixed fingerprint.
- Strict pack can require hermetic mode for certain workflows if desired.

    ## Migration and evolution

    - As new connectors are introduced, they must declare hermetic compatibility explicitly.
- If hermetic rules need to be expanded (e.g., filesystem restrictions), record as pack changes and document impact.
- Hermetic mode failures should produce clear incident reports (ADR 0018).
