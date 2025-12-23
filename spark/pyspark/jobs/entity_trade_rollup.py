from __future__ import annotations

import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, sum as fsum, count as fcount

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--trade-csv", required=True)
    p.add_argument("--matches-csv", required=True)
    p.add_argument("--registry-csv", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()

    spark = SparkSession.builder.appName("omphalos_entity_trade_rollup").getOrCreate()

    t = spark.read.option("header", True).csv(args.trade_csv).withColumn("value_usd", col("value_usd").cast("double"))
    m = spark.read.option("header", True).csv(args.matches_csv).withColumn("score", col("score").cast("double"))
    r = spark.read.option("header", True).csv(args.registry_csv)

    joined = (
        m.join(t, m.shipment_id == t.shipment_id, "inner")
         .join(r, m.entity_id == r.entity_id, "inner")
         .select(
             col("entity_id"),
             col("entity_name"),
             col("country").alias("entity_country"),
             col("value_usd"),
             col("score").alias("match_score"),
         )
    )

    out = (
        joined.groupBy("entity_id", "entity_name", "entity_country")
              .agg(
                  fcount("*").alias("shipment_count"),
                  fsum("value_usd").alias("total_value_usd"),
                  avg("match_score").alias("mean_match_score"),
              )
              .orderBy(col("total_value_usd").desc(), col("shipment_count").desc(), col("entity_id").asc())
    )

    out.write.mode("overwrite").parquet(args.out)
    spark.stop()

if __name__ == "__main__":
    main()
