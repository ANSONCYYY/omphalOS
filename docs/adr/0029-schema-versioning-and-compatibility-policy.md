# ADR: Schema versioning and compatibility policy

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Contracts are part of the public interface surface. Consumers integrate against JSON Schemas under `contracts/schemas/`.
Schema drift without policy creates two failure modes:
- silent breakage (producers change fields and consumers fail downstream)
- frozen evolution (schemas never improve because changes are risky)
We need explicit rules for additive vs breaking changes and a stable way to communicate contract versions in artifacts.

    ## Decision

    Every schema is treated as versioned by repository release version, and every produced artifact embeds:
- the schema id/name it claims to conform to
- the repository version (or contract bundle version) used to validate it
Compatibility rules:
- Additive changes (new optional fields; new enum values when consumers can ignore unknowns) are permitted in minor releases.
- Breaking changes (removed/renamed fields; tightened required sets; semantic redefinition) require a major release and a migration note.
- Schematized artifacts produced by the tool MUST validate against the schemas shipped in the same repository version.
Schema changes are reviewed as API changes and referenced in the changelog.

    ## Alternatives considered

    - No explicit versioning; rely on Git history — rejected (consumers need a machine-readable contract reference).
- Embed independent semantic versions per schema file — rejected (multi-version coordination becomes noisy; repo release is the coherent unit).
- Never change schemas — rejected (schemas must evolve as packs and products evolve).

    ## Consequences

    - Consumers can pin repository versions and know exactly which contracts apply.
- Maintainers can evolve schemas with discipline rather than fear.
- Pack rules can assume contracts are stable within a version and can be tightened deliberately with versioned changes.

    ## Verification hooks

    - `omphalos contracts validate` validates artifacts against the schema bundle in the repo.
- CI checks ensure all shipped example artifacts validate against shipped schemas.
- Tests cover backward-compatible parsing behavior for additive fields (unknown fields ignored where appropriate).

    ## Migration and evolution

    - If a schema must change in a breaking way, add a migration note in `docs/` and update pack rules to support a transition window when feasible.
- If artifact producers/consumers need multi-schema support, introduce explicit `schema_version` fields and a compatibility layer as a versioned feature.
- Schema ids remain stable; renaming a schema is treated as breaking unless a compatibility alias is provided.
