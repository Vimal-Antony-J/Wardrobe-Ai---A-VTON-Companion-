import CategorySelector from './components/CategorySelector.jsx'
import DropZone from './components/DropZone.jsx'
import ResultTag from './components/ResultTag.jsx'
import StatusBar from './components/StatusBar.jsx'
import { useTryOn } from './hooks/useTryOn.js'

export default function App() {
  const {
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
  } = useTryOn()

  const resultImageUrl = result ? `data:image/png;base64,${result.image_base64}` : null

  const handleDownload = () => {
    if (!resultImageUrl) return
    const a = document.createElement('a')
    a.href = resultImageUrl
    a.download = `tryon-${category}-${Date.now()}.png`
    a.click()
  }

  return (
    <div className="app-shell">
      <header className="header">
        <div>
          <span className="header__eyebrow"> WARDROBE AI </span>
          <h1 className="header__title">Your's AI Companion for Outfits</h1>
        </div>
        <StatusBar />
      </header>

      <main className="workbench">
        <section className="workbench__inputs">
          <DropZone
            index="01"
            title="Person"
            hint="Drop a full-body photo, or click to browse"
            file={personFile}
            previewUrl={personPreview}
            onFile={setPersonFile}
            disabled={status === 'loading'}
          />
          <DropZone
            index="02"
            title="Garment"
            hint="Drop a worn or flat-lay garment photo"
            file={garmentFile}
            previewUrl={garmentPreview}
            onFile={setGarmentFile}
            disabled={status === 'loading'}
          />
        </section>

        <section className="workbench__controls">
          <CategorySelector value={category} onChange={setCategory} disabled={status === 'loading'} />

          <div className="workbench__actions">
            <button type="button" className="generate-btn" onClick={submit} disabled={!canSubmit}>
              {status === 'loading' ? 'Stitching…' : 'Generate try-on'}
            </button>

            {(personFile || garmentFile || result) && (
              <button
                type="button"
                className="reset-btn"
                onClick={reset}
                disabled={status === 'loading'}
              >
                Start over
              </button>
            )}
          </div>
        </section>

        {error && (
          <div className="error-banner" role="alert">
            <strong>Generation failed.</strong> {error}
          </div>
        )}

        {status === 'loading' && (
          <p className="loading-note" role="status">
            Running pose detection and garment transfer — this can take a few seconds.
          </p>
        )}

        <ResultTag
          imageUrl={resultImageUrl}
          category={result?.category}
          elapsedSeconds={result?.processing_time_seconds}
          onDownload={handleDownload}
        />
      </main>
    </div>
  )
}
