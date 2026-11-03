# Module 6 Capstone Retrospective: AI Prototype Development

**Student Name:** Muna Mohammed Husen  
**Course:** FUSE AI-201: AI Model Development and Implementation  
**Project:** 30-Day Hospital Readmission Risk Engine for Diabetic Patients  
**Date:** November 2026  

---

## 1. Executive Summary & Key Achievements
This capstone successfully transitioned a retrospective clinical dataset (UCI Diabetes 130-US Hospitals, 101,766 encounters) into a working, decoupled decision-support system:
* **Methodological Integrity:** Established a zero-leakage patient-separated split strategy (`patient_nbr`), preventing optimistic performance inflation across multi-admission patients.
* **Empirical Modeling Benchmark:** Demonstrated that an ensemble Random Forest pipeline outperformed a linear Logistic Regression baseline (ROC-AUC 0.6694 vs. 0.6512).
* **Calibrated Decision Boundary:** Addressed class imbalance (~11.16% readmission rate) by tuning the decision threshold to τ = 0.48, satisfying the clinical sensitivity requirement (held-out test recall = 62.69%) while controlling false-alarm fatigue.
* **Full-Stack Prototyping:** Implemented an end-to-end architecture coupling a FastAPI inference microservice (port 8000) with Pydantic contract validation and an interactive Streamlit clinical care-coordinator dashboard (port 8501).
* **Demographic Parity Auditing:** Conducted automated subgroup fairness audits across Race, Gender, and Age cohorts, explicitly identifying model disparities rather than assuming uniform utility.

---

## 2. Technical Challenges & Overcoming Roadblocks
* **Data Leakage in Clinical Encounters:** Early exploration revealed that naive row-level splitting resulted in encounter crossover for recurring chronic patients. Resolving this required implementing strict identifier-grouped splitting on `patient_nbr`.
* **Preprocessing Pipeline Synchronization:** Ensuring identical transformations between training and live inference was achieved by encapsulating imputer, encoder, and classifier stages into a single serialized Scikit-learn pipeline (`readmission_rf_pipeline.joblib`), eliminating feature misalignment.
* **Environment and Deployment Constraints:** Initial containerization faced local Windows virtualization dependencies. Guided by the project proposal risk mitigation plan, container specifications (`Dockerfile`, `start.sh`) were formalized for reproducibility while native local Python execution served as the robust demonstration environment.

---

## 3. Critical Limitations & Ethical Considerations
* **Temporal & Practice Drift:** The training data spans 1999–2008 in US hospitals. Changes in clinical guidelines, newer antidiabetic agents, and modern electronic health record (EHR) systems limit direct generalizability to contemporary healthcare environments.
* **Subgroup Disparities:** The audit uncovered significant sensitivity degradation in underrepresented racial cohorts (Hispanic recall = 53.9%, Asian recall = 38.5%) and younger adults (20–40 years recall = 52%–58%). Universal thresholding without demographic adjustments risks elevated false negatives in minoritized patient groups.
* **Decision Support Boundary:** The prototype provides statistical risk estimation, not autonomous diagnostic or prescriptive medical judgment.

---

## 4. Lessons Learned & Future Improvements
1. **Clinical Data Science Requires Rigorous Evaluation:** High overall accuracy on imbalanced healthcare datasets masks severe false-negative penalties. Metrics such as ROC-AUC, class-specific recall, and subgroup error audits are essential for responsible modeling.
2. **Planned Future Improvements:**
   * Integrate modern post-discharge data sources to assess covariate drift.
   * Implement threshold calibration tailored to specific demographic risk profiles.
   * Introduce model explainability (SHAP / LIME) directly into the Streamlit interface to provide patient-specific clinical explanations.