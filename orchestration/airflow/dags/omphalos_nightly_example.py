from __future__ import annotations

import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

REPO_ROOT = os.environ.get("OMPHALOS_REPO_ROOT", "/opt/omphalos")
RUNS_ROOT = os.environ.get("OMPHALOS_RUNS_ROOT", "/opt/omphalos/artifacts/runs")
RELEASES_ROOT = os.environ.get("OMPHALOS_RELEASES_ROOT", "/opt/omphalos/artifacts/releases")

default_args = {
    "owner": "omphalos",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=10),
}

with DAG(
    dag_id="omphalos_nightly_example",
    description="Nightly deterministic run, verification, and release bundle build",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule="0 3 * * *",
    catchup=False,
    max_active_runs=1,
    tags=["omphalos"],
) as dag:
    run = BashOperator(
        task_id="run",
        bash_command=f"cd {REPO_ROOT} && omphalos run --config config/runs/example_run.yaml",
        env={"OMPHALOS_RUNS_ROOT": RUNS_ROOT},
    )

    verify = BashOperator(
        task_id="verify",
        bash_command="RUN_DIR=$(cd " + REPO_ROOT + " && omphalos run --config config/runs/example_run.yaml) && omphalos verify --run-dir ${RUN_DIR}",
        env={"OMPHALOS_RUNS_ROOT": RUNS_ROOT},
    )

    release = BashOperator(
        task_id="release",
        bash_command="RUN_DIR=$(cd " + REPO_ROOT + " && omphalos run --config config/runs/example_run.yaml) && mkdir -p " + RELEASES_ROOT + " && omphalos release build --run-dir ${RUN_DIR} --out " + RELEASES_ROOT + "/${AIRFLOW_RUN_ID}.tar.gz",
        env={"OMPHALOS_RUNS_ROOT": RUNS_ROOT, "OMPHALOS_RELEASES_ROOT": RELEASES_ROOT},
    )

    run >> verify >> release
