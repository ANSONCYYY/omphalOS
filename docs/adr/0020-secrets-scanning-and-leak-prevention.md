# ADR: Secrets scanning and leak prevention

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Accidental inclusion of secrets is one of the highest-impact failures for a publishable workbench.
Leak prevention must be multi-layered: local hooks, CI gates, and post-run scans.
Scanning must be deterministic, explainable, and fail closed for releases.

    ## Decision

    The publishability gate scans for disallowed patterns defined in YAML rule files.
The default pack scans source and documentation; strict pack expands coverage and patterns.
Pre-commit hooks and CI workflows run the scan and block merges/releases on failures.
Implementation: `omphalos.core.publishability` and workflow `publishability.yaml`.

    ## Alternatives considered

    - Rely on developer diligence only — rejected.
- Use only external secret scanners — rejected (the workbench must be self-contained and configurable).
- Scan every byte including binaries — rejected (noise and performance, higher false positives).

    ## Consequences

    - Accidental disclosure becomes rare and detectable.
- Failures are actionable because scan reports include file paths and pattern ids.
- Release processes are defensible and repeatable.

    ## Verification hooks

    - Unit tests validate that known secret-like fixtures are detected and benign fixtures are not.
- CI blocks on publishability scan failures.
- Reports validate against `publishability_report.schema.json`.

    ## Migration and evolution

    - Patterns evolve over time; changes are pack updates documented in changelog.
- False positives are addressed by narrowing patterns or adding ignore lists in config schema.
- Scanning scope changes are treated as behavior changes and are tested.
