import type { View, Input, Response } from "./types"
import { knockApi, parseDate, formatDate, knockApiNoContent } from "@/api"

const BASE_URL = "/api/payslip"

function toInput(payslip: Response): Input {
    return {
        ...payslip,
        date: parseDate(payslip.date),
    }
}

function toResponse(payslip: Input): Response {
    return {
        ...payslip,
        date: formatDate(payslip.date),
    }
}

export async function getList(): Promise<View[]> {
    return await knockApi<View[]>(BASE_URL) ?? []
}

export async function getLatest(): Promise<Input | null> {
    const payslip = await knockApi<Response>(`${BASE_URL}/latest`) ?? []

    return payslip ? toInput(payslip) : null

}

export function create(payslip: Input) {
    return knockApi<View>(BASE_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(toResponse(payslip)),
    })
}

export async function update(payslip: Input, id: string) {
    await knockApi(
        `${BASE_URL}/${id}`,
        {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(toResponse(payslip)),
        },
    );
}

export async function get(id: number | string) {
    const payslip = await knockApi<Response>(`${BASE_URL}/${id}`)

    return payslip ? toInput(payslip) : null
}


export async function remove(id: number | string) {
    return await knockApiNoContent(
        `${BASE_URL}/${id}`,
        {
            method: "DELETE",
        },
    );
}