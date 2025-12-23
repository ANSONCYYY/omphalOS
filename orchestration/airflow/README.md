Airflow integration

This directory holds DAGs that execute the omphalOS workbench as scheduled jobs.

DAGs
- omphalos_nightly_example: runs the example configuration, verifies the run, and builds a release bundle
- omphalos_backfill: parameterized backfill runner for a chosen config and date interval
