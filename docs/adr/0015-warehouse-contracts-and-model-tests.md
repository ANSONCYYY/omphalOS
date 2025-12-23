# ADR: Warehouse contracts and model tests

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Derived tables need clear expectations: column meaning, types, and primary keys.
A warehouse without contracts drifts silently and undermines downstream trust.
Model tests turn warehouse rules into enforceable checks.

    ## Decision

    Warehouse models declare contracts in `warehouse/models/schema.yml`.
The repo keeps the dbt project minimal but structured, and quality gates require the warehouse artifact to exist.
Model expectations are enforced via:
- schema declarations (types, keys, descriptions)
- SQL model structure conventions (staging vs marts)
- CI checks that the dbt project is syntactically valid

    ## Alternatives considered

    - No warehouse contracts — rejected (drift risk).
- Only runtime checks in Python — rejected (warehouse discipline should be expressed close to SQL).
- Put model tests outside the repo — rejected (weakens self-contained story).

    ## Consequences

    - Warehouse evolution becomes reviewable and predictable.
- Downstream metrics used in packets and narratives remain stable.
- Warehouse is a disciplined boundary, not a dumping ground.

    ## Verification hooks

    - Strict pack requires the warehouse artifact file to exist.
- CI lints dbt config and validates presence of schema.yml.
- Integration tests confirm warehouse artifacts appear in payload index.

    ## Migration and evolution

    - New models require schema entries and documentation.
- Renames require transitional views or versioned changes.
- If warehouse backend changes, schema-level contracts remain the portability anchor.
