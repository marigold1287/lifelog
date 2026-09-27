export function getId(value: string | string[] | undefined): number {
    const id = Number(value)

    if (!Number.isInteger(id)) {
        throw new Error("不正なIDです")
    }

    return id
}