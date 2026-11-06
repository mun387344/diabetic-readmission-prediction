# 🏥 Diabetic 30-Day Readmission Risk Engine

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://diabetic-readmission-risk.streamlit.app)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%20%7C%203.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688.svg)](https://fastapi.tiangolo.com)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

> **Academic Capstone & Clinical Decision-Support Prototype**  
> **Dataset:** UCI Diabetes 130-US Hospitals (1999–2008)  
> **Live Web Application:** [https://diabetic-readmission-risk.streamlit.app](https://diabetic-readmission-risk.streamlit.app)

---

## 1. Executive Summary & Clinical Problem Statement

Hospital readmissions within 30 days of discharge represent a major clinical and operational breakdown in diabetes management, frequently indicating incomplete glycemic stabilization, discharge medication errors, or insufficient outpatient follow-up.

This project delivers an audited, reproducible, and decoupled clinical decision-support prototype. Trained on 101,766 historical encounters from 130 US hospitals, the system ingests 46 clinical encounter features, estimates the statistical risk of 30-day readmission, and provides actionable discharge coordination guidance.

### Clinical Target Formulation
The raw UCI dataset records three encounter outcomes: `<30` (readmitted within 30 days), `>30` (readmitted after 30 days), and `NO` (no recorded readmission). For clinical intervention planning, the target is framed as a binary classification task:
* **Positive Class ($y=1$):** Readmitted in `<30` days (~11.16% base rate). Represents acute post-discharge breakdown requiring care coordination.
* **Negative Class ($y=0$):** `>30` days or `NO` (~88.84%). Represents standard post-discharge trajectory.



## 2. System Architecture & Serving Strategy

The system follows a decoupled microservice architecture separating inference validation from frontend presentation, featuring a self-healing fallback mechanism:
---

```text
┌────────────────────────────────────────────────────────┐
│             STREAMLIT FRONTEND (Port 8501)             │
│        diabetic-readmission-risk.streamlit.app         │
└───────────────────────────┬────────────────────────────┘
                            │
              HTTP POST /predict (Port 8000)
             [Fallback: Direct Embedded Joblib]
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│             FASTAPI ENGINE (app/api.py:8000)           │
│     Pydantic Contract Validation (app/schemas.py)      │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│            SERIALIZED SCIKIT-LEARN PIPELINE            │
│          app/readmission_rf_pipeline.joblib            │
│       Calibrated Decision Boundary: tau = 0.48         │
└────────────────────────────────────────────────────────┘

```


## Repository Layout

```text
diabetic-readmission-prediction/
├── app/
│   ├── api.py                    # FastAPI inference microservice (port 8000)
│   ├── schemas.py                # Pydantic contract with clinical validation rules
│   ├── ui.py                     # Streamlit clinical care coordinator dashboard
│   └── readmission_rf_pipeline.joblib  # Serialized Scikit-learn Random Forest pipeline (10.4 MB)
├── data/
│   ├── processed/                # Zero-leakage patient-separated train/test splits
│   └── diabetic_data.csv         # Raw UCI dataset (101,766 rows, 50 features)
├── docs/
│   ├── PRESENTATION_SLIDES.md    # Markdown slide notes
│   ├── RETROSPECTIVE.md          # Capstone written retrospective (Deliverable C)
│   ├── SIMULATED_DATA_STATEMENT.md # Secondary data statement (Deliverable D)
│   └── SPEAKER_SCRIPT.md         # 10-minute presentation recording script (Deliverable B)
├── tests/
│   ├── test_api_contract.py      # Automated contract & latency benchmarking suite
│   └── audit_subgroup_disparity.py # Demographic fairness audit (Race, Gender, Age)
├── Dockerfile                    # Container build specification
├── .dockerignore                 # Image size optimization exclusions
├── presentation_deck.html        # Interactive capstone HTML presentation deck
├── requirements.txt              # Pinned application runtime dependencies
├── start.sh                      # Dual-service launcher script
└── README.md                     # Engineering and evaluation documentation
```

---

## 3. Modeling Methodology & Evaluation Framework

### Zero-Leakage Patient-Separated Splitting
The UCI dataset contains 101,766 encounters across 71,518 unique patients (patient_nbr). Naive row-level splitting causes encounters from the same patient to cross between train and test partitions, inflating performance metrics.
* **Splitting Protocol:** Partitioning was executed strictly on distinct patient_nbr identifiers using an 80/20 train-test split.
* **Held-out Test Cohort:** Evaluated once on an untouched test set of 19,862 encounters with zero patient crossover.

### Baseline vs. Candidate Model Performance
Models were evaluated on the held-out test cohort across discrimination (ROC-AUC), clinical sensitivity (Recall), and precision:

| Model Architecture | Target Class | ROC-AUC | Recall (≥0.60) | Precision | Operational Threshold (τ) | Clinical Decision Verdict |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Logistic Regression (Baseline)** | $<30$ Days | 0.6512 | 0.5340 | 0.1620 | 0.50 | Baseline linear benchmark; misses $>46\%$ of high-risk patients. |
| **Random Forest (Selected)** | $<30$ Days | **0.6694** | **0.6269** | **0.1712** | **0.48** | **Deployed pipeline.** Captures non-linear interactions; satisfies $\ge 60\%$ recall requirement. |

> **Operational Threshold Rationale ($\tau = 0.48$)**  In hospital discharge management, a False Negative carries a severe clinical cost (a high-risk patient is discharged without transition coordination). Operating at $\tau = 0.48$ shifts the decision boundary to achieve $\ge 60\%$ sensitivity while minimizing unnecessary false alarms.

---

## 4. Demographic Subgroup Fairness Audit

In compliance with responsible AI governance, model behavior was audited across demographic subgroups on the held-out test cohort to evaluate potential disparate impact under the universal threshold ($\tau = 0.48$).

### Summary of Audit Findings

## 4. Demographic Subgroup Fairness Audit

In compliance with responsible AI governance, model behavior was audited across demographic subgroups on the held-out test cohort to evaluate potential disparate impact under the universal threshold (τ = 0.48).

### Summary of Audit Findings

| Demographic Cohort | Subgroup Category | Evaluated $N$ | Actual Positives ($y=1$) | True Positives ($TP$) | Recall ($\ge 0.60$) | False Negative Rate ($FNR$) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Racial Identity** | Caucasian | 15,081 | 1,732 | **1,121** | **0.6472** | 35.28% |
| | African American | 3,745 | 400 | **244** | **0.6100** | 39.00% |
| | Hispanic | 412 | 41 | 22 | 0.5366 | 46.34% |
| | Asian | 126 | 13 | 5 | 0.3846 | **61.54%** |
| **Gender Identity** | Female | 10,724 | 1,241 | **824** | **0.6640** | 33.60% |
| | Male | 9,138 | 977 | 573 | 0.5865 | 41.35% |
| **Age Cohort** | Geriatric ($70+$) | 4,904 | 573 | **372** | **0.6492** | 35.08% |
| | Young Adult ($20–40$) | 1,023 | 102 | 56 | 0.5490 | **45.10%** |

* **Racial Disparity:** Caucasian (64.7%) and African American (61.0%) cohorts met the project's operational sensitivity threshold. In contrast, historical representation disparities contributed to degraded sensitivity for Hispanic encounters (53.7%, catching 22 of 41 cases) and Asian encounters (38.5%, catching 5 of 13 cases), producing a 61.5% False Negative Rate for Asian patients.
* **Gender Disparity:** Female encounters achieved 66.4% recall (824 of 1,241 cases), whereas Male encounters achieved 58.6% recall (573 of 977 cases), landing slightly below the 60% operational target.
* **Age Distribution:** Geriatric encounters (70+ years) demonstrated higher sensitivity (64.9% recall, catching 372 of 573 true cases), whereas the younger adult cohort (20–40 years) had lower sensitivity (54.9% recall, catching 56 of 102 cases) due to sparser baseline chronic utilization history.
* **Statistical Uncertainty Notice:** The Asian cohort ($N=126$, with only 13 actual positive readmissions) and Hispanic cohort ($N=412$, with 41 actual positive readmissions) represent small empirical sample sizes. These sensitivity estimates carry wider confidence intervals and must be interpreted with clinical caution rather than definitive behavioral generalizations.

## 5. Local Setup & Execution Guide


### 1. Clone and Install Dependencies

```bash
git clone https://github.com/mun387344/diabetic-readmission-prediction.git
cd diabetic-readmission-prediction
py -m pip install -r requirements.txt
```

### 2. Launch Backend Inference Service

In your first terminal tab, start the FastAPI engine:

```bash
py -m uvicorn app.api:app --host 127.0.0.1 --port 8000 --reload
```

* Interactive API Documentation (Swagger): http://127.0.0.1:8000/docs
* Health Check Endpoint: http://127.0.0.1:8000/health

### 3. Launch Clinical UI

In a second terminal tab, start the Streamlit interface:

```bash
py -m streamlit run app/ui.py
```

* Clinical Dashboard: http://localhost:8501

### 4. Run Contract and Subgroup Audit Suites

To verify API contract reliability, latency benchmarks, and demographic parity:

```bash
py tests/test_api_contract.py
py tests/audit_subgroup_disparity.py
```

## 6. Containerization (Docker)

The repository provides an isolated multi-service container deployment:

# Build container image
docker build -t diabetic-readmission-engine:latest .

# Run containerized application
docker run -p 8000:8000 -p 8501:8501 diabetic-readmission-engine:latest

## 7. Clinical Limitations & Governance Notice

* **Retrospective Scope:** Trained on historical encounter data from 130 US hospitals (1999–2008). Clinical workflows, medications, and electronic health record systems have evolved significantly since this window.
* **Decision Support Only:** Predicted probabilities are statistical estimates intended to assist discharge care teams with follow-up coordination. The prototype does not provide medical diagnoses or replace clinical judgment.
* **Representational Skew:** Historical underrepresentation of non-Caucasian patients creates measurable false-negative disparities; predictions for minoritized cohorts require clinical caution.