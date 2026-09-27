import pandas as pd
from .models import WaterBill as Bill
from pathlib import Path
from app.db import SessionLocal, safe_commit
import math

PWD = Path(__file__).parent

df = pd.read_csv(PWD / "resources" / "water_bill.csv")

with SessionLocal() as session:
    for _, row in df.iterrows():
        total = math.floor(
          row["water_basic_fee"]
        + row["water_usage_fee"]
        + row["water_consumption_tax"]
        + row["sewer_basic_fee"]
        + row["sewer_usage_fee"]
        + row["sewer_consumption_tax"]
        + row["account_discount"]
        )
        provider = "東京水道局"
        record = Bill(**{
            "start_date": row["start_date"],
            "end_date": row["end_date"],
            "total": total,
            "usage": row["usage"],
            "provider": provider,
        })

        session.add(record)

    safe_commit(session)