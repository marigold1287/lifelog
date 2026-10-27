from collections import defaultdict
from .schemas import ResponseDetailSchema, EntrySchema, ResponseSchema
from app.asset.models import Holding, Price, Entry, AccountType
from decimal import Decimal
from dataclasses import dataclass

@dataclass
class HoldingSummary:
    holding: Holding
    price: Price | None = None
    account_name: str | None = None

    @property
    def total_quantity(self):
        total = 0
        for entry in self.holding.entries:
            if entry.account.type in [AccountType.EXPENSE, AccountType.INCOME, AccountType.EQUITY]:
                continue
            if self.account_name is None or entry.account.name == self.account_name:
                total += entry.quantity
        return total

    @property
    def acquisition_cost(self):
        cost = 0
        for entry in self.holding.entries:
            if entry.account.type in [AccountType.EXPENSE, AccountType.INCOME, AccountType.EQUITY]:
                continue
            if self.account_name is None or entry.account.name == self.account_name:
                cost += (
                    entry.quantity
                    * (entry.unit_price or Decimal("1"))
                    / self.holding.price_per_units
                )
        return cost

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

def to_detail_schema(holding: Holding, latest_price: Price | None):
    summaries = defaultdict(str)

    for entry in holding.entries:
        summaries[entry.account.name] = HoldingSummary(holding, latest_price, entry.account.name)

    entries = [
        EntrySchema(
            account=account_name,
            total_quantity=summary.total_quantity,
            average_unit_price=summary.average_unit_price,
            acquisition_cost=summary.acquisition_cost,
            current_value=summary.current_value,
            profit_loss=summary.profit_loss,
            profit_loss_rate=summary.profit_loss_rate,
        )
        for account_name, summary in summaries.items()
        if summary.total_quantity != 0
    ]

    summary = HoldingSummary(holding, latest_price)
    entries.append(
        EntrySchema(
            account="Total",
            total_quantity=summary.total_quantity,
            average_unit_price=summary.average_unit_price,
            acquisition_cost=summary.acquisition_cost,
            current_value=summary.current_value,
            profit_loss=summary.profit_loss,
            profit_loss_rate=summary.profit_loss_rate,
        )
    )

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