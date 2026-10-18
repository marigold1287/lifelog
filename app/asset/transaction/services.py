from decimal import Decimal
from collections import defaultdict
from sqlalchemy.orm import Session
from app.asset.models import TxType
from app.db import SessionLocal
from .repository import get_total_by_date
from dataclasses import dataclass, field

YearlyTotals = dict[int, Decimal]

@dataclass(frozen=True)
class YearlyDeduction:
    ideco: YearlyTotals = field(default_factory=dict)
    haitou: YearlyTotals = field(default_factory=dict)
    gensen: YearlyTotals = field(default_factory=dict)
    zatsu_shotoku: YearlyTotals = field(default_factory=dict)
    furusato: YearlyTotals = field(default_factory=dict)
    seimei_hoken: YearlyTotals = field(default_factory=dict)
    iryo_hoken: YearlyTotals = field(default_factory=dict)

_TARGETS: dict[str, tuple[TxType, str]] = {
    "ideco": (TxType.DEPOSIT, "iDeCo"),
    "haitou": (TxType.INCOME, "配当金(非上場)"),
    "gensen": (TxType.INCOME, "源泉徴収"),
    "zatsu_shotoku": (TxType.SELL, "雑所得"),
    "furusato": (TxType.EXPENSE, "ふるさと納税"),
    "seimei_hoken": (TxType.EXPENSE, "新生命保険料"),
    "iryo_hoken": (TxType.EXPENSE, "介護医療保険料"),
}

def _yearly_total(session: Session, tx_type: TxType, account_name: str) -> YearlyTotals:
    totals: defaultdict[int, Decimal] = defaultdict(Decimal)
    for trade_date, total in get_total_by_date(session, tx_type, account_name):
        totals[trade_date.year] += total or Decimal("0")
    return dict(totals)


def get_yearly_deduction(session: Session) -> YearlyDeduction:
    return YearlyDeduction(
        **{
            key: _yearly_total(session, tx_type, account_name)
            for key, (tx_type, account_name) in _TARGETS.items()
        }
    )

if __name__ == "__main__":
    with SessionLocal() as session:
        print(get_yearly_deduction(session))