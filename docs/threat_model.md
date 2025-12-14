# Threat model

This document describes generic threats and the mitigations encoded in the repository.

## Integrity threats

- modification of artifacts after a run completes
- substitution of outputs without detection

Mitigations: per-file fingerprints, payload root hash, verify/certify, release manifests.

## Confidentiality threats

- secrets or private endpoints included in source, docs, or artifacts
- sensitive strings leaking into logs

Mitigations: publishability gate, structured logging, central redaction.

## Reproducibility threats

- nondeterminism (time, randomness, locale, ordering)
- dependency drift

Mitigations: hermetic mode patterns, deterministic clock, locks, SBOM reporting.

## Supply-chain threats

- malicious or risky dependencies
- unreviewed plugin code

Mitigations: lock discipline, dependency policy hooks, plugin boundary and review posture.
