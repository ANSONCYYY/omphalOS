# ADR: Artifact immutability and retention

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Runs produce artifacts intended to be trusted. Trust requires immutability after completion.
If artifacts can be modified post-run, fingerprints lose meaning and manifests become misleading.
Retention provides a disciplined lifecycle for artifacts (what is kept, what is pruned, and how).

    ## Decision

    Artifacts are written using atomic writes and finalized at the end of the run.
After finalization, the run directory is treated as immutable by convention and by verification tooling.
A retention model is encoded via:
- Manifest fingerprints (detect drift if files change)
- Release bundles for long-term storage (`omphalos release build`)
Implementation: `omphalos.core.artifacts` and `omphalos.core.release`.

    ## Alternatives considered

    - Allow in-place edits and rely on timestamps — rejected (easy to tamper, hard to verify).
- Store artifacts only in a remote system — rejected (breaks self-contained runs and local verification).
- Treat all artifacts as immutable payload — rejected (control artifacts legitimately evolve during run).

    ## Consequences

    - Immutability can be enforced by tooling and policy without requiring special filesystems.
- Retention can be implemented by copying release bundles to storage and pruning local runs.
- Verification becomes meaningful: drift is detectable and attributable.

    ## Verification hooks

    - `omphalos verify` detects modified or missing files via fingerprint mismatch.
- `omphalos release verify` validates release manifests against extracted bundles.
- Integration tests ensure release build/verify round-trips correctly.

    ## Migration and evolution

    - Future work can add cryptographic signing of release manifests without changing payload hashing.
- Retention rules can be represented as config schema extensions and documented in `docs/governance.md`.
- If immutability enforcement changes (e.g., read-only flags), verification remains the ground truth.
