import streamlit as st
import requests

# Configure page layout and title
st.set_page_config(
    page_title="Diabetic 30-Day Readmission Risk Engine",
    page_icon="🏥",
    layout="wide"
)

# Header and Clinical Context
st.title("🏥 Diabetic 30-Day Readmission Risk Engine")
st.caption(
    "Decision-Support Prototype | UCI Diabetes 130-US Hospitals (1999–2008) | Group 15"
)

# Clinical Disclaimer required by governance & ethics protocol
st.info(
    "**Clinical Decision-Support Notice:** This system provides retrospective risk estimates "
    "to assist discharge care teams with follow-up coordination. It does not provide medical diagnoses "
    "or substitute for professional clinical judgment."
)

# API Health Check Endpoint
API_HEALTH_URL = "http://127.0.0.1:8000/health"
API_PREDICT_URL = "http://127.0.0.1:8000/predict"

col_status, _ = st.columns([1, 3])
with col_status:
    try:
        response = requests.get(API_HEALTH_URL, timeout=2)
        if response.status_code == 200:
            data = response.json()
            st.success(f"● Backend Connected (Threshold: {data['operational_threshold']})")
        else:
            st.warning("⚠️ Backend returned unexpected status.")
    except Exception:
        st.error("❌ Backend API Unreachable. Ensure Uvicorn is running on port 8000.")
        
        
        
        
st.markdown("---")
st.subheader("Patient Encounter Profile")

tab1, tab2, tab3, tab4 = st.tabs([
    "1. Demographics & Admission",
    "2. Hospitalization & Utilization",
    "3. Diagnoses & Testing",
    "4. Glycemic Medications"
])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        race = st.selectbox("Race", ["Caucasian", "AfricanAmerican", "Hispanic", "Asian", "Other", "?"])
        gender = st.selectbox("Gender", ["Female", "Male"])
        age = st.selectbox(
            "Age Bracket",
            ["[0-10)", "[10-20)", "[20-30)", "[30-40)", "[40-50)", 
             "[50-60)", "[60-70)", "[70-80)", "[80-90)", "[90-100)"],
            index=6
        )
    with col2:
        admission_type_id = st.number_input("Admission Type ID", min_value=1, max_value=8, value=1)
        admission_source_id = st.number_input("Admission Source ID", min_value=1, max_value=25, value=7)
        discharge_disposition_id = st.number_input("Discharge Disposition ID", min_value=1, max_value=30, value=1)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        time_in_hospital = st.slider("Time in Hospital (Days)", min_value=1, max_value=14, value=4)
        num_lab_procedures = st.number_input("Number of Lab Procedures", min_value=1, max_value=132, value=45)
        num_procedures = st.number_input("Number of Other Procedures", min_value=0, max_value=6, value=1)
    with col2:
        num_medications = st.number_input("Number of Medications", min_value=1, max_value=81, value=15)
        number_outpatient = st.number_input("Prior Outpatient Visits", min_value=0, max_value=42, value=0)
        number_emergency = st.number_input("Prior Emergency Visits", min_value=0, max_value=76, value=0)
        number_inpatient = st.number_input("Prior Inpatient Visits", min_value=0, max_value=21, value=0)
        number_diagnoses = st.number_input("Number of Diagnoses", min_value=1, max_value=16, value=7)

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        diag_1 = st.text_input("Primary Diagnosis (ICD-9)", value="414")
        diag_2 = st.text_input("Secondary Diagnosis (ICD-9)", value="411")
        diag_3 = st.text_input("Additional Diagnosis (ICD-9)", value="250")
    with col2:
        max_glu_serum = st.selectbox("Max Glucose Serum Test", ["None", "Norm", ">200", ">300"])
        A1Cresult = st.selectbox("HbA1c Test Result", ["None", "Norm", ">7", ">8"])

