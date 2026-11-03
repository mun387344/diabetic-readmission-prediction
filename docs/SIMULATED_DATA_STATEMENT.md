# Statement on Data Source and Synthetic/Simulated Data

**Course:** FUSE AI-201: AI Model Development and Implementation  
**Module:** Module 6 Capstone Deliverable D  
**Project:** Predicting 30-Day Hospital Readmission Risk in Diabetic Patients  
**Dataset:** Diabetes 130-US Hospitals for Years 1999–2008 (UCI Machine Learning Repository ID: 296)  

---

## 1. Primary Data Source Identification
This project **does not use synthetic or artificially simulated patient encounter data** for model training, threshold calibration, or fairness audits.

All data utilized across the exploratory analysis, model benchmarking, and subgroup auditing pipelines is derived from the publicly available, de-identified clinical research dataset:
* **Source:** UCI Machine Learning Repository / BioMed Research International (Strack et al., 2014)
* **Citation:** Clore, J., Cios, K., DeShazo, J., & Strack, B. (2014). *Diabetes 130-US Hospitals for Years 1999–2008*. UCI Machine Learning Repository. DOI: `10.24432/C5230J`.
* **Licensing:** Creative Commons Attribution 4.0 International (CC BY 4.0).
* **Scope:** 101,766 historical inpatient encounters across 130 US hospitals and integrated delivery networks between 1999 and 2008.

---

## 2. Distinction Between Secondary Historical Data and Real-Time Clinical EHR
While the dataset represents authentic clinical encounters, it is treated as a **retrospective decision-support benchmark** rather than a live electronic health record (EHR) stream:
1. **Temporal & Geographic Context:** The data covers 1999–2008 hospital encounters in the United States. Clinical standards, insulin regimens, and discharge protocols have shifted since collection.
2. **De-Identification & Anonymization:** Direct identifiers (`encounter_id`, `patient_nbr`) were excluded from predictive feature matrices to prevent identity memorization and protect privacy.
3. **Application Interaction:** The Streamlit dashboard accepts manual input of realistic encounter parameters for demonstration purposes. These inputs reflect historical encounter bounds but do not represent live hospital integration.

---

## 3. Methodological Integrity Notice
No evaluation metrics, subgroup audit findings, or latency benchmarks presented in this portfolio were simulated or synthetically manufactured. All reported scores (e.g., Random Forest ROC-AUC = 0.6694, held-out test recall = 62.69% at τ = 0.48) were computed directly on held-out patient-separated test encounters.