import type { AccountSummary, EntryResponse } from "./types"
import { knockApi } from "@/api"

const baseUrl = "/api/asset/kakeibo"

export async function get(year: number | string, month: number | string | null): Promise<AccountSummary> {
    const params = new URLSearchParams()
    params.set("year", String(year))

    if (month !== null) {
        params.set("month", String(month))
    }

    return await knockApi<AccountSummary>(
        `${baseUrl}?${params.toString()}`
    )
}

export async function getEntries(year: number | string | null, month: number | string | null): Promise<EntryResponse[]> {
    const params = new URLSearchParams()
    params.set("year", String(year))

    if (year !== null) {
        params.set("year", String(year))
    }

    if (month !== null) {
        params.set("month", String(month))
    }

    return await knockApi<EntryResponse[]>(
        `${baseUrl}/entry?${params.toString()}`
    )
}