with tab4:
    col1, col2, col3 = st.columns(3)
    med_options = ["No", "Steady", "Up", "Down"]
    with col1:
        metformin = st.selectbox("Metformin", med_options)
        glimepiride = st.selectbox("Glimepiride", med_options)
        glipizide = st.selectbox("Glipizide", med_options)
        glyburide = st.selectbox("Glyburide", med_options)
        pioglitazone = st.selectbox("Pioglitazone", med_options)
        rosiglitazone = st.selectbox("Rosiglitazone", med_options)
    with col2:
        insulin = st.selectbox("Insulin", med_options, index=1)
        repaglinide = st.selectbox("Repaglinide", med_options)
        nateglinide = st.selectbox("Nateglinide", med_options)
        chlorpropamide = st.selectbox("Chlorpropamide", med_options)
        acarbose = st.selectbox("Acarbose", med_options)
        miglitol = st.selectbox("Miglitol", med_options)
    with col3:
        change = st.selectbox("Change of Medications", ["No", "Ch"])
        diabetesMed = st.selectbox("Prescribed Diabetes Medication", ["Yes", "No"])
        


st.markdown("---")

# Predict Button
if st.button("Run Readmission Risk Assessment", type="primary", use_container_width=True):
    # 1. Package all widget values to match PatientEncounterInput schema
    payload = {
        "race": race,
        "gender": gender,
        "age": age,
        "admission_type_id": admission_type_id,
        "discharge_disposition_id": discharge_disposition_id,
        "admission_source_id": admission_source_id,
        "time_in_hospital": time_in_hospital,
        "num_lab_procedures": num_lab_procedures,
        "num_procedures": num_procedures,
        "num_medications": num_medications,
        "number_outpatient": number_outpatient,
        "number_emergency": number_emergency,
        "number_inpatient": number_inpatient,
        "diag_1": diag_1,
        "diag_2": diag_2,
        "diag_3": diag_3,
        "number_diagnoses": number_diagnoses,
        "max_glu_serum": max_glu_serum,
        "A1Cresult": A1Cresult,
        "metformin": metformin,
        "repaglinide": repaglinide,
        "nateglinide": nateglinide,
        "chlorpropamide": chlorpropamide,
        "glimepiride": glimepiride,
        "acetohexamide": "No",
        "glipizide": glipizide,
        "glyburide": glyburide,
        "tolbutamide": "No",
        "pioglitazone": pioglitazone,
        "rosiglitazone": rosiglitazone,
        "acarbose": acarbose,
        "miglitol": miglitol,
        "troglitazone": "No",
        "tolazamide": "No",
        "examide": "No",
        "citoglipton": "No",
        "insulin": insulin,
        "glyburide-metformin": "No",
        "glipizide-metformin": "No",
        "glimepiride-pioglitazone": "No",
        "metformin-rosiglitazone": "No",
        "metformin-pioglitazone": "No",
        "change": change,
        "diabetesMed": diabetesMed
    }

    # 2. Transmit to FastAPI inference microservice
    with st.spinner("Analyzing encounter data through calibrated Random Forest pipeline..."):
        try:
            res = requests.post(API_PREDICT_URL, json=payload, timeout=5)
            
            if res.status_code == 200:
                result = res.json()
                prob = result["readmission_probability"]
                tier = result["risk_tier"]
                threshold = result["operational_threshold"]
                rec = result["recommendation"]

                st.subheader("Clinical Risk Assessment Result")
                
                # Display metrics in prominent columns
                m_col1, m_col2, m_col3 = st.columns(3)
                with m_col1:
                    st.metric(
                        label="Predicted 30-Day Risk",
                        value=f"{prob * 100:.1f}%"
                    )
                with m_col2:
                    st.metric(
                        label="Operational Threshold (τ)",
                        value=f"{threshold * 100:.1f}%"
                    )
                with m_col3:
                    if "HIGH" in tier:
                        st.error(f"🚨 {tier}")
                    else:
                        st.success(f"✅ {tier}")

                # Clinical recommendation card
                if "HIGH" in tier:
                    st.warning(f"**Discharge Action Recommended:**\n\n{rec}")
                else:
                    st.info(f"**Discharge Action Recommended:**\n\n{rec}")

            else:
                st.error(f"API Error ({res.status_code}): {res.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to communicate with prediction API: {str(e)}")