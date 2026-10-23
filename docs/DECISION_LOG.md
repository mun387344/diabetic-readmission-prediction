## Milestone 5: Subgroup Fairness Audit and Final Modeling Synthesis

* **Date**: October 23, 2026
* **Decisions**:
  1. Subgroup Sensitivity: Audited recall across racial cohorts. While aggregate recall is 60.58%, Caucasian recall is 61.58% and African American recall is 57.94%. This demonstrates historical data representation limitations (Section 14 of Proposal).
  2. Artifact Readiness: Model pipeline `app/readmission_rf_pipeline.joblib` confirmed operational and smoke-tested on un-transformed feature sets.
  3. Notebook Hygiene: Exploration/splitting isolated to `notebooks/01_data_exploration_cleaning.ipynb`; pipeline training, tuning, and export isolated to `notebooks/02_preprocessing_modeling.ipynb`.
* **Status**: Confirmed
