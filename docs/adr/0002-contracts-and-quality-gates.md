# ADR: Contracts and quality gates

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Consumers need to trust that exported products are structurally valid and meet baseline expectations.
Contracts (schemas/specs) prevent silent structural drift; quality gates prevent silent semantic drift.
The workbench must fail closed: invalid outputs must not be promoted as if they were valid.

    ## Decision

    All first-class artifacts are governed by JSON Schema contracts in `contracts/schemas`.
Quality is evaluated by a deterministic rule engine driven by YAML rule packs in `contracts/quality_rules`.
Runs select an explicit **pack** (`baseline`, `strict`) defined in `contracts/packs/*.yaml` which declares:
- Which quality rule files apply
- Which publishability rule files apply
- Pack metadata for reporting and traceability
The pipeline writes `reports/quality_report.json` and fails the run if the selected pack fails.

    ## Alternatives considered

    - Only schemas, no semantic gates — rejected (passes structurally valid but unusable outputs).
- Hard-coded checks in Python — rejected (hard to review, hard to diff, hard to extend without code changes).
- Non-deterministic checks (sampling) — rejected (cannot be certified for reproducibility).

    ## Consequences

    - Rule packs can be reviewed and versioned like policy, not like implementation.
- Users can tighten gates by switching packs, without forking code.
- Every failed gate produces a machine-readable report for triage and automation.

    ## Verification hooks

    - `omphalos quality evaluate` (via run pipeline) produces `quality_report.json` validated by `quality_report.schema.json`.
- Unit tests cover each rule-kind interpreter in `omphalos.core.quality`.
- Integration tests run baseline and strict packs and assert PASS for reference configs.

    ## Migration and evolution

    - New checks are added as new rule kinds in the engine plus schema updates to the report model.
- Deprecated checks are retained for a deprecation window and removed only with major version.
- Pack changes are treated as behavior changes and documented in `CHANGELOG.md`.
