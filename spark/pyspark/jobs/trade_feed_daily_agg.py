from __future__ import annotations

import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, substring, sum as fsum, count as fcount

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--trade-csv", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()

    spark = SparkSession.builder.appName("omphalos_trade_feed_daily_agg").getOrCreate()

    df = spark.read.option("header", True).csv(args.trade_csv)
    df2 = (
        df.withColumn("value_usd", col("value_usd").cast("double"))
          .withColumn("hs2", substring(col("hs_code"), 1, 2))
    )

    out = (
        df2.groupBy("ship_date", "hs2", "country")
           .agg(fcount("*").alias("shipment_count"), fsum("value_usd").alias("total_value_usd"))
           .orderBy(col("ship_date").asc(), col("hs2").asc(), col("country").asc())
    )

    out.write.mode("overwrite").parquet(args.out)
    spark.stop()

if __name__ == "__main__":
    main()
