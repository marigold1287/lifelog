import type { Publisher } from "@/types/book"

export const customFilter = (
    value: unknown,
    query: string,
    item?: any,
) => {
    if (!item) return false

    const publisher = item.raw as Publisher

    const text = [
        publisher.id,
        publisher.name,
        publisher.yomigana,
        ...publisher.alias_records.map(record => record.alias),
    ]
    .filter(value => value != null)
    .join(" ")

    return text.toLowerCase().includes(query.toLowerCase())
}