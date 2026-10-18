import type { View, Input, Tax } from "./types"
import { knockApi, knockApiNoContent } from "@/api"

const BASE_URL = "/api/subsidy"

export async function getList(): Promise<View[]> {
    return await knockApi<View[]>(BASE_URL) ?? []
}

export async function getTax(): Promise<Tax> {
    return await knockApi<Tax>(`${BASE_URL}/tax`) ?? null
}

export function create(subsidy: Input) {
    return knockApi<View>(BASE_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(subsidy),
    })
}

export async function update(subsidy: Input, id: string) {
    await knockApi(
        `${BASE_URL}/${id}`,
        {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(subsidy),
        },
    );
}

export async function get(id: number | string) {
    const subsidy = await knockApi<Input>(`${BASE_URL}/${id}`)

    return subsidy ? subsidy : null
}


export async function remove(id: number | string) {
    return await knockApiNoContent(
        `${BASE_URL}/${id}`,
        {
            method: "DELETE",
        },
    );
}