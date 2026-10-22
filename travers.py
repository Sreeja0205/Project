from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("CUSTOMER_PROFITABILITY") \
    .config("spark.sql.catalog.gold_catalog", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.gold_catalog.type", "hadoop") \
    .config("spark.sql.catalog.gold_catalog.warehouse", "hdfs://localhost:9000/user/sreeja/capstone/gold/warehouse") \
    .getOrCreate()

margin = spark.table("gold_catalog.gold.kpi.kpi_true_net_margin")
discount = spark.table("gold_catalog.gold.kpi.kpi_discount_dependency").select("customer_id", "discount_dependency_ratio")
returns = spark.table("gold_catalog.gold.kpi.kpi_return_cost_index").select("customer_id", "return_cost_index")
customers = spark.table("gold_catalog.gold.dim_customer").select("customer_id", "customer_name")

customer_profitability = margin \
    .join(discount, "customer_id", "left") \
    .join(returns, "customer_id", "left") \
    .join(customers, "customer_id", "left") \
    .withColumn("return_cost_index", F.coalesce(F.col("return_cost_index"), F.lit(0.0))) \
    .withColumn(
        "segment",
        F.when((F.col("true_net_margin_pct") > 20) & (F.col("discount_dependency_ratio") < 0.10), "Core Profit Driver")
         .when(F.col("discount_dependency_ratio") >= 0.10, "Opportunistic Buyer")
         .otherwise("Margin Detractor")
    )

spark.sql("DROP TABLE IF EXISTS gold_catalog.gold.kpi.customer_profitability")
customer_profitability.write.format("iceberg").mode("overwrite").save("gold_catalog.gold.kpi.customer_profitability")
print("Customer Profitability table created successfully.")
spark.stop()
