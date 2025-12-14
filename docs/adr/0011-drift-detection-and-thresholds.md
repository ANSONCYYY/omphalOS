# ADR: Drift detection and thresholds

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Even with deterministic code, upstream inputs evolve.
Drift detection flags changes that may affect interpretability or downstream expectations.
Drift must be defined as a comparison between two runs (or two dataset snapshots) with explicit thresholds.

    ## Decision

    Drift is computed as deterministic summary deltas between a baseline run and a candidate run.
Drift signals include:
- distribution shifts on key fields (counts, top-k categories)
- rate changes for matching and review outcomes
- export product cardinality shifts
Thresholds are captured in rule packs and drift reports are emitted as control artifacts (diagnostic).

    ## Alternatives considered

    - Rely on human intuition — rejected (not scalable).
- Use nondeterministic sampling — rejected (breaks repeatability).
- Treat drift as determinism failure — rejected (inputs can drift legitimately; drift is governance, not equivalence).

    ## Consequences

    - Drift is measured and reported consistently.
- Operators can gate releases on drift thresholds without conflating drift with determinism.
- Drift reports integrate naturally with review workflows.

    ## Verification hooks

    - Unit tests for drift metric calculations.
- Integration tests compute drift between two known runs and validate report schema.
- Sensor scaffolding in `orchestration/sensors.py` consumes drift outputs.

    ## Migration and evolution

    - New drift metrics are additive and must include threshold configuration.
- Threshold changes are treated as pack updates and recorded in changelog.
- If drift reports become payload-relevant for a downstream consumer, they can be promoted (with a versioned decision).
