import { useState, useRef } from 'react';
import { Link } from 'react-router-dom';
import './AnalyzeRoomPage.css';

const API = import.meta.env.VITE_API_URL || '';

export default function AnalyzeRoomPage() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [roomType, setRoomType] = useState('Living Room');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [compositeUrl, setCompositeUrl] = useState('');
  const inputRef = useRef(null);

  const handleFile = (f) => {
    if (!f) return;
    setFile(f);
    setResult(null);
    setError('');
    setCompositeUrl('');
    const reader = new FileReader();
    reader.onload = (e) => setPreview(e.target.result);
    reader.readAsDataURL(f);
  };

  const analyze = async () => {
    if (!file) { setError('Please upload a room photo first.'); return; }
    setLoading(true);
    setResult(null);
    setError('');
    setCompositeUrl('');

    const fd = new FormData();
    fd.append('image', file);
    fd.append('room_type', roomType);

    try {
      const token = localStorage.getItem('gruha_token') || '';
      const res = await fetch(`${API}/analyze-room`, {
        method: 'POST',
        body: fd,
        credentials: 'include',
        headers: token ? { 'Authorization': `Bearer ${token}` } : {},
      });
      const data = await res.json();
      if (!res.ok || data.error) throw new Error(data.error || 'Analysis failed');
      setResult(data);

      // Issue 3 — fetch composite preview if we have furniture suggestions
      const names = (data.furniture_suggestions || []).map(f => f.name).filter(Boolean);
      if (names.length > 0 && data.image_path) {
        try {
          const compRes = await fetch(`${API}/preview-composite`, {
            method: 'POST',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
              ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
            },
            body: JSON.stringify({ image_path: data.image_path, furniture_names: names }),
          });
          const compData = await compRes.json();
          if (compData.preview_url) setCompositeUrl(`${API}${compData.preview_url}`);
        } catch (_) {}
      }
    } catch (e) {
      setError(e.message || 'Analysis failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="analyze-wrap">
      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <h1 className="gradient-text" style={{ fontSize: '2rem', fontWeight: 700 }}>Room Analysis</h1>
        <p style={{ color: 'var(--muted)', marginTop: '0.5rem' }}>Upload your room photo and AI will analyze dimensions, lighting, colors and suggest styles.</p>
      </div>

      <div className="analyze-step">
        <div className="step-header"><div className="step-number">1</div><h3 style={{ fontWeight: 700 }}>Upload Room Photo</h3></div>
        {!preview ? (
          <div className="drop-zone" onClick={() => inputRef.current?.click()} onDragOver={(e) => e.preventDefault()} onDrop={(e) => { e.preventDefault(); handleFile(e.dataTransfer.files[0]); }}>
            <i className="fas fa-cloud-upload-alt" style={{ fontSize: '3rem', color: 'var(--accent-soft)', display: 'block', marginBottom: '1rem' }}></i>
            <p style={{ fontWeight: 600, marginBottom: '0.5rem' }}>Click to upload your room photo</p>
            <p style={{ color: 'var(--dim)', fontSize: '0.85rem' }}>Supports JPG, PNG, WEBP • Max 5 MB</p>
          </div>
        ) : (
          <div style={{ position: 'relative' }}>
            <img src={preview} alt="Room preview" style={{ width: '100%', maxHeight: 350, objectFit: 'cover', borderRadius: 12 }} />
            <button onClick={() => inputRef.current?.click()} style={{ position: 'absolute', bottom: 12, right: 12, background: 'rgba(0,0,0,0.75)', color: 'white', border: 'none', borderRadius: 8, padding: '0.5rem 1rem', cursor: 'pointer' }}>
              <i className="fas fa-sync" style={{ marginRight: 4 }}></i>Change Photo
            </button>
          </div>
        )}
        <input ref={inputRef} type="file" accept="image/jpeg,image/png,image/webp" style={{ display: 'none' }} onChange={(e) => handleFile(e.target.files[0])} />
      </div>

      {/* Issue 8 — styled error box */}
      {error && (
        <div style={{ background: 'rgba(239,68,68,0.12)', border: '1px solid #ef4444', color: '#fca5a5', borderRadius: 10, padding: '0.85rem 1.2rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
          <i className="fas fa-exclamation-circle"></i> {error}
        </div>
      )}

      <div className="analyze-step">
        <div className="step-header"><div className="step-number">2</div><h3 style={{ fontWeight: 700 }}>Select Room Type</h3></div>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', flexWrap: 'wrap' }}>
          <select value={roomType} onChange={(e) => setRoomType(e.target.value)} style={{ minWidth: 200 }}>
            {['Living Room','Bedroom','Kitchen','Bathroom','Office','Dining Room'].map(r => <option key={r}>{r}</option>)}
          </select>
          <button className="btn btn-primary" onClick={analyze} disabled={loading}>
            <i className={`fas ${loading ? 'fa-spinner fa-spin' : 'fa-search'}`}></i> {loading ? 'Analyzing...' : 'Analyze Room'}
          </button>
        </div>
      </div>

      {loading && (
        <div className="analyze-step" style={{ textAlign: 'center', padding: '3rem' }}>
          <div className="loading-spinner"></div>
          <p style={{ fontSize: '1.1rem', fontWeight: 600 }}>Analyzing your room...</p>
        </div>
      )}

      {/* Issue 3 — composite preview */}
      {compositeUrl && (
        <div className="analyze-step fade-in">
          <h3 style={{ marginBottom: '0.8rem' }}>Furniture Placement Preview</h3>
          <img src={compositeUrl} alt="Furniture composite" style={{ width: '100%', borderRadius: 12, border: '1px solid var(--line)' }} />
        </div>
      )}

      {result && (
        <div className="analyze-step fade-in">
          <h3 style={{ marginBottom: '0.8rem' }}>Analysis Complete</h3>

          {/* Claude furniture suggestions */}
          {(result.furniture_suggestions || []).length > 0 && (
            <div style={{ marginBottom: '1rem' }}>
              <h4 style={{ marginBottom: '0.6rem', color: 'var(--accent)' }}>AI Furniture Suggestions</h4>
              <div style={{ display: 'grid', gap: '0.6rem' }}>
                {result.furniture_suggestions.map((f, i) => (
                  <div key={i} style={{ background: '#16213e', border: '1px solid var(--line)', borderRadius: 10, padding: '0.75rem 1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem' }}>
                    <div>
                      <strong>{f.name}</strong>
                      <p style={{ color: 'var(--muted)', fontSize: '0.82rem', margin: '2px 0 0' }}>{f.reason}</p>
                    </div>
                    <span style={{ color: '#10b981', fontWeight: 700, whiteSpace: 'nowrap' }}>₹{Number(f.price_inr || 0).toLocaleString('en-IN')}</span>
                  </div>
                ))}
              </div>
              {result.layout_tip && <p style={{ color: 'var(--muted)', fontSize: '0.88rem', marginTop: '0.75rem', fontStyle: 'italic' }}>💡 {result.layout_tip}</p>}
            </div>
          )}

          <p style={{ color: 'var(--muted)', lineHeight: 1.6 }}>Dimensions: {result.dimensions?.width} × {result.dimensions?.length} × {result.dimensions?.height} ft ({result.dimensions?.area} sq ft)</p>
          <p style={{ color: 'var(--muted)', lineHeight: 1.6 }}>Lighting: {result.lighting?.quality} ({result.lighting?.brightness}/255)</p>

          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', margin: '1rem 0' }}>
            {(result.colors || []).map((c, i) => <span key={i} style={{ width: 28, height: 28, borderRadius: '50%', display: 'inline-block', background: c, border: '1px solid var(--line-light)' }}></span>)}
          </div>

          <div style={{ display: 'grid', gap: '0.5rem' }}>
            {(result.style_recommendations || []).map((s, i) => (
              <div key={i} style={{ background: '#16213e', border: '1px solid var(--line)', borderRadius: 10, padding: '0.7rem 1rem' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--muted)' }}>#{i+1}</span> <strong>{s.style}</strong> ({s.score}%)
              </div>
            ))}
          </div>

          <div style={{ marginTop: '1rem' }}>
            <Link to="/design" className="btn btn-primary" style={{ fontWeight: 700 }}>Proceed to Design Studio</Link>
          </div>
        </div>
      )}
    </div>
  );
}
