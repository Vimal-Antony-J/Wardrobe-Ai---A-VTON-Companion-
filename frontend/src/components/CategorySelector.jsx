const CATEGORIES = [
  { value: 'tops', label: 'Tops' },
  { value: 'bottoms', label: 'Bottoms' },
  { value: 'one-pieces', label: 'One-Pieces' },
]

export default function CategorySelector({ value, onChange, disabled }) {
  return (
    <fieldset className="category-selector" disabled={disabled}>
      <legend className="category-selector__legend">Garment category</legend>
      <div className="category-selector__options">
        {CATEGORIES.map((c) => (
          <label key={c.value} className={`category-pill ${value === c.value ? 'is-active' : ''}`}>
            <input
              type="radio"
              name="category"
              value={c.value}
              checked={value === c.value}
              onChange={() => onChange(c.value)}
            />
            {c.label}
          </label>
        ))}
      </div>
    </fieldset>
  )
}
