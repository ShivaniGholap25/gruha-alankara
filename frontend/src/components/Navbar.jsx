import { useState, useRef, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navbar.css';

export default function Navbar() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);

  const links = [
    { to: '/', label: 'Home' },
    { to: '/analyze', label: 'Analyze Room' },
    { to: '/design', label: 'Design Studio' },
    { to: '/furniture', label: 'Furniture' },
    { to: '/catalog', label: 'My Catalog' },
    { to: '/my-bookings', label: 'My Bookings' },
  ];

  const isActive = (path) => location.pathname === path;

  const handleLogout = async () => {
    await logout();
    setDropdownOpen(false);
    setMenuOpen(false);
    navigate('/');
  };

  // Close dropdown on outside click
  useEffect(() => {
    function handleClick(e) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setDropdownOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

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
            /* ── Logged-in: compact user dropdown ── */
            <div className="nav-user-dropdown" ref={dropdownRef}>
              <button
                className="nav-user-btn"
                onClick={() => setDropdownOpen(!dropdownOpen)}
              >
                <i className="fas fa-user-circle"></i>
                <span>{user.username}</span>
                <i className={`fas fa-chevron-down nav-chevron ${dropdownOpen ? 'open' : ''}`}></i>
              </button>

              {dropdownOpen && (
                <div className="nav-dropdown">
                  <Link
                    to="/dashboard"
                    className="nav-dropdown-item"
                    onClick={() => { setDropdownOpen(false); setMenuOpen(false); }}
                  >
                    <i className="fas fa-tachometer-alt"></i> Dashboard
                  </Link>
                  <Link
                    to="/my-bookings"
                    className="nav-dropdown-item"
                    onClick={() => { setDropdownOpen(false); setMenuOpen(false); }}
                  >
                    <i className="fas fa-calendar-check"></i> My Bookings
                  </Link>
                  <div className="nav-dropdown-divider" />
                  <button className="nav-dropdown-item danger" onClick={handleLogout}>
                    <i className="fas fa-sign-out-alt"></i> Logout
                  </button>
                </div>
              )}
            </div>
          ) : (
            /* ── Logged-out: Sign In + Register ── */
            <>
              <Link
                to="/login"
                className="btn btn-outline"
                style={{ padding: '0.4rem 0.9rem', fontSize: '0.85rem' }}
                onClick={() => setMenuOpen(false)}
              >
                Sign In
              </Link>
              <Link
                to="/register"
                className="btn btn-primary"
                style={{ padding: '0.4rem 0.9rem', fontSize: '0.85rem' }}
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
