import argparse

import lightgbm as lgb

# ml libraries
import mlflow
import xgboost as xgb
from mlflow.models import infer_signature

# spark session
from pyspark.sql import SparkSession

# sklearn libraries
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, log_loss, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

spark = SparkSession.builder.getOrCreate()
# variables
parser = argparse.ArgumentParser()
parser.add_argument("--bundle_target", type=str, help="Variable passed from YAML")
args = parser.parse_args()
bundle_target = args.bundle_target
# load data
df = spark.table("deops_prd.telecom.customer_care_churn_gold")
df_pd = df.toPandas()
# split data
features_cat = [column for column, tipo in df.dtypes if tipo in ("string", "boolean")]
features_num = list(set(df.columns) - set(features_cat) - {"churn", "Customer_ID"})
x = df_pd[features_num + features_cat]
y = df_pd["churn"]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=67)
# model pipeline
cat_transformer = Pipeline(steps=[("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))])
preprocessor = ColumnTransformer(transformers=[("cat", cat_transformer, features_cat)])

# nombre del experimento
experiment = mlflow.set_experiment(f"/Shared/telecom-customer_care_churn-{bundle_target}")
# modelo xgboost
XGB_MODEL_NAME = f"mlops_{bundle_target}.telecom.cc_churn_xgb_model"
with mlflow.start_run(run_name="xgboost") as run:
    # Definir el pipeline con el clasificador
    xgb_pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                xgb.XGBClassifier(
                    # setting inicial
                    n_estimators=600,
                    learning_rate=0.1,
                    max_depth=4,
                    # para overfitting
                    subsample=0.8,
                    colsample_bytree=0.7,
                    # regularizaciones
                    reg_alpha=0.1,
                    reg_lambda=1.0,
                    # others
                    random_state=67,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    # Entrenar
    xgb_pipeline.fit(x_train, y_train)

    # Evaluar
    preds = xgb_pipeline.predict(x_test)
    probs = xgb_pipeline.predict_proba(x_test)[:, 1]
    acc = accuracy_score(y_test, preds)
    loss = log_loss(y_test, probs)
    recall = recall_score(y_test, preds)

    # MLflow Logs
    mlflow.log_param("model_type", "xgboost")
    mlflow.log_param("n_estimators", 600)
    mlflow.log_metric("accuracy", acc)
    mlflow.log_metric("log_loss", loss)
    mlflow.log_metric("recall", recall)
    # Guarda un artefacto
    sample_dict = {"dataset_size": len(df_pd), "features_used": list(x.columns)}
    mlflow.log_dict(sample_dict, "metadata.json")

    # Registrar el modelo en el Unity Catalog / Model Registry
    signature = infer_signature(x_train, preds)
    mlflow.sklearn.log_model(
        sk_model=xgb_pipeline,
        artifact_path="xgb-pipeline-model",
        registered_model_name=XGB_MODEL_NAME,
        signature=signature,
    )

# modelo lightgbm
LGB_MODEL_NAME = f"mlops_{bundle_target}.telecom.cc_churn_lgb_model"
with mlflow.start_run(run_name="lightgbm") as run:
    # Definir el pipeline con el clasificador
    lgb_pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                lgb.LGBMClassifier(
                    n_estimators=400,
                    learning_rate=0.03,
                    num_leaves=31,
                    max_depth=6,
                    min_child_samples=50,
                    # overfitting
                    subsample=0.8,
                    subsample_freq=1,
                    colsample_bytree=0.6,  # Feature fraction: Usa solo el 60% de tus 100 columnas por árbol
                    # regularización
                    reg_alpha=0.5,
                    reg_lambda=1.5,
                    # others
                    random_state=67,
                    n_jobs=-1,
                    verbose=1,
                ),
            ),
        ]
    )

    # Entrenar
    lgb_pipeline.fit(x_train, y_train)

    # Evaluar
    preds = lgb_pipeline.predict(x_test)
    probs = lgb_pipeline.predict_proba(x_test)[:, 1]
    acc = accuracy_score(y_test, preds)
    loss = log_loss(y_test, probs)
    recall = recall_score(y_test, preds)

    # MLflow Logs
    mlflow.log_param("model_type", "lightgbm")
    mlflow.log_param("n_estimators", 400)
    mlflow.log_metric("accuracy", acc)
    mlflow.log_metric("log_loss", loss)
    mlflow.log_metric("recall", recall)
    # Guarda un artefacto
    sample_dict = {"dataset_size": len(df_pd), "features_used": list(x.columns)}
    mlflow.log_dict(sample_dict, "metadata.json")

    # Registrar el modelo en el Unity Catalog / Model Registry
    signature = infer_signature(x_train, preds)
    mlflow.sklearn.log_model(
        sk_model=lgb_pipeline,
        artifact_path="lgb-pipeline-model",
        registered_model_name=LGB_MODEL_NAME,
        signature=signature,
    )
