from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class PatientEncounterInput(BaseModel):
    # Demographics
    race: str = Field(default="Caucasian", description="Patient demographic cohort")
    gender: str = Field(default="Female", description="Patient biological sex")
    age: str = Field(default="[60-70)", description="10-year age bracket")

    # Encounter logistics
    admission_type_id: int = Field(default=1, ge=1, le=8, description="1=Emergency, 2=Urgent, 3=Elective, etc.")
    discharge_disposition_id: int = Field(default=1, ge=1, le=30, description="Discharge destination code")
    admission_source_id: int = Field(default=7, ge=1, le=26, description="7=Emergency Room, 1=Physician, etc.")
    time_in_hospital: int = Field(default=4, ge=1, le=14, description="Stay duration in days (1 to 14)")
    payer_code: str = Field(default="MC", description="Payer/billing code (e.g. MC, HM, SP)")
    medical_specialty: str = Field(default="InternalMedicine", description="Admitting specialty")

    # Clinical counts and past utilization
    num_lab_procedures: int = Field(default=45, ge=1, le=132, description="Number of lab tests performed")
    num_procedures: int = Field(default=0, ge=0, le=6, description="Number of non-lab medical procedures")
    num_medications: int = Field(default=15, ge=1, le=81, description="Number of distinct medications administered")
    number_outpatient: int = Field(default=0, ge=0, description="Outpatient visits in prior 12 months")
    number_emergency: int = Field(default=0, ge=0, description="Emergency visits in prior 12 months")
    number_inpatient: int = Field(default=0, ge=0, description="Inpatient admissions in prior 12 months")
    number_diagnoses: int = Field(default=7, ge=1, le=16, description="Number of diagnoses entered")
    
# Diagnostic disease groups (the 9 mapped categories)
    diag_1_group: str = Field(default="Circulatory", description="Primary ICD-9 diagnosis group")
    diag_2_group: str = Field(default="Diabetes", description="Secondary diagnosis group")
    diag_3_group: str = Field(default="Respiratory", description="Tertiary diagnosis group")

    # Glycemic test results
    max_glu_serum: str = Field(default="None", description="Peak glucose test: None, Norm, >200, >300")
    A1Cresult: str = Field(default="None", description="HbA1c test: None, Norm, >7, >8")

    # Diabetes medications (23 standard therapies)
    metformin: str = Field(default="No", description="No, Steady, Up, Down")
    repaglinide: str = Field(default="No")
    nateglinide: str = Field(default="No")
    chlorpropamide: str = Field(default="No")
    glimepiride: str = Field(default="No")
    acetohexamide: str = Field(default="No")
    glipizide: str = Field(default="No")
    glyburide: str = Field(default="No")
    tolbutamide: str = Field(default="No")
    pioglitazone: str = Field(default="No")
    rosiglitazone: str = Field(default="No")
    acarbose: str = Field(default="No")
    miglitol: str = Field(default="No")
    troglitazone: str = Field(default="No")
    tolazamide: str = Field(default="No")
    examide: str = Field(default="No")
    citoglipton: str = Field(default="No")
    insulin: str = Field(default="No", description="No, Steady, Up, Down")
    glyburide_metformin: str = Field(default="No", alias="glyburide-metformin")
    glipizide_metformin: str = Field(default="No", alias="glipizide-metformin")
    glimepiride_pioglitazone: str = Field(default="No", alias="glimepiride-pioglitazone")
    metformin_rosiglitazone: str = Field(default="No", alias="metformin-rosiglitazone")
    metformin_pioglitazone: str = Field(default="No", alias="metformin-pioglitazone")

    # Overall medication decisions
    change: str = Field(default="No", description="Any diabetic medication dosage changed: Ch or No")
    diabetesMed: str = Field(default="Yes", description="Any diabetic medication prescribed: Yes or No")

    model_config = ConfigDict(populate_by_name=True)


class ReadmissionPredictionResponse(BaseModel):
    readmission_probability: float
    risk_tier: str
    operational_threshold: float
    recommendation: str