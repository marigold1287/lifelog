from collections import defaultdict
from .schemas import ResponseDetailSchema, EntrySchema, ResponseSchema
from app.asset.models import Holding, Price, Entry, AccountType
from decimal import Decimal
from dataclasses import dataclass, InitVar

@dataclass
class HoldingAggregate:
    total_quantity: Decimal = Decimal("0")
    acquisition_cost: Decimal = Decimal("0")

    def add(self, entry: Entry, holding: Holding) -> None:
        self.total_quantity += entry.quantity
        self.acquisition_cost += (
            entry.quantity
            * (entry.unit_price or Decimal("1"))
            / holding.price_per_units
        )

@dataclass
class HoldingSummary:
    holding: Holding
    price: Price | None = None
    account_name: str | None = None

    def __post_init__(self):
        self.total_quantity = 0
        self.acquisition_cost = 0
        for entry in self.holding.entries:
            if entry.account.type in [AccountType.EXPENSE, AccountType.INCOME, AccountType.EQUITY]:
                continue
            if self.account_name is None or entry.account.name == self.account_name:
                self.total_quantity += entry.quantity
                self.acquisition_cost += (
                    entry.quantity
                    * (entry.unit_price or Decimal("1"))
                    / self.holding.price_per_units
                )


    @property
    def current_value(self):
        if self.price is None:
            return None
        else:
            return round(self.total_quantity * self.price.price / self.holding.price_per_units)

    @property
    def average_unit_price(self):
        if self.total_quantity == 0:
            return None
        return self.acquisition_cost / self.total_quantity * self.holding.price_per_units

    @property
    def profit_loss(self) -> Decimal | None:
        if self.current_value is None:
            return None
        return round(self.current_value - self.acquisition_cost)


    @property
    def profit_loss_rate(self) -> Decimal | None:
        if self.current_value is None:
            return None
        if self.acquisition_cost == 0:
            return Decimal("0")
        return round(self.profit_loss / self.acquisition_cost * 100, 2)

def to_list_response_schema(holding: Holding, latest_price: Price | None):
    summary = HoldingSummary(holding, price=latest_price, account_name=None)

    return ResponseSchema(
        id=holding.id,
        name=holding.name,
        type=holding.type,
        symbol=holding.symbol,
        total_quantity=summary.total_quantity,
        acquisition_cost=summary.acquisition_cost,
        current_value=summary.current_value,
        profit_loss=summary.profit_loss,
        profit_loss_rate=summary.profit_loss_rate,
        price_per_units=holding.price_per_units,
    )

def to_entry_schema(
    account_name: str,
    aggregate: HoldingAggregate,
    holding: Holding,
    price: Price | None,
) -> EntrySchema:
    quantity = aggregate.total_quantity
    cost = aggregate.acquisition_cost

    current_value = (
        round(quantity * price.price / holding.price_per_units)
        if price is not None
        else None
    )

    profit_loss = (
        round(current_value - cost)
        if current_value is not None
        else None
    )

    return EntrySchema(
        account=account_name,
        total_quantity=quantity,
        average_unit_price=(
            cost / quantity * holding.price_per_units
            if quantity != 0
            else None
        ),
        acquisition_cost=cost,
        current_value=current_value,
        profit_loss=profit_loss,
        profit_loss_rate=(
            round(profit_loss / cost * 100, 2)
            if profit_loss is not None and cost != 0
            else Decimal("0") if profit_loss is not None
            else None
        ),
    )

def to_detail_schema(
    holding: Holding,
    latest_price: Price | None,
) -> ResponseDetailSchema:
    summaries: dict[str, HoldingAggregate] = defaultdict(
        HoldingAggregate
    )
    total = HoldingAggregate()

    excluded_types = {
        AccountType.EXPENSE,
        AccountType.INCOME,
        AccountType.EQUITY,
    }

    for entry in holding.entries:
        if entry.account.type in excluded_types:
            continue

        summaries[entry.account.name].add(entry, holding)
        total.add(entry, holding)

    entries = [
        to_entry_schema(account_name, summary, holding, latest_price)
        for account_name, summary in summaries.items()
        if summary.total_quantity != 0
    ]

    entries.append(
        to_entry_schema("Total", total, holding, latest_price)
    )

    return ResponseDetailSchema(
        id=holding.id,
        name=holding.name,
        type=holding.type,
        symbol=holding.symbol,
        currency=holding.currency,
        current_unit_price=(
            latest_price.price if latest_price else None
        ),
        price_source=holding.price_source,
        price_per_units=holding.price_per_units,
        entries=entries,
    )
