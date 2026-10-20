import pandas as pd
from .models import HealthCheckup
from pathlib import Path
from app.db import SessionLocal, safe_commit

PWD = Path(__file__).parent

df = pd.read_csv(PWD / "resources" / "health.csv")
df = df.astype(object).where(df.notna(), None)

with SessionLocal() as session:
    for _, row in df.iterrows():
        record = HealthCheckup(
            date=row["date"],
            height=row["height"],
            weight=row["weight"],
            waist=row["waist_circumference"],
            systolic_bp=row["systolic_bp"],
            diastolic_bp=row["diastolic_bp"],
            vision_right=row["right_vision"],
            vision_left=row["left_vision"],
            hearing_right=row["right_hearing"],
            hearing_left=row["left_hearing"],
            urinalysis=row["urine_test"],
            rbc=row["rbc_count"],
            hemoglobin=row["hemoglobin"],
            wbc=row["wbc_count"],
            hematocrit=row["ht"],
            platelets=row["plt"],
            esr=row["esr"],
            hdl_cholesterol=row["hdl_cholesterol"],
            ldl_cholesterol=row["ldl_cholesterol"],
            triglycerides=row["triglycerides"],
            blood_glucose=row["blood_sugar"],
            hba1c=row["hba1c"],
            ast=row["ast"],
            alt=row["alt"],
            gamma_gtp=row["gamma_gtp"],
            ecg=row["ecg"],
        )
        session.add(record)

    safe_commit(session)