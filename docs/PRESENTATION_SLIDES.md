#### System Architecture Diagram

**Title:** End-to-End System & Serving Architecture

**Subtitle:** Decoupled Clinical Decision-Support Pipeline

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        DATA & PREPROCESSING TIER                       │
│                                                                        │
│   UCI 130-US Hospitals (101,766 Encounters)                            │
│   ├── Target Framing: <30 Days (y=1) vs. >=30 / NO (y=0)               │
│   └── Leakage Prevention: Patient-Separated Split (patient_nbr)        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      INFERENCE & PIPELINE ENGINE                       │
│                                                                        │
│   Serialized Pipeline: app/readmission_rf_pipeline.joblib              │
│   ├── Median Imputation + Categorical One-Hot Encoding                 │
│   ├── Random Forest Classifier (n_estimators=100)                      │
│   └── Calibrated Operational Decision Boundary: tau = 0.48             │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                         SERVING & INTERFACE TIER                       │
│                                                                        │
│   FastAPI Microservice (Port 8000)                                     │
│   ├── Pydantic Contract Validation (app/schemas.py)                    │
│   ├── Health Endpoint: GET /health (200 OK)                            │
│   └── Inference Latency: P95 = 362 ms                                  │
│                                   │                                    │
│                                   ▼ HTTP (Port 8000 -> 8501)           │
│   Streamlit Clinical Dashboard (Port 8501)                             │
│   ├── Parameter Input Forms & Risk Meter Gauge                         │
│   └── Actionable Post-Discharge Clinical Care Recommendations          │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      CONTAINERIZATION SPECIFICATION                    │
│                                                                        │
│   Docker Environment: python:3.11-slim Base Image                      │
│   Entrypoint: start.sh (Dual-Service Launch: Uvicorn & Streamlit)      │
└────────────────────────────────────────────────────────────────────────┘

```

---

#### Empirical Model Benchmark Table

**Title:** Held-Out Test Set Performance & Baseline Comparison

**Context:** Evaluated once on an untouched test cohort of 19,862 encounters with zero patient crossover.

| Model Architecture | Target Class | ROC-AUC | Recall ($\ge 0.60$) | Precision | Operational Threshold ($\tau$) | Clinical Decision Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| **Logistic Regression (Baseline)** | $<30$ Days | 0.6512 | 0.5340 | 0.1620 | 0.50 | Baseline linear benchmark; misses $>46\%$ of true positive readmissions. |
| **Random Forest (Selected Engine)** | $<30$ Days | **0.6694** | **0.6269** | **0.1712** | **0.48** | **Selected Pipeline.** Captures non-linear clinical interactions; satisfies sensitivity requirement. |

**Key Takeaways:**

* Setting $\tau = 0.48$ shifts the decision threshold away from default $0.50$ to prioritize high-risk recall in an imbalanced setting (11.16% base rate).
* Achieved **62.69% Sensitivity** on the positive class while preserving operational precision.

---

#### Demographic Subgroup Fairness Audit

**Title:** Subgroup Fairness & Disparity Audit ($\tau = 0.48$)

**Context:** Verification of model behavior across protected attributes to detect disparate impact.

| Demographic Cohort | Subgroup Category | Evaluated $N$ | True Positives ($<30$) | Recall ($\ge 0.60$) | False Negative Rate (FNR) |
| --- | --- | --- | --- | --- | --- |
| **Racial Identity** | Caucasian | 15,081 | 1,732 | **0.6472** | 35.28% |
|  | African American | 3,745 | 400 | **0.6100** | 39.00% |
|  | Hispanic | 412 | 41 | 0.5390 | 46.10% |
|  | Asian | 126 | 13 | 0.3846 | **61.54%** |
| **Gender Identity** | Female | 10,724 | 1,241 | **0.6640** | 33.60% |
|  | Male | 9,138 | 977 | 0.5870 | 41.30% |
| **Age Bracket** | Geriatric ($70–80$) | 4,904 | 573 | **0.6492** | 35.08% |
|  | Young Adult ($20–30$) | 277 | 25 | 0.5200 | **48.00%** |

**Clinical Governance Action:**

* Severe representation disparities in historical data result in elevated false negatives for Asian (61.5% FNR), Hispanic, and younger cohorts.
* Disclosed as explicit clinical governance warnings in both the UI and repository documentation.

---

#### Production Monitoring & Support Plan

**Title:** Continuous Governance & Maintenance Architecture

**Context:** MLOps lifecycle design for monitoring post-prototype deployment.

```text
┌───────────────────────────────┐        ┌──────────────────────────────┐
│     DRIFT DETECTION LAYER     │        │     AUTOMATED RETRAINING     │
│                               │        │                              │
│   Evidently AI Engine         │        │   Cadence: Weekly Trigger    │
│   ├── Population Stability    │───────►│   ├── Data Window: 90 Days   │
│   │   Index (PSI > 0.25)      │        │   ├── Gate: AUC >= 0.6694    │
│   └── KS-Test (Numeric Drift) │        │   └── Rollback: Prior Joblib │
└───────────────────────────────┘        └──────────────────────────────┘
                                                        ▲
                                                        │
┌───────────────────────────────┐                       │
│    PREDICTION LOGGING DB      │                       │
│                               │                       │
│   SQLite / PostgreSQL Logs    │───────────────────────┘
│   ├── Latency (P95 < 363 ms)  │
│   ├── Input Payloads          │
│   └── 30-Day Ground Truth     │
└───────────────────────────────┘

```

* **Feedback Integration:** Ingest confirmed readmission outcomes at the 30-day post-discharge mark.
* **Safety Gate:** Model promotion requires zero degradation against the active production artifact.

---