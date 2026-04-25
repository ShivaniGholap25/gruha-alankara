import { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navbar.css';

export default function Navbar() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  const links = [
    { to: '/', label: 'Home' },
    { to: '/analyze', label: 'Analyze Room' },
    { to: '/design', label: 'Design Studio' },
    { to: '/catalog', label: 'My Catalog' },
    { to: '/style-quiz', label: 'Style Quiz' },
  ];

  const isActive = (path) => location.pathname === path;

  const handleLogout = async () => {
    await logout();
    navigate('/');
    setMenuOpen(false);
  };

  return (
    <nav className="navbar">
      <Link to="/" className="nav-brand">
        <i className="fas fa-home"></i>
        Gruha Alankara
      </Link>

      <button className="nav-hamburger" onClick={() => setMenuOpen(!menuOpen)}>
        <i className={`fas ${menuOpen ? 'fa-xmark' : 'fa-bars'}`}></i>
      </button>

      <div className={`nav-links ${menuOpen ? 'open' : ''}`}>
        {links.map((link) => (
          <Link
            key={link.to}
            to={link.to}
            className={`nav-link ${isActive(link.to) ? 'active' : ''}`}
            onClick={() => setMenuOpen(false)}
          >
            {link.label}
          </Link>
        ))}

        <div className="nav-auth">
          {user ? (
            <>
              <span className="nav-user">
                <i className="fas fa-user-circle"></i>
                {user.username}
              </span>
              <Link
                to="/dashboard"
                className="btn btn-outline"
                style={{ padding: '0.4rem 0.8rem', fontSize: '0.82rem' }}
                onClick={() => setMenuOpen(false)}
              >
                Dashboard
              </Link>
              <button className="nav-logout" onClick={handleLogout}>
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="btn btn-outline"
                style={{ padding: '0.4rem 0.8rem', fontSize: '0.82rem' }}
                onClick={() => setMenuOpen(false)}
              >
                Sign In
              </Link>
              <Link
                to="/register"
                className="btn btn-primary"
                style={{ padding: '0.4rem 0.8rem', fontSize: '0.82rem' }}
                onClick={() => setMenuOpen(false)}
              >
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
