import os
from datetime import datetime, timezone
from pyspark.sql import SparkSession, Window
from pyspark.sql import functions as F
from pyspark.sql import types as T

def ingest_orders_to_bronze(spark: SparkSession, source_path: str, batch_id: str):
    """
    Reads raw orders from Landing, applies schema validation, deduplicates, 
    and routes records to bronze_valid or bronze_quarantine in HDFS.
    """
    
    # 1. Define the Expected Schema and Relationship Schema[cite: 5]
    relationship_schema = T.StructType([
        T.StructField("id", T.LongType(), False),
        T.StructField("name", T.StringType(), False),
    ])

    expected_schema = T.StructType([
        T.StructField("id", T.LongType(), False),
        T.StructField("name", T.StringType(), True),
        T.StructField("partner_id", relationship_schema, True),
        T.StructField("date_order", T.TimestampType(), True),
        T.StructField("state", T.StringType(), True),
        T.StructField("amount_untaxed", T.DecimalType(38, 18), True),
        T.StructField("amount_total", T.DecimalType(38, 18), True),
        T.StructField("currency_id", relationship_schema, True),
        T.StructField("create_date", T.TimestampType(), True),
        T.StructField("write_date", T.TimestampType(), True),
        T.StructField("company_id", relationship_schema, True),
        T.StructField("user_id", relationship_schema, True),
        T.StructField("team_id", relationship_schema, True),
        T.StructField("client_order_ref", T.StringType(), True),
        T.StructField("ops_order_at", T.TimestampType(), True),
        T.StructField("ops_confirmed_at", T.TimestampType(), True),
        T.StructField("ops_unmet_demand", T.BooleanType(), True),
        T.StructField("ops_closed", T.BooleanType(), True),
    ])

    # 2. Add the _corrupt_record column for Permissive Reading[cite: 5]
    # We read everything as Strings first to prevent Spark from dropping rows that fail type casting.
    read_schema = T.StructType(
        [T.StructField(field.name, T.StringType(), True) for field in expected_schema.fields] + 
        [T.StructField("_corrupt_record", T.StringType(), True)]
    )

    # 3. Read the Data from Landing (File System)[cite: 5]
    raw_df = spark.read \
        .schema(read_schema) \
        .option("mode", "PERMISSIVE") \
        .option("header", True) \
        .option("multiLine", True) \
        .option("escape", '"') \
        .option("columnNameOfCorruptRecord", "_corrupt_record") \
        .csv(source_path)

    # Attach tracking metadata[cite: 5]
    ingestion_timestamp = datetime.now(timezone.utc).replace(tzinfo=None)
    records = raw_df \
        .withColumn("_source_file", F.input_file_name()) \
        .withColumn("_batch_id", F.lit(batch_id)) \
        .withColumn("_ingestion_timestamp", F.lit(ingestion_timestamp))

    # 4. Apply `try_cast` and parse Odoo relationships (e.g., [501, "Name"])[cite: 5]
    for field in expected_schema:
        if isinstance(field.dataType, T.StructType):
            records = records.withColumn(
                "_pair", F.from_json(F.col(field.name), T.ArrayType(T.StringType()))
            )
            relationship = F.struct(
                F.expr("try_cast(element_at(_pair, 1) as bigint)").alias("id"),
                F.element_at("_pair", 2).alias("name"),
            )
            records = records.withColumn(
                field.name, F.when(F.size("_pair") == 2, relationship)
            ).drop("_pair")
        elif isinstance(field.dataType, T.StringType):
            records = records.withColumn(
                field.name,
                F.when(F.lower(F.col(field.name)) == "false", None).otherwise(F.col(field.name))
            )
        else:
            records = records.withColumn(
                field.name,
                F.expr(f"try_cast(`{field.name}` as {field.dataType.simpleString()})")
            )

    # 5. Split the Data: Valid vs. Quarantine
    # A record is bad if Spark's CSV parser failed OR if the mandatory business key 'id' is null.
    quarantine_df = records.filter(F.col("_corrupt_record").isNotNull() | F.col("id").isNull())
    
    valid_df = records.filter(F.col("_corrupt_record").isNull() & F.col("id").isNotNull())

    # 6. Deduplicate the Valid Data (Keeping the most recently updated row)
    # Partitions by the order ID, orders by write_date descending, and keeps row 1.
    window_spec = Window.partitionBy("id").orderBy(F.col("write_date").desc())
    deduplicated_valid_df = valid_df \
        .withColumn("_row_num", F.row_number().over(window_spec)) \
        .filter(F.col("_row_num") == 1) \
        .drop("_row_num")

    # 7. Write Outputs to HDFS (Appending to Bronze)
    valid_destination = "hdfs:///datalake/bronze_valid/orders"
    quarantine_destination = "hdfs:///datalake/bronze_quarantine/orders"

    deduplicated_valid_df.write.mode("append").format("parquet").save(valid_destination)
    quarantine_df.write.mode("append").format("parquet").save(quarantine_destination)

    print(f"Batch {batch_id} processed. Valid and Quarantine records saved to HDFS.")
    return deduplicated_valid_df, quarantine_df

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("Bronze_Ingestion_Pipeline") \
        .config("spark.sql.session.timeZone", "UTC") \
        .getOrCreate()
        
    # Example Airflow execution call
    ingest_orders_to_bronze(
        spark=spark, 
        source_path="file:///path/to/your/landing/orders/*.csv", 
        batch_id="batch_01"
    )
