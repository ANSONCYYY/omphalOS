# ADR: Reproducible runs and manifests

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Reproducibility requires a stable definition of “what the run produced” and a stable way to prove it.
Naively hashing a directory is error-prone because runs contain mutable control artifacts (logs) and self-referential files (the manifest).
We need a manifest that is:
- Self-describing (what ran, with what configuration)
- Integrity-carrying (fingerprints of artifacts)
- Non-recursive (does not hash itself)
- Portable (does not depend on absolute paths or host-specific details)

    ## Decision

    Each run writes a `run_manifest.json` that separates artifacts into two strata:
- **Payload artifacts**: content that defines the semantic output of the run (exports, warehouse products, lineage stream).
- **Control artifacts**: diagnostics and governance outputs (logs, SBOM, gate reports).
A run’s equivalence class is defined by the **payload root hash** computed over payload artifact fingerprints only.
The manifest records both payload and control fingerprints, but only payload fingerprints contribute to the payload root hash.
Implementation lives in `omphalos.core.artifacts`, `omphalos.core.fingerprint`, and `omphalos.core.pipeline`.

    ## Alternatives considered

    - Hash every file including logs — rejected (logs are intentionally verbose and timing-sensitive).
- Include the manifest in its own hash — rejected (self-reference).
- Define equivalence by environment snapshot — rejected (host and toolchain drift is expected; output identity is the goal).

    ## Consequences

    - Runs can be compared across machines and directories if the payload root matches.
- Control artifacts remain verifiable and attributable without contaminating output identity.
- Auditors can trace what happened (control), while consumers can pin what changed (payload).

    ## Verification hooks

    - `omphalos verify` recomputes payload root hash and checks artifact fingerprints against the manifest.
- `omphalos certify` compares two runs by payload root and reports control differences diagnostically.
- Schema validation: `contracts/schemas/run_manifest.schema.json` enforced by tests and CLI.

    ## Migration and evolution

    - New artifacts must be classified as payload vs control and added to indexing rules.
- If a previously control artifact becomes semantically relevant, promote it to payload with a versioned schema change and migration note.
- The artifact layout is stable; new subdirectories are additive and recorded in the manifest.
