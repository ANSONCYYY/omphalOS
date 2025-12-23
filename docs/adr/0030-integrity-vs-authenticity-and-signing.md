# ADR: Integrity vs authenticity, and signing posture

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    The workbench provides integrity primitives (fingerprints, root hashes, manifests). Integrity answers: “has this changed?”
Authenticity answers: “who vouches for this and under what verification?” Authenticity requires signing or attestation outside pure hashing.
Conflating integrity with authenticity is a common design error: hashes do not indicate trust or identity by themselves.

    ## Decision

    We explicitly separate:
- **Integrity**: provided by manifests (run/release) and verification commands.
- **Authenticity**: provided by external signing/attestation systems that consume the integrity outputs.
The workbench will:
- emit attestation hook documents that reference payload and/or release root hashes
- never require a specific signing backend
- never embed key material or signing secrets
If signing is integrated later, it will be implemented as a detachable artifact (e.g., signature file) over a stable hash.

    ## Alternatives considered

    - Implement signing in-core — rejected (forces key management assumptions and reduces portability).
- Treat hash equality as authenticity — rejected (hashes don’t identify a trusted signer).
- Do nothing about authenticity — rejected (hooks are low-cost and enable strong deployments).

    ## Consequences

    - The workbench remains neutral and portable while enabling high-assurance workflows.
- Releases can be verified for integrity anywhere; authenticity can be layered on where required.
- Security posture improves because the tool never needs to handle signing secrets.

    ## Verification hooks

    - Release build/verify tests ensure hashes referenced by attestations are stable and correct.
- Publishability gate rules explicitly forbid embedded private keys and common credential patterns.
- Docs describe how to sign externally (without naming a specific institutional actor).

    ## Migration and evolution

    - If new hash algorithms are introduced, keep SHA-256 as baseline for compatibility unless a deliberate breaking change is made.
- If authenticity requirements expand (e.g., transparency logs), implement adapters that consume existing integrity artifacts.
- Attestation schema evolves additively; breaking changes require a major version and migration notes.
