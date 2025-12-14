# Artifacts and verification

This document defines the run record: what is written, what it means, and what can be verified.

## Run directory contract

A run directory is rooted at:

`artifacts/runs/<run_id>/`

The directory contains:

- `run_manifest.json` — the index of artifacts, fingerprints, and run metadata
- `exports/` — user-facing products (tables, packets, narratives)
- `lineage/` — append-only lineage event stream
- `warehouse/` — file-backed warehouse artifact
- `reports/` — gate results and governance diagnostics
- `logs/` — structured execution logs

## Payload vs control

The workbench separates artifacts into two strata.

### Payload artifacts

Payload artifacts are the bytes that define what the run produced:

- `exports/**`
- `lineage/**`
- `warehouse/**`

Payload artifacts are fingerprinted and contribute to the **payload root hash**.

### Control artifacts

Control artifacts are diagnostics and governance outputs:

- `logs/**`
- `reports/**`

Control artifacts are fingerprinted and verifiable, but they do not change the run’s payload identity.

This separation avoids brittle equivalence when logs or environment inventories vary.

## Fingerprints

Each file fingerprint is computed as:

- SHA-256 of raw bytes
- recorded alongside file size in the manifest
- referenced by relative path (no absolute paths in the identity surface)

## Payload root hash

The payload root hash is computed deterministically from the set of payload fingerprints:

- paths are sorted lexicographically
- each entry is canonicalized as `{path, sha256, size}`
- the canonical list is hashed to produce a single root

The payload root hash defines run equivalence.

## Verify

`omphalos verify <run_dir>`:

- recomputes file fingerprints for all manifest-listed payload and control artifacts
- recomputes the payload root hash from payload artifacts
- reports missing/extra files and mismatches

Verification answers: “does this directory still match what the manifest says it is?”

## Certify

`omphalos certify <runA> <runB>`:

- PASS if payload root hashes are equal
- FAIL if payload roots differ, with a diff of which payload files differ
- always reports control differences as diagnostics

Certification answers: “did the outputs change?”

## Release bundles

A release bundle is a portable archive of a run directory.

`omphalos release build` produces:

- a tarball
- a `release_manifest.json` listing each file and its hash plus a bundle root hash

`omphalos release verify` confirms the archive matches its manifest.

## Retention guidance

Treat run directories as immutable after completion.

If long-term storage is needed:

- build a release bundle
- store the tarball and its release manifest together
