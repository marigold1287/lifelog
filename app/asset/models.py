"""資産DB + 家計簿 統合モデル。

考え方（簡易な複式簿記）
- Transaction = 1回の買い物・1回の売買などの「できごと」（ヘッダ）
- Entry       = そのできごとが各口座に与えた増減（明細）。1取引に2行以上
- 円換算の合計が0になるのが決まり
    円              : quantity
    投資（ファンド等）: quantity * unit_price / price_per_units
  例) カード払いの買い物:  食費>食料品 +358 / カードA -358
      引き落とし(振替):    銀行 -358 / カードA +358
- 符号: 資産・負債は残高そのもの（負債はマイナス）。
        費用は+で積み上がり、収入は-で積み上がる（画面では符号を反転して見せる）。
- 純資産 = NET_WORTH_TYPES の口座の「数量 × 時価」の合計。
  expense / income / equity は含めない。
- 残高は保存せず、Entry の合計から導出する（VIEWで作る）。
  通帳の残高は照合用のスナップショットとして別に持つのはOK。
- 生活側（cash/bank/card/expense/income）と投資側（taxable/nisa/pension）は、
  銀行⇄投資口座の振替（deposit / withdraw）だけでつながる。
  売買の中身は家計簿の収支に出ない。
"""
from __future__ import annotations
import enum
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    UniqueConstraint,
    Date,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    func,
    text,
    select,
    case
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, aliased
from sqlalchemy.ext.hybrid import hybrid_property
from app.db import Base


def _enum(e: type[enum.Enum], name: str) -> SAEnum:
    return SAEnum(
        e,
        name=name,
        native_enum=False,
        length=20,
        values_callable=lambda x: [m.value for m in x],
    )


class AccountType(enum.StrEnum):
    # 資産
    CASH = "cash"
    BANK = "bank"
    TAXABLE = "taxable"
    NISA = "nisa"
    PENSION = "pension"
    # 負債
    CARD = "card"
    # 勘定（残高ではなく「積み上がる量」を見る側）
    EXPENSE = "expense"  # 費用カテゴリ（食費>食料品 など）
    INCOME = "income"  # 収入カテゴリ（給与 など）
    EQUITY = "equity"  # 期首残高・未分類の支払元


# 純資産に含める口座タイプ（カードは負の残高として効く）
NET_WORTH_TYPES = frozenset(
    {
        AccountType.CASH,
        AccountType.BANK,
        AccountType.TAXABLE,
        AccountType.NISA,
        AccountType.PENSION,
        AccountType.CARD,
    }
)


class HoldingType(enum.StrEnum):
    CASH = "cash"  # 円もこれ。「JPY」のHoldingを1つ作り、家計簿の明細はすべてこれを使う
    FUND = "fund"
    STOCK = "stock"


class TxType(enum.StrEnum):
    # TRANSFERとDEPOSIT/WITHDRAWを分けるのは無理がある気がする
    # 家計簿
    EXPENSE = "expense"  # 支出（買い物、水道代など）
    INCOME = "income"  # 収入
    TRANSFER = "transfer"  # 口座間の振替（カード引き落とし、ATM出金、PASMOチャージなど）
    # 投資
    INITIAL = "initial"
    BUY = "buy"
    SELL = "sell"
    DIVIDEND_REINVEST = "dividend_reinvest"
    DEPOSIT = "deposit"  # 投資口座への入金（銀行→投資口座の橋）
    WITHDRAW = "withdraw"  # 投資口座からの出金（投資口座→銀行の橋）
    ADJUST = "adjust"  # 残高調整
    SPLIT = "split"  # 株式分割


class Account(Base):
    """口座・勘定。銀行口座もカード、「食費>食料品」のようなカテゴリも1行。"""

    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    type: Mapped[AccountType] = mapped_column(_enum(AccountType, "account_type"))
    currency: Mapped[str] = mapped_column(String(3), default="JPY")
    sort_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("account.id"))  # 食費>食料品

    parent: Mapped[Account | None] = relationship(
        remote_side="Account.id", back_populates="children"
    )
    children: Mapped[list[Account]] = relationship(back_populates="parent")
    entries: Mapped[list[Entry]] = relationship(back_populates="account")

    __table_args__ = (
        # 同じ親の下で名前が重複しない（Zaimの「その他」が複数の大カテゴリにあるため）
        UniqueConstraint("parent_id", "name"),
        # 最上位（parent_id が NULL）は NULL どうしが重複扱いにならないので別途保証
        # Index(
        #     "uq_account_root_name",
        #     "name",
        #     unique=True,
        #     postgresql_where=text("parent_id IS NULL"),
        # ),
    )
    
    @hybrid_property
    def label(self) -> str:
        return f"{self.parent.name} > {self.name}" if self.parent else self.name

    @label.inplace.expression
    @classmethod
    def _label_expression(cls):
        parent = aliased(cls)
        parent_name = (
            select(parent.name)
            .where(parent.id == cls.parent_id)
            .scalar_subquery()
        )
        return case(
            (cls.parent_id.is_not(None), parent_name + " > " + cls.name),
            else_=cls.name,
        )

