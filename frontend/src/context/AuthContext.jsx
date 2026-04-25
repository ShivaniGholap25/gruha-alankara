import { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../api/client';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  async function checkAuth() {
    try {
      const res = await api.get('/api/me');
      if (res.ok && res.data.authenticated) {
        setUser(res.data.user);
      } else {
        setUser(null);
      }
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  }

  async function login(email, password) {
    const res = await api.post('/login', { email, password });
    if (res.ok && res.data.success) {
      setUser(res.data.user);
      return { success: true };
    }
    return { success: false, error: res.data.error || 'Login failed' };
  }

  async function register(username, email, password) {
    const res = await api.post('/register', { username, email, password });
    if (res.ok && res.data.success) {
      return { success: true };
    }
    return { success: false, error: res.data.error || 'Registration failed' };
  }

  async function logout() {
    await api.post('/logout', {});
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, checkAuth }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
