type APIErrorResponse = {
  code: string;
  message: string;
};

export class CustomApiError extends Error {
  code: string;

  constructor(data: APIErrorResponse) {
    super(data.message);
    this.name = "CustomApiError";
    this.code = data.code;
  }
}

async function request(
    url: string,
    options?: RequestInit,
): Promise<Response> {
    const response = await fetch(url, options)

    if (!response.ok) {
        let errorData: APIErrorResponse

        try {
            errorData = await response.json()
        } catch {
            errorData = {
                code: "unknown_error",
                message: `HTTPエラーが発生いたしました (${response.status})`,
            }
        }

        throw new CustomApiError(errorData)
    }

    return response
}

export async function knockApi<T>(
    url: string,
    options?: RequestInit,
): Promise<T> {
    const response = await request(url, options)

    return response.json() as Promise<T>
}

export async function knockApiNoContent(
    url: string,
    options?: RequestInit,
): Promise<void> {
    await request(url, options)
}

export function formatDate(date: Date): string {
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, "0")
    const day = String(date.getDate()).padStart(2, "0")

    return `${year}-${month}-${day}`
}

export function parseDate(value: string): Date {
    const [year, month, day] = value.split("-").map(Number)

    if (typeof year !== "number" || typeof month !== "number" || typeof day !== "number") {
        throw Error("無効なフォーマットです。YYYY-MM-DDで入力してください")
    }

    return new Date(year, month - 1, day)
}

export function getErrorMessage(error: unknown): string {
    if (error instanceof CustomApiError) {
        return error.message
    }

    if (error instanceof Error) {
        return error.message
    }

    return "予期しないエラーが発生いたしました"
}