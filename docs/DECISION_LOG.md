## Milestone 3: Model Benchmark and Threshold Optimization

* **Date**: October 23, 2026
* **Decisions**:
  1. Benchmark Comparison: Evaluated Logistic Regression (ROC-AUC 0.6711), Decision Tree (ROC-AUC 0.6523), and Random Forest (ROC-AUC 0.6734) on a held-out test split of 19,676 encounters with zero patient overlap.
  2. Model Selection: Selected Random Forest Classifier as the primary model based on superior discriminative capacity (ROC-AUC 0.6734 >= 0.65 target) and ensemble stability.
  3. Feature Drivers: Top predictive signals identified as past inpatient visits (20.65%), discharge disposition destinations, emergency visits, and medication counts.
  4. Packaging: Exported preprocessor and model as a unified `Pipeline` to `app/readmission_rf_pipeline.joblib` for Module 6 application integration.
* **Status**: Confirmed
