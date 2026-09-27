import type { WorkView, WorkInput, WorkResponse } from "./types"
import { knockApi, parseDate, formatDate } from "@/api"

const BASE_URL = "/api/work"

function toWorkInput(work: WorkResponse): WorkInput {
    return {
        ...work,
        book_records: work.book_records.map(book => ({
            ...book,
            registration_date: parseDate(book.registration_date),
            read_dates: book.read_dates.map(readDate => ({
                ...readDate,
                read_date: parseDate(readDate.read_date),
            })),
        })),
    }
}

function toWorkResponse(work: WorkInput): WorkResponse {
    return {
        ...work,
        book_records: work.book_records.map(book => ({
            ...book,
            registration_date: formatDate(book.registration_date),
            read_dates: book.read_dates.map(readDate => ({
                ...readDate,
                read_date: formatDate(readDate.read_date),
            })),
        })),
    }
}


export async function getList(): Promise<WorkView[]> {
    return await knockApi<WorkView[]>(BASE_URL) ?? []
}

export function create(work: WorkInput) {
    return knockApi<WorkView>(BASE_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(toWorkResponse(work)),
    })
}

export async function update(work: WorkInput, id: string) {
    await knockApi(
        `${BASE_URL}/${id}`,
        {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(toWorkResponse(work)),
        },
    );
}

export async function get(id: number | string) {
    const work = await knockApi<WorkResponse>(`${BASE_URL}/${id}`)

    return work ? toWorkInput(work) : null
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