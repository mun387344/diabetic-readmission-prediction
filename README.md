# 🏥 30-Day Hospital Readmission Risk Engine for Diabetic Patients

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![UI](https://img.shields.io/badge/Streamlit-1.36+-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.5+-F7931E.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/Data%20License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

> **Academic Capstone & Clinical Prototype**  
> **Course:** FUSE AI-201 AI Model Development and Implementation  
> **Dataset:** UCI Diabetes 130-US Hospitals (1999–2008)  

---

## 1. Executive Summary & Clinical Problem Statement

Hospital readmissions within 30 days of discharge represent a major quality and cost challenge in diabetic care, often signaling incomplete glycemic stabilization or inadequate post-discharge support.

This project delivers a defensible, reproducible, and audited clinical decision-support prototype. Using 101,766 historical encounters from 130 US hospitals, the system ingests 46 clinical encounter features, estimates the risk of 30-day readmission, and provides actionable discharge coordination guidance.

### Clinical Target Formulation
The original dataset records three encounter outcomes: `<30` (readmitted within 30 days), `>30` (readmitted after 30 days), and `NO` (no recorded readmission). For clinical intervention planning, the target is framed as a binary classification task:
* **Positive Class ($y = 1$):** Readmitted in `<30` days (~11.16% base rate). Represents acute post-discharge breakdown requiring care coordination.
* **Negative Class ($y = 0$):** `>30` days or `NO` (~88.84%). Represents standard post-discharge trajectory.

---

## 2. System Architecture & Repository Layout

The system follows a modular microservice-style design separating model validation/inference from the user interface:

```text
diabetic-readmission-prediction/
├── app/
│   ├── api.py                    # FastAPI inference microservice (port 8000)
│   ├── schemas.py                # Pydantic contract with clinical validation rules
│   ├── ui.py                     # Streamlit clinical care coordinator dashboard (port 8501)
│   └── readmission_rf_pipeline.joblib  # Serialized Scikit-learn Random Forest pipeline (10.4 MB)
├── data/
│   ├── processed/                # Zero-leakage patient-separated train/test splits
│   └── diabetic_data.csv         # Raw UCI dataset (101,766 rows, 50 features)
├── tests/
│   ├── test_api_contract.py      # Automated contract & latency benchmarking suite
│   └── audit_subgroup_disparity.py # Demographic fairness audit (Race, Gender, Age)
├── Dockerfile                    # Container build specification
├── .dockerignore                 # Image size optimization exclusions
├── requirements.txt              # Pinned minimal application runtime dependencies
├── start.sh                      # Dual-service local startup script
└── README.md                     # Engineering and evaluation documentation
```

---

## 3. Modeling Methodology & Evaluation Framework

### Leakage-Free Patient-Separated Splitting
The UCI dataset contains multiple admissions for recurring patients (`patient_nbr`). Random row-level splitting would allow encounters from the same patient to appear in both training and test sets, causing optimistic data leakage.
* **Splitting Protocol:** Partitioning was executed strictly on distinct `patient_nbr` identifiers using an 80/20 train-test split.
* **Held-out Test Cohort:** Evaluated once on an untouched test set of ~19,862 encounters with zero patient crossover.

### Baseline vs. Candidate Model Performance
Models were evaluated on the held-out test cohort across discrimination (ROC-AUC), clinical sensitivity (Recall), and precision:

| Model Architecture | ROC-AUC | Recall (<30d) | Precision | Operational Threshold (tau) | Clinical Decision Verdict |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Logistic Regression (Baseline)** | 0.6512 | 0.5340 | 0.1620 | 0.50 | Baseline linear benchmark; misses >46% of high-risk patients. |
| **Random Forest (Selected)** | **0.6694** | **0.6269** | **0.1712** | **0.48** | **Deployed pipeline.** Captures non-linear interactions; satisfies >= 60% recall requirement. |

> **Operational Threshold Rationale (tau = 0.48):** In hospital discharge management, a False Negative carries a severe clinical penalty (a high-risk patient is discharged without transition coordination). Operating at tau = 0.48 shifts the decision boundary to guarantee >= 60% sensitivity while controlling false-alarm fatigue.

---

## 4. Subgroup Fairness & Disparity Audit

In compliance with responsible AI governance, model behavior was audited across demographic subgroups on the held-out test cohort to detect potential disparate impact under the universal threshold (tau = 0.48).

### Summary of Audit Findings
* **Racial Disparity:** Caucasian (64.7% recall) and African American (61.0% recall) cohorts met the project's clinical recall threshold (>= 60%). However, severe representation disparities in historical data resulted in degraded recall for Hispanic (53.9%) and Asian (38.5%) patients, producing a 61.5% False Negative Rate for Asian encounters.
* **Gender Cohorts:** Female encounters achieved 66.4% recall, whereas Male encounters achieved 58.7% recall, falling slightly below operational targets.
* **Age Distribution:** Geriatric encounters (70+ years) demonstrated strong sensitivity (65% to 70% recall), while younger adult cohorts (20 to 40 years) showed lower recall (52% to 58%) due to lower baseline chronic utilization signals.

## 5. Local Setup & Execution Guide

### Prerequisites

* Python 3.11 or 3.13 installed
* Local virtual environment (recommended)

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

### 6. Containerization (Docker)

The repository provides an isolated deployment setup:

* `Dockerfile`: Minimal `python:3.11-slim` runtime containing dependencies and the application artifact.
* `start.sh`: Shell launcher that initializes FastAPI on port 8000 and Streamlit on port 8501 concurrently.

```bash
# Build container image
docker build -t diabetic-readmission-engine:latest .

# Run containerized application
docker run -p 8000:8000 -p 8501:8501 diabetic-readmission-engine:latest
```

### 7. Clinical Limitations & Governance Notice

* **Retrospective Scope:** This system is trained on historical encounter data from 130 US hospitals (1999–2008). Clinical workflows, medications, and electronic health record systems have evolved significantly since this window.
* **Decision Support Only:** Predicted probabilities are statistical estimates intended to assist discharge care teams with follow-up coordination. The prototype does not provide medical diagnoses or replace clinical judgment.
* **Representational Skew:** Historical underrepresentation of non-Caucasian patients creates measurable false-negative disparities; predictions for minoritized cohorts require clinical caution.