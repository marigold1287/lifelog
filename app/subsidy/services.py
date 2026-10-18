from collections import defaultdict
import numpy as np
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.payslip.services import get_yearly_deduction as get_yearly_deduction_from_payslip, YearlyTotal
from app.asset.transaction.services import get_yearly_deduction as get_yearly_deduction_from_transaction, YearlyDeduction
from .repository import get_all
from .models import Subsidy
from .schemas import NenmatsuChoseiSchema, KakuteiShinkokuSchema, JuminZeiSchema, TaxSchema


def get_shotoku_zeiritsu(value):
    if value < 1950000:
        return 0.05
    elif value < 3299000:
        return 0.1
    elif value < 6949000:
        return 0.2
    elif value < 8999000:
        return 0.23
    elif value < 17999000:
        return 0.33


def get_sokusan_deduction(value):
    """所得税の速算表の控除額"""
    if value < 1950000:
        return 0
    elif value < 3299000:
        return 97500
    elif value < 6949000:
        return 427500
    elif value < 8999000:
        return 636000
    elif value < 17999000:
        return 1536000


def get_fukko_zeiritsu(year):
    return 0.021 if year <= 2047 else 0.0


def to_shotoku_zei_hoken_deduction(value):
    if value < 20000:
        return value
    elif value < 40000:
        return value / 2.0 + 10000
    elif value < 80000:
        return value / 4.0 + 20000
    else:
        return 40000


def to_jumin_zei_hoken_deduction(value):
    if value < 12000:
        return value
    elif value < 32000:
        return value / 2.0 + 6000
    elif value < 56000:
        return value / 4.0 + 14000
    else:
        return 28000


def furusato_deduction_base_amount(donation_total):
    return donation_total - 2000 if donation_total > 2000 else 0


def floor_to_unit(value, base):
    """
    baseの位で切り捨て
    (157, 10) => 150
    """
    return float(base * np.floor(value / base))

def calculate_kakutei_shinkoku(
        year: int,
        subsidy: Subsidy,
        nenmatsu_chosei_result: NenmatsuChoseiSchema,
        deduction_from_transaction: YearlyDeduction,
    ) -> KakuteiShinkokuSchema:
    furusato = int(deduction_from_transaction.furusato.get(year, 0))
    zatsu_shotoku = int(deduction_from_transaction.zatsu_shotoku.get(year, 0))
    haitou = int(deduction_from_transaction.haitou.get(year, 0))
    shotoku = (
        subsidy.amount_after_salary_deductions
      + zatsu_shotoku
      + haitou
    )
    shotoku_donation_deduction = furusato_deduction_base_amount(furusato)
    shotoku_deduction = nenmatsu_chosei_result.total_deduction + shotoku_donation_deduction
    kazei_shotoku = floor_to_unit(
        shotoku - shotoku_deduction, 1000
    )

    shotoku_zei_donation = int(
        sum([
            donation.entry.quantity
            for donation in subsidy.donations
            if donation.is_shotoku_zei_deduction
        ])
    )
    zeigaku_deduction = (
        (shotoku_zei_donation * 0.4 if shotoku_zei_donation >= 2000 else 0)
      + subsidy.shotoku_zei_fixed_deduction
      + int(deduction_from_transaction.haitou.get(year, 0)) * 0.1
    )
    shotoku_zeiritsu = get_shotoku_zeiritsu(kazei_shotoku)
    sokusan_deduction = get_sokusan_deduction(kazei_shotoku)

    fukko_zeiritsu = get_fukko_zeiritsu(year)



    shotoku_zei = int(np.floor(
        (1.0 + fukko_zeiritsu)
      * (kazei_shotoku
      * shotoku_zeiritsu
      - sokusan_deduction
      - zeigaku_deduction)
      )
    )

    paid_shotoku_zei = int(np.floor(
        nenmatsu_chosei_result.shotoku_zei + int(deduction_from_transaction.gensen.get(year, 0))
    ))

    kanpu = paid_shotoku_zei - shotoku_zei

    return KakuteiShinkokuSchema(
        shotoku=shotoku,
        zatsu_shotoku=zatsu_shotoku,
        haitou=haitou,
        kazei_shotoku=kazei_shotoku,
        furusato=furusato,
        shotoku_zei_donation=shotoku_zei_donation,
        shotoku_donation_deduction=shotoku_donation_deduction,
        shotoku_deduction=shotoku_deduction,
        zeigaku_deduction=zeigaku_deduction,
        shotoku_zei=shotoku_zei,
        paid_shotoku_zei=paid_shotoku_zei,
        kanpu=kanpu,
    )


