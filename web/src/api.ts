export interface HealthResponse {
  status: string
  [key: string]: unknown
}

const API_BASE = import.meta.env.VITE_API_BASE ?? '/api'

export const fetchHealth = async (): Promise<HealthResponse> => {
  const response = await fetch(`${API_BASE}/health`)

  if (!response.ok) {
    throw new Error(`API responded with ${response.status}`)
  }

  return response.json() as Promise<HealthResponse>
}
