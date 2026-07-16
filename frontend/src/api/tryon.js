const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

export async function checkHealth() {
  const res = await fetch(`${API_BASE_URL}/health`)
  if (!res.ok) throw new Error('Health check failed')
  return res.json()
}

export async function runTryOn({ personFile, garmentFile, category }) {
  const form = new FormData()
  form.append('person_image', personFile)
  form.append('garment_image', garmentFile)
  form.append('category', category)

  const res = await fetch(`${API_BASE_URL}/tryon`, {
    method: 'POST',
    body: form,
  })

  const data = await res.json().catch(() => null)

  if (!res.ok) {
    const message = data?.detail || data?.error || `Request failed with status ${res.status}`
    throw new Error(message)
  }

  return data
}
