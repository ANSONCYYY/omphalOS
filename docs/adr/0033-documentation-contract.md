# ADR: Documentation contract

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    A workbench intended for handoff must be legible to new operators and reviewers.
Without a documentation contract, the README and docs drift, and the repo becomes “correct but unusable.”
Documentation should be treated as part of the interface surface.

    ## Decision

    The repository maintains a minimal required documentation set:
- `README.md`: purpose, boundaries, quickstart, and artifact map reference
- `docs/artifacts.md`: the run record contract and verification semantics
- `docs/cli.md`: command reference and examples
- `docs/packs.md`: baseline vs strict pack semantics and extension guidance
- `docs/open_source_readiness.md`: publishability and release checklist
Changes that affect interfaces (schemas, artifact layout, CLI commands, pack semantics) must update the relevant docs in the same change.

    ## Alternatives considered

    - Treat docs as optional — rejected (adoption and correctness both suffer).
- Single monolithic doc — rejected (hard to maintain and hard to navigate).
- Auto-generated docs only — rejected (not all decisions are derivable from code).

    ## Consequences

    - New adopters can understand the workbench quickly and accurately.
- Reviewers can locate the authoritative description of run identity and verification.
- Docs become enforceable through CI checks (presence + basic consistency tests).

    ## Verification hooks

    - CI checks ensure required doc files exist and basic anchors are present.
- A docs workflow can render markdown and fail on broken links where configured.
- Pack and schema changes are required to update docs in review checklists.

    ## Migration and evolution

    - Documentation requirements evolve additively. Removals require a migration plan or replacement doc.
- If doc structure changes, update this ADR and the README links.
- Keep docs neutral and technical; do not embed operational instructions requiring privileged context.
