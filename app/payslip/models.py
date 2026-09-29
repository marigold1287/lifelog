from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
import datetime
from app.db import Base

class Payslip(Base):
    __tablename__ = "payslip"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column()

    honkyu: Mapped[int] = mapped_column()
    noryokukyu: Mapped[int] = mapped_column()
    mibunkyu: Mapped[int] = mapped_column()
    shokuji_teate: Mapped[int] = mapped_column()
    kenkyuin_teate: Mapped[int] = mapped_column()
    tsukin_teate: Mapped[int] = mapped_column()
    jutaku_teate: Mapped[int] = mapped_column()
    nitto_teate: Mapped[int] = mapped_column()
    kekkin_koujo: Mapped[int] = mapped_column()
    jitan_kyushutsu_teate: Mapped[int] = mapped_column()
    shoyo: Mapped[int] = mapped_column()
    shoyo_kakyu: Mapped[int] = mapped_column()
    tokubetsu_kakyu: Mapped[int] = mapped_column()
    tokushu_kinmu_teate: Mapped[int] = mapped_column()
    sonota_shikyu: Mapped[int] = mapped_column()

    kenko_hoken: Mapped[int] = mapped_column()
    kosei_nenkin: Mapped[int] = mapped_column()
    koyo_hoken: Mapped[int] = mapped_column()
    kodomo_shienkin: Mapped[int] = mapped_column()
    shotoku_zei: Mapped[int] = mapped_column()
    jumin_zei: Mapped[int] = mapped_column()
    senyukaihi: Mapped[int] = mapped_column()
    shokuji_dai: Mapped[int] = mapped_column()
    shataku_ryo: Mapped[int] = mapped_column() # 社宅料
    ryohi: Mapped[int] = mapped_column() # 寮の食費
    seimei_hoken: Mapped[int] = mapped_column()
    sonota_kojo: Mapped[int] = mapped_column()
    nencho_kabusoku: Mapped[int] = mapped_column()

    @hybrid_property
    def total_shikyu(self) -> int:
        return (
            self.honkyu
          + self.noryokukyu
          + self.mibunkyu
          + self.shokuji_teate
          + self.kenkyuin_teate
          + self.tsukin_teate
          + self.jutaku_teate
          + self.nitto_teate
          + self.kekkin_koujo
          + self.jitan_kyushutsu_teate
          + self.shoyo
          + self.shoyo_kakyu
          + self.tokubetsu_kakyu
          + self.tokushu_kinmu_teate
          + self.sonota_shikyu
        )

    @hybrid_property
    def total_kojo(self) -> int:
        return (
            self.kenko_hoken
          + self.kosei_nenkin
          + self.koyo_hoken
          + self.kodomo_shienkin
          + self.shotoku_zei
          + self.jumin_zei
          + self.senyukaihi
          + self.shokuji_dai
          + self.seimei_hoken
          + self.shataku_ryo
          + self.ryohi
          + self.sonota_kojo
          + self.nencho_kabusoku
        )

    @hybrid_property
    def tedori(self) -> int:
        return self.total_shikyu - self.total_kojo

    @hybrid_property
    def shakai_hokenryo(self) -> int:
        return self.kenko_hoken + self.kosei_nenkin + self.koyo_hoken + self.kodomo_shienkin


