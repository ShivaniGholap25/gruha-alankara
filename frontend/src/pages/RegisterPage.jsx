import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function RegisterPage() {
  const { register: doRegister } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await doRegister(username, email, password);
      navigate('/login');
    } catch (err) {
      setError(err.data?.error || 'Registration failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-wrapper">
      <div className="auth-card fade-in">
        <div className="auth-icon"><i className="fas fa-user-plus"></i></div>
        <h1 className="gradient-text">Create Account</h1>
        <p className="subtitle">Join Gruha Alankara and start designing your dream space</p>

        {error && (
          <div style={{ background: 'rgba(239,68,68,0.15)', border: '1px solid #ef4444', color: '#ef4444', padding: '0.75rem', borderRadius: 8, marginBottom: '1rem', fontSize: '0.9rem' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username</label>
            <div className="input-wrapper">
              <i className="fas fa-user input-icon"></i>
              <input className="form-input" type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Your name" required />
            </div>
          </div>
          <div className="form-group">
            <label>Email Address</label>
            <div className="input-wrapper">
              <i className="fas fa-envelope input-icon"></i>
              <input className="form-input" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" required />
            </div>
          </div>
          <div className="form-group">
            <label>Password</label>
            <div className="input-wrapper">
              <i className="fas fa-lock input-icon"></i>
              <input className="form-input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Create a strong password" required />
            </div>
          </div>
          <button type="submit" className="btn-submit" disabled={loading}>
            <i className="fas fa-user-plus"></i>
            {loading ? 'Creating...' : 'Create Account'}
          </button>
        </form>
        <div className="divider"><span>or</span></div>
        <div className="auth-footer">Already have an account? <Link to="/login">Sign in here</Link></div>
      </div>
    </div>
  );
}
