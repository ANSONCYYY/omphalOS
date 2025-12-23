# Examples

This directory contains small, self-contained materials that make it easier to understand the system without running it first.

- `sample_run/` is a compact example run directory that validates against the repository's schemas. You can point the CLI at it:

```bash
python -m omphalos verify --run-dir examples/sample_run
```

To generate fresh outputs, run the reference pipeline:

```bash
python -m omphalos run --config config/runs/example_run.yaml
```
