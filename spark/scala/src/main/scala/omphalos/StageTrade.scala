package omphalos

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.{col, substring}

object StageTrade {
  def main(args: Array[String]): Unit = {
    val runId = sys.env.getOrElse("OMPHALOS_RUN_ID", "")
    if (runId.isEmpty) throw new IllegalArgumentException("OMPHALOS_RUN_ID required")
    val runsRoot = sys.env.getOrElse("OMPHALOS_RUNS_ROOT", "artifacts/runs")
    val dbPath = s"${runsRoot}/${runId}/warehouse/warehouse.duckdb"
    val outDir = s"${runsRoot}/${runId}/exports/spark_parquet/trade_feed_scala"

    val spark = SparkSession.builder.appName("omphalos_stage_trade_scala").getOrCreate()
    val df = spark.read
      .format("jdbc")
      .option("url", s"jdbc:duckdb:${dbPath}")
      .option("dbtable", "trade_feed")
      .load()

    val df2 = df.withColumn("hs2", substring(col("hs_code"), 1, 2)).withColumn("hs4", substring(col("hs_code"), 1, 4))
    df2.write.mode("overwrite").parquet(outDir)
    spark.stop()
  }
}
