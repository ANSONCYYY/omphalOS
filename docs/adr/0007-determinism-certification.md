# ADR: Determinism certification

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Determinism is not just “no randomness”; it is the ability to re-run the same declared computation and obtain the same payload outputs.
Certification must be precise about what is compared to avoid false failures.
Control artifacts (logs, SBOM, diagnostic reports) are valuable, but they should not redefine output identity.

    ## Decision

    Determinism certification compares two runs by **payload root hash** equality.
Certification report contains:
- PASS/FAIL based on payload root equality
- A detailed diff of payload file hashes when failing
- A diagnostic diff of control file hashes (always reported, never changes PASS/FAIL)
Implementation: `omphalos.core.determinism`.

    ## Alternatives considered

    - Require control file equality for PASS — rejected (logs and tooling metadata are allowed to vary).
- Compare only a subset of exports — rejected (creates blind spots).
- Rely on unit tests alone — rejected (does not detect cross-run nondeterminism).

    ## Consequences

    - A run’s semantic identity is stable and portable.
- Operators still get high-signal diagnostics when control artifacts differ.
- Certification can be automated and used as a release gate without being brittle.

    ## Verification hooks

    - `omphalos certify <runA> <runB>` emits a schema-validated determinism report.
- Integration test runs two outputs roots and asserts PASS for payload root.
- Golden fixtures pin expected payload roots for reference configs.

    ## Migration and evolution

    - If new payload artifacts are added, they must be included in payload indexing to keep certification complete.
- If a new class of artifact is controversial (payload vs control), the classification is decided via ADR update and versioned migration.
- Strict pack may add a separate “control-equality” check as a distinct rule kind (not as determinism status).