def calculate_nenmatsu_chosei(
    year: int,
    subsidy: Subsidy,
    deduction_from_payslip: YearlyTotal,
    deduction_from_transaction: YearlyDeduction,
) -> NenmatsuChoseiSchema:
    nenshu = deduction_from_payslip.nenshu.get(year, 0)
    shiharai_kingaku = nenshu - deduction_from_payslip.tsukin.get(year, 0)
    ideco = int(deduction_from_transaction.ideco.get(year, 0))
    shakai_hoken_deduction = deduction_from_payslip.shakai_hoken_ryo.get(year, 0)
    total_shakai_hoken_deduction = ideco + shakai_hoken_deduction
    seimei_hoken_deduction = (
        to_shotoku_zei_hoken_deduction(int(deduction_from_transaction.iryo_hoken.get(year, 0)))
      + to_shotoku_zei_hoken_deduction(int(deduction_from_transaction.seimei_hoken.get(year, 0)))
    )
    basic_deduction = subsidy.shotoku_zei_basic_deduction
    total_deduction = int(np.ceil(
        total_shakai_hoken_deduction
      + seimei_hoken_deduction
      + basic_deduction
    ))
    kazei_shotoku = subsidy.amount_after_salary_deductions - total_deduction
    paid_shotoku_zei = deduction_from_payslip.shotoku_zei.get(year, 0)

    shotoku_zeiritsu = get_shotoku_zeiritsu(kazei_shotoku)
    sokusan_deduction = get_sokusan_deduction(kazei_shotoku)

    shotoku_zei = (
        kazei_shotoku
      * shotoku_zeiritsu
      - sokusan_deduction
      - subsidy.shotoku_zei_fixed_deduction
    )

    fukko_zeiritsu = get_fukko_zeiritsu(year)
    shotoku_zei = floor_to_unit(shotoku_zei, 100) * (1.0 + fukko_zeiritsu)
    shotoku_zei = floor_to_unit(shotoku_zei, 100)

    nenmatsu_chosei_kabusoku = paid_shotoku_zei - shotoku_zei


    return NenmatsuChoseiSchema(
        nenshu=nenshu,
        shiharai_kingaku=shiharai_kingaku,
        ideco=ideco,
        shakai_hoken_deduction=shakai_hoken_deduction,
        total_shakai_hoken_deduction=total_shakai_hoken_deduction,
        seimei_hoken_deduction=seimei_hoken_deduction,
        basic_deduction=basic_deduction,
        total_deduction=total_deduction,
        kazei_shotoku=kazei_shotoku,
        paid_shotoku_zei=paid_shotoku_zei,
        shotoku_zei=shotoku_zei,
        nenmatsu_chosei_kabusoku=nenmatsu_chosei_kabusoku,
    )


import numpy as np

