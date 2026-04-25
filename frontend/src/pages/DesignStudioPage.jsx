import { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { api } from '../api/client';
import { showToast } from '../components/Toast';
import './DesignStudioPage.css';

const colorThemes = [
  { name: 'Warm Neutrals', gradient: 'linear-gradient(90deg,#f5f0e8,#d4a373,#ccd5ae,#e9edc9)' },
  { name: 'Cool Blue', gradient: 'linear-gradient(90deg,#03045e,#0077b6,#00b4d8,#90e0ef)' },
  { name: 'Earth Tones', gradient: 'linear-gradient(90deg,#6b4226,#a0522d,#d2691e,#deb887)' },
  { name: 'Forest Green', gradient: 'linear-gradient(90deg,#1b4332,#2d6a4f,#52b788,#b7e4c7)' },
  { name: 'Sunset Vibes', gradient: 'linear-gradient(90deg,#ff6b6b,#ffa07a,#ffd93d,#6bcb77)' },
  { name: 'Royal Purple', gradient: 'linear-gradient(90deg,#10002b,#3c096c,#7b2fbe,#e0aaff)' },
  { name: 'Monochrome', gradient: 'linear-gradient(90deg,#1a1a1a,#4a4a4a,#8a8a8a,#dadada)' },
  { name: 'Ocean Breeze', gradient: 'linear-gradient(90deg,#023e8a,#0096c7,#48cae4,#ade8f4)' },
];

function inr(v) { return 'Rs. ' + Number(v || 0).toLocaleString('en-IN'); }
function barWidth(amount, budget) { return Math.max(4, Math.round((Number(amount || 0) / Number(budget || 1)) * 100)); }

export default function DesignStudioPage() {
  const [searchParams] = useSearchParams();
  const [style, setStyle] = useState(searchParams.get('style') || 'Modern Minimalist');
  const [budget, setBudget] = useState(Number(searchParams.get('budget')) || 50000);
  const [roomType, setRoomType] = useState(searchParams.get('room_type') || 'Living Room');
  const [colorTheme, setColorTheme] = useState('Warm Neutrals');
  const [width, setWidth] = useState(12);
  const [length, setLength] = useState(14);
  const [height, setHeight] = useState(9);
  const [activeTab, setActiveTab] = useState('overview');
  const [design, setDesign] = useState(null);
  const [status, setStatus] = useState('AI Status: Ready');
  const [generating, setGenerating] = useState(false);

  const area = width * length;

  const generate = async () => {
    setGenerating(true);
    setStatus('AI Status: Generating...');
    const res = await api.post('/generate-design', {
      style_theme: style, budget, room_type: roomType, color_theme: colorTheme,
      dimensions: { width, length, height },
    });
    if (res.ok) {
      setDesign(res.data);
      setStatus('AI Status: ' + (res.data.ai_status || 'Complete'));
      setActiveTab('overview');
    } else {
      setStatus('AI Status: Error - ' + (res.data?.error || 'Try again'));
    }
    setGenerating(false);
  };

  const saveDesign = async () => {
    if (!design) { showToast('Generate a design first.', 'warning'); return; }
    const res = await api.post('/save-design', design);
    if (res.ok) showToast('Design saved to catalog!');
    else showToast(res.data?.error || 'Could not save design.', 'error');
  };

  const tabs = [
    { key: 'overview', label: 'Overview' },
    { key: 'furniture', label: 'Furniture' },
    { key: 'budget_tab', label: 'Budget' },
    { key: 'view3d', label: '3D View' },
    { key: 'mood', label: 'Mood Board' },
  ];

  return (
    <div className="studio-wrap">
      <div style={{ marginBottom: '1.2rem' }}>
        <h1 className="gradient-text" style={{ fontSize: '2rem', fontWeight: 800 }}>Design Studio</h1>
        <p style={{ color: 'var(--muted)' }}>Generate room-specific furniture, budget breakdown, and mood board recommendations with AI.</p>
      </div>
      <div className="studio-grid">
        <aside className="studio-sidebar">
          <h3 style={{ fontSize: '1rem', marginBottom: '1rem' }}>Design Controls</h3>
          <label style={{ fontSize: '0.85rem', color: 'var(--muted)', display: 'block', marginBottom: '0.3rem' }}>Style Theme</label>
          <select value={style} onChange={(e) => setStyle(e.target.value)}>
            {['Modern Minimalist', 'Scandinavian', 'Industrial', 'Bohemian', 'Traditional', 'Contemporary'].map((s) => <option key={s}>{s}</option>)}
          </select>

          <div style={{ marginTop: '0.8rem' }}>
            <label style={{ fontSize: '0.85rem', color: 'var(--muted)', display: 'block', marginBottom: '0.3rem' }}>Budget (INR)</label>
            <input type="number" min={10000} step={1000} value={budget} onChange={(e) => setBudget(Number(e.target.value))} />
            <input type="range" min={10000} max={300000} step={1000} value={budget} onChange={(e) => setBudget(Number(e.target.value))} style={{ marginTop: '0.6rem' }} />
          </div>

          <div style={{ marginTop: '0.8rem' }}>
            <label style={{ fontSize: '0.85rem', color: 'var(--muted)', display: 'block', marginBottom: '0.3rem' }}>Room Type</label>
            <select value={roomType} onChange={(e) => setRoomType(e.target.value)}>
              {['Living Room', 'Bedroom', 'Kitchen', 'Bathroom', 'Office', 'Dining Room'].map((r) => <option key={r}>{r}</option>)}
            </select>
          </div>

          <div style={{ marginTop: '0.8rem' }}>
            <label style={{ fontSize: '0.85rem', color: 'var(--muted)', display: 'block', marginBottom: '0.3rem' }}>Color Theme</label>
            <div className="theme-grid">
              {colorThemes.map((ct) => (
                <button key={ct.name} className={`theme-swatch ${colorTheme === ct.name ? 'active' : ''}`} onClick={() => setColorTheme(ct.name)}>
                  <div className="swatch-bar" style={{ background: ct.gradient }}></div>
                  <p style={{ fontSize: '0.6rem', color: '#cbd5e1', margin: '4px 0 0' }}>{ct.name.split(' ')[0]}</p>
                </button>
              ))}
            </div>
            <p style={{ fontSize: '0.75rem', color: 'var(--accent-soft)', marginTop: 4 }}>{colorTheme} selected</p>
          </div>

          <div style={{ marginTop: '0.8rem' }}>
            <label style={{ fontSize: '0.85rem', color: 'var(--muted)', display: 'block', marginBottom: '0.3rem' }}>Room Dimensions (ft)</label>
            <div className="dims-grid">
              <input type="number" min={5} value={width} onChange={(e) => setWidth(Number(e.target.value))} placeholder="W" />
              <input type="number" min={5} value={length} onChange={(e) => setLength(Number(e.target.value))} placeholder="L" />
              <input type="number" min={7} value={height} onChange={(e) => setHeight(Number(e.target.value))} placeholder="H" />
            </div>
            <p style={{ fontSize: '0.75rem', color: 'var(--muted)', marginTop: 6 }}>Area: {area} sq ft</p>
          </div>

          <button className="btn btn-primary" style={{ width: '100%', marginTop: '1rem', justifyContent: 'center' }} onClick={generate} disabled={generating}>
            <i className="fas fa-wand-magic-sparkles"></i> {generating ? 'Generating...' : 'Generate Design'}
          </button>
          <button className="btn btn-outline" style={{ width: '100%', marginTop: '0.7rem', justifyContent: 'center' }} onClick={saveDesign}>
            <i className="fas fa-bookmark"></i> Save to Catalog
          </button>
          <button className="btn btn-outline" style={{ width: '100%', marginTop: '0.7rem', justifyContent: 'center' }} onClick={() => window.print()}>
            <i className="fas fa-file-pdf"></i> Export PDF
          </button>

          <div className="tips-box">
            <p style={{ fontSize: '0.78rem', color: 'var(--muted)' }}>Quick Tips</p>
            <ul style={{ margin: '0.4rem 0 0 1rem', color: 'var(--text-secondary)', fontSize: '0.78rem', lineHeight: 1.6 }}>
              <li>Keep a 2.5 ft movement path.</li>
              <li>Use layered lighting for depth.</li>
              <li>Start with high priority furniture.</li>
            </ul>
          </div>
          <p style={{ marginTop: '0.7rem', fontSize: '0.85rem', color: 'var(--success)' }}>{status}</p>
        </aside>

        <section className="studio-main">
          <div className="tabs">
            {tabs.map((t) => (
              <button key={t.key} className={`tab ${activeTab === t.key ? 'active' : ''}`} onClick={() => setActiveTab(t.key)}>{t.label}</button>
            ))}
          </div>

          {activeTab === 'overview' && (
            <div className="fade-in">
              {design ? (
                <>
                  <div className="card"><h3>{design.style_theme} • {design.room_type}</h3><p style={{ color: 'var(--muted)', margin: '0.5rem 0' }}>{design.description}</p><p style={{ color: 'var(--text-secondary)' }}>{design.ai_story || ''}</p></div>
                  <div className="overview-half">
                    <div className="card"><h4>Color Palette</h4><div style={{ display: 'flex', gap: 8, marginTop: '0.8rem' }}>{(design.colors || []).map((c, i) => <div key={i} className="color-dot" style={{ background: c }} title={c}></div>)}</div></div>
                    <div className="card"><h4>Materials</h4><p style={{ color: 'var(--muted)', marginTop: '0.8rem' }}>{(design.materials || []).join(', ')}</p></div>
                  </div>
                </>
              ) : (
                <>
                  <div className="overview-cards">
                    <div className="card"><p style={{ color: 'var(--muted)', marginBottom: '0.4rem' }}>Style Suggestions</p><h3>No design generated</h3><p style={{ color: 'var(--muted)', marginTop: '0.5rem' }}>Use the left panel to generate a concept.</p></div>
                    <div className="card"><p style={{ color: 'var(--muted)', marginBottom: '0.4rem' }}>Selected Color Palette</p><p style={{ color: 'var(--muted)' }}>No palette selected.</p></div>
                    <div className="card"><p style={{ color: 'var(--muted)', marginBottom: '0.4rem' }}>Materials</p><p style={{ color: 'var(--muted)' }}>No material list yet.</p></div>
                  </div>
                  <div className="card" style={{ marginTop: '1rem' }}><h4>AI Story</h4><p style={{ color: 'var(--muted)', marginTop: '0.6rem' }}>Generated story will appear here.</p></div>
                </>
              )}
            </div>
          )}

          {activeTab === 'furniture' && (
            <div className="fade-in">
              {design ? (
                <div className="furniture-grid-studio">
                  {(design.furniture_list || []).map((f, i) => (
                    <div className="card" key={i}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <h4>{f.name}</h4>
                        <span className="badge" style={{ background: f.priority === 'High' ? '#ef4444' : f.priority === 'Medium' ? '#f59e0b' : '#10b981', color: f.priority === 'Medium' ? 'black' : 'white' }}>{f.priority || 'Low'}</span>
                      </div>
                      <p style={{ color: 'var(--muted)' }}>Material: {f.material || 'N/A'}</p>
                      <p style={{ fontWeight: 700 }}>{inr(f.price)}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="card"><p style={{ color: 'var(--muted)' }}>No furniture generated yet.</p></div>
              )}
            </div>
          )}

          {activeTab === 'budget_tab' && (
            <div className="fade-in">
              {design ? (
                <div className="card">
                  <h4>Budget Breakdown ({inr(design.budget)})</h4>
                  {(design.budget_breakdown || []).map((b, i) => (
                    <div key={i} style={{ marginTop: '0.8rem' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between' }}><span style={{ color: 'var(--muted)' }}>{b.category}</span><strong>{inr(b.amount)}</strong></div>
                      <div className="progress-bar"><div className="progress-fill" style={{ width: barWidth(b.amount, design.budget) + '%' }}></div></div>
                    </div>
                  ))}
                  <div style={{ marginTop: '1rem' }}>
                    <p style={{ color: 'var(--muted)', fontSize: '0.85rem' }}>Savings Tips</p>
                    <ul style={{ margin: '0.4rem 0 0 1rem', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
                      {(design.savings_tips || []).map((t, i) => <li key={i}>{t}</li>)}
                    </ul>
                  </div>
                </div>
              ) : (
                <div className="card"><p style={{ color: 'var(--muted)' }}>No budget breakdown generated yet.</p></div>
              )}
            </div>
          )}

          {activeTab === 'view3d' && (
            <div className="view3d-grid fade-in">
              <Link to="/live-ar" className="card" style={{ textDecoration: 'none', color: 'var(--text)' }}>
                <i className="fas fa-camera" style={{ color: 'var(--accent-soft)' }}></i>
                <h4 style={{ margin: '0.5rem 0' }}>AR Camera</h4>
                <p style={{ color: 'var(--muted)' }}>Try placement overlays with live camera.</p>
              </Link>
              <div className="card"><i className="fas fa-cube" style={{ color: 'var(--accent-soft)' }}></i><h4 style={{ margin: '0.5rem 0' }}>3D Viewer</h4><p style={{ color: 'var(--muted)' }}>Interactive model view with room depth.</p></div>
              <div className="card"><i className="fas fa-globe" style={{ color: 'var(--accent-soft)' }}></i><h4 style={{ margin: '0.5rem 0' }}>360 Preview</h4><p style={{ color: 'var(--muted)' }}>Walkthrough perspective preview.</p></div>
            </div>
          )}

          {activeTab === 'mood' && (
            <div className="fade-in">
              {design ? (
                <div className="card">
                  <h4>Mood Board</h4>
                  <p style={{ color: 'var(--muted)', marginTop: '0.7rem' }}>Theme: {design.color_theme} | Style: {design.style_theme}</p>
                  <div className="mood-colors">{(design.colors || []).map((c, i) => <div key={i} className="mood-swatch" style={{ background: c }}></div>)}</div>
                </div>
              ) : (
                <div className="card"><p style={{ color: 'var(--muted)' }}>Mood board appears after generation.</p></div>
              )}
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
