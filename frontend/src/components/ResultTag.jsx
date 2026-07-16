export default function ResultTag({ imageUrl, category, elapsedSeconds, onDownload }) {
  if (!imageUrl) return null

  return (
    <div className="result-tag">
      <span className="result-tag__hole" aria-hidden="true" />
      <img className="result-tag__image" src={imageUrl} alt="Generated try-on result" />
      <div className="result-tag__meta">
        <span>CATEGORY: {category?.toUpperCase()}</span>
        <span>RENDER TIME: {elapsedSeconds}s</span>
      </div>
      <button type="button" className="result-tag__download" onClick={onDownload}>
        Download image
      </button>
    </div>
  )
}
