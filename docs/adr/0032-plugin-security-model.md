# ADR: Plugin security model

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Plugins are executable code. They can read environment variables, access the network, and write files unless constrained.
The core needs a clear model for what plugins are allowed to do and what the host will trust.
A security model must balance extensibility with auditability and determinism.

    ## Decision

    Plugins are treated as **trusted code by default**, but the platform makes their behavior explicit and constrainable:
- Plugins must declare capabilities (connector/exporter/lineage sink) and hermetic compatibility.
- Plugins should write artifacts only through the artifact store API to preserve manifest correctness.
- Plugins must not mutate finalized run directories.
- Plugin provenance is part of the SBOM/dependency inventory and can be gated by allow/deny policy.
The host may run in a constrained mode (hermetic) where plugins that declare incompatibility are rejected.

    ## Alternatives considered

    - Sandbox plugins at runtime in-core — rejected (complex, platform-specific, and not always enforceable).
- Allow arbitrary plugin behavior with no declaration — rejected (un-auditable, nondeterministic).
- Ban plugins — rejected (forces forks and defeats extensibility).

    ## Consequences

    - Adopters can extend the system without changing core code while retaining auditability.
- Hermetic mode becomes enforceable as a policy boundary.
- Supply-chain review can include plugins explicitly rather than implicitly.

    ## Verification hooks

    - Unit tests validate plugin interface version checks and capability declarations.
- Integration tests run the reference pipeline through the same plugin loading path used for external plugins.
- Strict pack can require `hermetic_compatible=true` for runs intended for certification/release.

    ## Migration and evolution

    - If stronger sandboxing is required, implement it as an external runner that invokes the CLI in a constrained environment.
- Capability declarations can evolve additively; breaking interface changes require major version.
- Document recommended operational hardening (pin versions, review diffs) as part of docs, not code assumptions.
