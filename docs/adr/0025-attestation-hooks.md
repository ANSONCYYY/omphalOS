# ADR: Attestation hooks

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Some environments require signed claims about runs or releases (who built it, what was verified).
Hard-wiring signing infrastructure reduces portability and increases coupling.
Hooks provide a stable interface where external tooling can inject attestations.

    ## Decision

    The workbench emits an attestation placeholder document conforming to `attestation.schema.json`.
Attestation documents reference:
- payload root hash
- release root hash (if built)
- pack id and contract versions
- verification results (quality, publishability, determinism)
External tooling may sign and attach attestations without modifying run artifacts.

    ## Alternatives considered

    - Implement signing directly — rejected (forces key management assumptions).
- Store attestations only in CI logs — rejected (not portable).
- Skip attestations entirely — rejected (hooks are low-cost and high-leverage).

    ## Consequences

    - Attestation becomes interoperable with different signing ecosystems.
- Downstream verification can incorporate signed claims without altering payload identity.
- The workbench stays neutral and portable while supporting stronger assurance models.

    ## Verification hooks

    - Schema validation of attestation documents.
- Release build/verify integration tests ensure attestation references remain stable.
- Docs describe attestation integration in purely technical terms.

    ## Migration and evolution

    - New attestation claims are additive fields.
- If a downstream ecosystem requires a specific format, it can be produced by an adapter tool that consumes the placeholder document.
- Attestation should never include host-specific secrets or identifiers.
