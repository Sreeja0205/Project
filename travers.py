from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("KPI_RETURN_COST_INDEX") \
    .config("spark.sql.catalog.gold_catalog", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.gold_catalog.type", "hadoop") \
    .config("spark.sql.catalog.gold_catalog.warehouse", "hdfs://localhost:9000/user/sreeja/capstone/gold/warehouse") \
    .getOrCreate()

# Load Silver orders (has cancellation state) and Gold fact_sales (has discounts)
orders = spark.table("silver_catalog.silver.orders")
fact_sales = spark.table("gold_catalog.gold.fact_sales")

# Extract customer_id from partner_id string in orders
orders_clean = orders.withColumn(
    "customer_id", F.regexp_extract(F.col("partner_id"), r"\[(\d+),", 1).cast("long")
).select("id", "customer_id", "state")

# Join to compute cancellation leakage + discount cost per customer
leakage_df = fact_sales.join(orders_clean, fact_sales["order_key"] == orders_clean["id"], "left") \
    .groupBy(fact_sales["customer_id"]).agg(
        F.sum(F.when(F.col("state") == "cancel", F.col("gross_sales")).otherwise(0.0)).alias("cancellation_loss"),
        F.sum("discount_amount").alias("total_discounts")
    ).withColumn(
        "return_cost_index", F.col("cancellation_loss") + (F.col("total_discounts") * 0.10)
    )

# Save to Iceberg Gold table
spark.sql("DROP TABLE IF EXISTS gold_catalog.gold.kpi.kpi_return_cost_index")

leakage_df.write \
    .format("iceberg") \
    .mode("overwrite") \
    .save("gold_catalog.gold.kpi.kpi_return_cost_index")

print("KPI Return Cost Index updated successfully.")
spark.stop()
