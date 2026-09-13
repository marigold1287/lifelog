import pandas as pd
from .models import ElectricBill as Bill
from pathlib import Path
from app.db import SessionLocal, safe_commit


PWD = Path(__file__).parent

df = pd.read_csv(PWD / "resources" / "electric_bill.csv")

with SessionLocal() as session:
    for _, row in df.iterrows():
        total = (
            row["basic_rate"]
        + row["tier_one_rate"]
        + row["tier_two_rate"]
        + row["fuel_adjustment_cost"]
        + row["renewable_energy_surcharge"]
        + row["special_discount"]
        )
        if row["basic_rate"] == 550.0:
            provider = "ハチドリ電力"
        else:
            provider = "東京電力"
        record = Bill(**{
            "start_date": row["start_date"],
            "end_date": row["end_date"],
            "total": total,
            "usage": row["usage"],
            "provider": provider,
        })

        session.add(record)

    safe_commit(session)