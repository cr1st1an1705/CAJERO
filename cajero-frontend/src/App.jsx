import { useState } from 'react'
import Keypad from './Keypad'
import './App.css'

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '')
const ATM_ORIGEN = 'ATM-LOCAL'
const MIN_WITHDRAWAL_PROCESSING_MS = 1500

const VIEWS = {
  WELCOME: 'WELCOME',
  PIN: 'PIN',
  ACCOUNT_SELECT: 'ACCOUNT_SELECT',
  MENU: 'MENU',
  WITHDRAW: 'WITHDRAW',
  BALANCE: 'BALANCE',
  SUCCESS: 'SUCCESS',
}

async function apiRequest(path, { method = 'GET', token, body } = {}) {
  const headers = {}

  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  if (body) {
    headers['Content-Type'] = 'application/json'
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  })

  let payload = null
  try {
    payload = await response.json()
  } catch {
    payload = null
  }

  if (!response.ok) {
    const detail = payload?.detail || payload?.mensaje || 'Error al comunicarse con el backend'
    throw new Error(detail)
  }

  return payload
}

function WelcomeScreen({ accountNumber, onChangeAccount, onInsertCard, status }) {
  return (
    <div className="screen">
      <h1>Cajero Automático</h1>
      <p className="screen-subtitle">Ingresa tu número de cuenta para comenzar</p>
      <label htmlFor="numero-cuenta" className="atm-screen__label">Número de cuenta</label>
      <input
        id="numero-cuenta"
        className="screen-input"
        type="text"
        inputMode="numeric"
        placeholder="Ej. 12345"
        value={accountNumber}
        onChange={(event) => onChangeAccount(event.target.value.replace(/\D/g, ''))}
      />
      {status ? <p className="screen-status">{status}</p> : null}
      <button
        type="button"
        className="screen-action"
        onClick={onInsertCard}
      >
        Insertar tarjeta
      </button>
    </div>
  )
}

function PinScreen({ pin, status, isError, onPinInput, onCancel, isLoading }) {
  const maskedPin = pin.replace(/./g, '•')

  return (
    <div className="screen screen--fade-in">
      <h1>Verificación de PIN</h1>
      <p className="screen-subtitle">Digita tu clave para continuar</p>
      <div className={`atm-screen ${isError ? 'atm-screen--error' : ''}`} aria-live="polite" aria-atomic="true">
        <span className="atm-screen__label">PIN</span>
        <output className="atm-screen__value">{maskedPin || '----'}</output>
        <p className={`atm-screen__status ${isError ? 'atm-screen__status--error' : ''}`}>{status}</p>
      </div>
      {!isLoading ? <Keypad onKeyPress={onPinInput} /> : null}
      <button type="button" className="screen-action screen-action--secondary" onClick={onCancel}>
        Cancelar
      </button>
    </div>
  )
}

function AccountSelectionScreen({ userName, accountNumber, tipoCuenta, onSelectSavings, onSelectChecking, onLogout, isLoading }) {
  const isSavings = tipoCuenta === 'AHORRO'
  const isChecking = tipoCuenta === 'MONETARIA'
  const [noAccessMsg, setNoAccessMsg] = useState('')

  const handleSavings = () => {
    if (!isSavings) {
      setNoAccessMsg('No cuentas con una cuenta de ahorro asociada a esta tarjeta.')
    } else {
      onSelectSavings()
    }
  }

  const handleChecking = () => {
    if (!isChecking) {
      setNoAccessMsg('No cuentas con una cuenta monetaria asociada a esta tarjeta.')
    } else {
      onSelectChecking()
    }
  }

  return (
    <div className="screen screen--centered">
      <h1>Bienvenido</h1>
      <p className="welcome-name">{userName}</p>
      <p className="screen-subtitle">Cuenta principal: {accountNumber}</p>
      <div className="menu-actions menu-actions--account-types" role="group" aria-label="Tipos de cuenta">
        <button
          type="button"
          className={`screen-action screen-action--account${!isSavings ? ' screen-action--disabled-look' : ''}`}
          onClick={handleSavings}
          disabled={isLoading}
        >
          <span>Cuenta de ahorro</span>
        </button>
        <button
          type="button"
          className={`screen-action screen-action--account${!isChecking ? ' screen-action--disabled-look' : ''}`}
          onClick={handleChecking}
          disabled={isLoading}
        >
          <span>Cuenta monetaria</span>
        </button>
      </div>
      <button type="button" className="screen-action screen-action--secondary" onClick={onLogout} disabled={isLoading}>
        Cerrar sesión
      </button>

      {noAccessMsg && (
        <section className="modal-backdrop" role="dialog" aria-modal="true" aria-labelledby="no-acceso-titulo">
          <div className="modal-card">
            <h2 id="no-acceso-titulo">Acceso no permitido</h2>
            <p style={{ textAlign: 'center', margin: '0.5rem 0 1rem' }}>{noAccessMsg}</p>
            <div className="modal-actions">
              <button type="button" className="screen-action" onClick={() => setNoAccessMsg('')}>
                Aceptar
              </button>
            </div>
          </div>
        </section>
      )}
    </div>
  )
}

