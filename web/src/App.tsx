import { useEffect, useState } from 'react'
import { fetchHealth, type HealthResponse } from './api'
import './App.css'

type LoadStatus = 'loading' | 'success' | 'error'

const App = () => {
  const [status, setStatus] = useState<LoadStatus>('loading')
  const [data, setData] = useState<HealthResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    const loadHealth = async () => {
      try {
        const payload = await fetchHealth()
        if (!cancelled) {
          setData(payload)
          setStatus('success')
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : 'Request failed')
          setStatus('error')
        }
      }
    }

    void loadHealth()

    return () => {
      cancelled = true
    }
  }, [])

  return (
    <main className="app">
      <header>
        <h1>Multi-Service Application</h1>
        <p>React frontend connected to the Flask API through Nginx.</p>
      </header>

      <section className="panel">
        <h2>API Health</h2>

        {status === 'loading' && <p className="muted">Checking API status…</p>}

        {status === 'error' && (
          <div className="alert error">
            <p>Could not reach the API.</p>
            <p className="detail">{error}</p>
          </div>
        )}

        {status === 'success' && data && (
          <div className="alert success">
            <p>API is reachable.</p>
            <pre>{JSON.stringify(data, null, 2)}</pre>
          </div>
        )}

        <button type="button" onClick={() => window.location.reload()}>
          Retry
        </button>
      </section>
    </main>
  )
}

export default App
