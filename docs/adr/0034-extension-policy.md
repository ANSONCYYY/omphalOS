# ADR: Extension policy

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    A workbench is durable when it is extensible without forks.
Extensions should add connectors, steps, exporters, and lineage sinks without modifying core code.
A stable plugin boundary prevents dependency explosion and keeps the core auditable.

    ## Decision

    Extensions integrate via `omphalos.plugins` interfaces and a registry/loader mechanism.
Plugins are discovered via Python entry points and must declare:
- the interface version they implement
- capabilities (connector/exporter/etc.)
- hermetic compatibility requirements
The reference implementation lives under `omphalos.reference` and is not treated as a required dependency for external plugins.

    ## Alternatives considered

    - Allow arbitrary imports into core — rejected (coupling and audit risk).
- Fork-per-adopter — rejected (splits ecosystem).
- Dynamic code loading without versioning — rejected (unsafe, nondeterministic).

    ## Consequences

    - Core remains stable while the ecosystem evolves.
- Adopters can keep sensitive integrations out-of-tree while still using the same contracts and gates.
- Plugin versioning clarifies upgrade paths and avoids silent breakage.

    ## Verification hooks

    - Unit tests validate interface typing and registry behavior.
- Integration tests run reference pipeline through the same plugin boundary used by external plugins.
- Docs describe plugin authoring in technical terms without contextual narrative.

    ## Migration and evolution

    - Interface changes are breaking and require major version.
- New capabilities are additive and versioned.
- Deprecations are announced with migration notes and a defined support window.
