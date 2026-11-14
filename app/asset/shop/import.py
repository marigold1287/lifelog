from app.asset.models import Shop
from pathlib import Path
from app.db import SessionLocal

PWD = Path(__file__).parent



with open(PWD / "resources" / "shop.csv", "r") as f:
    with SessionLocal() as session:
        for row in f:
            stripped = row.strip()
            if stripped:
                session.add(
                    Shop(
                        name=stripped
                    )
                )

        session.commit()
