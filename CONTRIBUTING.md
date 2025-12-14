# Contributing

## What we accept

- bug fixes with tests
- contract or rule improvements with clear rationale
- documentation that clarifies the run record contract
- new pack rules when they are deterministic and reviewable

## Standards

- keep interfaces stable (schemas, artifact layout, CLI semantics)
- add tests for new behavior
- do not introduce real datasets or privileged connectors

## Development

```bash
make bootstrap
make test
```
