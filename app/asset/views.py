# import datetime as dt
 
# from sqlalchemy import BigInteger, Date, String
# from sqlalchemy.orm import Mapped, mapped_column
 
# from app.db import ViewBase


# class DailyByCategory(ViewBase):
#     __tablename__ = "daily_by_category"
 
#     # VIEWには主キーが無いので、行を一意にする列をprimary_keyと宣言しておく
#     date: Mapped[dt.date] = mapped_column(primary_key=True)
#     category: Mapped[str] = mapped_column(String(20), primary_key=True)
#     value: Mapped[int] = mapped_column(BigInteger)
 
# class DailyTotal(ViewBase):
#     __tablename__ = "daily_total"
 
#     date: Mapped[dt.date] = mapped_column(Date, primary_key=True)
#     total: Mapped[int] = mapped_column(BigInteger)
 
