import calendar
import datetime as dt
from decimal import Decimal
from collections import defaultdict

from sqlalchemy import Date, case, column, func, select, values, or_
from sqlalchemy.orm import Session, aliased, selectinload, joinedload

from app.asset.models import Account, Entry, Holding, Price, Transaction, AccountType, NET_WORTH_TYPES, HoldingType
from app.asset.schemas import AssetResponseSchema, EntryResponseSchema


class AssetRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_history(
        self,
        start_date: dt.date,
        end_date: dt.date,
    ) -> list[AssetResponseSchema]:
        month_ends = self._evaluation_dates(start_date, end_date)

        if not month_ends:
            return []

        month_values = values(
            column("date", Date),
            name="month_ends",
        ).data(
            [(date,) for date in month_ends]
        ).cte("month_ends")

        balances = (
            select(
                month_values.c.date,
                Entry.holding_id,
                Account.type.label("account_type"),
                func.sum(Entry.quantity).label("quantity"),
            )
            .select_from(month_values)
            .join(
                Transaction,
                Transaction.trade_date <= month_values.c.date,
            )
            .join(
                Entry,
                Entry.transaction_id == Transaction.id,
            )
            .join(
                Account,
                Account.id == Entry.account_id,
            )
            .where(
                Account.type.in_(NET_WORTH_TYPES),
                Entry.holding_id.is_not(None),
            )
            .group_by(
                month_values.c.date,
                Entry.holding_id,
                Account.type,
            )
            .cte("balances")
        )

        latest_price = (
            select(Price.price)
            .where(
                Price.holding_id == balances.c.holding_id,
                Price.price_date <= balances.c.date,
            )
            .order_by(Price.price_date.desc())
            .limit(1)
            .scalar_subquery()
        )

        category = case(
            (
                balances.c.account_type == AccountType.PENSION,
                "pension",
            ),
            (
                Holding.type == HoldingType.CASH,
                "cash",
            ),
            (
                Holding.type == HoldingType.FUND,
                "fund",
            ),
            (
                Holding.type == HoldingType.STOCK,
                "stock",
            ),
        ).label("category")

        stmt = (
            select(
                balances.c.date,
                category,
                func.sum(
                    balances.c.quantity
                    * latest_price
                    / Holding.price_per_units
                ).label("value"),
            )
            .select_from(balances)
            .join(
                Holding,
                Holding.id == balances.c.holding_id,
            )
            .where(
                latest_price.is_not(None),
            )
            .group_by(
                balances.c.date,
                category,
            )
            .order_by(
                balances.c.date,
            )
        )

        rows = self.session.execute(stmt).all()

        return self._to_response(rows, month_ends)

    @staticmethod
    def _evaluation_dates(
        start_date: dt.date,
        end_date: dt.date,
    ) -> list[dt.date]:
        result: list[dt.date] = []

        current = start_date.replace(day=1)

        while current <= end_date:
            last_day = calendar.monthrange(
                current.year,
                current.month,
            )[1]

            month_end = current.replace(day=last_day)

            if start_date <= month_end <= end_date:
                result.append(month_end)

            if current.month == 12:
                current = current.replace(
                    year=current.year + 1,
                    month=1,
                )
            else:
                current = current.replace(
                    month=current.month + 1,
                )

        # 最終月の月末がまだ来ていない場合は、end_dateを追加
        if not result or result[-1] != end_date:
            result.append(end_date)

        return result

    @staticmethod
    def _to_response(
        rows,
        month_ends: list[dt.date],
    ) -> list[AssetResponseSchema]:
        values: dict[dt.date, dict[str, Decimal]] = {
            date: {}
            for date in month_ends
        }

        for row in rows:
            values[row.date][row.category] = row.value or Decimal("0")

        return [
            AssetResponseSchema(
                date=date,
                cash=int(values[date].get("cash", 0)),
                fund=int(values[date].get("fund", 0)),
                pension=int(values[date].get("pension", 0)),
                stock=int(values[date].get("stock", 0)),
                total=int(
                    sum(
                        values[date].values(),
                        Decimal("0"),
                    )
                ),
            )
            for date in reversed(month_ends)

        ]



class KakeiboRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_statistics(
        self,
        year: int,
        month: int | None,
    ):
        start_date, end_date = self._parse_start_end_date(year, month)

        monthly_entries = (
            select(
                Entry.account_id.label("account_id"),
                Entry.quantity.label("quantity"),
            )
            .join(
                Transaction,
                Entry.transaction_id == Transaction.id,
            )
            .where(
                Transaction.trade_date >= start_date,
                Transaction.trade_date < end_date,
            )
            .subquery()
        )

        query = (
            select(
                Account.id,
                Account.name,
                Account.parent_id,
                Account.type,
                Account.sort_order,
                func.coalesce(
                    func.sum(monthly_entries.c.quantity),
                    0,
                ).label("total_quantity"),
            )
            .select_from(Account)
            .outerjoin(
                monthly_entries,
                monthly_entries.c.account_id == Account.id,
            )
            .where(
                Account.type.in_([
                    AccountType.EXPENSE,
                    AccountType.INCOME,
                ]),
            )
            .group_by(
                Account.id,
                Account.name,
                Account.parent_id,
                Account.type,
                Account.sort_order,
            )
        )

        return self._to_response(self.session.execute(query).all())

    def get_entries(
        self,
        year: int | None,
        month: int | None,
    ):
        start_date, end_date = self._parse_start_end_date(year, month)

        query = (
            select(
                Transaction.id.label("transaction_id"),
                Transaction.trade_date,
                Transaction.type.label("transaction_type"),
                Transaction.shop,
                Transaction.note,
                Account.label.label("account"),
                Account.type.label("account_type"),
                Holding.name.label("holding"),
                Holding.type.label("holding_type"),
                Entry.item_name,
                Entry.quantity,
                Entry.unit_price,
                Entry.memo,
            )
            .where(
                Transaction.trade_date >= start_date,
                Transaction.trade_date < end_date,
            )
            .join(Entry, Entry.transaction_id == Transaction.id)
            .join(Account, Entry.account_id == Account.id)
            .join(Holding, Entry.holding_id == Holding.id)
            .order_by(Transaction.trade_date)
        )
        rows = self.session.execute(query).all()
        return [EntryResponseSchema(**row._mapping) for row in rows]


    def _parse_start_end_date(self, year: int | None, month: int | None=None):
        if year is None:
            return dt.date(1000, 1, 1), dt.date(3000, 1, 1)

        start_date = dt.date(year, 1, 1)

        if month is None:
            end_date = dt.date(year + 1, 1, 1)
        else:
            start_date = dt.date(year, month, 1)

            if month == 12:
                end_date = dt.date(year + 1, 1, 1)
            else:
                end_date = dt.date(year, month + 1, 1)

        return start_date, end_date


    @staticmethod
    def _to_response(
        rows,
    ):
        nodes = {}

        # 1. 各勘定科目のノードを作成
        for row in rows:
            nodes[row.id] = {
                "id": row.id,
                "name": row.name,
                "parent_id": row.parent_id,
                "type": row.type.value,
                "sort_order": row.sort_order,
                "direct_quantity": row.total_quantity,
                "total_quantity": row.total_quantity,
                "children": [],
            }

        roots = []

        # 2. 親子関係を構築
        for node in nodes.values():
            parent_id = node["parent_id"]

            if parent_id is None:
                roots.append(node)
            elif parent_id in nodes:
                nodes[parent_id]["children"].append(node)

        # 3. 子孫を含めた合計を計算
        def calculate_total(node):
            total = node["direct_quantity"]

            for child in node["children"]:
                total += calculate_total(child)

            node["total_quantity"] = total
            return total

        for root in roots:
            calculate_total(root)

        # 4. APIレスポンス用に整形
        def serialize(node):
            return {
                "id": node["id"],
                "name": node["name"],
                "type": node["type"],
                "total_quantity": node["total_quantity"],
                "children": [
                    serialize(child)
                    for child in node["children"]
                ],
            }

        def sort_tree(nodes):
            nodes.sort(
                key=lambda node: (
                    node["sort_order"],
                    node["id"],
                )
            )

            for node in nodes:
                sort_tree(node["children"])

        sort_tree(roots)

        expense = [
            serialize(node)
            for node in roots
            if node["type"] == AccountType.EXPENSE.value
        ]

        income = [
            serialize(node)
            for node in roots
            if node["type"] == AccountType.INCOME.value
        ]

        expense_total = abs(sum(
            (node["total_quantity"] for node in roots
            if node["type"] == AccountType.EXPENSE.value),
            Decimal("0"),
        ))

        income_total = abs(sum(
            (node["total_quantity"] for node in roots
            if node["type"] == AccountType.INCOME.value),
            Decimal("0"),
        ))

        return {
            "expense": expense,
            "income": income,
            "expense_total": expense_total,
            "income_total": income_total,
            "total": income_total - expense_total,
        }