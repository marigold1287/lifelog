export type AccountType =
  | "cash"
  | "bank"
  | "taxable"
  | "nisa"
  | "card"
  | "pension"
  | "expense"
  | "income"
  | "equity"

export interface Input {
  name: string
  type: AccountType
  currency: string
  parent_id: number | null
  sort_order: number
}


export interface View {
  id: number
  name: string
  type: AccountType
  currency: string
  label: string
  sort_order: number
}