import { useState, useEffect } from 'react';
import { api } from '../api/client';
import { showToast } from '../components/Toast';

export default function MyBookingsPage() {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => { loadBookings(); }, []);

  const loadBookings = async () => {
    const res = await api.get('/my-bookings');
    setBookings(res.ok && Array.isArray(res.data) ? res.data : []);
    setLoading(false);
  };

  const cancel = async (id) => {
    if (!confirm('Cancel this booking?')) return;
    const res = await api.post(`/cancel-booking/${id}`, {});
    if (res.ok) { showToast('Booking cancelled'); loadBookings(); }
    else showToast(res.data?.error || 'Failed', 'error');
  };

  const statusColor = (s) => {
    const st = (s||'').toLowerCase();
    if (st==='confirmed') return { bg: '#14532d', color: '#bbf7d0' };
    if (st==='cancelled') return { bg: '#7f1d1d', color: '#fecaca' };
    return { bg: '#78350f', color: '#fde68a' };
  };

  return (
    <section style={{ maxWidth: 1100, margin: '0 auto', padding: '2rem 1.25rem' }}>
      <h1 className="gradient-text" style={{ fontSize: '2rem', fontWeight: 800 }}>My Bookings</h1>
      <p style={{ color: 'var(--muted)', margin: '0.35rem 0 1.5rem' }}>Track and manage your furniture bookings</p>
      {loading ? (
        <div style={{ textAlign: 'center', padding: '3rem' }}><div style={{ width: 48, height: 48, border: '3px solid var(--line)', borderTopColor: 'var(--accent)', borderRadius: '50%', animation: 'spin 1s linear infinite', margin: '0 auto' }}></div></div>
      ) : bookings.length ? (
        <div style={{ overflow: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead><tr style={{ borderBottom: '1px solid var(--line)' }}>
              <th style={{ padding: '0.75rem', textAlign: 'left', color: 'var(--text-secondary)' }}>Furniture</th>
              <th style={{ padding: '0.75rem', textAlign: 'left', color: 'var(--text-secondary)' }}>Category</th>
              <th style={{ padding: '0.75rem', textAlign: 'left', color: 'var(--text-secondary)' }}>Price</th>
              <th style={{ padding: '0.75rem', textAlign: 'left', color: 'var(--text-secondary)' }}>Status</th>
              <th style={{ padding: '0.75rem', textAlign: 'left', color: 'var(--text-secondary)' }}>Date</th>
              <th style={{ padding: '0.75rem', textAlign: 'left', color: 'var(--text-secondary)' }}>Action</th>
            </tr></thead>
            <tbody>
              {bookings.map(b => {
                const sc = statusColor(b.status);
                return (
                  <tr key={b.id} style={{ borderBottom: '1px solid #273142' }}>
                    <td style={{ padding: '0.75rem' }}>{b.furniture_name}</td>
                    <td style={{ padding: '0.75rem', color: 'var(--muted)' }}>{b.furniture_category}</td>
                    <td style={{ padding: '0.75rem' }}>Rs. {Number(b.price||0).toLocaleString()}</td>
                    <td style={{ padding: '0.75rem' }}><span className="badge" style={{ background: sc.bg, color: sc.color }}>{b.status}</span></td>
                    <td style={{ padding: '0.75rem', color: 'var(--muted)' }}>{b.date}</td>
                    <td style={{ padding: '0.75rem' }}>{(b.status||'').toLowerCase()!=='cancelled' && <button className="btn btn-danger" style={{ fontSize: '0.82rem', padding: '0.3rem 0.7rem' }} onClick={() => cancel(b.id)}>Cancel</button>}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      ) : (
        <div style={{ border: '1px dashed var(--line-light)', borderRadius: 14, padding: '2rem', textAlign: 'center', color: 'var(--muted)' }}>No bookings found. Browse <a href="/furniture">Furniture Catalog</a></div>
      )}
    </section>
  );
}
