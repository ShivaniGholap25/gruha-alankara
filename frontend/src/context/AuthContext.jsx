import { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => { checkAuth() }, [])

  async function checkAuth() {
    try {
      const r = await fetch('/api/me', {credentials:'include'})
      const d = await r.json()
      setUser(d.authenticated ? d.user : null)
    } catch { setUser(null) }
    finally { setLoading(false) }
  }

  async function login(email, password) {
    const r = await fetch('/login', {
      method:'POST',
      credentials:'include',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({email, password})
    })
    const d = await r.json()
    if(d.success) { setUser(d.user); return {success:true} }
    return {success:false, error:d.error}
  }

  async function register(username, email, password) {
    const r = await fetch('/register', {
      method:'POST',
      credentials:'include',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({username, email, password})
    })
    const d = await r.json()
    return d.success ? {success:true} : {success:false, error:d.error}
  }

  async function logout() {
    await fetch('/logout', {method:'POST', credentials:'include'})
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{user, loading, login, register, logout}}>
      {!loading && children}
    </AuthContext.Provider>
  )
}

export function useAuth() { return useContext(AuthContext) }