import { useCallback, useEffect, useState } from 'react'
import { runTryOn } from '../api/tryon.js'

function useObjectUrl(file) {
  const [url, setUrl] = useState(null)

  useEffect(() => {
    if (!file) {
      setUrl(null)
      return undefined
    }
    const objectUrl = URL.createObjectURL(file)
    setUrl(objectUrl)
    return () => URL.revokeObjectURL(objectUrl)
  }, [file])

  return url
}

export function useTryOn() {
  const [personFile, setPersonFile] = useState(null)
  const [garmentFile, setGarmentFile] = useState(null)
  const [category, setCategory] = useState('tops')
  const [status, setStatus] = useState('idle') // idle | loading | success | error
  const [result, setResult] = useState(null) // { image_base64, category, processing_time_seconds }
  const [error, setError] = useState(null)

  const personPreview = useObjectUrl(personFile)
  const garmentPreview = useObjectUrl(garmentFile)

  const canSubmit = Boolean(personFile && garmentFile && category) && status !== 'loading'

  const submit = useCallback(async () => {
    if (!personFile || !garmentFile) return
    setStatus('loading')
    setError(null)
    try {
      const data = await runTryOn({ personFile, garmentFile, category })
      setResult(data)
      setStatus('success')
    } catch (err) {
      setError(err.message || 'Something went wrong')
      setStatus('error')
    }
  }, [personFile, garmentFile, category])

  const reset = useCallback(() => {
    setPersonFile(null)
    setGarmentFile(null)
    setResult(null)
    setError(null)
    setStatus('idle')
  }, [])

  return {
    personFile,
    setPersonFile,
    personPreview,
    garmentFile,
    setGarmentFile,
    garmentPreview,
    category,
    setCategory,
    status,
    result,
    error,
    canSubmit,
    submit,
    reset,
  }
}
