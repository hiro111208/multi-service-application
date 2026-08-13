import { render, screen, waitFor } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import App from './App'
import * as api from './api'

describe('App', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('shows API health data when the request succeeds', async () => {
    vi.spyOn(api, 'fetchHealth').mockResolvedValue({ status: 'ok' })

    render(<App />)

    expect(screen.getByText('Checking API status…')).toBeInTheDocument()

    await waitFor(() => {
      expect(screen.getByText('API is reachable.')).toBeInTheDocument()
    })

    expect(screen.getByText(/"status": "ok"/)).toBeInTheDocument()
  })

  it('shows an error message when the API request fails', async () => {
    vi.spyOn(api, 'fetchHealth').mockRejectedValue(new Error('Network error'))

    render(<App />)

    await waitFor(() => {
      expect(screen.getByText('Could not reach the API.')).toBeInTheDocument()
    })

    expect(screen.getByText('Network error')).toBeInTheDocument()
  })
})
