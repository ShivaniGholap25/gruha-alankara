import { useState, useEffect } from 'react';
import { api } from '../api/client';
import { showToast } from '../components/Toast';

const categories = ['All','Sofa','Table','Chair','Lamp','Shelf'];
const catIcon = (c) => ({sofa:'fa-couch',table:'fa-table',chair:'fa-chair',lamp:'fa-lightbulb',shelf:'fa-book-open'}[c?.toLowerCase()] || 'fa-cube');
const catColor = (c) => ({sofa:'#a78bfa',table:'#22d3ee',chair:'#34d399',lamp:'#fbbf24',shelf:'#fb7185'}[c?.toLowerCase()] || '#94a3b8');
const inr = (v) => `Rs. ${Number(v||0).toLocaleString('en-IN')}`;

export default function FurniturePage() {
  const [items, setItems] = useState([]);
  const [cat, setCat] = useState('All');
  const [search, setSearch] = useState('');
  const [modal, setModal] = useState(null);
  const [booking, setBooking] = useState(false);

  useEffect(() => { api.get('/get-furniture').then(res => setItems(res.ok && Array.isArray(res.data) ? res.data : [])); }, []);

  const filtered = items.filter(i => {
    const matchCat = cat === 'All' || (i.category||'').toLowerCase() === cat.toLowerCase();
    const matchSearch = !search || (i.name||'').toLowerCase().includes(search.toLowerCase());
    return matchCat && matchSearch;
  });

  const book = async () => {
    if (!modal) return;
    setBooking(true);
    const res = await api.post('/book-furniture', { furniture_id: modal.id });
    if (res.ok) {
      setModal(null); showToast('Furniture booked successfully!');
    } else if (res.status === 401) {
      window.location.href = '/login';
    } else {
      showToast(res.data?.error || 'Booking failed', 'error');
    }
    setBooking(false);
  };

  return (
    <section style={{ maxWidth: 1200, margin: '0 auto', padding: '2rem 1.25rem' }}>
      <h1 className="gradient-text" style={{ fontSize: '2rem', fontWeight: 800, marginBottom: '0.35rem' }}>Furniture Catalog</h1>
      <p style={{ color: 'var(--muted)', marginBottom: '1.5rem' }}>Browse and book premium furniture</p>

      <input type="text" value={search} onChange={e => setSearch(e.target.value)} placeholder="Search furniture by name..." style={{ width: '100%', padding: '0.85rem 1rem', borderRadius: 10, border: '1px solid var(--line-light)', background: '#111827', color: 'var(--text)', marginBottom: '1rem' }} />
      <div style={{ display: 'flex', gap: '0.65rem', flexWrap: 'wrap', marginBottom: '1rem' }}>
        {categories.map(c => (
          <button key={c} onClick={() => setCat(c)} style={{ padding: '0.45rem 0.85rem', borderRadius: 999, border: cat===c?'none':'1px solid var(--line-light)', background: cat===c?'var(--grad)':'#111827', color: cat===c?'#fff':'var(--text-secondary)', cursor: 'pointer' }}>{c}</button>
        ))}
      </div>

      {!items.length ? (
        <div style={{ background: '#111827', border: '1px dashed var(--line-light)', borderRadius: 14, padding: '2rem', textAlign: 'center', color: 'var(--muted)' }}>No furniture available. Visit /seed-db first</div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill,minmax(300px,1fr))', gap: '1rem' }}>
          {filtered.length ? filtered.map(item => {
            const color = catColor(item.category);
            return (
              <article key={item.id} style={{ background: '#111827', border: '1px solid var(--line-light)', borderRadius: 14, padding: '1rem', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                <div style={{ height: 130, borderRadius: 10, background: `radial-gradient(circle at top right,${color}33,#0b1220)`, display: 'grid', placeItems: 'center', border: '1px solid var(--line-light)' }}>
                  <i className={`fas ${catIcon(item.category)}`} style={{ fontSize: '2rem', color }}></i>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <strong>{item.name}</strong>
                  <span style={{ padding: '0.2rem 0.6rem', borderRadius: 999, background: `${color}22`, border: `1px solid ${color}66`, color, fontSize: '0.75rem', fontWeight: 700 }}>{(item.category||'').toUpperCase()}</span>
                </div>
                <div style={{ fontSize: '1rem', fontWeight: 700, color: '#ddd6fe' }}>{inr(item.price)}</div>
                <p style={{ color: 'var(--muted)', lineHeight: 1.5, minHeight: 44 }}>{item.description || 'No description available.'}</p>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.55rem', marginTop: 'auto' }}>
                  <button className="btn btn-primary" style={{ justifyContent: 'center' }} onClick={() => setModal(item)}>Book Now</button>
                  <button className="btn btn-outline" style={{ justifyContent: 'center' }} onClick={() => showToast('Added to wishlist')}>Wishlist</button>
                </div>
              </article>
            );
          }) : <div style={{ gridColumn: '1/-1', background: '#111827', border: '1px dashed var(--line-light)', borderRadius: 12, padding: '1.1rem', color: 'var(--muted)', textAlign: 'center' }}>No furniture matches your filters.</div>}
        </div>
      )}

      {modal && (
        <div style={{ position: 'fixed', inset: 0, background: 'rgba(2,6,23,0.75)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '1rem', zIndex: 1500 }} onClick={e => { if (e.target === e.currentTarget) setModal(null); }}>
          <div style={{ width: 'min(460px,100%)', background: '#111827', border: '1px solid var(--line-light)', borderRadius: 14, padding: '1.25rem' }}>
            <h3 style={{ marginBottom: '0.7rem' }}>Confirm Booking</h3>
            <p style={{ color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: '1rem' }}>Book {modal.name} for {inr(modal.price)}?</p>
            <div style={{ display: 'flex', gap: '0.65rem', justifyContent: 'flex-end' }}>
              <button className="btn btn-outline" onClick={() => setModal(null)}>Cancel</button>
              <button className="btn btn-primary" onClick={book} disabled={booking}>{booking ? 'Booking...' : 'Confirm Booking'}</button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