function MenuScreen({ accountTypeLabel, onGoToWithdraw, onGoToBalance, onBack, onLogout, isLoading }) {
  return (
    <div className="screen">
      <h1>{accountTypeLabel}</h1>
      <p className="screen-subtitle">Selecciona una operación</p>
      <div className="menu-actions" role="group" aria-label="Operaciones disponibles">
        <button type="button" className="screen-action" onClick={onGoToWithdraw} disabled={isLoading}>
          Retirar efectivo
        </button>
        <button type="button" className="screen-action" onClick={onGoToBalance} disabled={isLoading}>
          Consultar saldo
        </button>
      </div>
      <div className="menu-footer-actions">
        <button type="button" className="screen-action screen-action--secondary" onClick={onLogout} disabled={isLoading}>
          Cerrar sesión
        </button>
        <button type="button" className="screen-action screen-action--secondary" onClick={onBack} disabled={isLoading}>
          Regresar
        </button>
      </div>
    </div>
  )
}

function WithdrawScreen({ balance, onWithdraw, onBack, isLoading }) {
  const options = [50, 100, 200, 300, 500, 1000, 1500, 2000]
  const [customAmount, setCustomAmount] = useState('')
  const [customAmountError, setCustomAmountError] = useState('')
  const [insufficientFundsMessage, setInsufficientFundsMessage] = useState('')

  const openInsufficientFundsModal = () => {
    setInsufficientFundsMessage('Favor consultar saldo.')
  }

  const closeInsufficientFundsModal = () => {
    setInsufficientFundsMessage('')
  }

  const handleQuickWithdrawal = (amount) => {
    if (amount > balance) {
      openInsufficientFundsModal()
      return
    }

    onWithdraw(amount)
  }

  const handleCustomWithdrawal = () => {
    const amount = Number(customAmount)

    if (!Number.isInteger(amount) || amount <= 0) {
      setCustomAmountError('Ingresa un monto entero mayor que cero')
      return
    }

    if (amount % 50 !== 0) {
      setCustomAmountError('El monto debe ser multiplo de Q50')
      return
    }

    if (amount > balance) {
      openInsufficientFundsModal()
      return
    }

    setCustomAmountError('')
    onWithdraw(amount)
  }

  return (
    <div className="screen">
      <h1>Retiro</h1>
      <p className="screen-subtitle">Saldo disponible: Q{balance.toFixed(2)}</p>
      <div className="menu-actions" role="group" aria-label="Montos de retiro">
        {options.map((amount) => (
          <button
            key={amount}
            type="button"
            className="screen-action"
            disabled={isLoading}
            onClick={() => handleQuickWithdrawal(amount)}
          >
            Q{amount}
          </button>
        ))}
      </div>
      <label htmlFor="monto-variable" className="atm-screen__label">Monto variable</label>
      <input
        id="monto-variable"
        className="screen-input"
        type="text"
        inputMode="numeric"
        placeholder="Ej. 250"
        value={customAmount}
        onChange={(event) => {
          setCustomAmount(event.target.value.replace(/\D/g, ''))
          setCustomAmountError('')
        }}
      />
      {customAmountError ? <p className="screen-status">{customAmountError}</p> : null}
      <button
        type="button"
        className="screen-action"
        disabled={isLoading || !customAmount}
        onClick={handleCustomWithdrawal}
      >
        Retirar monto ingresado
      </button>
      <button type="button" className="screen-action screen-action--secondary" onClick={onBack}>
        Volver al menú
      </button>

      {insufficientFundsMessage ? (
        <section className="modal-backdrop" role="dialog" aria-modal="true" aria-labelledby="saldo-insuficiente-titulo">
          <div className="modal-card modal-card--centered">
            <h2 id="saldo-insuficiente-titulo">Saldo insuficiente</h2>
            <p>{insufficientFundsMessage}</p>
            <div className="modal-actions">
              <button type="button" className="screen-action" onClick={closeInsufficientFundsModal}>
                Aceptar
              </button>
            </div>
          </div>
        </section>
      ) : null}
    </div>
  )
}

