# ADR: Incident taxonomy and failure modes

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    A resilient system expects failures and makes them diagnosable.
Incidents should be classified so remediation and prevention are systematic.
Failure information must be captured without leaking sensitive details and without breaking determinism.

    ## Decision

    Incidents are recorded using `contracts/schemas/incident_report.schema.json`.
The workbench uses a consistent taxonomy of failure modes:
- Contract violations (schema, boundary checks)
- Quality gate failures (semantic thresholds)
- Determinism violations (payload mismatch under certification)
- Publishability violations (secret patterns, disallowed disclosures)
- Runtime failures (exceptions, IO errors)
Runbooks in `docs/runbooks/incident.md` describe response procedures in purely technical terms.

    ## Alternatives considered

    - Free-form incident notes only — rejected (hard to automate, hard to trend).
- Treat every failure the same — rejected (different remediations).
- Store stack traces unredacted — rejected (may include secrets).

    ## Consequences

    - Failures become measurable and preventable.
- Operators can route remediation based on category.
- Incident artifacts can be shared without leaking uncontrolled data.

    ## Verification hooks

    - Unit tests ensure incident schema accepts expected fields and rejects malformed reports.
- Publishability gate scans incident outputs where produced.
- Integration tests assert clean, informative failures for adversarial inputs.

    ## Migration and evolution

    - Taxonomy additions are additive; consumers should ignore unknown categories.
- If incident reporting becomes mandatory for certain failures, encode that as a strict-pack rule.
- Redaction logic evolves centrally in `omphalos.core.redaction`.
