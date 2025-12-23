from __future__ import annotations

import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.models.param import Param
from airflow.operators.bash import BashOperator

REPO_ROOT = os.environ.get("OMPHALOS_REPO_ROOT", "/opt/omphalos")
RUNS_ROOT = os.environ.get("OMPHALOS_RUNS_ROOT", "/opt/omphalos/artifacts/runs")

default_args = {
    "owner": "omphalos",
    "depends_on_past": False,
    "retries": 0,
}

with DAG(
    dag_id="omphalos_backfill",
    description="Backfill runner for a selected config file",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    params={
        "config_path": Param("config/runs/example_run.yaml", type="string"),
        "output_root": Param(RUNS_ROOT, type="string"),
    },
    tags=["omphalos"],
) as dag:
    run = BashOperator(
        task_id="run",
        bash_command="cd " + REPO_ROOT + " && omphalos run --config {{ params.config_path }}",
        env={"OMPHALOS_RUNS_ROOT": "{{ params.output_root }}"},
    )

    verify = BashOperator(
        task_id="verify",
        bash_command="cd " + REPO_ROOT + " && RUN_DIR=$(omphalos run --config {{ params.config_path }}) && omphalos verify --run-dir ${RUN_DIR}",
        env={"OMPHALOS_RUNS_ROOT": "{{ params.output_root }}"},
    )

    run >> verify
