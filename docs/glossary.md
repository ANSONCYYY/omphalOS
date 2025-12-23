# Glossary

**Artifact**: A file produced by a run and recorded in the manifest.

**Run record**: The run directory plus its manifest; intended to stand alone.

**Manifest**: `run_manifest.json`, an index of artifacts and fingerprints plus run metadata.

**Payload artifacts**: Outputs that define the semantic result of a run (exports, lineage, warehouse).

**Control artifacts**: Diagnostics and governance outputs (logs, reports). Fingerprinted but excluded from payload identity.

**Payload root hash**: A single hash computed over payload artifact fingerprints; used for equivalence.

**Verify**: Recompute fingerprints and confirm a run directory matches its manifest.

**Certify**: Compare two runs by payload root equality and report differences.

**Pack**: A named selection of rule files (quality and publishability) that define the run’s gate posture.
