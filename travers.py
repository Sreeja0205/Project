from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("KPI_TRUE_NET_MARGIN") \
    .config("spark.sql.catalog.gold_catalog", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.gold_catalog.type", "hadoop") \
    .config("spark.sql.catalog.gold_catalog.warehouse", "hdfs://localhost:9000/user/sreeja/capstone/gold/warehouse") \
    .getOrCreate()

fact_sales = spark.table("gold_catalog.gold.fact_sales")

kpi_margin = fact_sales.groupBy("customer_id").agg(
    F.sum("gross_sales").alias("gross_revenue"),
    F.sum("discount_amount").alias("discount_cost"),
    F.sum("net_sales").alias("net_revenue")
).withColumn(
    "return_cost", F.lit(0.0)
).withColumn(
    "true_net_profit", F.col("net_revenue") - F.col("return_cost")
).withColumn(
    "true_net_margin_pct", F.round((F.col("true_net_profit") / F.when(F.col("gross_revenue") == 0, 1).otherwise(F.col("gross_revenue"))) * 100, 2)
)

spark.sql("CREATE NAMESPACE IF NOT EXISTS gold_catalog.gold.kpi")
spark.sql("DROP TABLE IF EXISTS gold_catalog.gold.kpi.kpi_true_net_margin")

kpi_margin.write.format("iceberg").mode("overwrite").save("gold_catalog.gold.kpi.kpi_true_net_margin")
print("KPI True Net Margin completed.")
spark.stop()
