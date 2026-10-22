from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("KPI_DISCOUNT_DEPENDENCY") \
    .config("spark.sql.catalog.gold_catalog", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.gold_catalog.type", "hadoop") \
    .config("spark.sql.catalog.gold_catalog.warehouse", "hdfs://localhost:9000/user/sreeja/capstone/gold/warehouse") \
    .getOrCreate()

fact_sales = spark.table("gold_catalog.gold.fact_sales")

kpi_discount = fact_sales.groupBy("customer_id").agg(
    F.avg("discount_pct").alias("avg_discount_pct"),
    F.sum("discount_amount").alias("total_discount_amount"),
    F.sum("gross_sales").alias("total_gross_sales")
).withColumn(
    "discount_dependency_ratio", F.col("total_discount_amount") / F.when(F.col("total_gross_sales") == 0, 1).otherwise(F.col("total_gross_sales"))
)

spark.sql("DROP TABLE IF EXISTS gold_catalog.gold.kpi.kpi_discount_dependency")
kpi_discount.write.format("iceberg").mode("overwrite").save("gold_catalog.gold.kpi.kpi_discount_dependency")
print("KPI Discount Dependency completed.")
spark.stop()
