import pandas as pd
from .models import LegacySnapshot
from pathlib import Path
from app.db import SessionLocal, safe_commit
import math

PWD = Path(__file__).parent

df = pd.read_csv(PWD / "resources" / "asset.csv")

records = []

for _, row in df.iterrows():
    records.append(LegacySnapshot(
        date=row["date"],
        category="cash",
        value=row["cash"]
    ))
    records.append(LegacySnapshot(
        date=row["date"],
        category="stock",
        value=row["stock"]
    ))
    records.append(LegacySnapshot(
        date=row["date"],
        category="pension",
        value=row["pension"]
    ))
    records.append(LegacySnapshot(
        date=row["date"],
        category="fund",
        value=row["investment_trust"]
    ))

with SessionLocal() as session:
    session.add_all(records)
    safe_commit(session)