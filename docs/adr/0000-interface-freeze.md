# ADR: Interface freeze

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    A contracts-first workbench becomes useful to others only when its integration surface is predictable.
The integration surface here includes:
- CLI commands and exit-code semantics (`omphalos.cli`)
- Artifact directory layout under `artifacts/runs/<run_id>/…`
- JSON Schemas in `contracts/schemas/…` (manifests, reports, packets)
- Rule DSL structures in `contracts/quality_rules/…`
- Plugin interface types under `omphalos.plugins`
Without an explicit stability boundary, downstream users will couple to incidental behavior (file paths, field names, ordering) and upgrades become risky.

    ## Decision

    We freeze the public interface surface at the level of **schema contracts + CLI semantics + artifact layout**, not at internal module structure.
Any change that breaks backward compatibility must be treated as a **major-version change** and shipped with a migration guide and compatibility tests.
Internal modules are free to evolve provided the frozen surface remains stable.

    ## Alternatives considered

    - Freeze everything, including internal modules — rejected (prevents refactoring and performance work).
- Freeze only the CLI — rejected (schemas and artifact layout are the real integration points).
- Freeze only schemas — rejected (scripts and CI depend on CLI exit codes and subcommands).

    ## Consequences

    - Downstream integrations bind to explicit artifacts and contracts rather than implementation details.
- Refactors remain possible without breaking users as long as the contract surface is preserved.
- Version bumps must be disciplined: contract diffs are reviewed like API changes.

    ## Verification hooks

    - Contract validation: `omphalos contracts validate …` validates artifacts against `contracts/schemas`.
- CLI snapshot tests under `tests/unit/test_cli_surface.py` (command availability + exit codes).
- Golden fixture checks on manifest fields and artifact layout under `tests/golden/…`.

    ## Migration and evolution

    - Additive changes (new optional fields, new artifacts) are permitted in minor versions if schemas remain backward-compatible.
- Breaking changes require: (1) major version bump, (2) migration doc in `docs/`, (3) a compatibility test that demonstrates upgrade behavior.
- Deprecations are announced in `CHANGELOG.md` and enforced after a published deprecation window.
