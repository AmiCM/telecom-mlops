import dlt

from pyspark.sql.functions import *

@dlt.table(
        name="raw_data",
        comment="Raw data ingested from the surce GCS bucket",
        table_properties={"quality": "bronze"}
        )
def raw_data():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("cloudFiles.schemaLocation", "/tmp/schema/events")
        .option("cloudFiles.inferColumnTypes", "true")
        .load("gs://amicampos_telecom/customer_care")
    )

#@dlt.table(
#        name="cleaned_data",
#        comment="Cleaned data with only active records and valid IDs"
#        )
#@dlt.expect_or_drop("valid_id", "id IS NOT NULL")
#def cleaned_data():
#    return (
#        dlt.read("raw_data").filter(col("status") == "active")
#    )