from __future__ import annotations

import os
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, substring

def main() -> None:
    runs_root = Path(os.environ.get("OMPHALOS_RUNS_ROOT", "artifacts/runs"))
    run_id = os.environ.get("OMPHALOS_RUN_ID")
    if not run_id:
        raise SystemExit("OMPHALOS_RUN_ID required")
    db_path = runs_root / run_id / "warehouse" / "warehouse.duckdb"
    out_dir = runs_root / run_id / "exports" / "spark_parquet" / "trade_feed"
    out_dir.mkdir(parents=True, exist_ok=True)

    spark = SparkSession.builder.appName("omphalos_stage_trade").getOrCreate()
    df = spark.read.format("jdbc").option("url", f"jdbc:duckdb:{db_path}").option("dbtable", "trade_feed").load()
    df2 = df.withColumn("hs2", substring(col("hs_code"), 1, 2)).withColumn("hs4", substring(col("hs_code"), 1, 4))
    df2.write.mode("overwrite").parquet(str(out_dir))
    spark.stop()

if __name__ == "__main__":
    main()
