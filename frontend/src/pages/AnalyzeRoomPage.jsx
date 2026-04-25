import { useState, useRef } from 'react';
import { Link } from 'react-router-dom';
import './AnalyzeRoomPage.css';

export default function AnalyzeRoomPage() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [roomType, setRoomType] = useState('Living Room');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const inputRef = useRef(null);

  const handleFile = (f) => {
    if (!f) return;
    setFile(f);
    const reader = new FileReader();
    reader.onload = (e) => setPreview(e.target.result);
    reader.readAsDataURL(f);
  };

  const analyze = async () => {
    if (!file) { alert('Please upload a room photo first.'); return; }
    setLoading(true);
    setResult(null);
    const fd = new FormData();
    fd.append('image', file);
    fd.append('room_type', roomType);
    try {
      const res = await fetch('/analyze-room', { method: 'POST', body: fd, credentials: 'include' });
      const data = await res.json();
      if (!res.ok || data.error) throw new Error(data.error || 'Analysis failed');
      setResult(data);
    } catch (e) {
      alert(e.message || 'Analysis failed.');
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
            <p style={{ color: 'var(--dim)', fontSize: '0.85rem' }}>Supports JPG, PNG, WEBP, GIF</p>
          </div>
        ) : (
          <div style={{ position: 'relative' }}>
            <img src={preview} alt="Room preview" style={{ width: '100%', maxHeight: 350, objectFit: 'cover', borderRadius: 12 }} />
            <button onClick={() => inputRef.current?.click()} style={{ position: 'absolute', bottom: 12, right: 12, background: 'rgba(0,0,0,0.75)', color: 'white', border: 'none', borderRadius: 8, padding: '0.5rem 1rem', cursor: 'pointer' }}>
              <i className="fas fa-sync" style={{ marginRight: 4 }}></i>Change Photo
            </button>
          </div>
        )}
        <input ref={inputRef} type="file" accept="image/*" style={{ display: 'none' }} onChange={(e) => handleFile(e.target.files[0])} />
      </div>

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

      {result && (
        <div className="analyze-step fade-in">
          <h3 style={{ marginBottom: '0.8rem' }}>Analysis Complete</h3>
          <p style={{ color: 'var(--muted)', lineHeight: 1.6 }}>Dimensions: {result.dimensions.width} x {result.dimensions.length} x {result.dimensions.height} ft ({result.dimensions.area} sq ft)</p>
          <p style={{ color: 'var(--muted)', lineHeight: 1.6 }}>Lighting: {result.lighting.quality} ({result.lighting.brightness}/255)</p>
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
