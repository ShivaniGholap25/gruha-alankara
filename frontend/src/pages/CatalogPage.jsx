import { useState, useEffect } from 'react';
import { api } from '../api/client';
import { showToast } from '../components/Toast';

export default function CatalogPage() {
  const [designs, setDesigns] = useState([]);
  const [styleFilter, setStyleFilter] = useState('');
  const [roomFilter, setRoomFilter] = useState('');
  const [sortFilter, setSortFilter] = useState('newest');
  const [search, setSearch] = useState('');
  const [selected, setSelected] = useState(new Set());
  const [showCompare, setShowCompare] = useState(false);

  useEffect(() => { loadDesigns(); }, []);

  const loadDesigns = async () => {
    try {
      const res = await api.get('/get-designs');
      setDesigns(res.ok && Array.isArray(res.data) ? res.data : []);
    } catch { setDesigns([]); }
  };

  const uniqueVals = (key) => [...new Set(designs.map(d => d[key]).filter(Boolean))].sort();
  const filtered = () => {
    let list = [...designs];
    if (styleFilter) list = list.filter(d => d.style_theme === styleFilter);
    if (roomFilter) list = list.filter(d => d.room_type === roomFilter);
    if (search) { const q = search.toLowerCase(); list = list.filter(d => (d.title||'').toLowerCase().includes(q) || (d.style_theme||'').toLowerCase().includes(q) || (d.room_type||'').toLowerCase().includes(q)); }
    if (sortFilter === 'newest') list.sort((a,b) => new Date(b.created_at) - new Date(a.created_at));
    else if (sortFilter === 'oldest') list.sort((a,b) => new Date(a.created_at) - new Date(b.created_at));
    else if (sortFilter === 'budgetHigh') list.sort((a,b) => (b.budget||0) - (a.budget||0));
    else if (sortFilter === 'budgetLow') list.sort((a,b) => (a.budget||0) - (b.budget||0));
    return list;
  };

  const toggleCompare = (id) => {
    const s = new Set(selected);
    if (s.has(id)) s.delete(id); else if (s.size < 2) s.add(id); else { showToast('Select only 2 for comparison', 'warning'); return; }
    setSelected(s);
  };

  const deleteDesign = async (id) => {
    if (!confirm('Delete this design?')) return;
    const res = await api.delete(`/delete-design/${id}`);
    if (res.ok) { setDesigns(d => d.filter(x => x.id !== id)); showToast('Design deleted'); }
    else showToast(res.data?.error || 'Delete failed', 'error');
  };
  const duplicateDesign = async (id) => {
    const res = await api.post(`/duplicate-design/${id}`, {});
    if (res.ok) { loadDesigns(); showToast('Design duplicated'); }
    else showToast(res.data?.error || 'Duplicate failed', 'error');
  };

  const list = filtered();
  const comparedDesigns = designs.filter(d => selected.has(d.id));

  return (
    <div style={{ maxWidth: 1240, margin: '0 auto', padding: '2rem' }}>
      <h1 className="gradient-text" style={{ fontSize: '2rem' }}>My Design Catalog</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: '0.8rem', background: 'var(--panel)', border: '1px solid var(--line)', borderRadius: 14, padding: '1rem', margin: '1rem 0' }}>
        <select value={styleFilter} onChange={e => setStyleFilter(e.target.value)}><option value="">All Styles</option>{uniqueVals('style_theme').map(s => <option key={s}>{s}</option>)}</select>
        <select value={roomFilter} onChange={e => setRoomFilter(e.target.value)}><option value="">All Rooms</option>{uniqueVals('room_type').map(r => <option key={r}>{r}</option>)}</select>
        <select value={sortFilter} onChange={e => setSortFilter(e.target.value)}><option value="newest">Newest First</option><option value="oldest">Oldest First</option><option value="budgetHigh">Budget High→Low</option><option value="budgetLow">Budget Low→High</option></select>
        <input type="text" value={search} onChange={e => setSearch(e.target.value)} placeholder="Search..." style={{ background: '#0f172a', border: '1px solid var(--line-light)', color: 'var(--text)', borderRadius: 10, padding: '0.7rem' }} />
      </div>

      {selected.size === 2 && <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '0.9rem' }}><button className="btn btn-primary" onClick={() => setShowCompare(true)}><i className="fas fa-balance-scale"></i> Compare Selected</button></div>}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: '1rem' }}>
        {list.length > 0 ? list.map(d => (
          <article className="card" key={d.id} style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div><h3 style={{ fontSize: '1rem' }}>{d.title || 'Untitled'}</h3><div style={{ fontSize: '0.88rem', color: 'var(--muted)' }}>Created: {d.created_at || 'N/A'}</div></div>
              <span className="badge" style={{ background: 'rgba(124,58,237,0.18)', border: '1px solid rgba(124,58,237,0.35)', color: '#ddd6fe' }}>{d.style_theme}</span>
            </div>
            <div style={{ fontSize: '0.88rem', color: 'var(--muted)' }}>Budget: Rs. {Number(d.budget||0).toLocaleString()}</div>
            <label style={{ display: 'flex', alignItems: 'center', gap: 8, color: 'var(--text-secondary)', fontSize: '0.86rem' }}>
              <input type="checkbox" checked={selected.has(d.id)} onChange={() => toggleCompare(d.id)} /> Compare
            </label>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginTop: 'auto' }}>
              <button className="btn btn-primary" style={{ fontSize: '0.85rem' }} onClick={() => window.location.href = `/design?edit=${d.id}`}><i className="fas fa-pen"></i> Edit</button>
              <button className="btn btn-outline" style={{ fontSize: '0.85rem' }} onClick={() => duplicateDesign(d.id)}><i className="fas fa-copy"></i> Duplicate</button>
              <button className="btn btn-danger" style={{ fontSize: '0.85rem' }} onClick={() => deleteDesign(d.id)}><i className="fas fa-trash"></i> Delete</button>
            </div>
          </article>
        )) : <div style={{ gridColumn: '1/-1', border: '1px dashed var(--line-light)', borderRadius: 12, padding: '1.2rem', color: 'var(--muted)', textAlign: 'center' }}>{designs.length ? 'No designs match filters.' : 'No designs saved yet.'}</div>}
      </div>

      {showCompare && comparedDesigns.length === 2 && (
        <div style={{ position: 'fixed', inset: 0, background: 'rgba(4,8,19,0.78)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '1rem', zIndex: 1000 }} onClick={(e) => { if (e.target === e.currentTarget) setShowCompare(false); }}>
          <div style={{ width: 'min(980px,100%)', maxHeight: '90vh', overflow: 'auto', background: '#171727', border: '1px solid #36435f', borderRadius: 16, padding: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h2>Design Comparison</h2>
              <button style={{ background: 'none', border: 'none', color: 'var(--muted)', fontSize: '1.1rem', cursor: 'pointer' }} onClick={() => setShowCompare(false)}><i className="fas fa-xmark"></i></button>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              {comparedDesigns.map(d => (
                <div key={d.id} className="card-dark" style={{ padding: '0.9rem' }}>
                  <h3 style={{ marginBottom: '0.8rem' }}>{d.title}</h3>
                  <p style={{ color: 'var(--muted)', fontSize: '0.9rem' }}>Style: {d.style_theme}</p>
                  <p style={{ color: 'var(--muted)', fontSize: '0.9rem' }}>Room: {d.room_type}</p>
                  <p style={{ color: 'var(--muted)', fontSize: '0.9rem' }}>Budget: Rs. {Number(d.budget||0).toLocaleString()}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
