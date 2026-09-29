import type { BillView } from "./types"
import { parseDate } from "@/api"

export type BillValueKey = "usage" | "total"

export type GroupedBills = {
  /** 昇順にソートした年 */
  years: number[]
  /** 昇順にソートした月（0始まり） */
  months: number[]
  /** grouped[year][month] = 合計値 */
  grouped: Record<number, Record<number, number>>
}

export function groupBillsByYearMonth(
  bills: BillView[],
  key: BillValueKey,
): GroupedBills {
  const grouped: Record<number, Record<number, number>> = {}
  const monthSet = new Set<number>()

  for (const bill of bills) {
    const date = parseDate(bill.end_date)
    const year = date.getFullYear()
    const month = date.getMonth()

    grouped[year] ??= {}
    grouped[year][month] = (grouped[year][month] ?? 0) + Number(bill[key])
    monthSet.add(month)
  }

  return {
    years: Object.keys(grouped).map(Number).sort((a, b) => a - b),
    months: [...monthSet].sort((a, b) => a - b),
    grouped,
  }
}