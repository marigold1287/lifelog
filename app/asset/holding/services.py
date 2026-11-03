from .schemas import EntrySchema, ResponseSchema, HoldingSummarySchema, AccountSummarySchema
from app.asset.models import Holding, Price, AccountType, HoldingType
from decimal import Decimal
from dataclasses import dataclass, replace


excluded_types = {
    AccountType.EXPENSE,
    AccountType.INCOME,
    AccountType.EQUITY,
}


@dataclass
class HoldingSummary:
    id:int
    name: str
    type: HoldingType
    symbol: str | None
    price_per_units: int
    total_quantity: Decimal = Decimal("0")
    acquisition_cost: Decimal = Decimal("0")
    price: Price | None = None
    account_name: str | None = None

    @property
    def current_value(self) -> Decimal | None:
        if self.price is None:
            return None

        return round(
            self.total_quantity * self.price.price / self.price_per_units
        )


    @property
    def average_unit_price(self) -> Decimal | None:
        if self.total_quantity == 0:
            return None

        return (
            self.acquisition_cost
            / self.total_quantity
            * self.price_per_units
        )

    @property
    def profit_loss(self) -> Decimal | None:
        current_value = self.current_value

        if current_value is None:
            return None

        return round(current_value - self.acquisition_cost)

    @property
    def profit_loss_rate(self) -> Decimal | None:
        profit_loss = self.profit_loss

        if profit_loss is None:
            return None

        if self.acquisition_cost == 0:
            return Decimal("0")

        return round(
            profit_loss / self.acquisition_cost * 100,
            2,
        )

def to_list_response_schema(holding_summmary: HoldingSummarySchema, latest_price: Price | None):
    summary = HoldingSummary(**holding_summmary.model_dump(), price=latest_price, account_name=None)

    return ResponseSchema(
        id=summary.id,
        name=summary.name,
        type=summary.type,
        symbol=summary.symbol,
        total_quantity=summary.total_quantity,
        acquisition_cost=summary.acquisition_cost,
        current_value=summary.current_value,
        profit_loss=summary.profit_loss,
        profit_loss_rate=summary.profit_loss_rate,
        price_per_units=summary.price_per_units,
    )


def _to_list_response_schema(holding: Holding, latest_price: Price | None):
    summary = replace(holding, price=latest_price, account_name=None)

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
    account_summary: AccountSummarySchema,
    price: Price | None,
) -> EntrySchema:

    current_value = (
        round(account_summary.total_quantity * price.price / account_summary.price_per_units)
        if price is not None
        else None
    )

    profit_loss = (
        round(current_value - account_summary.acquisition_cost)
        if current_value is not None
        else None
    )

    return EntrySchema(
        account=account_summary.name,
        total_quantity=account_summary.total_quantity,
        average_unit_price=(
            account_summary.acquisition_cost / account_summary.total_quantity * account_summary.price_per_units
            if account_summary.total_quantity != 0
            else None
        ),
        acquisition_cost=account_summary.acquisition_cost,
        current_value=current_value,
        profit_loss=profit_loss,
        profit_loss_rate=(
            round(profit_loss / account_summary.acquisition_cost * 100, 2)
            if profit_loss is not None and account_summary.acquisition_cost != 0
            else Decimal("0") if profit_loss is not None
            else None
        ),
    )


def calculate_total(account_summaries: list[AccountSummarySchema], price_per_units: int, price: Price | None) -> EntrySchema:

    total_quantity = sum(
        [
            summary.total_quantity
            for summary in account_summaries
        ]
    )

    acquisition_cost = sum(
        [
            summary.acquisition_cost
            for summary in account_summaries
        ]
    )

    current_value = (
        round(total_quantity * price.price / price_per_units)
        if price is not None
        else None
    )



    profit_loss = (
        round(current_value - acquisition_cost)
        if current_value is not None
        else None
    )


    average_unit_price = (
        acquisition_cost / total_quantity * price_per_units
        if total_quantity != 0
        else None
    )

    return EntrySchema(
        account="Total",
        total_quantity=total_quantity,
        average_unit_price=average_unit_price,
        acquisition_cost=acquisition_cost,
        current_value=current_value,
        profit_loss=profit_loss,
        profit_loss_rate=(
            round(profit_loss / acquisition_cost * 100, 2)
            if profit_loss is not None and acquisition_cost != 0
            else Decimal("0") if profit_loss is not None
            else None
        ),
    )
