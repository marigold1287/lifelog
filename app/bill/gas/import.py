import pandas as pd
from .models import GasBill as Bill
from pathlib import Path
from app.db import SessionLocal, safe_commit
import math

PWD = Path(__file__).parent

df = pd.read_csv(PWD / "resources" / "gas_bill.csv")

with SessionLocal() as session:
    for _, row in df.iterrows():
        total = math.floor(
              row["basic_rate"]
            + row["consumption_rate"]
            + row["fuel_adjustment_cost"]
            + row["start_discount"]
        )
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