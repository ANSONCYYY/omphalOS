# omphalOS

omphalOS was built for **U.S. federal interagency analytic workflows** where results must survive handoff, review, and later re-examination.
This public repository is a **sanitized** implementation: it ships with synthetic inputs, neutral interfaces, and no operational connectors.

omphalOS does one thing uncompromisingly: it turns a declared run into a **run record**—a directory of outputs plus a manifest that lets you verify what is inside and compare runs without argument.

---

## What you get after a run

A run writes to `artifacts/runs/<run_id>/`:

```text
artifacts/runs/<run_id>/
  run_manifest.json
  exports/
    briefing_tables/
    packets/
    narratives/
  lineage/
    lineage.jsonl
  warehouse/
    warehouse.sqlite
  reports/
    quality_report.json
    determinism_report.json
    publishability_report.json
    sbom_manifest.json
  logs/
    run.jsonl
```

The manifest lists artifacts and their fingerprints. It also records the run’s **pack** (baseline/strict), configuration fingerprint, and verification status.

---

## Terms used here (precise meanings)

- **Payload artifacts**: the outputs whose bytes define “what the run produced” (exports, lineage stream, warehouse file).
- **Control artifacts**: diagnostics and governance outputs (logs, SBOM, gate reports). They are still fingerprinted and verifiable.
- **Payload root hash**: a single hash computed over payload fingerprints. It is the run’s identity for equivalence.
- **Verify**: re-compute fingerprints and the payload root; confirm the run matches its manifest.
- **Certify**: compare two runs by payload root equality; report payload diffs on failure and control diffs as diagnostics.

These definitions are enforced in code and described in `docs/artifacts.md`.

---

## How to run

### 1) Bootstrap

```bash
make bootstrap
```

### 2) Run the reference pipeline

```bash
omphalos run config/runs/example_run.yaml
```

### 3) Verify a run directory

```bash
omphalos verify artifacts/runs/<run_id>
```

### 4) Certify equivalence across runs

```bash
omphalos certify artifacts/runs/<run_id_A> artifacts/runs/<run_id_B>
```

### 5) Build and verify a portable release bundle

```bash
omphalos release build artifacts/runs/<run_id> -o artifacts/releases/<run_id>.tar.gz
omphalos release verify artifacts/releases/<run_id>.tar.gz
```

---

## What this repository includes

- A complete **reference pipeline** with synthetic inputs and deterministic behavior.
- A **contracts directory** (`contracts/`) containing JSON Schemas and rule packs.
- A **quality gate** engine driven by YAML rules.
- A **publishability gate** to prevent accidental disclosures.
- Release bundling and integrity verification.

---

## What this repository does not include

- Operational connectors to external systems.
- Any institutional policy positions, agency-specific workflows, or privileged datasets.
- A claim that outputs are “correct” by default. The workbench proves *what ran* and *what it produced*; correctness is enforced by your contracts and gates.

---

## Packs

Runs select a pack (baseline/strict). Packs define which rule files apply and how hard the gates are.

- `baseline`: usable defaults for development and iteration
- `strict`: the “ship it” posture (stronger thresholds and additional required artifacts)

See `docs/packs.md`.

---

## Extending omphalOS

Real-world integrations belong outside the core in plugins. Plugins are versioned interfaces that can add connectors, exporters, and lineage sinks without changing the core.

See `docs/plugins.md`.

---

## Security and publishability

The publishability gate exists to support public distribution and safe sharing:

```bash
omphalos publishability scan .
```

See `docs/open_source_readiness.md` and `SECURITY.md`.

---

## License

Apache License 2.0. See `LICENSE` and `NOTICE`.
