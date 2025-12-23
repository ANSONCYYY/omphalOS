# Sample run

This folder is a minimal run directory produced by the reference pipeline.

It includes:
- `run_manifest.json` describing the run and all recorded artifacts
- `reports/` for determinism, quality, publishability, and SBOM manifests
- `exports/` containing briefing tables, evidence packets, and a narrative
- `warehouse/` containing a small local SQLite database for the run

You can validate and verify it:

```bash
python -m omphalos verify --run-dir examples/sample_run
```
