import type { AuthorView } from "./types"

export function generateSearchText(author: AuthorView) {
    return [
        author.name,
        author.yomigana,
        ...author.alias_records.map(record => record.alias),
    ]
    .filter(value => value != null)
    .join(" ")
}

export function generateAuthorMap(authors: AuthorView[]) {
    return new Map(authors.map(author => [author.id, author]))
}

export const customFilter = (
    value: unknown,
    query: string,
    item?: any,
) => {
    if (!item) return false

    const author = item.raw as AuthorView

    const text = generateSearchText(author)

    return text.toLowerCase().includes(query.toLowerCase())
}