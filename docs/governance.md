# Governance

omphalOS treats contracts and packs as interface surfaces.

## Change control

- Schema changes are reviewed like API changes.
- Pack changes are behavioral changes and must be documented.
- Breaking changes require a version bump and migration notes.

## Release process

A release-ready run should:

- PASS selected pack gates
- verify cleanly against its manifest
- pass publishability scan for the distribution scope
- be bundled with a release manifest for distribution
