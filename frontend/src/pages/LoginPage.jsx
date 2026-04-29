import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const G_ICON = (
  <svg width="18" height="18" viewBox="0 0 48 48">
    <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
    <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
    <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
    <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.18 1.48-4.97 2.31-8.16 2.31-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
  </svg>
)

export default function LoginPage() {
  const [email, setEmail]       = useState('')
  const [password, setPassword] = useState('')
  const [error, setError]       = useState('')
  const [loading, setLoading]   = useState(false)
  const { login }  = useAuth()
  const navigate   = useNavigate()

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    const result = await login(email, password)
    if (result.success) { navigate('/') }
    else { setError(result.error || 'Login failed') }
    setLoading(false)
  }

  const card = { background:'#1a1a2e', border:'1px solid #2d3748', borderRadius:'16px', padding:'2.5rem', width:'100%', maxWidth:'420px', boxShadow:'0 25px 50px rgba(0,0,0,0.5)' }
  const inputStyle = { width:'100%', background:'#0d0d1a', border:'1px solid #2d3748', color:'#e2e8f0', borderRadius:'8px', padding:'0.75rem', fontSize:'0.95rem', outline:'none', boxSizing:'border-box' }
  const divider = (label) => (
    <div style={{display:'flex',alignItems:'center',gap:'1rem',margin:'1.25rem 0'}}>
      <div style={{flex:1,height:'1px',background:'#2d3748'}}/>
      <span style={{color:'#475569',fontSize:'0.8rem'}}>{label}</span>
      <div style={{flex:1,height:'1px',background:'#2d3748'}}/>
    </div>
  )

  return (
    <div style={{minHeight:'100vh',display:'flex',alignItems:'center',justifyContent:'center',background:'radial-gradient(ellipse at center,#1e1b4b 0%,#0d0d1a 60%)',padding:'2rem'}}>
      <div style={card}>
        <div style={{width:'64px',height:'64px',background:'linear-gradient(135deg,#7c3aed,#a855f7)',borderRadius:'50%',display:'flex',alignItems:'center',justifyContent:'center',margin:'0 auto 1.5rem'}}>
          <i className="fas fa-user" style={{fontSize:'1.5rem',color:'white'}}></i>
        </div>
        <h1 style={{textAlign:'center',fontSize:'1.8rem',fontWeight:'700',marginBottom:'0.5rem',background:'linear-gradient(135deg,#818cf8,#a855f7)',WebkitBackgroundClip:'text',WebkitTextFillColor:'transparent'}}>Welcome Back</h1>
        <p style={{textAlign:'center',color:'#94a3b8',marginBottom:'1.5rem',fontSize:'0.9rem'}}>Sign in to continue designing your dream space</p>

        {/* Google button — top */}
        <a href={`${import.meta.env.VITE_API_URL || ''}/auth/google`}
          style={{display:'flex',alignItems:'center',justifyContent:'center',gap:'10px',width:'100%',padding:'0.75rem',background:'#fff',color:'#1f2937',borderRadius:'8px',fontSize:'0.95rem',fontWeight:'600',cursor:'pointer',textDecoration:'none',boxSizing:'border-box'}}>
          {G_ICON} Continue with Google
        </a>

        {divider('or sign in with email')}

        {error && <div style={{background:'rgba(239,68,68,0.15)',border:'1px solid #ef4444',color:'#ef4444',padding:'0.75rem',borderRadius:'8px',marginBottom:'1rem',fontSize:'0.9rem'}}>{error}</div>}

        <form onSubmit={handleSubmit}>
          <div style={{marginBottom:'1.25rem'}}>
            <label style={{display:'block',fontSize:'0.85rem',color:'#94a3b8',marginBottom:'0.5rem'}}>Email</label>
            <input type="email" value={email} onChange={e=>setEmail(e.target.value)} placeholder="you@example.com" required style={inputStyle}/>
          </div>
          <div style={{marginBottom:'1.25rem'}}>
            <label style={{display:'block',fontSize:'0.85rem',color:'#94a3b8',marginBottom:'0.5rem'}}>Password</label>
            <input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Enter your password" required style={inputStyle}/>
          </div>
          <button type="submit" disabled={loading}
            style={{width:'100%',padding:'0.85rem',background:'linear-gradient(135deg,#7c3aed,#a855f7)',color:'white',border:'none',borderRadius:'8px',fontSize:'1rem',fontWeight:'600',cursor:loading?'not-allowed':'pointer',opacity:loading?0.7:1}}>
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <p style={{textAlign:'center',marginTop:'1.25rem',fontSize:'0.9rem',color:'#94a3b8'}}>
          No account? <Link to="/register" style={{color:'#818cf8',textDecoration:'none',fontWeight:'600'}}>Register here</Link>
        </p>
      </div>
    </div>
  )
}
