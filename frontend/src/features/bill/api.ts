import type { BillView, BillResponse, BillInput, BillApi } from "./types"
import { knockApi, knockApiNoContent, parseDate, formatDate } from "@/api"

export type BillType = "electric" | "water" | "gas"

function toBillInput(bill: BillResponse): BillInput {
    return {
        ...bill,
        start_date: parseDate(bill.start_date),
        end_date: parseDate(bill.end_date),
    }
}

function toBillResponse(bill: BillInput): BillResponse {
    return {
        ...bill,
        start_date: formatDate(bill.start_date),
        end_date: formatDate(bill.end_date),
    }
}

export function createBillApi(type: BillType): BillApi {
    const baseUrl = `/api/bill/${type}`

    return {
        type: type,

        async getList(): Promise<BillView[]> {
            return await knockApi<BillView[]>(baseUrl)
        },


        async getProviderList(): Promise<string[]> {
            return await knockApi<string[]>(`${baseUrl}/provider`)
        },


        async create(bill: BillInput) {
            return knockApi<BillView>(baseUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(toBillResponse(bill)),
            })
        },

        async update(bill: BillInput, id: string) {
            await knockApi(
                `${baseUrl}/${id}`,
                {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(toBillResponse(bill)),
                },
            )
        },

        async get(id: number | string) {
            const bill = await knockApi<BillView>(`${baseUrl}/${id}`)

            return bill ? toBillInput(bill) : null
        },

        async getLatest() {
            const bill = await knockApi<BillResponse>(`${baseUrl}/latest`)

            return bill ? toBillInput(bill) : null
        },

        async remove(id: number | string) {
            return await knockApiNoContent(
                `${baseUrl}/${id}`,
                {
                    method: "DELETE",
                },
            )
        },
    }
}



// export async function getList(): Promise<BillView[]> {
//     return await knockApi<BillView[]>(BASE_URL) ?? []
// }

// export function create(bill: BillInput) {
//     return knockApi<BillView>(BASE_URL, {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json",
//         },
//         body: JSON.stringify(toBillResponse(bill)),
//     })
// }

// export async function update(bill: BillInput, id: string) {
//     await knockApi(
//         `${BASE_URL}/${id}`,
//         {
//         method: "PUT",
//         headers: {
//             "Content-Type": "application/json",
//         },
//         body: JSON.stringify(toBillResponse(bill)),
//         },
//     );
// }

// export async function get(id: number | string) {
//     const bill = await knockApi<BillView>(`${BASE_URL}/${id}`)

//     return bill ? toBillInput(bill) : null
// }

// export async function getLatest() {
//     const bill = await knockApi<BillResponse>(`${BASE_URL}/latest`)

//     return bill ? toBillInput(bill) : null
// }

// export async function remove(id: number | string) {
//     return await knockApi<null>(
//         `${BASE_URL}/${id}`,
//         {
//             method: "DELETE",
//         },
//     );
// }