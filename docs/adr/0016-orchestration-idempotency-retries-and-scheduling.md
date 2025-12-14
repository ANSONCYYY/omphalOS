# ADR: Orchestration idempotency, retries, and scheduling

    - Status: **Accepted**
    - Date: **2025-12-14**
    - Scope: **omphalOS** (import path: `omphalos`)

    ## Context

    Pipelines are run repeatedly: scheduled runs, backfills, and retries after failures.
Orchestration must be safe under repeated invocation and partial failure.
Idempotency prevents duplicated outputs; retry logic prevents transient failures from becoming permanent outages.

    ## Decision

    Orchestration entrypoints (`orchestration/jobs.py`, `schedules.py`, `sensors.py`) treat a run as the unit of work.
Each run writes to a unique run directory keyed by the run id.
Retries:
- do not overwrite finalized artifacts
- write a new run with a new run id if inputs/config differ
- resume only by re-running the full pipeline when safe (hermetic mode makes this predictable)
Scheduling is separated from pipeline logic; pipeline remains a pure function of config + inputs.

    ## Alternatives considered

    - In-place retries that mutate runs — rejected (breaks immutability).
- Complex distributed scheduler requirement — rejected (keeps workbench self-contained).
- Hidden stateful checkpoints — rejected (hard to audit, hard to verify).

    ## Consequences

    - Runs remain verifiable and immutable even under retries.
- Schedulers can be swapped without changing pipeline semantics.
- Failure recovery is documented in runbooks and enforceable via artifacts.

    ## Verification hooks

    - Integration tests simulate reruns and verify distinct run ids when config changes.
- Runbooks in `docs/runbooks/` describe rerun/backfill patterns.
- Quality gates fail closed; orchestration surfaces failures rather than masking them.

    ## Migration and evolution

    - Introduce explicit checkpointing only with a contract that preserves auditability (record checkpoints as artifacts).
- If adding new scheduler backends, keep orchestration modules thin and configurable.
- Retry policies evolve as configuration schema extensions rather than hard-coded behavior.
