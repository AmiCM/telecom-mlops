# Databricks notebook source
df = spark.read.table("deops_prd.telecom.customer_care_churn_gold")
display(df)

# COMMAND ----------
