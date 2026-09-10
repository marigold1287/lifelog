import type { Author } from "@/types/book"

export const customFilter = (
    value: unknown,
    query: string,
    item?: any,
) => {
    if (!item) return false

    const author = item.raw as Author

    const text = [
        author.id,
        author.name,
        author.yomigana,
        author.note,
        ...author.alias_records.map(record => record.alias),
    ]
    .filter(value => value != null)
    .join(" ")

    return text.toLowerCase().includes(query.toLowerCase())
}