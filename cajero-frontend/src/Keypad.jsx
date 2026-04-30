import './Keypad.css'

const KEYS = [
  { label: '1', value: '1' },
  { label: '2', value: '2' },
  { label: '3', value: '3' },
  { label: '4', value: '4' },
  { label: '5', value: '5' },
  { label: '6', value: '6' },
  { label: '7', value: '7' },
  { label: '8', value: '8' },
  { label: '9', value: '9' },
  { label: 'Borrar', value: 'clear', kind: 'clear' },
  { label: '0', value: '0' },
  { label: 'Confirmar', value: 'enter', kind: 'enter' },
]

function Keypad({ onKeyPress }) {
  const handleClick = (keyValue) => {
    if (typeof onKeyPress === 'function') {
      onKeyPress(keyValue)
    }
  }

  return (
    <div className="atm-keypad" role="group" aria-label="Teclado numérico">
      {KEYS.map((key) => (
        <button
          key={key.value}
          type="button"
          className={`atm-key ${key.kind ? `atm-key--${key.kind}` : ''}`.trim()}
          onClick={() => handleClick(key.value)}
          aria-label={key.label}
        >
          <span>{key.label}</span>
        </button>
      ))}
    </div>
  )
}

export default Keypad