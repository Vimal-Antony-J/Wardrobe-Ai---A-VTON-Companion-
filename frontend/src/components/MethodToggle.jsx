export default function MethodToggle({ value, onChange, disabled, showOverlayHint }) {
  return (
    <fieldset className="method-toggle" disabled={disabled}>
      <legend className="category-selector__legend">Generation method</legend>
      <div className="category-selector__options">
        <label className={`category-pill ${value === 'ai' ? 'is-active' : ''}`}>
          <input
            type="radio"
            name="method"
            value="ai"
            checked={value === 'ai'}
            onChange={() => onChange('ai')}
          />
          AI model
        </label>
        <label className={`category-pill ${value === 'classical-overlay' ? 'is-active' : ''}`}>
          <input
            type="radio"
            name="method"
            value="classical-overlay"
            checked={value === 'classical-overlay'}
            onChange={() => onChange('classical-overlay')}
          />
          Classical overlay
        </label>
      </div>
      {showOverlayHint && value === 'ai' && (
        <p className="method-toggle__hint">
          Draped garments (sarees, dupattas) tend to come out as an unrelated Western
          silhouette with the AI model - try classical overlay instead.
        </p>
      )}
      {value === 'classical-overlay' && (
        <p className="method-toggle__hint">
          Pose-warps the garment onto the body directly - preserves the garment's shape,
          but looks like a fitted decal rather than a photoreal render.
        </p>
      )}
    </fieldset>
  )
}
