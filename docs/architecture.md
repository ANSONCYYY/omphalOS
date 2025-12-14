# Architecture

omphalOS is organized around a single invariant: a completed run directory can be verified against its manifest.

## Core components

- **Artifact store**: atomic writes, stable paths, and file indexing
- **Fingerprinting**: canonical hashing for files and structured data
- **Contracts**: JSON Schema validation for first-class artifacts
- **Packs**: rule selections that define gate posture (baseline/strict)
- **Quality engine**: deterministic evaluation of YAML-defined checks
- **Publishability gate**: deterministic scanning for disallowed patterns and artifacts
- **Release bundling**: portable archives with a release manifest and verification

## Dataflow

ingest → normalize → resolve → analyze → export → report → finalize

The reference pipeline demonstrates this flow with synthetic data and deterministic behavior.
