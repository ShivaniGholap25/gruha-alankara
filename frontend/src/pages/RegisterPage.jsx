import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './LoginPage.css';

export default function RegisterPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setLoading(true);

    if (!username || !email || !password) {
      setError('Please fill in all fields');
      setLoading(false);
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      setLoading(false);
      return;
    }

    try {
      const result = await register(username, email, password);
      
      if (result.success) {
        navigate('/login', { 
          state: { message: 'Registration successful! Please log in.' }
        });
      } else {
        setError(result.error || 'Registration failed');
      }
    } catch (error) {
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <div className="auth-icon">
          <i className="fas fa-user-plus"></i>
        </div>
        <h1>Create Account</h1>
        <p className="auth-subtitle">Join Gruha Alankara to start designing</p>

        {error && (
          <div className="auth-error">
            <i className="fas fa-exclamation-circle"></i> {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username</label>
            <div className="input-wrapper">
              <i className="fas fa-user input-icon"></i>
              <input
                type="text"
                placeholder="Your username"
                value={username}
                onChange={e => setUsername(e.target.value)}
                required
                disabled={loading}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Email Address</label>
            <div className="input-wrapper">
              <i className="fas fa-envelope input-icon"></i>
              <input
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={e => setEmail(e.target.value)}
                required
                disabled={loading}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Password</label>
            <div className="input-wrapper">
              <i className="fas fa-lock input-icon"></i>
              <input
                type="password"
                placeholder="At least 6 characters"
                value={password}
                onChange={e => setPassword(e.target.value)}
                required
                disabled={loading}
                minLength={6}
              />
            </div>
          </div>

          <button type="submit" className="btn-submit" disabled={loading}>
            {loading ? (
              <><i className="fas fa-spinner fa-spin"></i> Creating Account...</>
            ) : (
              <><i className="fas fa-user-plus"></i> Create Account</>
            )}
          </button>
        </form>

        <div className="auth-footer">
          Already have an account? <Link to="/login">Sign in here</Link>
        </div>
      </div>
    </div>
  );
}