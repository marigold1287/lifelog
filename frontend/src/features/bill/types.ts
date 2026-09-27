import type { BillType } from "./api"

export interface BillView {
  id: number
  start_date: string
  end_date: string
  usage: number
  total: number
  unit_price: number | null
  daily_cost: number | null
  provider: string
}

export interface BillResponse {
  start_date: string
  end_date: string
  usage: number
  total: number
  provider: string
}


export interface BillInput {
  start_date: Date
  end_date: Date
  usage: number
  total: number
  provider: string
}

export interface BillApi {
  type: BillType
  getList(): Promise<BillView[]>
  getProviderList(): Promise<string[]>
  create(bill: BillInput): Promise<BillView>
  update(bill: BillInput, id: string): Promise<void>
  get(id: number | string): Promise<BillInput | null>
  getLatest(): Promise<BillInput | null>
  remove(id: number | string): Promise<void>
}


export const billTypeLabels: Record<BillType, string> = {
    electric: "電気",
    gas: "ガス",
    water: "水道",
}
