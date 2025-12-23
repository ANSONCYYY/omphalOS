package omphalos.spark

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.{col, substring, sum => fsum, count => fcount}

object TradeDailyAgg {
  def main(args: Array[String]): Unit = {
    val parsed = Args.parse(args)
    val spark = SparkSession.builder.appName("omphalos_trade_daily_agg").getOrCreate()

    val df = spark.read.option("header", "true").csv(parsed.tradeCsv)
      .withColumn("value_usd", col("value_usd").cast("double"))
      .withColumn("hs2", substring(col("hs_code"), 1, 2))

    val out = df.groupBy(col("ship_date"), col("hs2"), col("country"))
      .agg(
        fcount("*").as("shipment_count"),
        fsum(col("value_usd")).as("total_value_usd")
      )
      .orderBy(col("ship_date").asc, col("hs2").asc, col("country").asc)

    out.write.mode("overwrite").parquet(parsed.out)
    spark.stop()
  }
}
