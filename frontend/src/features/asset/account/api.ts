import type { View, Input } from "./types"
import { knockApi, knockApiNoContent, parseDate, formatDate } from "@/api"

const baseUrl = "/api/account"

export async function getList(): Promise<View[]> {
    return await knockApi<View[]>(baseUrl)
}


export async function get(id: number | string): Promise<Input> {
    return await knockApi<Input>(`${baseUrl}/${id}`)
}

export async function getParentList(id: number | string | null): Promise<View[]> {
    const url = id !== null ? `${baseUrl}/parent/exclude/${id}` : `${baseUrl}/parent`
    return await knockApi<View[]>(url)
}

export async function getLeafList(): Promise<View[]> {
    return await knockApi<View[]>(`${baseUrl}/leaf`)
}

export async function getAccountTypeList(): Promise<string[]> {
    return await knockApi<string[]>(`${baseUrl}/type-list`)
}



export async function create(account: Input): Promise<View> {
    return await knockApi<View>(baseUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(account),
            })
        }


export async function update(account: Input, id: number | string): Promise<View> {
    return await knockApi<View>(`${baseUrl}/${id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(account),
            })
        }



export async function remove(id: number | string): Promise<void> {
    return await knockApiNoContent(`${baseUrl}/${id}`, {
                method: "DELETE",
            })
        }

