from pyspark.sql.functions import *
# CONSTANTS
## Columns that should be changed as double type
DOUBLE_COLS = [
    "rev_Mean", "mou_Mean", "totmrc_Mean", "da_Mean", "ovrmou_Mean",
    "ovrrev_Mean", "vceovr_Mean", "datovr_Mean", "roam_Mean", "change_mou",
    "change_rev", "drop_vce_Mean", "drop_dat_Mean", "blck_vce_Mean",
    "blck_dat_Mean", "unan_vce_Mean", "unan_dat_Mean", "plcd_vce_Mean",
    "plcd_dat_Mean", "recv_vce_Mean", "recv_sms_Mean", "comp_vce_Mean",
    "comp_dat_Mean", "custcare_Mean", "ccrndmou_Mean", "cc_mou_Mean",
    "inonemin_Mean", "threeway_Mean", "mou_cvce_Mean", "mou_cdat_Mean",
    "mou_rvce_Mean", "owylis_vce_Mean", "mouowylisv_Mean", "iwylis_vce_Mean",
    "mouiwylisv_Mean", "peak_vce_Mean", "peak_dat_Mean", "mou_peav_Mean",
    "mou_pead_Mean", "opk_vce_Mean", "opk_dat_Mean", "mou_opkv_Mean",
    "mou_opkd_Mean", "drop_blk_Mean", "attempt_Mean", "complete_Mean",
    "callfwdv_Mean", "callwait_Mean", "totrev", "adjrev", "adjmou",
    "totmou", "avgrev", "avgmou", "avgqty", "hnd_price"
]
## Columns that pass through unchanged
PASSTHROUGH_COLS = [
    "churn", "months", "uniqsubs", "actvsubs", "new_cell", "crclscod",
    "asl_flag", "totcalls", "adjqty", "avg3mou", "avg3qty",
    "avg3rev", "avg6mou", "avg6qty", "avg6rev", "prizm_social_one", "area",
    "dualband", "refurb_new", "phones", "models", "hnd_webcap", "truck",
    "rv", "ownrent", "lor", "dwlltype", "marital", "adults", "infobase",
    "income", "numbcars", "HHstatin", "dwllsize", "forgntvl", "ethnic",
    "kid0_2", "kid3_5", "kid6_10", "kid11_15", "kid16_17", "creditcd",
    "eqpdays", "Customer_ID",
]
## Columns that should be managed manually for null values (high null value rate)
WHITELIST_COLUMNS = ["lor", "adults", "income", "numbcars", "prizm_social_one", "ownrent", "dwlltype", "infobase", "HHstatin", "dwllsize"]
## Manual columns for null fills
IMPUTATION_COLUMNS = {
    "numbcars": 0,
    "ownrent": "Unkown",
    "dwlltype": "Unknown",
    "infobase": "Missing",
    "HHstatin": "Missing",
    "dwllsize": "Missing",
    "lor": 5.0,
    "income": 6.0,
    "adults": 2,
    "prizm_social_one": "S"
}

# Functions
def telecom_select_exprs():
    """Lista para eliminar nulos de columnas con bajo null rate"""
    return (
        [regexp_replace(col(c), ",", ".").cast("double").alias(c) for c in DOUBLE_COLS]
        + [col(c) for c in PASSTHROUGH_COLS]
    )