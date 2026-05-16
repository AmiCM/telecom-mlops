# ruff: noqa
# from pyspark import pipelines as dp
import dlt
from pyspark.sql.functions import *
from utils.utils import IMPUTATION_COLUMNS, WHITELIST_COLUMNS, telecom_select_exprs

checkpoint_base = spark.conf.get("checkpoint_volume_path")


@dlt.table(
    name="customer_care_churn_bronze",
    comment="Raw data ingested from the source GCS bucket",
    table_properties={"quality": "bronze"},
)
@dlt.expect("null_check_churn", "churn IS NOT NULL")
def raw_data():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("cloudFiles.schemaLocation", f"{checkpoint_base}/schema/raw_data")
        .option("cloudFiles.inferColumnTypes", "true")
        .option("header", "true")
        .option("escape", '"')
        .option("inferSchema", "true")
        .option("decimalSeparator", ",")
        .option("sep", ";")
        .load("gs://amicampos_telecom/customer_care")
    )


@dlt.table(
    name="customer_care_churn_silver",
    comment="Silver data from customer_care_churn_bronze table",
    table_properties={"quality": "silver"},
)
def nulls_data():
    df = dlt.read("customer_care_churn_bronze").select(telecom_select_exprs())
    columns_dropna = list(set(df.columns) - set(WHITELIST_COLUMNS))
    df_nulls = df.dropna(subset=columns_dropna)
    return df_nulls


@dlt.table(
    name="customer_care_churn_metrics",
    comment="Audit metrics for customer_care_churn_silver table",
)
def audit_metrics():
    stats_to_calc = ["percentile_approx(lor, 0.5) as median_lor", "percentile_approx(income, 0.5) as median_income"]
    return (
        dlt.read("customer_care_churn_silver")
        .selectExpr(*stats_to_calc)
        .withColumn("snapshot_timestamp", current_timestamp())
    )


@dlt.table(
    name="customer_care_churn_gold",
    comment="Golden data from customer_care_churn_silver table. Null values fully filled",
    table_properties={"quality": "gold"},
)
def cleaned_data():
    return (
        dlt.read("customer_care_churn_silver")
        .withColumn("missing_income", when(col("income").isNull(), "Y").otherwise("N"))
        .withColumn("missing_adults", when(col("adults").isNull(), "Y").otherwise("N"))
        .fillna(IMPUTATION_COLUMNS)
    )
