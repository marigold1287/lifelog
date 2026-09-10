
export async function validateStringEntered(value: string) {
    if (!value) return "入力してください"
    if (!value.trim()) return "空白のみの入力値は許可されません"

    return true
}

