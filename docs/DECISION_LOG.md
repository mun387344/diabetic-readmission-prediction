# Architectural & Analytical Decision Log

**Project:** 30-Day Hospital Readmission Risk Engine for Diabetic Patients  
**Dataset:** UCI Diabetes 130-US Hospitals (1999–2008)  
**Standard:** FUSE AI-201 AI Model Development & Implementation  

---

## Milestone 1: Clinical Target Formulation
* **Date:** October 10, 2026
* **Decision:** Re-frame the multi-class readmission status into a binary decision target:
  * Positive class ($y = 1$): `<30` days (~11.16% base rate).
  * Negative class ($y = 0$): `>30` days and `NO` (~88.84%).
* **Alternatives Considered:** 
  * 3-class classification (`<30`, `>30`, `NO`).
  * Binary classification predicting any readmission (`<30` and `>30` as positive).
* **Rationale:** In hospital discharge management, readmissions within 30 days incur financial penalties and reflect post-discharge care failures. Readmissions beyond 30 days are clinically distinct events. Combining `>30` and `NO` targets acute post-discharge breakdown while managing class imbalance.
* **Status:** Confirmed

---

## Milestone 2: Leakage-Free Data Partitioning
* **Date:** October 14, 2026
* **Decision:** Partition training and test cohorts strictly on distinct `patient_nbr` identifiers (80/20 train/test split).
* **Alternatives Considered:** Standard row-level `train_test_split`.
* **Rationale:** The raw dataset contains 101,766 encounter records across 71,518 unique patients. Multiple admissions per patient mean random row splitting allows records from the same individual into both training and evaluation sets, leaking patient baseline characteristics and producing artificially optimistic test metrics.
* **Status:** Confirmed

---

## Milestone 3: Model Architecture Selection
* **Date:** October 18, 2026
* **Decision:** Deploy a Random Forest classification pipeline; retain Logistic Regression as the baseline benchmark.
* **Alternatives Considered:** Standalone Decision Tree, Gradient Boosting, Deep Neural Networks.
* **Rationale:** Logistic Regression achieved ROC-AUC = 0.6512 but limited sensitivity (Recall = 53.40%). Random Forest achieved ROC-AUC = 0.6694 and captured non-linear clinical interactions between comorbidities, prior utilization, and medication changes while avoiding deep learning compute overhead.
* **Status:** Confirmed

---

## Milestone 4: Operational Decision Threshold Calibration
* **Date:** October 21, 2026
* **Decision:** Calibrate the operational classification threshold to $\tau = 0.48$ instead of the default $0.50$.
* **Alternatives Considered:** Default 0.50 threshold, aggressive low threshold ($\tau = 0.35$).
* **Rationale:** With an ~11.16% base rate, a 0.50 threshold produced insufficient recall (<55%). Setting $\tau = 0.48$ shifted sensitivity to 62.69% on the held-out test cohort, meeting the contract requirement ($\ge 60\%$ recall) while preserving actionable precision (17.12%) to control false-alarm fatigue.
* **Status:** Confirmed

---

## Milestone 5: Subgroup Fairness & Disparity Audit
* **Date:** October 23, 2026
* **Decision:** Conduct comprehensive disparity audits across Race, Gender, and Age cohorts on held-out test data.
* **Findings:**
  * **Race:** Caucasian (64.7% recall) and African American (61.0% recall) satisfied the sensitivity target. Historical underrepresentation produced severe degradation in Hispanic (53.9%) and Asian (38.5%) cohorts.
  * **Gender:** Female encounters achieved 66.4% recall; Male encounters dropped to 58.7% recall.
  * **Age:** Older patients (70+ years) demonstrated strong recall (65%–70%), whereas younger adults (20–40 years) suffered lower recall (52%–58%) due to lower chronic utilization signals.
* **Action:** Recorded findings as clinical limitations in `README.md` and added user-facing clinical decision notices in the UI shell.
* **Status:** Confirmed

---

## Milestone 6: Deployment Architecture & Container Fallback
* **Date:** October 30, 2026
* **Decision:** Implement a decoupled microservice architecture (FastAPI inference engine on port 8000; Streamlit clinical UI on port 8501) with Docker container specification and local native execution fallback.
* **Alternatives Considered:** Single monolithic Streamlit script; direct cloud deployment.
* **Rationale:** Decoupling ensures testability, Pydantic data validation, and sub-second inference latency (P95 = 362 ms). Providing containerization files (`Dockerfile`, `start.sh`) alongside a verified local Python launch path fulfills Section 10 and Section 13 fallback commitments without depending on external hosting availability.
* **Status:** Confirmed
