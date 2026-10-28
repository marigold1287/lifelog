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
    transaction_type: string
    trade_date: string
    shop: string | null
    note: string | null
    account: string
    account_type: string
    holding: string
    holding_type: string
    item_name: string | null
    quantity: number
    unit_price: number | null
    memo: string | null
}