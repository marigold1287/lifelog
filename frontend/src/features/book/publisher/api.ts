import type { PublisherView, PublisherInput } from "./types"
import type { WorkView } from "@/features/book/work/types"
import { knockApi } from "@/api"

const BASE_URL = "/api/publisher"

export async function getList(): Promise<PublisherView[]> {
    return await knockApi<PublisherView[]>(BASE_URL) ?? []
}

export function create(publisher: PublisherInput) {
    return knockApi<PublisherView>(BASE_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(publisher),
    })
}

export async function update(publisher: PublisherInput, id: string) {
    await knockApi(
        `${BASE_URL}/${id}`,
        {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(publisher),
        },
    );
}

export async function get(id: number | string) {
    return await knockApi<PublisherInput>(`${BASE_URL}/${id}`)
}

export async function getWorks(id: number | string) {
    return await knockApi<WorkView[]>(`${BASE_URL}/${id}/works`)
}

export async function remove(id: number | string) {
    return await knockApi<null>(
        `${BASE_URL}/${id}`,
        {
            method: "DELETE",
        },
    );
}