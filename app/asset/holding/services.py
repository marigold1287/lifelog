from collections import defaultdict
from .schemas import ResponseDetailSchema, EntrySchema, ResponseSchema
from app.asset.models import Holding, Price, Entry, AccountType
from decimal import Decimal
from dataclasses import dataclass

@dataclass
class HoldingSummary:
    total_quantity: int = 0
    acquisition_cost: Decimal = Decimal("0")
    current_value: Decimal = Decimal("0")

    @property
    def profit_loss(self) -> Decimal:
        return self.current_value - self.acquisition_cost

    @property
    def profit_loss_rate(self) -> Decimal:
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

def calculate_holding_value(
    entries: list[Entry],
    price: Price,
    price_per_units: int,
) -> HoldingSummary:
    value = HoldingSummary()

    for entry in entries:
        if entry.account.type in [AccountType.EXPENSE, AccountType.INCOME, AccountType.EQUITY]:
            continue

        value.total_quantity += entry.quantity
        value.acquisition_cost += acquisition_cost(
            entry.quantity,
            entry.unit_price,
            price_per_units,
        )

    value.current_value = current_value(
        value.total_quantity,
        price.price,
        price_per_units,
    )

    return value

def calculate_account_values(
    entries: list[Entry],
    price: Price,
    price_per_units: int,
) -> dict[str, HoldingSummary]:

    values = defaultdict(HoldingSummary)

    for entry in entries:
        if entry.account.type in [AccountType.EXPENSE, AccountType.INCOME, AccountType.EQUITY]:
            continue
        value = values[entry.account.name]

        value.total_quantity += entry.quantity
        value.acquisition_cost += acquisition_cost(
            entry.quantity,
            entry.unit_price,
            price_per_units,
        )

    for value in values.values():
        value.current_value = current_value(
            value.total_quantity,
            price.price,
            price_per_units,
        )

    return values

def to_list_response_schema(holding: Holding, latest_price: Price):
    value = calculate_holding_value(
        holding.entries,
        latest_price,
        holding.price_per_units,
    )

    return ResponseSchema(
        id=holding.id,
        name=holding.name,
        type=holding.type,
        symbol=holding.symbol,
        total_quantity=value.total_quantity,
        acquisition_cost=round(value.acquisition_cost),
        current_value=round(value.current_value),
        profit_loss=round(value.profit_loss),
        profit_loss_rate=round(value.profit_loss_rate, 2),
        price_per_units=holding.price_per_units,
    )




def to_detail_schema(holding: Holding, latest_price: Price):
    account_values = calculate_account_values(
        holding.entries,
        latest_price,
        holding.price_per_units,
    )

    entries = [
        EntrySchema(
            account=account_name,
            total_quantity=value.total_quantity,
            average_unit_price=round(
                value.acquisition_cost
                / value.total_quantity
                * holding.price_per_units
            ),
            acquisition_cost=round(value.acquisition_cost),
            current_unit_price=latest_price.price,
            current_value=round(value.current_value),
            profit_loss=round(value.profit_loss),
            profit_loss_rate=round(value.profit_loss_rate, 2),
        )
        for account_name, value in account_values.items()
        if value.total_quantity != 0
    ]

    return ResponseDetailSchema(
        id=holding.id,
        name=holding.name,
        type=holding.type,
        symbol=holding.symbol,
        currency=holding.currency,
        price_source=holding.price_source,
        price_per_units=holding.price_per_units,
        entries=entries,
    )