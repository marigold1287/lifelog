export interface AccountNode {
  id: number
  name: string
  type: string
  total_quantity: number
  children: AccountNode[]
}

export interface AccountSummary {
    expense: AccountNode[]
    income: AccountNode[]
    expense_total: number
    income_total: number
    total: number
}


export interface EntryResponse {
    transaction_id: number
    trade_date: string
    shop: string | null
    note: string | null
    account: string
    holding: string
    item_name: string | null
    quantity: number
    memo: string | null
}