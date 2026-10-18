import type { View, Input, Draft, EntrySchema } from "./types"
import { knockApi, knockApiNoContent } from "@/api"

const BASE_URL = "/api/subsidy/donation"

export async function getList(): Promise<View[]> {
    return await knockApi<View[]>(BASE_URL) ?? []
}

function toInput(d: Draft) {
    if (d.entry_id == null || d.deduction_year == null) {
        throw new Error('エントリーと控除対象年を入力してください')
    }
    return { ...d, entry_id: d.entry_id, deduction_year: d.deduction_year }
}

function toDraft(i: Input): Draft {
    return { ...i }
}

export async function getEntriesWithoutDonationDeduction(
    entry_id: string | number | null,
) {
    const params = new URLSearchParams();

    if (entry_id !== null) {
        params.set("entry_id", String(entry_id));
    }

    const query = params.toString();
    const url = `${BASE_URL}/entry${query ? `?${query}` : ""}`;

    console.log(url)

    const records = await knockApi<EntrySchema[]>(url) ?? [];
    return records;
}

export function create(deduction: Draft) {
    return knockApi<View>(BASE_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(toInput(deduction)),
    })
}

export async function update(deduction: Draft, id: string) {
    await knockApi(
        `${BASE_URL}/${id}`,
        {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(toInput(deduction)),
        },
    );
}

export async function get(id: number | string) {
    const deduction = await knockApi<Input>(`${BASE_URL}/${id}`)

    return deduction ? toDraft(deduction) : null
}


export async function remove(id: number | string) {
    return await knockApiNoContent(
        `${BASE_URL}/${id}`,
        {
            method: "DELETE",
        },
    );
}