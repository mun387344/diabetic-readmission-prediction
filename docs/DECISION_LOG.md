## Milestone 4: Operational Threshold Selection and Subgroup Audit

* **Date**: October 23, 2026
* **Decisions**:
  1. Operational Threshold: Calibrated Random Forest decision threshold from default 0.50 to 0.49 to meet the project recall requirement (Recall: 60.58% >= 0.60 target; False Negatives reduced from 984 to 874).
  2. Artifact Serialization: Packaged end-to-end ColumnTransformer and RandomForestClassifier into `app/readmission_rf_pipeline.joblib` (7.09 MB). Smoke tests verified end-to-end functionality on raw DataFrame rows.
  3. Ethical Subgroup Audit: Evaluated performance disparities across race and age cohorts on held-out test data (N=19,676) to identify differential sensitivity.
* **Status**: Confirmed
