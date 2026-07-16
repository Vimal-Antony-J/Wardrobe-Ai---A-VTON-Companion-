import { useCallback, useId, useRef, useState } from 'react'

export default function DropZone({ index, title, hint, file, previewUrl, onFile, disabled }) {
  const inputRef = useRef(null)
  const [isDragging, setIsDragging] = useState(false)
  const inputId = useId()

  const handleFiles = useCallback(
    (fileList) => {
      const picked = fileList?.[0]
      if (picked && picked.type.startsWith('image/')) {
        onFile(picked)
      }
    },
    [onFile],
  )

  const onDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    if (disabled) return
    handleFiles(e.dataTransfer.files)
  }

  const onKeyDown = (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault()
      inputRef.current?.click()
    }
  }

  return (
    <div className="dropzone-wrap">
      <span className="dropzone__tag">
        {index} · {title.toUpperCase()}
      </span>

      <div
        className={[
          'dropzone',
          isDragging ? 'is-dragging' : '',
          file ? 'is-filled' : '',
          disabled ? 'is-disabled' : '',
        ]
          .filter(Boolean)
          .join(' ')}
        role="button"
        tabIndex={disabled ? -1 : 0}
        aria-label={`Upload ${title.toLowerCase()} photo`}
        onClick={() => !disabled && inputRef.current?.click()}
        onKeyDown={onKeyDown}
        onDragOver={(e) => {
          e.preventDefault()
          if (!disabled) setIsDragging(true)
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={onDrop}
      >
        <span className="dropzone__notch dropzone__notch--tl" aria-hidden="true" />
        <span className="dropzone__notch dropzone__notch--tr" aria-hidden="true" />
        <span className="dropzone__notch dropzone__notch--bl" aria-hidden="true" />
        <span className="dropzone__notch dropzone__notch--br" aria-hidden="true" />

        {previewUrl ? (
          <img className="dropzone__preview" src={previewUrl} alt={`${title} preview`} />
        ) : (
          <div className="dropzone__empty">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path
                d="M12 4v12M6 10l6-6 6 6M4 20h16"
                stroke="currentColor"
                strokeWidth="1.6"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <p className="dropzone__hint">{hint}</p>
          </div>
        )}

        <input
          ref={inputRef}
          id={inputId}
          type="file"
          accept="image/*"
          className="sr-only"
          disabled={disabled}
          onChange={(e) => handleFiles(e.target.files)}
        />
      </div>

      {file && (
        <button
          type="button"
          className="dropzone__clear"
          onClick={() => onFile(null)}
          disabled={disabled}
        >
          Remove photo
        </button>
      )}
    </div>
  )
}
