import type { TransactionDraft, TransactionInput, TransactionView, TransactionResponse, EntryDraft, EntryInput, EntryResponse } from "./types"
import { knockApi, knockApiNoContent, parseDate, formatDate } from "@/api"

const baseUrl = "/api/transaction"

function toInput(transaction: TransactionDraft): TransactionInput {
    if (transaction.type === null) {
        throw new Error("取引タイプを選択してください")
    }
    return {
        type: transaction.type,
        shop: transaction.shop,
        note: transaction.note,
        trade_date: formatDate(transaction.trade_date),
        entries: transaction.entries.map(e => toEntryInput(e)),
    }
}

function toEntryInput(d: EntryDraft): EntryInput {
  if (d.account_id == null || d.holding_id == null || d.quantity == null) {
    throw new Error('口座・銘柄・数量は必須です')
  }
  return { ...d, account_id: d.account_id, holding_id: d.holding_id, quantity: d.quantity }
}

export function toDraft(r: TransactionResponse): TransactionDraft {
  return {
    trade_date: parseDate(r.trade_date),
    type: r.type,
    shop: r.shop,
    note: r.note,
    entries: r.entries.map(toEntryDraft),
  }
}

function toEntryDraft(e: EntryResponse): EntryDraft {
  return {
    id: e.id,
    account_id: e.account_id,
    holding_id: e.holding_id,
    quantity: e.quantity,
    unit_price: e.unit_price,
    item_name: e.item_name,
    memo: e.memo,
  }
}

export async function getList(): Promise<TransactionView[]> {
    return await knockApi<TransactionView[]>(baseUrl)
}


export async function get(id: number | string): Promise<TransactionDraft | null> {
    const transaction = await knockApi<TransactionResponse | null>(`${baseUrl}/${id}`)
    return transaction ? toDraft(transaction) : null
}

export async function getTransactionTypeList(): Promise<string[]> {
    return await knockApi<string[]>(`${baseUrl}/type-list`)
}

export async function create(transaction: TransactionDraft): Promise<TransactionResponse> {
    JSON.stringify(toInput(transaction))
    return await knockApi<TransactionResponse>(baseUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(toInput(transaction)),
            })
        }


export async function update(transaction: TransactionDraft, id: number | string): Promise<TransactionView> {
    return await knockApi<TransactionView>(`${baseUrl}/${id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(toInput(transaction)),
            })
        }



export async function remove(id: number | string): Promise<void> {
    return await knockApiNoContent(`${baseUrl}/${id}`, {
                method: "DELETE",
            })
        }

