import os
import joblib
import pandas as pd
from pathlib import Path
from fastapi import FastAPI, HTTPException
from app.schemas import PatientEncounterInput, ReadmissionPredictionResponse

app = FastAPI(
    title="Diabetic 30-Day Readmission Risk Engine",
    description="Clinical decision-support prototype for identifying high-risk diabetic patient readmissions.",
    version="1.0.0"
)

# Operational decision threshold calibrated to achieve >= 60% positive-class recall
OPERATIONAL_THRESHOLD = 0.48

# Load model pipeline artifact relative to project layout
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "readmission_rf_pipeline.joblib"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model artifact not found at {MODEL_PATH}")

pipeline = joblib.load(MODEL_PATH)


@app.get("/health")
def health_check():
    """Verify that the API service is active and the model pipeline is loaded."""
    return {
        "status": "healthy",
        "model_loaded": pipeline is not None,
        "operational_threshold": OPERATIONAL_THRESHOLD
    }


@app.post("/predict", response_model=ReadmissionPredictionResponse)
def predict_readmission(encounter: PatientEncounterInput):
    """
    Generate 30-day readmission risk prediction and risk classification
    for a hospitalized diabetic patient encounter.
    """
    try:
        # 1. Convert validated Pydantic model into a dictionary
        input_dict = encounter.model_dump(by_alias=True)

        # 2. Reconstruct single-row DataFrame matching training schema
        input_df = pd.DataFrame([input_dict])

        # 3. Compute continuous readmission probability from pipeline
        prob_readmit = float(pipeline.predict_proba(input_df)[0, 1])

        # 4. Evaluate against operational decision threshold (tau = 0.48)
        if prob_readmit >= OPERATIONAL_THRESHOLD:
            risk_tier = "HIGH RISK (<30d)"
            recommendation = (
                "Flagged for clinical care coordination: arrange 48-72h post-discharge "
                "follow-up call and verify glycemic medication regimen."
            )
        else:
            risk_tier = "STANDARD RISK"
            recommendation = "Standard discharge protocol: routine outpatient follow-up."

        return ReadmissionPredictionResponse(
            readmission_probability=round(prob_readmit, 4),
            risk_tier=risk_tier,
            operational_threshold=OPERATIONAL_THRESHOLD,
            recommendation=recommendation
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Inference pipeline execution failure: {str(e)}"
        )