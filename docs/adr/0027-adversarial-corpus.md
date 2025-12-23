# ADR: Adversarial corpus

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Robust systems are defined as much by how they fail as by how they succeed.
Adversarial inputs exercise boundary validation, redaction, and error reporting.
A corpus prevents regressions where failures become confusing, unsafe, or nondeterministic.

    ## Decision

    The repo includes synthetic adversarial fixtures under `tests/golden/fixtures/` and related integration tests.
Adversarial cases include:
- malformed identifiers and unexpected encodings
- high-entropy strings that resemble secrets
- boundary violations (negative quantities, invalid codes)
- ambiguous entity names that must go to review
Expected outcomes are: fail closed, produce informative reports, avoid leaking raw sensitive-like strings.

    ## Alternatives considered

    - Rely on random fuzzing — rejected (nondeterministic, hard to maintain expected results).
- No adversarial testing — rejected (unsafe failures remain undiscovered).
- Keep corpus outside the repo — rejected (weakens self-contained guarantees).

    ## Consequences

    - Failure modes become predictable and safe.
- Publishability and redaction logic are continuously exercised.
- Quality gates and contracts remain meaningful under stress.

    ## Verification hooks

    - Integration tests run adversarial configs and assert the correct failure category and schema-valid reports.
- Publishability scan tests ensure adversarial fixtures do not leak into release artifacts.
- Redaction unit tests ensure adversarial strings are handled deterministically.

    ## Migration and evolution

    - New adversarial cases are added when real failure classes are discovered.
- Each adversarial case includes an expected failure mode and a regression test.
- Corpus remains synthetic and bounded to preserve publishability.
