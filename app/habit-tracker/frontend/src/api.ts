/**
 * Client for the habit tracker backend API.
 *
 * The base URL comes from VITE_API_BASE_URL and defaults to the relative path
 * `/api`, which the development server proxies to the backend and which a
 * reverse proxy serves in deployed environments. No environment-specific value
 * is hardcoded.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api'

export interface ServiceStatus {
  service: string
  status: string
  environment: string
}

/** An API call that failed. `status` is null when the request never completed. */
export class ApiError extends Error {
  readonly status: number | null

  constructor(message: string, status: number | null = null) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

async function request<T>(path: string): Promise<T> {
  let response: Response

  try {
    response = await fetch(`${API_BASE_URL}${path}`)
  } catch {
    throw new ApiError('Cannot reach the API. Check that the backend is running.')
  }

  if (!response.ok) {
    throw new ApiError(
      `The API returned ${response.status} ${response.statusText}.`,
      response.status,
    )
  }

  try {
    return (await response.json()) as T
  } catch {
    throw new ApiError('The API response could not be read as JSON.')
  }
}

export function fetchServiceStatus(): Promise<ServiceStatus> {
  return request<ServiceStatus>('/')
}
