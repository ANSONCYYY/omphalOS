# ADR: Quality rules language and evaluation

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Quality checks must be auditable, deterministic, and easy to review.
A small rule DSL is preferable to embedding business logic in Python for every check.
Rules must produce structured, machine-readable results.

    ## Decision

    Quality rules are expressed as YAML entries with a `kind` plus parameters.
The engine interprets rule kinds deterministically and emits a `quality_report.json` that records:
- rule id, description, severity
- PASS/FAIL result
- measured value and threshold when applicable
- evidence pointers (artifact paths, record counts)
Rule kinds are implemented centrally in `omphalos.core.quality`.

    ## Alternatives considered

    - General-purpose expression language — rejected (complexity and injection risk).
- SQL-only checks — rejected (not all checks are SQL-shaped, and we want portability).
- Hard-coded checks — rejected (review and extension friction).

    ## Consequences

    - Rules are easy to diff in code review.
- New checks are added with a clear contract: implement rule kind + tests + documentation.
- Strict pack can extend the DSL surface while baseline remains stable.

    ## Verification hooks

    - Unit tests cover each rule kind and ensure deterministic evaluation.
- Integration tests run packs and check failure modes are informative and schema-valid.
- Pack loader tests ensure rule file resolution is stable and predictable.

    ## Migration and evolution

    - New rule kinds are additive; changing semantics of an existing kind is treated as breaking unless strictly bug-fix.
- Rule deprecations are announced and kept for a compatibility window.
- Rule ids are stable; renaming ids is treated as a migration event for automation consumers.
