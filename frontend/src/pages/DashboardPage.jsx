import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { api } from '../api/client';
import './DashboardPage.css';

function fmtDate(ts) {
  if (!ts) return 'N/A';
  return new Date(ts).toLocaleString();
}

function statusBadge(status) {
  const s = (status || '').toLowerCase();
  const colors = {
    confirmed: { bg: '#14532d', color: '#bbf7d0' },
    cancelled: { bg: '#7f1d1d', color: '#fecaca' },
    pending: { bg: '#78350f', color: '#fde68a' },
  };
  const c = colors[s] || colors.pending;
  return (
    <span className="badge" style={{ background: c.bg, color: c.color }}>{status}</span>
  );
}

export default function DashboardPage() {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const res = await api.get('/dashboard/stats');
        if (res.ok) setStats(res.data);
        else setError('Failed to load dashboard');
      } catch (err) {
        setError(err.message || 'Failed to load dashboard');
      }
    })();
  }, []);

  return (
    <div className="dash-container">
      <h1 className="dash-title gradient-text">Dashboard</h1>
      <p className="dash-welcome">Welcome {user?.username || 'Designer'}. Monitor your projects, bookings and activity from one place.</p>

      {error && <div style={{ color: '#fca5a5', marginBottom: '1rem' }}>{error}</div>}

      <section className="dash-section">
        <h2>Stats Overview</h2>
        <div className="dash-grid">
          <article className="dash-stat-card"><h3>Total Designs</h3><div className="dash-stat-val">{stats?.total_designs || 0}</div></article>
          <article className="dash-stat-card"><h3>Total Bookings</h3><div className="dash-stat-val">{stats?.total_bookings || 0}</div></article>
          <article className="dash-stat-card"><h3>Favorite Style</h3><div className="dash-stat-val" style={{ fontSize: '1.1rem' }}>{stats?.favorite_style || '-'}</div></article>
          <article className="dash-stat-card"><h3>Most Used Room</h3><div className="dash-stat-val" style={{ fontSize: '1.1rem' }}>{stats?.most_used_room || '-'}</div></article>
        </div>
      </section>

      <section className="dash-section">
        <h2>Quick Actions</h2>
        <div className="dash-actions">
          <Link className="btn btn-primary" to="/design"><i className="fas fa-wand-magic-sparkles"></i> New Design</Link>
          <Link className="btn btn-outline" to="/analyze"><i className="fas fa-camera"></i> Analyze Room</Link>
          <Link className="btn btn-outline" to="/catalog"><i className="fas fa-book"></i> View Catalog</Link>
        </div>
      </section>

      <section className="dash-section">
        <h2>Recent Designs</h2>
        <div className="design-grid">
          {(stats?.recent_designs || []).length > 0 ? stats.recent_designs.map((d) => (
            <article className="design-item" key={d.id}>
              {d.image_path ? (
                <img className="design-thumb" src={`/${d.image_path.replace(/^\/+/, '')}`} alt={d.title} style={{ objectFit: 'cover' }} />
              ) : (
                <div className="design-thumb">No image</div>
              )}
              <h4 style={{ marginTop: '0.55rem' }}>{d.title}</h4>
              <p style={{ color: 'var(--muted)', fontSize: '0.88rem' }}>{d.style_theme} | {d.room_type}</p>
              <p style={{ color: 'var(--muted)', fontSize: '0.88rem' }}>{fmtDate(d.created_at)}</p>
            </article>
          )) : (
            <article className="design-item"><p style={{ color: 'var(--muted)' }}>No designs yet.</p></article>
          )}
        </div>
      </section>

      <section className="dash-section">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.8rem' }}>
          <h2 style={{ margin: 0 }}>Recent Bookings</h2>
        </div>
        <div style={{ overflow: 'auto' }}>
          <table className="dash-table">
            <thead><tr><th>Furniture</th><th>Status</th><th>Date</th></tr></thead>
            <tbody>
              {(stats?.recent_bookings || []).length > 0 ? stats.recent_bookings.map((b) => (
                <tr key={b.id}>
                  <td>{b.furniture}</td>
                  <td>{statusBadge(b.status)}</td>
                  <td>{fmtDate(b.booking_date)}</td>
                </tr>
              )) : (
                <tr><td colSpan={3} style={{ color: 'var(--muted)' }}>No bookings found.</td></tr>
              )}
            </tbody>
          </table>
        </div>
        <div style={{ marginTop: '0.8rem' }}>
          <Link className="btn btn-outline" to="/my-bookings"><i className="fas fa-list"></i> View All Bookings</Link>
        </div>
      </section>

      <section className="dash-section">
        <h2>Activity Timeline</h2>
        <div className="timeline">
          {(stats?.timeline || []).length > 0 ? stats.timeline.map((item, i) => (
            <div className="timeline-item" key={i}>
              <span>
                <i className={`fas ${item.type === 'booking' ? 'fa-calendar-check' : 'fa-pen-ruler'}`} style={{ marginRight: 8, color: '#c4b5fd' }}></i>
                {item.label}
              </span>
              <span style={{ color: 'var(--muted)', fontSize: '0.88rem' }}>{fmtDate(item.timestamp)}</span>
            </div>
          )) : (
            <div className="timeline-item"><span style={{ color: 'var(--muted)' }}>No recent activity.</span></div>
          )}
        </div>
      </section>
    </div>
  );
}
