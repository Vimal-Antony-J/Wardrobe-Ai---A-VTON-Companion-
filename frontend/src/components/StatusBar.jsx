import { useEffect, useState } from 'react'
import { checkHealth } from '../api/tryon.js'

const POLL_INTERVAL_MS = 10000

export default function StatusBar() {
  const [health, setHealth] = useState({ status: 'checking', device: '—', model_loaded: false })

  useEffect(() => {
    let cancelled = false
    let timer

    const poll = async () => {
      try {
        const data = await checkHealth()
        if (!cancelled) setHealth(data)
      } catch {
        if (!cancelled) setHealth({ status: 'unreachable', device: '—', model_loaded: false })
      } finally {
        if (!cancelled) timer = setTimeout(poll, POLL_INTERVAL_MS)
      }
    }

    poll()

    return () => {
      cancelled = true
      clearTimeout(timer)
    }
  }, [])

  const tone = health.status === 'ok' ? 'ok' : health.status === 'loading' ? 'loading' : 'error'

  ///return (
    //<div className={`status-pill status-pill--${tone}`} role="status">
      //<span className="status-pill__dot" aria-hidden="true" />
      //{health.status === 'ok' && `Model ready · ${health.device}`}
      //{health.status === 'loading' && 'Model loading…'}
      //{health.status === 'checking' && 'Checking backend…'}
      //{health.status === 'unreachable' && 'Backend unreachable'}
    //</div>
  //)
}
