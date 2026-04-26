import { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext(null)

const API = import.meta.env.VITE_API_URL || ''

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => { checkAuth() }, [])

  async function checkAuth() {
    try {
      const r = await fetch(`${API}/api/me`, { credentials: 'include' })
      const d = await r.json()
      setUser(d.authenticated ? d.user : null)
    } catch { setUser(null) }
    finally { setLoading(false) }
  }

  async function login(email, password) {
    try {
      const r = await fetch(`${API}/login`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
      const d = await r.json()
      if (d.success) { setUser(d.user); return { success: true } }
      return { success: false, error: d.error }
    } catch { return { success: false, error: 'Network error' } }
  }

  async function register(username, email, password) {
    try {
      const r = await fetch(`${API}/register`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password })
      })
      const d = await r.json()
      return d.success ? { success: true } : { success: false, error: d.error }
    } catch { return { success: false, error: 'Network error' } }
  }

  async function logout() {
    try {
      await fetch(`${API}/logout`, { method: 'POST', credentials: 'include' })
    } catch {}
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {!loading && children}
    </AuthContext.Provider>
  )
}

export function useAuth() { return useContext(AuthContext) }