class Holding(Base):
    __tablename__ = "holding"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    type: Mapped[HoldingType] = mapped_column(_enum(HoldingType, "holding_type"))
    symbol: Mapped[str | None] = mapped_column(String(50))  # ティッカー/ファンドコード
    currency: Mapped[str] = mapped_column(String(3), default="JPY")
    price_source: Mapped[str | None] = mapped_column(String(50))  # 使うAPI名など。Nullは手入力
    # 価額の単位口数。投信の基準価額は「1万口あたり」なので 10000、株・現金は 1
    price_per_units: Mapped[int] = mapped_column(Integer, default=1)

    entries: Mapped[list[Entry]] = relationship(back_populates="holding")
    prices: Mapped[list[Price]] = relationship(back_populates="holding")

    __table_args__ = (CheckConstraint("price_per_units > 0", name="holding_price_per_units_check"),)


class Transaction(Base):
    """ヘッダ。1回の買い物・1回の売買・1回の振替。"""

    __tablename__ = "transactions"  # transactionは予約語に近いからここだけ複数にしておく

    id: Mapped[int] = mapped_column(primary_key=True)
    trade_date: Mapped[date] = mapped_column(Date)
    type: Mapped[TxType] = mapped_column(_enum(TxType, "tx_type"))
    shop: Mapped[str | None] = mapped_column(String(100))  # 将来は shop_id に置き換える余地あり
    note: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    entries: Mapped[list[Entry]] = relationship(
        back_populates="transaction", cascade="all, delete-orphan"
    )

    __table_args__ = (Index("ix_transactions_trade_date", "trade_date"),)


class Entry(Base):
    """明細。どの口座の、どの銘柄が、どれだけ増減したか。旧 Transaction に相当。"""

    __tablename__ = "entry"

    id: Mapped[int] = mapped_column(primary_key=True)
    transaction_id: Mapped[int] = mapped_column(
        ForeignKey("transactions.id", ondelete="CASCADE")
    )
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    holding_id: Mapped[int] = mapped_column(ForeignKey("holding.id"))
    quantity: Mapped[Decimal] = mapped_column(Numeric(20, 6))
    unit_price: Mapped[Decimal | None] = mapped_column(Numeric(20, 6))
    item_name: Mapped[str | None] = mapped_column(String(200))  # きゃべつ、ヨーグルトなど
    memo: Mapped[str | None] = mapped_column(String(500))

    transaction: Mapped[Transaction] = relationship(back_populates="entries")
    account: Mapped[Account] = relationship(back_populates="entries")
    holding: Mapped[Holding] = relationship(back_populates="entries")

    __table_args__ = (
        Index("ix_entry_transaction", "transaction_id"),
        Index("ix_entry_account_holding", "account_id", "holding_id"),
        Index("ix_entry_holding", "holding_id"),
    )


class Price(Base):
    __tablename__ = "price"

    holding_id: Mapped[int] = mapped_column(ForeignKey("holding.id"), primary_key=True)
    price_date: Mapped[date] = mapped_column(Date, primary_key=True)
    price: Mapped[Decimal] = mapped_column(Numeric(20, 6))
    source: Mapped[str] = mapped_column(String(50), default="api")  # api / manual

    holding: Mapped[Holding] = relationship(back_populates="prices")


# ---------------------------------------------------------------------------
# Future work（今は作らない）
#
# 1. shop テーブル（チェーン>店舗）
#      Shop(id, name, parent_id -> shop.id)  ※自己参照。例: イトーヨーカドー > 綾瀬店
#      transactions.shop_id を NULL可で追加し、既存の shop 文字列から埋める
#
# 2. item テーブル（品目マスタ + バーコード）
#      Item(id, name, parent_id -> item.id, barcode UNIQUE NULL, default_account_id -> account.id)
#      ※総称（もやし）の下に、バーコードあり/なしの品目をぶら下げる。深さは2段まで
#      entry.item_id を NULL可で追加。item_name は元の表記として残す
#      品目ごとの個数・単価を持つなら entry に item_count などを別列で足す
#      （今の quantity は円の数量なので流用しない）
#
# 3. 未払金（発生主義）
#      請求日と引き落とし日を分けたくなったら、type=card 相当の「未払金」勘定をはさむ
#
# 4. 投資の取得原価・売却益の確定（平均法など）
# ---------------------------------------------------------------------------