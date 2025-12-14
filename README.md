# omphalOS

omphalOS exists to solve an old problem in analytic work: _The result is rarely sufficient on its own_.

In many environments — particularly within U.S.-governmental analytical work (for which this project was created in May 2024 \[and modernized in December 2025\]) — any output that might inform action must remain legible under scrutiny, traceable to its provenance, and distributable only with appropriate restraint.

This project was written to make that posture routine, to which end the repository includes a reference pipeline and example artifacts.

All example data is synthetic.

## What a run is

A run is a bounded execution that produces two things at once: (1) reader-facing deliverables and (2) a record adequate to explain, reproduce, and verify those deliverables later, when the original context and the original operator are no longer present.

A typical run directory contains:

- run_manifest.json, which inventories the run’s outputs and records integrity fingerprints
- exports/, which holds the materials intended for readers (tables, narrative, packet-style records)
- reports/, which contains structured checks (quality, determinism comparison, publishability scan, dependency inventory)
- lineage/, which records the run as an append-only sequence of events
- warehouse/, which contains a local SQLite artifact used by the reference pipeline

A completed run directory should be verifiable against its manifest, so that post-hoc editing—accidental or deliberate—can be detected without argument.

## Why this approach is necessary

In settings where analyses circulate beyond the originating workspace, the questions that matter are predictable and rarely polite:

- What inputs were admitted, and what boundaries were enforced?
- What rules were applied, and where are those rules written down?
- Which outputs are final, which are intermediate, and which require human review?
- What can be shared, with whom, and with what risk of inadvertent disclosure?
- If two runs disagree, is the disagreement substantive or procedural?

omphalOS is designed so these questions can be answered from the artifacts themselves, without appeals to memory or authority.

## Getting started

You may verify the included sample run without installing anything beyond Python:

python -m omphalos verify --run-dir examples/sample_run

To execute the synthetic reference pipeline, run:

python -m omphalos run --config config/runs/example_run.yaml

Runs typically materialize under artifacts/runs/. To verify a specific run directory:

python -m omphalos verify --run-dir artifacts/runs/<run_id>

If you wish to compare two runs for equivalence at the payload level:

python -m omphalos certify --run-a artifacts/runs/<runA> --run-b artifacts/runs/<runB>

## Release bundles and downstream verification

When a run must be transmitted as a single object, you may build a portable bundle:

python -m omphalos release build --run-dir artifacts/runs/<run_id> --out artifacts/releases/<run_id>.tar.gz

And verify that bundle after transport:

python -m omphalos release verify --bundle artifacts/releases/<run_id>.tar.gz

## Publishability scanning

Before distributing outputs outside the environment in which they were generated, it is prudent to scan for common disclosure hazards:

python -m omphalos publishability scan --path . --out artifacts/reports/publishability.json

This scan is a safeguard, not a guarantee. Treat it as a gate that reduces avoidable error, not as an absolution.

## Configuration, contracts, and explicitness

Run configurations live in config/runs/. Schemas and rule packs live in contracts/.

The project’s bias is explicitness. If an output matters, its shape should be declared. If a rule matters, it should be written down. If a check fails, the failure should be inspectable, not mystical.

## Scope and limits

omphalOS does not adjudicate policy, assign legal meaning, or substitute for domain judgment. It records what occurred, checks what can be checked, and packages work products so they remain intelligible under review. It is therefore most useful to practitioners who already understand what they are trying to decide, and who need their work to withstand retelling.

## Documentation

The most direct entry points are:

- docs/overview.md
- docs/architecture.md
- docs/artifacts.md
- docs/cli.md
- docs/open_source_readiness.md
- docs/threat_model.md

## License

Apache-2.0. See LICENSE and NOTICE. Citation metadata is provided in CITATION.cff.
