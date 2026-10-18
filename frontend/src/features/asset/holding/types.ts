export type HoldingType =
  | "cash"
  | "fund"
  | "stock"

  export interface Response {
  name: string
  type: HoldingType
  symbol: string | null
  currency: string
  price_source: string | null
  price_per_units: number
  entries: EntryView[]
}

  export interface Input {
  name: string
  type: HoldingType
  symbol: string | null
  currency: string
  price_source: string | null
  price_per_units: number
}

export interface View {
  id: number
  name: string
  type: HoldingType
  symbol: string | null
  total_quantity: number
  acquisition_cost: number
  current_value: number
  profit_loss: number
  profit_loss_rate: number
  price_per_units: number
}

export interface EntryView {
  account: string
  total_quantity: number
  average_unit_price: number
  acquisition_cost: number
  current_unit_price: number
  current_value: number
  profit_loss: number
  profit_loss_rate: number
}