import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    const result = await login(email, password)
    if(result.success) {
      navigate('/')
    } else {
      setError(result.error || 'Login failed')
    }
    setLoading(false)
  }

  return (
    <div style={{minHeight:'100vh',display:'flex',alignItems:'center',justifyContent:'center',background:'radial-gradient(ellipse at center,#1e1b4b 0%,#0d0d1a 60%)',padding:'2rem'}}>
      <div style={{background:'#1a1a2e',border:'1px solid #2d3748',borderRadius:'16px',padding:'2.5rem',width:'100%',maxWidth:'420px',boxShadow:'0 25px 50px rgba(0,0,0,0.5)'}}>
        <div style={{width:'64px',height:'64px',background:'linear-gradient(135deg,#7c3aed,#a855f7)',borderRadius:'50%',display:'flex',alignItems:'center',justifyContent:'center',margin:'0 auto 1.5rem'}}>
          <i className="fas fa-user" style={{fontSize:'1.5rem',color:'white'}}></i>
        </div>
        <h1 style={{textAlign:'center',fontSize:'1.8rem',fontWeight:'700',marginBottom:'0.5rem',background:'linear-gradient(135deg,#818cf8,#a855f7)',WebkitBackgroundClip:'text',WebkitTextFillColor:'transparent'}}>Welcome Back</h1>
        <p style={{textAlign:'center',color:'#94a3b8',marginBottom:'2rem',fontSize:'0.9rem'}}>Sign in to continue designing your dream space</p>
        {error && <div style={{background:'rgba(239,68,68,0.15)',border:'1px solid #ef4444',color:'#ef4444',padding:'0.75rem',borderRadius:'8px',marginBottom:'1rem',fontSize:'0.9rem'}}>{error}</div>}
        <form onSubmit={handleSubmit}>
          <div style={{marginBottom:'1.25rem'}}>
            <label style={{display:'block',fontSize:'0.85rem',color:'#94a3b8',marginBottom:'0.5rem'}}>Email</label>
            <input type="email" value={email} onChange={e=>setEmail(e.target.value)} placeholder="you@example.com" required
              style={{width:'100%',background:'#0d0d1a',border:'1px solid #2d3748',color:'#e2e8f0',borderRadius:'8px',padding:'0.75rem',fontSize:'0.95rem',outline:'none',boxSizing:'border-box'}}/>
          </div>
          <div style={{marginBottom:'1.25rem'}}>
            <label style={{display:'block',fontSize:'0.85rem',color:'#94a3b8',marginBottom:'0.5rem'}}>Password</label>
            <input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Enter your password" required
              style={{width:'100%',background:'#0d0d1a',border:'1px solid #2d3748',color:'#e2e8f0',borderRadius:'8px',padding:'0.75rem',fontSize:'0.95rem',outline:'none',boxSizing:'border-box'}}/>
          </div>
          <button type="submit" disabled={loading}
            style={{width:'100%',padding:'0.85rem',background:'linear-gradient(135deg,#7c3aed,#a855f7)',color:'white',border:'none',borderRadius:'8px',fontSize:'1rem',fontWeight:'600',cursor:loading?'not-allowed':'pointer',opacity:loading?0.7:1}}>
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
        <p style={{textAlign:'center',marginTop:'1.5rem',fontSize:'0.9rem',color:'#94a3b8'}}>No account? <Link to="/register" style={{color:'#818cf8',textDecoration:'none',fontWeight:'600'}}>Register here</Link></p>
      </div>
    </div>
  )
}