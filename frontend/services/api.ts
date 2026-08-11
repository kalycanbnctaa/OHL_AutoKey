const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function request<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new ApiError(`Request failed: ${path}`, response.status);
  }

  return (await response.json()) as T;
}

export const api = {
  get: <T>(path: string, signal?: AbortSignal, headers?: HeadersInit) =>
    request<T>(path, { method: "GET", signal, headers }),
  post: <T>(
    path: string,
    body: unknown,
    signal?: AbortSignal,
    headers?: HeadersInit,
  ) =>
    request<T>(path, {
      method: "POST",
      body: JSON.stringify(body),
      signal,
      headers,
    }),
};

export { API_URL };