# ADR: Dataset contracts and boundary validation

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Input variability is the largest source of downstream failures.
A dataset contract sets expectations about required fields, types, and boundary conditions (allowed values, ranges).
Boundary validation should be deterministic and reportable.

    ## Decision

    Normalized datasets are validated against `contracts/schemas/dataset_contract.schema.json` and boundary rules in `contracts/quality_rules/dataset_boundary_rules.yaml`.
Boundary rules capture constraints such as:
- allowed categorical values (e.g., country codes, transaction types)
- numeric ranges (e.g., non-negative quantities)
- required field presence (e.g., identifiers)
Validation results are recorded in `quality_report.json` with explicit failures.

    ## Alternatives considered

    - Validate only at ingestion time — rejected (normalization can introduce new violations).
- Rely on database constraints only — rejected (reference pipeline must remain self-contained and portable).
- Allow invalid records silently — rejected (creates downstream ambiguity).

    ## Consequences

    - Errors are caught early and explained precisely.
- Boundary rules become reviewable artifacts and can evolve by pack.
- Downstream outputs are protected from invalid upstream data shapes.

    ## Verification hooks

    - Unit tests cover boundary rule evaluation determinism.
- Integration tests run adversarial configs and assert clean failure reports.
- Schema validation is enforced in strict pack runs.

    ## Migration and evolution

    - Adding new fields requires updating schemas and (when relevant) boundary rules.
- Boundary tightening is a behavior change and is recorded in changelog and pack versioning.
- If adopting a new code system (e.g., new categorical domain), boundary rules become a migration artifact.
