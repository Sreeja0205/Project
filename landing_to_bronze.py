# src/bronze_engine.py
from datetime import datetime, timezone
from pyspark.sql import SparkSession, functions as F, types as T

# Import the instructor's profilers
from data_profilers.schema_drift import profile_schema_drift, profile_corrupt_records
from data_profilers.exploration import explore_data, write_exploration_to_iceberg

def process_bronze_batch(spark: SparkSession, dataset_name: str, source_path: str, expected_schema: T.StructType, batch_id: str, source_format: str = "csv"):
    
    # 1. Audit: Check for file-level Schema Drift using instructor's tool
    profile_schema_drift(
        spark=spark,
        input_path=source_path,
        expected_schema=expected_schema,
        source_format=source_format,
        dataset_name=dataset_name,
        run_id=batch_id
    )

    # 2. Append _corrupt_record for Permissive Reading
    # Read everything as String first to catch malformed rows without crashing
    read_schema = T.StructType(
        [T.StructField(field.name, T.StringType(), True) for field in expected_schema.fields] + 
        [T.StructField("_corrupt_record", T.StringType(), True)]
    )

    # 3. Read Data
    reader = spark.read.schema(read_schema).option("mode", "PERMISSIVE").option("columnNameOfCorruptRecord", "_corrupt_record")
    if source_format == "csv":
        raw_df = reader.option("header", True).option("escape", '"').option("multiLine", True).csv(source_path)
    else:
        raw_df = reader.json(source_path)

    # 4. Attach Traceability Metadata
    ingestion_timestamp = datetime.now(timezone.utc).replace(tzinfo=None)
    records = raw_df \
        .withColumn("_source_file", F.input_file_name()) \
        .withColumn("_batch_id", F.lit(batch_id)) \
        .withColumn("_ingestion_timestamp", F.lit(ingestion_timestamp))

    # 5. Apply try_cast to convert Strings to Expected Schema Types
    for field in expected_schema:
        if isinstance(field.dataType, T.StructType):
            # Parse Odoo array relationships like [501, "Meier Enterprises"] into Structs
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
            # Handle Odoo exporting missing data as the string "false"
            records = records.withColumn(
                field.name,
                F.when(F.lower(F.col(field.name)) == "false", F.lit(None).cast("string")).otherwise(F.col(field.name))
            )
        else:
            # Safely cast numeric/timestamp fields. Invalid data becomes Null.
            records = records.withColumn(
                field.name,
                F.expr(f"try_cast(`{field.name}` as {field.dataType.simpleString()})")
            )
            
    landing_df = records

    # 6. Audit: Log Corrupt Records and Exploratory Stats using instructor's tools
    profile_corrupt_records(landing_df, dataset_name=dataset_name, run_id=batch_id)
    
    measures = explore_data(spark, landing_df, dataset_name=dataset_name, run_id=batch_id, required_columns=["id"], processing_stage="LANDING")
    write_exploration_to_iceberg(spark, measures)

    # 7. Split Valid and Quarantine Data
    # Valid = No parser failure AND mandatory primary key 'id' is present
    valid_df = landing_df.filter(F.col("_corrupt_record").isNull() & F.col("id").isNotNull())
    quarantine_df = landing_df.filter(F.col("_corrupt_record").isNotNull() | F.col("id").isNull())

    # 8. Write to Iceberg (Bronze Valid) and HDFS (Quarantine)
    valid_table = f"datalake.bronze.{dataset_name}"
    
    spark.sql("CREATE NAMESPACE IF NOT EXISTS datalake.bronze")
    if not spark.catalog.tableExists(valid_table):
        valid_df.writeTo(valid_table).using("iceberg").create()
    else:
        valid_df.writeTo(valid_table).append()

    quarantine_path = f"hdfs:///datalake/quarantine/{dataset_name}"
    quarantine_df.write.mode("append").format("parquet").save(quarantine_path)

    print(f"Batch {batch_id} complete. Valid records written to {valid_table}. Bad records written to {quarantine_path}.")
    return valid_df, quarantine_df
