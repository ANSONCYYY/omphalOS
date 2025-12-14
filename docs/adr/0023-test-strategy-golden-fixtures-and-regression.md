# ADR: Test strategy: golden fixtures and regression

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Reproducibility claims must be tested continuously; otherwise they decay.
Some properties are best tested by golden fixtures (byte-for-byte stable outputs).
Tests must cover both core primitives and end-to-end behavior.

    ## Decision

    The test suite is layered:
- Unit tests for deterministic primitives (hashing, schema validation, rule evaluation, redaction).
- Integration tests for end-to-end runs (baseline and strict packs).
- Golden fixtures for payload roots and representative exports.
Golden fixtures are used sparingly and only for artifacts intended to be stable.

    ## Alternatives considered

    - Only unit tests — rejected (misses integration nondeterminism).
- Only end-to-end tests — rejected (slow and hard to diagnose failures).
- Snapshot everything — rejected (brittle, high maintenance).

    ## Consequences

    - Regressions are caught early and explained well.
- Determinism certification remains meaningful because it is continuously exercised.
- Packs can evolve while tests enforce invariants and expected tightening.

    ## Verification hooks

    - `pytest` runs in CI; failures block merges.
- Golden roots under `tests/golden/` checked by integration tests.
- Schema validation tests ensure contracts remain consistent and enforceable.

    ## Migration and evolution

    - When golden fixtures change intentionally, updates must include a rationale in changelog and (for strict pack) an ADR note if behavior is materially altered.
- New pipeline steps must include both unit tests and at least one integration assertion.
- Test data remains synthetic and bounded to avoid disclosure risk.
