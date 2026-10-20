import pandas as pd
from .models import Daily
from pathlib import Path
from app.db import SessionLocal, safe_commit

PWD = Path(__file__).parent

df = pd.read_csv(PWD / "resources" / "lifelog.csv")

with SessionLocal() as session:
    for _, row in df.iterrows():
        record = Daily(
            date=row["date"],
            weight=row["weight"],
            body_temperature=row["body_temperature"],
            room_temperature=row["room_temperature"],
            room_humidity=row["room_humidity"],
        )
        session.add(record)

    safe_commit(session)