function BalanceScreen({ accountNumber, accountTypeLabel, balance, nodoBd, onBack }) {
  return (
    <div className="screen">
      <h1>Consulta de saldo</h1>
      <p className="screen-subtitle">Cuenta: {accountNumber}</p>
      <p className="screen-subtitle">Tipo: {accountTypeLabel}</p>
      <div className="atm-screen" aria-live="polite" aria-atomic="true">
        <span className="atm-screen__label">Saldo actual</span>
        <output className="atm-screen__value">Q{balance.toFixed(2)}</output>
        {/* <p className="atm-screen__status">Nodo BD: {nodoBd || 'desconocido'}</p> */}
      </div>
      <button type="button" className="screen-action" onClick={onBack}>
        Volver al menú
      </button>
    </div>
  )
}

function SuccessScreen({ message, onMenu }) {
  return (
    <div className="screen">
      <h1>Operación exitosa</h1>
      <p className="screen-subtitle">{message}</p>
      <button type="button" className="screen-action" onClick={onMenu}>
        Regresar al menú
      </button>
    </div>
  )
}

function App() {
  const [currentView, setCurrentView] = useState(VIEWS.WELCOME)
  const [accountNumber, setAccountNumber] = useState('')
  const [activeAccountNumber, setActiveAccountNumber] = useState('')
  const [userName, setUserName] = useState('')
  const [tipoCuenta, setTipoCuenta] = useState('')
  const [selectedAccountType, setSelectedAccountType] = useState('')
  const [pin, setPin] = useState('')
  const [pinStatus, setPinStatus] = useState('Ingresa tu PIN')
  const [welcomeStatus, setWelcomeStatus] = useState('')
  const [isPinError, setIsPinError] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [token, setToken] = useState('')
  const [balance, setBalance] = useState(0)
  const [nodoBd, setNodoBd] = useState('')
  const [lastActionMessage, setLastActionMessage] = useState('')
  const [pendingWithdrawalAmount, setPendingWithdrawalAmount] = useState(null)
  const [isProcessingWithdrawal, setIsProcessingWithdrawal] = useState(false)
  const [isCashReadyModalOpen, setIsCashReadyModalOpen] = useState(false)

  const resetSession = () => {
    setActiveAccountNumber('')
    setUserName('')
    setTipoCuenta('')
    setSelectedAccountType('')
    setPin('')
    setPinStatus('Ingresa tu PIN')
    setIsPinError(false)
    setToken('')
    setBalance(0)
    setNodoBd('')
    setLastActionMessage('')
    setPendingWithdrawalAmount(null)
    setIsProcessingWithdrawal(false)
    setIsCashReadyModalOpen(false)
  }

  const handleInsertCard = () => {
    const sanitizedAccount = accountNumber.trim()

    if (sanitizedAccount.length < 5) {
      setWelcomeStatus('El número de cuenta debe tener al menos 5 dígitos')
      return
    }

    setActiveAccountNumber(sanitizedAccount)
    setAccountNumber('')
    setWelcomeStatus('')
    setPin('')
    setPinStatus('Ingresa tu PIN')
    setIsPinError(false)
    setCurrentView(VIEWS.PIN)
  }

  const fetchBalance = async (authToken, nextView = VIEWS.BALANCE) => {
    const data = await apiRequest('/api/atm/saldo', {
      method: 'GET',
      token: authToken,
    })
    setBalance(Number(data.saldo))
    setNodoBd(data.nodo_bd)
    setCurrentView(nextView)
  }

  const handleLogin = async () => {
    if (!activeAccountNumber) {
      setPin('')
      setPinStatus('Vuelve a ingresar el número de cuenta')
      setIsPinError(true)
      setCurrentView(VIEWS.WELCOME)
      return
    }

    if (pin.length !== 4) {
      setPinStatus('El PIN debe tener 4 dígitos')
      setIsPinError(true)
      return
    }

    setIsLoading(true)
    setPinStatus('Validando credenciales...')
    setIsPinError(false)

    try {
      const loginData = await apiRequest('/api/auth/login', {
        method: 'POST',
        body: {
          numero_cuenta: activeAccountNumber,
          pin,
          atm_origen: ATM_ORIGEN,
        },
      })

      setToken(loginData.access_token)
      setUserName(loginData.titular_nombre)
      setTipoCuenta(loginData.tipo_cuenta || 'AHORRO')
      setPin('')
      setPinStatus('PIN correcto')
      setCurrentView(VIEWS.ACCOUNT_SELECT)
    } catch (error) {
      setPin('')
      setIsPinError(true)
      setPinStatus(error.message)
    } finally {
      setIsLoading(false)
    }
  }

  const handlePinInput = (key) => {
    if (isLoading) return

    if (key === 'clear') {
      setPin((current) => current.slice(0, -1))
      setPinStatus('Se borró un dígito')
      setIsPinError(false)
      return
    }

    if (key === 'enter') {
      handleLogin()
      return
    }

    setPin((current) => {
      if (current.length >= 4) {
        setPinStatus('PIN completo, presiona Confirmar')
        return current
      }
      setPinStatus('Capturando PIN...')
      setIsPinError(false)
      return `${current}${key}`
    })
  }

  const handleGoToBalance = async () => {
    if (!token) return

    setIsLoading(true)
    try {
      await fetchBalance(token, VIEWS.BALANCE)
    } catch (error) {
      setLastActionMessage(error.message)
      setCurrentView(VIEWS.SUCCESS)
    } finally {
      setIsLoading(false)
    }
  }

  const handleGoToWithdraw = async () => {
    if (!token) return

    setIsLoading(true)
    try {
      await fetchBalance(token, VIEWS.WITHDRAW)
    } catch (error) {
      setLastActionMessage(error.message)
      setCurrentView(VIEWS.SUCCESS)
    } finally {
      setIsLoading(false)
    }
  }

  const handleWithdrawal = async (amount) => {
    if (!token) {
      setLastActionMessage('Sesion expirada. Inicia sesion nuevamente.')
      return { ok: false }
    }

    setIsLoading(true)
    try {
      const data = await apiRequest('/api/atm/retirar', {
        method: 'POST',
        token,
        body: { monto: amount },
      })

      setBalance(Number(data.saldo_nuevo))
      setNodoBd(data.nodo_bd)
      setLastActionMessage(`${data.mensaje}. Retiro: Q${amount}. Saldo nuevo: Q${Number(data.saldo_nuevo).toFixed(2)}`)
      return { ok: true }
    } catch (error) {
      setLastActionMessage(error.message)
      return { ok: false }
    } finally {
      setIsLoading(false)
    }
  }

  const requestWithdrawal = (amount) => {
    if (isLoading) return
    setPendingWithdrawalAmount(amount)
  }

  const cancelWithdrawalConfirmation = () => {
    if (isLoading) return
    setPendingWithdrawalAmount(null)
  }

  const confirmWithdrawal = async () => {
    if (pendingWithdrawalAmount === null) return
    const amountToWithdraw = pendingWithdrawalAmount
    setPendingWithdrawalAmount(null)
    setIsProcessingWithdrawal(true)

    const [withdrawalResult] = await Promise.all([
      handleWithdrawal(amountToWithdraw),
      new Promise((resolve) => setTimeout(resolve, MIN_WITHDRAWAL_PROCESSING_MS)),
    ])

    setIsProcessingWithdrawal(false)

    if (withdrawalResult?.ok) {
      setIsCashReadyModalOpen(true)
      return
    }

    setCurrentView(VIEWS.SUCCESS)
  }

  const closeCashReadyModal = () => {
    if (isLoading) return
    setIsCashReadyModalOpen(false)
    setCurrentView(VIEWS.MENU)
  }

  const handleLogout = async () => {
    setIsLoading(true)
    try {
      if (token) {
        await apiRequest('/api/atm/logout', {
          method: 'POST',
          token,
        })
      }
    } catch {
      // The local session must end even if the backend is unavailable.
    } finally {
      resetSession()
      setCurrentView(VIEWS.WELCOME)
      setIsLoading(false)
    }
  }

  const handleSelectAccountType = (accountType) => {
    setSelectedAccountType(accountType)
    setCurrentView(VIEWS.MENU)
  }

  const accountTypeLabel = selectedAccountType || 'Cuenta seleccionada'

  const renderView = () => {
    switch (currentView) {
      case VIEWS.WELCOME:
        return (
          <WelcomeScreen
            accountNumber={accountNumber}
            onChangeAccount={setAccountNumber}
            onInsertCard={handleInsertCard}
            status={welcomeStatus}
          />
        )
      case VIEWS.PIN:
        return (
          <PinScreen
            pin={pin}
            status={pinStatus}
            isError={isPinError}
            isLoading={isLoading}
            onPinInput={handlePinInput}
            onCancel={() => {
              resetSession()
              setCurrentView(VIEWS.WELCOME)
            }}
          />
        )
      case VIEWS.ACCOUNT_SELECT:
        return (
          <AccountSelectionScreen
            userName={userName}
            accountNumber={activeAccountNumber}
            tipoCuenta={tipoCuenta}
            isLoading={isLoading}
            onSelectSavings={() => handleSelectAccountType('Cuenta de ahorro')}
            onSelectChecking={() => handleSelectAccountType('Cuenta monetaria')}
            onLogout={handleLogout}
          />
        )
      case VIEWS.MENU:
        return (
          <MenuScreen
            accountTypeLabel={accountTypeLabel}
            isLoading={isLoading}
            onGoToWithdraw={handleGoToWithdraw}
            onGoToBalance={handleGoToBalance}
            onBack={() => setCurrentView(VIEWS.ACCOUNT_SELECT)}
            onLogout={handleLogout}
          />
        )
      case VIEWS.WITHDRAW:
        return (
          <WithdrawScreen
            balance={balance}
            isLoading={isLoading}
            onWithdraw={requestWithdrawal}
            onBack={() => setCurrentView(VIEWS.MENU)}
          />
        )
      case VIEWS.BALANCE:
        return (
          <BalanceScreen
            accountNumber={activeAccountNumber}
            accountTypeLabel={accountTypeLabel}
            balance={balance}
            nodoBd={nodoBd}
            onBack={() => setCurrentView(VIEWS.MENU)}
          />
        )
      case VIEWS.SUCCESS:
        return (
          <SuccessScreen
            message={lastActionMessage || 'Operación completada'}
            onMenu={() => setCurrentView(VIEWS.MENU)}
          />
        )
      default:
        return null
    }
  }

  return (
    <main className="atm-demo">
      <section className="atm-panel" aria-label="Cajero automático">
        {renderView()}
      </section>

      {pendingWithdrawalAmount !== null ? (
        <section className="modal-backdrop" role="dialog" aria-modal="true" aria-labelledby="confirmar-retiro-titulo">
          <div className="modal-card">
            <h2 id="confirmar-retiro-titulo">Confirmar retiro</h2>
            <p>¿Es correcto el monto a retirar?</p>
            <p className="modal-amount">Q{pendingWithdrawalAmount}</p>
            <div className="modal-actions">
              <button
                type="button"
                className="screen-action"
                onClick={confirmWithdrawal}
                disabled={isLoading}
              >
                OK
              </button>
              <button
                type="button"
                className="screen-action screen-action--secondary"
                onClick={cancelWithdrawalConfirmation}
                disabled={isLoading}
              >
                Cancelar
              </button>
            </div>
          </div>
        </section>
      ) : null}

      {isProcessingWithdrawal ? (
        <section className="modal-backdrop" role="dialog" aria-modal="true" aria-labelledby="procesando-retiro-titulo">
          <div className="modal-card modal-card--centered">
            <h2 id="procesando-retiro-titulo">Procesando retiro</h2>
            <div className="spinner-balls" aria-hidden="true">
              <span className="spinner-ball" />
              <span className="spinner-ball" />
              <span className="spinner-ball" />
            </div>
            <p className="modal-processing-text">Procesando...</p>
          </div>
        </section>
      ) : null}

      {isCashReadyModalOpen ? (
        <section className="modal-backdrop" role="dialog" aria-modal="true" aria-labelledby="retire-efectivo-titulo">
          <div className="modal-card modal-card--centered">
            <h2 id="retire-efectivo-titulo">Retire su efectivo</h2>
            <p>Tu transaccion fue procesada correctamente.</p>
            <div className="modal-actions">
              <button
                type="button"
                className="screen-action"
                onClick={closeCashReadyModal}
                disabled={isLoading}
              >
                Aceptar
              </button>
            </div>
          </div>
        </section>
      ) : null}
    </main>
  )
}

export default App
