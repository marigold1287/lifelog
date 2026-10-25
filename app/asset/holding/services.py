from collections import defaultdict
from .schemas import ResponseDetailSchema, EntrySchema, ResponseSchema
from app.asset.models import Holding, Price, Entry, AccountType
from decimal import Decimal
from dataclasses import dataclass

@dataclass
class HoldingSummary:
    total_quantity: int = 0
    acquisition_cost: Decimal = Decimal("0")
    current_value: Decimal | None = None

    @property
    def profit_loss(self) -> Decimal | None:
        if self.current_value is None:
            return None
        return self.current_value - self.acquisition_cost

    @property
    def profit_loss_rate(self) -> Decimal | None:
        if self.current_value is None:
            return None
        if self.acquisition_cost == 0:
            return Decimal("0")
        return self.profit_loss / self.acquisition_cost * 100


def acquisition_cost(
    quantity: int,
    unit_price: Decimal,
    price_per_units: int,
) -> Decimal:
    return (
        quantity
        * (unit_price or Decimal("1"))
        / price_per_units
    )

def current_value(
    quantity: int,
    price: Decimal,
    price_per_units: int,
) -> Decimal:
    return quantity * price / price_per_units

def to_list_response_schema(holding: Holding, latest_price: Price | None):
    summary = HoldingSummary()

    for entry in holding.entries:
        (quantity, acquisition_cost_) = get_quantity_and_acquisition_cost(entry, holding.price_per_units)

        summary.total_quantity += quantity
        summary.acquisition_cost += acquisition_cost_
    if latest_price:
        summary.current_value = current_value(
            summary.total_quantity,
            latest_price.price,
            holding.price_per_units,
        )
    else:
        summary.current_value = None

    return ResponseSchema(
        id=holding.id,
        name=holding.name,
        type=holding.type,
        symbol=holding.symbol,
        total_quantity=summary.total_quantity,
        acquisition_cost=round(summary.acquisition_cost),
        current_value=round(summary.current_value) if summary.current_value else None,
        profit_loss=round(summary.profit_loss) if summary.current_value else None,
        profit_loss_rate=round(summary.profit_loss_rate, 2) if summary.current_value else None,
        price_per_units=holding.price_per_units,
    )

def get_quantity_and_acquisition_cost(entry: Entry, price_per_units: int):
    if entry.account.type in [AccountType.EXPENSE, AccountType.INCOME, AccountType.EQUITY]:
        (quantity, acquisition_cost_) = [Decimal("0"), Decimal("0")]
    else:
        quantity = entry.quantity
        acquisition_cost_ = acquisition_cost(
            entry.quantity,
            entry.unit_price,
            price_per_units,
        )

    return quantity, acquisition_cost_



def to_detail_schema(holding: Holding, latest_price: Price | None):
    summaries = defaultdict(HoldingSummary)

    for entry in holding.entries:
        (quantity, acquisition_cost_) = get_quantity_and_acquisition_cost(entry, holding.price_per_units)
        if entry.account.type in [AccountType.EXPENSE, AccountType.INCOME, AccountType.EQUITY]:
            continue
        summary = summaries[entry.account.name]

        summary.total_quantity += quantity
        summary.acquisition_cost += acquisition_cost_

    if latest_price is not None:
        for summary in summaries.values():
            summary.current_value = current_value(
                summary.total_quantity,
                latest_price.price,
                holding.price_per_units,
            )

    entries = [
        EntrySchema(
            account=account_name,
            total_quantity=summary.total_quantity,
            average_unit_price=round(
                summary.acquisition_cost
                / summary.total_quantity
                * holding.price_per_units
            ),
            acquisition_cost=round(summary.acquisition_cost),
            current_value=round(summary.current_value) if summary.current_value else None,
            profit_loss=round(summary.profit_loss) if summary.current_value else None,
            profit_loss_rate=round(summary.profit_loss_rate, 2) if summary.current_value else None,
        )
        for account_name, summary in summaries.items()
        if summary.total_quantity != 0
    ]

    return ResponseDetailSchema(
        id=holding.id,
        name=holding.name,
        type=holding.type,
        symbol=holding.symbol,
        currency=holding.currency,
        current_unit_price=latest_price.price if latest_price else None,
        price_source=holding.price_source,
        price_per_units=holding.price_per_units,
        entries=entries,
    )