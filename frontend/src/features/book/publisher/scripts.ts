import type { PublisherView } from "./types"

export function generateSearchText(publisher: PublisherView) {
    return [
        publisher.name,
        publisher.yomigana,
        ...publisher.alias_records.map(record => record.alias),
    ]
    .filter(value => value != null)
    .join(" ")
}

export function generatePublisherMap(publishers: PublisherView[]) {
    return new Map(publishers.map(publisher => [publisher.id, publisher]))
}

export const customFilter = (
    value: unknown,
    query: string,
    item?: any,
) => {
    if (!item) return false

    const publisher = item.raw as PublisherView

    const text = generateSearchText(publisher)

    return text.toLowerCase().includes(query.toLowerCase())
}