def calculate_jumin_zei(
    year: int,
    subsidy: Subsidy,
    deduction_from_payslip: YearlyTotal,
    deduction_from_transaction: YearlyDeduction,
) -> JuminZeiSchema:
    SHINRIN_ZEI = 1000  # 国税（森林環境税）
    KINTO_KENMIN_ZEI = 1000
    KINTO_SHIMIN_ZEI = 3000
    JINTEKI_DEDUCTION_DIFFERENCE = 50000

    # 1. 所得・所得控除・課税所得の算出
    shotoku = (
        subsidy.amount_after_salary_deductions
      + int(deduction_from_transaction.zatsu_shotoku.get(year, 0))
      + int(deduction_from_transaction.haitou.get(year, 0))
    )
    total_deduction = int(np.ceil(
        int(deduction_from_transaction.ideco.get(year, 0))
      + to_jumin_zei_hoken_deduction(int(deduction_from_transaction.iryo_hoken.get(year, 0)))
      + to_jumin_zei_hoken_deduction(int(deduction_from_transaction.seimei_hoken.get(year, 0)))
      + deduction_from_payslip.shakai_hoken_ryo.get(year, 0)
      + subsidy.jumin_zei_basic_deduction
    ))
    kazei_shotoku = floor_to_unit(max(0, shotoku - total_deduction), 1000)
    
    # 所得税率の取得
    shotoku_zeiritsu = get_shotoku_zeiritsu(kazei_shotoku - JINTEKI_DEDUCTION_DIFFERENCE)

    # 2. 調整控除 (chosei_deduction) の計算修正
    if kazei_shotoku <= 2000000:
        chosei_deduction = min(JINTEKI_DEDUCTION_DIFFERENCE, kazei_shotoku) * 0.05
    else:
        # 人的控除差額の合計 - (課税所得 - 200万) が 5万円未満（マイナス含む）なら5万円とみなす
        diff_base = JINTEKI_DEDUCTION_DIFFERENCE - (kazei_shotoku - 2000000)
        chosei_deduction = max(50000, diff_base) * 0.05  # 最低2,500円を保証

    chosei_shimin = chosei_deduction * 0.6
    chosei_kenmin = chosei_deduction * 0.4

    # 3. 配当控除 (haitou_deduction) の算出（所得1,000万円以下を想定: 市民税1.6% / 県民税1.2%）
    haitou_shotoku = int(deduction_from_transaction.haitou.get(year, 0))
    haitou_deduction_shimin = haitou_shotoku * 0.016
    haitou_deduction_kenmin = haitou_shotoku * 0.012
    haitou_deduction_total = haitou_shotoku * 0.028

    # 4. 寄付金控除（一般寄付金 ＋ ふるさと納税基本分）
    shimin_zei_donation_deduction = int(
        sum([donation.entry.quantity for donation in subsidy.donations if donation.is_shimin_zei_deduction])
    ) * 0.1 * 0.6
    kenmin_zei_donation_deduction = int(
        sum([donation.entry.quantity for donation in subsidy.donations if donation.is_kenmin_zei_deduction])
    ) * 0.1 * 0.4

    furusato = int(deduction_from_transaction.furusato.get(year, 0))
    furusato_base = furusato_deduction_base_amount(furusato)
    
    furusato_base_shimin = furusato_base * 0.1 * 0.6
    furusato_base_kenmin = furusato_base * 0.1 * 0.4

    # 5. ふるさと納税 特例分の算出（2割上限の適用ロジックを追加）
    fukko_zeiritsu = get_fukko_zeiritsu(year)
    tokurei_rate = 0.9 - shotoku_zeiritsu * (1.0 + fukko_zeiritsu)
    
    # 本来の特例分（上限なし）
    furusato_tokurei_shimin_raw = furusato_base * tokurei_rate * 0.6
    furusato_tokurei_kenmin_raw = furusato_base * tokurei_rate * 0.4
    furusato_tokurei_total_raw = furusato_tokurei_shimin_raw + furusato_tokurei_kenmin_raw

    # 特例分の上限額 ＝（算出所得割額 - 調整控除 - 配当控除）× 20%
    # ※ 一般寄付金やふるさと基本分を引く前の所得割額ベースで判定
    shimin_shotoku_wari_base = kazei_shotoku * 0.06 - chosei_shimin - haitou_deduction_shimin
    kenmin_shotoku_wari_base = kazei_shotoku * 0.04 - chosei_kenmin - haitou_deduction_kenmin
    tokurei_limit_total = (shimin_shotoku_wari_base + kenmin_shotoku_wari_base) * 0.2

    # 特例分の上限判定と按分 (市民税6割 / 県民税4割)
    if furusato_tokurei_total_raw > tokurei_limit_total:
        furusato_tokurei_shimin = np.floor(tokurei_limit_total * 0.6)
        furusato_tokurei_kenmin = np.floor(tokurei_limit_total * 0.4)
    else:
        furusato_tokurei_shimin = furusato_tokurei_shimin_raw
        furusato_tokurei_kenmin = furusato_tokurei_kenmin_raw

    # 6. 所得割額の仮算出（100円未満切り捨て）
    shiminzei_shotoku_warigaku = floor_to_unit(
        max(0, kazei_shotoku * 0.06 - np.ceil(
            chosei_shimin + haitou_deduction_shimin + shimin_zei_donation_deduction + furusato_base_shimin + furusato_tokurei_shimin
        )), 100
    )
    kenmin_zei_shotoku_warigaku = floor_to_unit(
        max(0, kazei_shotoku * 0.04 - np.ceil(
            chosei_kenmin + haitou_deduction_kenmin + kenmin_zei_donation_deduction + furusato_base_kenmin + furusato_tokurei_kenmin
        )), 100
    )

    # 7. 定額減税 (fixed_deduction) の適用（所得割額が上限）
    fixed_deduction_shimin = subsidy.jumin_zei_fixed_deduction * 0.6
    fixed_deduction_kenmin = subsidy.jumin_zei_fixed_deduction * 0.4

    shiminzei_shotoku_warigaku = max(0, shiminzei_shotoku_warigaku - fixed_deduction_shimin)
    kenmin_zei_shotoku_warigaku = max(0, kenmin_zei_shotoku_warigaku - fixed_deduction_kenmin)

    # 8. 均等割の加算と合計住民税の算出
    shimin_zei = int(shiminzei_shotoku_warigaku + KINTO_SHIMIN_ZEI)
    kenmin_zei = int(kenmin_zei_shotoku_warigaku + KINTO_KENMIN_ZEI)
    jumin_zei = shimin_zei + kenmin_zei + SHINRIN_ZEI
    
    furusato_limit = floor_to_unit(
        ((kazei_shotoku * 0.1 - chosei_deduction) * 0.2) / 
        (1.0 - 0.1 - shotoku_zeiritsu * (1.0 + fukko_zeiritsu)) + 2000,
        1000
    )

    return JuminZeiSchema(
        shotoku=shotoku,
        total_deduction=total_deduction,
        kazei_shotoku=kazei_shotoku,
        shimin_zei=shimin_zei,
        kenmin_zei=kenmin_zei,
        jumin_zei=jumin_zei,
        furusato_limit=furusato_limit,
    )


