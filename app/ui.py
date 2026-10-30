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