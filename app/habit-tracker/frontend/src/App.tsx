import { useCallback, useEffect, useState } from 'react'
import './App.css'
import { ApiError, fetchServiceStatus, type ServiceStatus } from './api'

type LoadState =
  | { phase: 'loading' }
  | { phase: 'ready'; service: ServiceStatus }
  | { phase: 'error'; message: string }

function App() {
  const [state, setState] = useState<LoadState>({ phase: 'loading' })

  // Does not set the loading state itself: on mount that is already the initial
  // state, and setting it synchronously from the effect forces a second render.
  const load = useCallback(async () => {
    try {
      const service = await fetchServiceStatus()
      setState({ phase: 'ready', service })
    } catch (error) {
      const message =
        error instanceof ApiError ? error.message : 'An unexpected error occurred.'
      setState({ phase: 'error', message })
    }
  }, [])

  // Fetching from the API on mount is synchronisation with an external system,
  // which is what effects are for. The rule's alternatives - deriving during
  // render or initialising state directly - cannot apply to a server response.
  useEffect(() => {
    // oxlint-disable-next-line react/set-state-in-effect
    void load()
  }, [load])

  const retry = useCallback(() => {
    setState({ phase: 'loading' })
    void load()
  }, [load])

  return (
    <main className="app">
      <header className="header">
        <h1>Habit Tracker</h1>
        <p className="tagline">Build streaks. Earn points. Collect badges.</p>
      </header>

      <section className="panel" aria-live="polite">
        <h2>Backend status</h2>

        {state.phase === 'loading' && <p className="muted">Checking the API…</p>}

        {state.phase === 'error' && (
          <div className="error" role="alert">
            <p>{state.message}</p>
            <button type="button" onClick={retry}>
              Retry
            </button>
          </div>
        )}

        {state.phase === 'ready' && (
          <dl className="status">
            <dt>Service</dt>
            <dd>{state.service.service}</dd>
            <dt>Status</dt>
            <dd>{state.service.status}</dd>
            <dt>Environment</dt>
            <dd>{state.service.environment}</dd>
          </dl>
        )}
      </section>

      <p className="muted note">
        This is the application shell. Habit management, completions, streaks,
        points, and badges are not implemented yet.
      </p>
    </main>
  )
}

export default App
