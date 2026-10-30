import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import recall_score, precision_score, roc_auc_score

# 1. Paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "app" / "readmission_rf_pipeline.joblib"
TEST_DATA_PATH = BASE_DIR / "data" / "processed" / "test_encounters.csv"

OPERATIONAL_THRESHOLD = 0.48

def audit_race_subgroups():
    print(f"Loading test encounters from: {TEST_DATA_PATH}")
    df_test = pd.read_csv(TEST_DATA_PATH)
    
    # Isolate true label: <30 is positive (1), else 0
    y_true = (df_test["readmitted"] == "<30").astype(int)
    
    # Feature columns expected by pipeline (drop target and IDs)
    drop_cols = ["readmitted", "encounter_id", "patient_nbr"]
    X_test = df_test.drop(columns=[c for c in drop_cols if c in df_test.columns])
    
    print(f"Loading pipeline from: {MODEL_PATH}")
    pipeline = joblib.load(MODEL_PATH)
    
    # Predict continuous probabilities
    y_probs = pipeline.predict_proba(X_test)[:, 1]
    y_pred = (y_probs >= OPERATIONAL_THRESHOLD).astype(int)
    
    # Add evaluation columns to a working dataframe
    eval_df = pd.DataFrame({
        "race": df_test["race"].fillna("Missing/?"),
        "y_true": y_true,
        "y_pred": y_pred,
        "y_prob": y_probs
    })
    
    # Group by Race
    records = []
    for race_group, group in eval_df.groupby("race"):
        n_total = len(group)
        positives = group["y_true"].sum()
        
        # Ensure subgroup has sufficient positive cases for meaningful metrics
        if positives >= 10:
            rec = recall_score(group["y_true"], group["y_pred"], zero_division=0)
            prec = precision_score(group["y_true"], group["y_pred"], zero_division=0)
            try:
                auc = roc_auc_score(group["y_true"], group["y_prob"])
            except ValueError:
                auc = np.nan
            fnr = 1.0 - rec
        else:
            rec, prec, auc, fnr = np.nan, np.nan, np.nan, np.nan
            
        records.append({
            "Subgroup (Race)": race_group,
            "N": n_total,
            "True Readmits (<30)": int(positives),
            "Recall (>=0.60)": round(rec, 4) if not np.isnan(rec) else "N/A (low sample)",
            "Precision": round(prec, 4) if not np.isnan(prec) else "N/A (low sample)",
            "FNR (False Neg)": round(fnr, 4) if not np.isnan(fnr) else "N/A (low sample)",
            "ROC-AUC": round(auc, 4) if not np.isnan(auc) else "N/A (low sample)"
        })
        
    summary_table = pd.DataFrame(records)
    print("\n" + "="*80)
    print("SUBGROUP FAIRNESS & DISPARITY AUDIT: RACE COHORTS")
    print(f"Operational Decision Threshold: tau = {OPERATIONAL_THRESHOLD}")
    print("="*80)
    print(summary_table.to_string(index=False))
    print("="*80)

if __name__ == "__main__":
    audit_race_subgroups()
    
    
    
def audit_gender_subgroups():
    df_test = pd.read_csv(TEST_DATA_PATH)
    y_true = (df_test["readmitted"] == "<30").astype(int)
    
    drop_cols = ["readmitted", "encounter_id", "patient_nbr"]
    X_test = df_test.drop(columns=[c for c in drop_cols if c in df_test.columns])
    
    pipeline = joblib.load(MODEL_PATH)
    y_probs = pipeline.predict_proba(X_test)[:, 1]
    y_pred = (y_probs >= OPERATIONAL_THRESHOLD).astype(int)
    
    eval_df = pd.DataFrame({
        "gender": df_test["gender"].fillna("Missing"),
        "y_true": y_true,
        "y_pred": y_pred,
        "y_prob": y_probs
    })
    
    records = []
    for gender_group, group in eval_df.groupby("gender"):
        n_total = len(group)
        positives = group["y_true"].sum()
        
        if positives >= 10:
            rec = recall_score(group["y_true"], group["y_pred"], zero_division=0)
            prec = precision_score(group["y_true"], group["y_pred"], zero_division=0)
            try:
                auc = roc_auc_score(group["y_true"], group["y_prob"])
            except ValueError:
                auc = np.nan
            fnr = 1.0 - rec
        else:
            rec, prec, auc, fnr = np.nan, np.nan, np.nan, np.nan
            
        records.append({
            "Subgroup (Gender)": gender_group,
            "N": n_total,
            "True Readmits (<30)": int(positives),
            "Recall (>=0.60)": round(rec, 4) if not np.isnan(rec) else "N/A",
            "Precision": round(prec, 4) if not np.isnan(prec) else "N/A",
            "FNR (False Neg)": round(fnr, 4) if not np.isnan(fnr) else "N/A",
            "ROC-AUC": round(auc, 4) if not np.isnan(auc) else "N/A"
        })
        
    summary_table = pd.DataFrame(records)
    print("\n" + "="*80)
    print("SUBGROUP FAIRNESS & DISPARITY AUDIT: GENDER COHORTS")
    print(f"Operational Decision Threshold: tau = {OPERATIONAL_THRESHOLD}")
    print("="*80)
    print(summary_table.to_string(index=False))
    print("="*80)

if __name__ == "__main__":
    audit_gender_subgroups()