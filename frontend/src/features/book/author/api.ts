import type { AuthorView, AuthorInput } from "./types"
import type { WorkView } from "@/features/book/work/types"
import { knockApi } from "@/api"

const BASE_URL = "/api/author"

export async function getList(): Promise<AuthorView[]> {
    return await knockApi<AuthorView[]>(BASE_URL) ?? []
}

export function create(author: AuthorInput) {
    return knockApi<AuthorView>(BASE_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(author),
    })
}

export async function update(author: AuthorInput, id: string) {
    await knockApi(
        `${BASE_URL}/${id}`,
        {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(author),
        },
    );
}

export async function get(id: number | string) {
    return await knockApi<AuthorInput>(`${BASE_URL}/${id}`)
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