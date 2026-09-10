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

export async function knockApi<T = any>(url: string, options?: RequestInit): Promise<T | undefined> {
    const response = await fetch(url, options);

    // 正常系ハンドリング
    if (response.ok) {
        if (response.status === 204) {
            return undefined as T;
        }

        // ボディが存在する場合のみ JSON パースを行う
        const text = await response.text();
        return text ? (JSON.parse(text) as T) : (undefined as T);
    }

    // 異常系ハンドリング（エラーレスポンスの JSON パース）
    let errorData: APIErrorResponse;
    try {
        errorData = await response.json();
    } catch {
        errorData = {
            code: "unknown_error",
            message: `HTTPエラーが発生いたしました (${response.status})`,
        };
    }

    throw new CustomApiError(
        errorData
    );

}