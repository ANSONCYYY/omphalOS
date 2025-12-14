# Packs

A pack is a named selection of rule files that define the run’s “bar to clear.”

Packs live under `contracts/packs/` and are referenced by name in run configs.

## Baseline pack

Baseline is designed for iteration:

- contract validation is enforced
- quality thresholds are set to catch obvious failures without blocking development
- publishability scanning covers the most common disclosure hazards

## Strict pack

Strict is the release posture:

- additional required artifacts (narratives, warehouse)
- tighter thresholds
- schema validation across packet globs
- expanded publishability scanning and stricter disallowed patterns

## How packs are applied

A pack declares:

- quality rule file paths
- publishability rule file paths
- pack id and version metadata

The pipeline loads the pack, evaluates rules deterministically, and writes `reports/quality_report.json`.

## Creating a new pack

1. Create `contracts/packs/<name>.yaml`.
2. List the rule files that apply.
3. Add or tune rule YAMLs under `contracts/quality_rules/`.
4. Run the reference pipeline and check `quality_report.json` is informative and stable.

Packs are part of the interface surface: treat changes as behavioral changes and record them in `CHANGELOG.md`.
