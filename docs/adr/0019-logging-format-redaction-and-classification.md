# ADR: Logging format, redaction, and classification

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Logs are essential for debugging but are a common source of unintended disclosure.
Logs should be structured for machine processing and redacted deterministically.
Log formatting must not introduce nondeterminism that leaks into payload identity.

    ## Decision

    Logs are emitted as structured JSONL under `logs/run.jsonl`.
A redaction layer runs on all log fields before emission.
Logs are classified as **control artifacts** and never contribute to payload root hash.
Implementation: `omphalos.core.logging` and `omphalos.core.redaction`.

    ## Alternatives considered

    - Plaintext logs — rejected (hard to process, harder to redact safely).
- Redaction by regex in ad-hoc places — rejected (inconsistent and untestable).
- Treat logs as payload — rejected (brittle determinism).

    ## Consequences

    - Logs remain useful while reducing disclosure risk.
- Log consumers can filter/search using structured fields.
- Determinism remains about outputs, not diagnostics.

    ## Verification hooks

    - Unit tests for redaction transformations (stable input → stable output).
- Publishability scan includes log directories in strict mode when desired.
- Integration tests confirm log files exist but do not affect certification PASS/FAIL.

    ## Migration and evolution

    - Add new redaction patterns centrally and test them.
- If log schema evolves, do it additively and update runbooks.
- Never embed absolute paths or host identifiers in required log fields.