def calculate_taxes_for_year(
    year: int,
    subsidy: Subsidy,
    deduction_from_payslip: YearlyTotal,
    deduction_from_transaction: YearlyDeduction,
) -> TaxSchema:
    nenmatsu_chosei = calculate_nenmatsu_chosei(
        year, subsidy, deduction_from_payslip, deduction_from_transaction,
    )
    kakutei_shinkoku = calculate_kakutei_shinkoku(
        year, subsidy, nenmatsu_chosei, deduction_from_transaction,
    )
    jumin_zei = calculate_jumin_zei(
        year, subsidy, deduction_from_payslip, deduction_from_transaction,
    )

    return TaxSchema(
        nenmatsu_chosei=nenmatsu_chosei,
        kakutei_shinkoku=kakutei_shinkoku,
        jumin_zei=jumin_zei,
    )


def calculate_taxes(session: Session) -> dict[int, TaxSchema]:
    deduction_from_payslip = get_yearly_deduction_from_payslip(session)
    deduction_from_transaction = get_yearly_deduction_from_transaction(session)

    return {
        subsidy.year: calculate_taxes_for_year(
            subsidy.year,
            subsidy,
            deduction_from_payslip,
            deduction_from_transaction,
        )
        for subsidy in get_all(session)
    }


if __name__ == "__main__":
    with SessionLocal() as session:
        taxes = calculate_taxes(session)
        for year, tax in taxes.items():
            print(year)
            print("\t", tax.nenmatsu_chosei.nenmatsu_chosei_kabusoku)
            print("\t", tax.kakutei_shinkoku.kanpu)
            print("\t", tax.jumin_zei.jumin_zei)