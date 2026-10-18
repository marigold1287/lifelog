from dataclasses import dataclass, field
from collections import defaultdict
from sqlalchemy.orm import Session
from .repository import get_deduction_total_by_date
from app.db import SessionLocal

YearlyTotals = dict[int, int]

@dataclass(frozen=True)
class YearlyTotal:
    nenshu: YearlyTotals = field(default_factory=dict)
    tsukin: YearlyTotals = field(default_factory=dict)
    shakai_hoken_ryo: YearlyTotals = field(default_factory=dict)
    shotoku_zei: YearlyTotals = field(default_factory=dict)


def get_yearly_deduction(session: Session) -> YearlyTotal:
    nenshu: defaultdict[int, int] = defaultdict(int)
    tsukin: defaultdict[int, int] = defaultdict(int)
    shakai: defaultdict[int, int] = defaultdict(int)
    shotoku: defaultdict[int, int] = defaultdict(int)

    for date, n, t, s, z in get_deduction_total_by_date(session):
        year = date.year
        nenshu[year] += n or 0
        tsukin[year] += t or 0
        shakai[year] += s or 0
        shotoku[year] += z or 0

    return YearlyTotal(
        nenshu=dict(nenshu),
        tsukin=dict(tsukin),
        shakai_hoken_ryo=dict(shakai),
        shotoku_zei=dict(shotoku),
    )


if __name__ == "__main__":
    with SessionLocal() as session:
        print(get_yearly_deduction(session))