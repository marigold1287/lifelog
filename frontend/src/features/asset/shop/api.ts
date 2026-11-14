import type { ShopView } from "./types"
import { knockApi } from "@/api"

const baseUrl = "/api/shop"


export async function getList(): Promise<ShopView[]> {
    return await knockApi(baseUrl)
}

export async function getNameList(): Promise<string[]> {
    return await knockApi(`${baseUrl}/name`)
}