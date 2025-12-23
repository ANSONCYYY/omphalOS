Warehouse

The reference pipeline writes a SQLite warehouse into each run directory at:

warehouse/warehouse.sqlite

Schema and views
- warehouse/db/schema.sql
- warehouse/db/derived_views.sql

dbt
- warehouse/dbt_project.yml
- warehouse/models (staging, intermediate, marts)
- warehouse/macros
