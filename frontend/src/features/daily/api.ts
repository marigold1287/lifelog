import type { Response, Input, Draft } from "./types"
import { knockApi, parseDate, formatDate, knockApiNoContent } from "@/api"

const BASE_URL = "/api/daily"

function toDraft(daily: Response): Draft {
    return {
        ...daily,
        date: parseDate(daily.date),
    }
}

function toInput(daily: Draft): Input {
    if (daily.date == null) {
        throw new Error("日付を入力してください")
    }
    return {
        ...daily,
        date: formatDate(daily.date),
    }
}

export async function getList(): Promise<Response[]> {
    return await knockApi<Response[]>(BASE_URL) ?? []
}

export function create(daily: Draft) {
    return knockApi<Response>(BASE_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(toInput(daily)),
    })
}

export async function update(daily: Draft, id: string) {
    await knockApi(
        `${BASE_URL}/${id}`,
        {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(toInput(daily)),
        },
    );
}

export async function get(id: number | string) {
    const daily = await knockApi<Response>(`${BASE_URL}/${id}`)

    return daily ? toDraft(daily) : null
}


export async function remove(id: number | string) {
    return await knockApiNoContent(
        `${BASE_URL}/${id}`,
        {
            method: "DELETE",
        },
    );
}