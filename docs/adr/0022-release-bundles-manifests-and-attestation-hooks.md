# ADR: Release bundles, manifests, and attestation hooks

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    A run directory is convenient locally but releases require a portable unit.
Bundles must be verifiable and reproducible.
Attestation hooks allow downstream systems to sign or certify releases without coupling the workbench to any specific signing infrastructure.

    ## Decision

    `omphalos release build` produces a tarball bundle and a `release_manifest.json` containing per-file hashes and a root hash.
`omphalos release verify` checks the manifest against extracted files.
Attestation hooks are emitted as a schema-defined placeholder document (`attestation.schema.json`) that external tools can populate.
Release manifests are control artifacts for governance; payload identity remains payload root hash inside `run_manifest.json`.

    ## Alternatives considered

    - Zip without manifest — rejected (no integrity semantics).
- Sign bundles inside the tool only — rejected (forces a signing choice).
- Treat release root hash as payload identity — rejected (bundling includes control artifacts).

    ## Consequences

    - Bundles can be stored and shared while preserving integrity semantics.
- External attestation integrates cleanly without modifying core hashing rules.
- Release verification becomes an automated gate in CI.

    ## Verification hooks

    - Integration tests build and verify a release bundle round-trip.
- Release manifest schema validated during build and verify.
- CI runs release build/verify workflow for tagged releases.

    ## Migration and evolution

    - Future signing support can be added by producing detached signatures over the release root hash.
- Manifest format changes are breaking; additive fields are preferred.
- Attestation schema can be extended additively to include new claims.
