import pandas as pd
from .models import Payslip
from pathlib import Path
from app.db import SessionLocal, safe_commit
import math

PWD = Path(__file__).parent

df = pd.read_csv(PWD / "resources" / "payslip.csv")

with SessionLocal() as session:
    for _, row in df.iterrows():
        record = Payslip(
            date=row["date"],
            honkyu=row["base_salary"],
            noryokukyu=row["performance_salary"],
            mibunkyu=row["position_allowance"],
            shokuji_teate=row["meal_allowance"],
            jutaku_teate=row["housing_allowance"],
            kenkyuin_teate=row["researcher_allowance"],
            tsukin_teate=row["commuting_allowance"],
            kekkin_koujo=0,
            jitan_kyushutsu_teate=row["overtime_allowance"],
            shoyo=row["bonus"],
            shoyo_kakyu=row["bonus_allowance"],
            tokubetsu_kakyu=row["special_allowance"],
            tokushu_kinmu_teate=row["special_work_allowance"],
            nitto_teate=row["per_diem_allowance"],
            sonota_shikyu=row["other_payments"],

            kenko_hoken=row["health_insurance"],
            kosei_nenkin=row["welfare_pension"],
            koyo_hoken=row["employment_insurance"],
            kodomo_shienkin=0,
            shotoku_zei=row["income_tax"],
            jumin_zei=row["residence_tax"],
            senyukaihi=row["club_membership_fee"],
            shokuji_dai=row["meal_cost"],
            ryohi=row["dormitory_fee"],
            shataku_ryo=row["company_housing_fee"],
            sonota_kojo=row["other_deductions"],
            nencho_kabusoku=row["year_end_adjustment"],
            seimei_hoken=row["life_insurance"]
        )

        session.add(record)

    safe_commit(session)