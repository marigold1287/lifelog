export type TxType =
  // 家計簿
  | "expense"  // 支出（買い物、水道代など）
  | "income"  // 収入
  | "transfer"  // 口座間の振替（カード引き落とし、ATM出金、PASMOチャージなど）

  // 投資
  | "initial"
  | "buy"
  | "sell"
  | "dividend_reinvest"  // 配当金再投資
  | "deposit"  // 投資口座への入金（銀行→投資口座の橋）
  | "withdraw"  // 投資口座からの出金（投資口座→銀行の橋）
  | "adjust"  // 残高調整
  | "split"  // 株式分割


// Form用
export interface TransactionDraft {
  trade_date: Date
  type: TxType
  shop: string | null
  note: string | null
  entries: EntryDraft[]
}

export interface EntryDraft {
  id: number | null
  account_id: number | null
  holding_id: number | null
  quantity: number | null
  unit_price: number | null
  item_name: string | null
  memo: string | null
}

// APIへの送信
export interface TransactionInput {
  trade_date: string
  type: TxType
  shop: string | null
  note: string | null
  entries: EntryInput[]
}

export interface EntryInput {
  id: number | null
  account_id: number
  holding_id: number
  quantity: number
  unit_price: number | null
  item_name: string | null
  memo: string | null
}




// APIからの受信
export interface TransactionResponse {
  id: number
  trade_date: string
  type: TxType
  shop: string | null
  note: string | null
  entries: EntryResponse[]
}

export interface EntryResponse {
  id: number
  account_id: number
  holding_id: number
  quantity: number
  unit_price: number | null
  item_name: string | null
  memo: string | null

}


// List用
export interface TransactionView {
  id: number
  trade_date: string
  type: TxType
  shop: string | null
  note: string | null
}


// Decimal型はstringで送られてくる。バックエンドでnumberに直すか、フロントで直す
// Response, Draft, Inputの3つに分ける