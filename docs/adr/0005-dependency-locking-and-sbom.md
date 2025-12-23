# ADR: Dependency locking and SBOM

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Reproducibility depends on both code and the dependency graph.
Two environments with different transitive dependencies can produce different behavior even with identical source.
A Software Bill of Materials (SBOM) provides traceability and enables supply-chain review.

    ## Decision

    The repo maintains lock artifacts (`uv.lock`, `pylock.toml`) and emits an SBOM manifest per run.
Each run writes `reports/sbom_manifest.json` listing resolved distributions and versions.
SBOM is treated as a **control artifact** (important for governance, not part of payload identity).
Implementation lives in `omphalos.core.sbom`.

    ## Alternatives considered

    - Rely only on `pyproject.toml` without locks — rejected (transitive drift).
- Hash the entire environment directory — rejected (host-dependent, noisy).
- Treat SBOM as payload — rejected (makes output identity depend on packaging differences).

    ## Consequences

    - Runs can be audited against a dependency inventory without destabilizing output equivalence.
- Supply-chain scanning can be performed on SBOM outputs, both in CI and post-run.
- Lockfiles document a supported, known-good environment.

    ## Verification hooks

    - SBOM schema validated by `contracts/schemas/sbom_manifest.schema.json`.
- CI builds SBOM report and checks schema validity.
- Publishability scan examines SBOM for disallowed disclosures (paths, hostnames).

    ## Migration and evolution

    - Lockfile format changes are treated as major changes if they affect reproducibility.
- SBOM fields are additive; breaking changes require schema version bump.
- New dependency-policy rules integrate with ADR 0021.
