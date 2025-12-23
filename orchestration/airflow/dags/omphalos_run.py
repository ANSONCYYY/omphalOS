from __future__ import annotations

import os
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

RUNS_ROOT = os.environ.get("OMPHALOS_RUNS_ROOT", "artifacts/runs")
CFG = os.environ.get("OMPHALOS_CONFIG", "config/runs/example_run.yaml")

with DAG(
    dag_id="omphalos_reference_run",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:
    run = BashOperator(
        task_id="run",
        bash_command=f"omphalos run --config {CFG}",
        env={"OMPHALOS_RUNS_ROOT": RUNS_ROOT},
    )
