import type { AssetView } from "./types"
import { knockApi, knockApiNoContent, parseDate, formatDate } from "@/api"

// function toInput(bill: BillResponse): BillInput {
//     return {
//         ...bill,
//         start_date: parseDate(bill.start_date),
//         end_date: parseDate(bill.end_date),
//     }
// }

// function toResponse(bill: BillInput): BillResponse {
//     return {
//         ...bill,
//         start_date: formatDate(bill.start_date),
//         end_date: formatDate(bill.end_date),
//     }
// }

const baseUrl = "/api/asset"

export async function getAssetList(): Promise<AssetView[]> {
    return await knockApi<AssetView[]>(baseUrl)
}


