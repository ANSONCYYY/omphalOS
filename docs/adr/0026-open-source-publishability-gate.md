# ADR: Open-source publishability gate

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    A public repository must avoid leaking secrets, private endpoints, or undisclosed data.
Publishability is more than secrets: it includes stray artifacts, caches, and environment files.
A gate formalizes what is allowed and blocks releases that violate it.

    ## Decision

    Publishability gate scans the repository tree for disallowed patterns and disallowed file classes.
The gate produces a schema-validated report and fails closed for release workflows.
The scan respects ignore rules and uses size/binary heuristics to reduce false positives while maintaining coverage.

    ## Alternatives considered

    - Manual review only — rejected (not scalable and not repeatable).
- Use only external scanning tools — rejected (policy needs to be codified in-repo).
- Treat publishability gate as informational only — rejected (should block releases).

    ## Consequences

    - Public releases become repeatable and defensible.
- Violations are actionable with path + pattern ids.
- The gate can be tightened via strict packs without code changes.

    ## Verification hooks

    - CI runs `omphalos publishability scan` and fails on violations.
- Unit tests assert detection of known secret-like fixtures.
- Pack-aware scanning is tested to ensure strict policies apply when selected.

    ## Migration and evolution

    - Scanning policy evolves via rule files and ignore settings in config schema.
- Pattern updates are documented with rationale to manage false positives.
- If new artifact types are introduced, include them in the scan scope deliberately.
