import type { View } from "./types"
import { parseDate } from "@/api"


export type GroupedBills = {
  /** 昇順にソートした年 */
  years: number[]
  /** 昇順にソートした月（0始まり） */
  months: number[]
  /** grouped[year][month] = 合計値 */
  grouped: Record<number, Record<number, number>>
}

export function groupPayslipsByYearMonth(
  payslips: View[],
): GroupedBills {
  const grouped: Record<number, Record<number, number>> = {}
  const monthSet = new Set<number>()

  for (const payslip of payslips) {
    const date = parseDate(payslip.date)
    const year = date.getFullYear()
    const month = date.getMonth()

    grouped[year] ??= {}
    grouped[year][month] = (grouped[year][month] ?? 0) + Number(payslip.tedori)
    monthSet.add(month)
  }

  return {
    years: Object.keys(grouped).map(Number).sort((a, b) => a - b),
    months: [...monthSet].sort((a, b) => a - b),
    grouped,
  }
}