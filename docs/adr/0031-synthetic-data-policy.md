# ADR: Synthetic data policy for tests and examples

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Public repositories must not include real operational datasets or identifiers.
Tests and demos still need realistic structure to exercise contracts, quality gates, and failure modes.
A synthetic-data policy prevents “accidental realism” that could drift into disclosure risk over time.

    ## Decision

    All fixtures, examples, and demo connectors MUST use synthetic data.
Synthetic in this repository means:
- no real-person names, emails, addresses, phone numbers, or identifiers
- no real operational endpoints, tokens, keys, or credentials
- bounded vocabularies chosen for structure, not correspondence to real registries
- adversarial strings are generated to test scanners/redaction, not copied from real incidents
Any sample file added to the repo is subject to publishability scanning and must be reviewed like code.

    ## Alternatives considered

    - Allow curated 'anonymized' data — rejected (anonymization is brittle and often reversible).
- Allow real data in a private branch — rejected (branches leak; policy should be repo-wide).
- No fixtures at all — rejected (tests and examples would be weak and adoption would suffer).

    ## Consequences

    - The repo stays safe to publish and safe to fork.
- Tests remain meaningful because fixtures keep realistic shape and failure classes.
- Publishability gating remains credible because it is exercised on representative content.

    ## Verification hooks

    - CI runs publishability scan over the repo tree and fails on violations.
- Unit tests validate that demo generators produce deterministic outputs from fixed seeds/configs.
- A lint step can enforce fixture directory boundaries and size limits.

    ## Migration and evolution

    - If a fixture is found to be too close to real data, remove/replace it and rotate any derived artifacts.
- If new fixture categories are introduced, update the publishability rules and this ADR to define allowed forms.
- Keep fixture sizes bounded; large fixtures should be generated at test time, not committed.
