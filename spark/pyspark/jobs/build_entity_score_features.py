from __future__ import annotations

import os
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as ssum, count as scount

def main() -> None:
    runs_root = Path(os.environ.get("OMPHALOS_RUNS_ROOT", "artifacts/runs"))
    run_id = os.environ.get("OMPHALOS_RUN_ID")
    if not run_id:
        raise SystemExit("OMPHALOS_RUN_ID required")
    db_path = runs_root / run_id / "warehouse" / "warehouse.duckdb"
    out_dir = runs_root / run_id / "exports" / "spark_parquet" / "entity_features"
    out_dir.mkdir(parents=True, exist_ok=True)

    spark = SparkSession.builder.appName("omphalos_entity_features").getOrCreate()
    matches = spark.read.format("jdbc").option("url", f"jdbc:duckdb:{db_path}").option("dbtable", "entity_matches").load()
    trade = spark.read.format("jdbc").option("url", f"jdbc:duckdb:{db_path}").option("dbtable", "trade_feed").load()

    joined = matches.join(trade, on="shipment_id", how="left").where(col("status") == "MATCH")
    feats = joined.groupBy("entity_id").agg(
        scount("*").alias("matched_shipments"),
        ssum(col("value_usd")).alias("matched_value_usd"),
    )
    feats.write.mode("overwrite").parquet(str(out_dir))
    spark.stop()

if __name__ == "__main__":
    main()
