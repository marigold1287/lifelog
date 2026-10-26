import type { View, Input, Response, PriceResponse } from "./types"
import { knockApi, knockApiNoContent, parseDate, formatDate } from "@/api"

const baseUrl = "/api/holding"

export async function getList(): Promise<View[]> {
    return await knockApi<View[]>(baseUrl)
}


export async function get(id: number | string): Promise<Response> {
    return await knockApi<Response>(`${baseUrl}/${id}`)
}

export async function getPrices(holding_id: number | string): Promise<PriceResponse[]> {
    return await knockApi<PriceResponse[]>(`/api/price/holding/${holding_id}`)
}

export async function create(holding: Input): Promise<View> {
    return await knockApi<View>(baseUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(holding),
            })
        }


export async function update(holding: Input, id: number | string): Promise<View> {
    return await knockApi<View>(`${baseUrl}/${id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(holding),
            })
        }



export async function remove(id: number | string): Promise<void> {
    return await knockApiNoContent(`${baseUrl}/${id}`, {
                method: "DELETE",
            })
        }

