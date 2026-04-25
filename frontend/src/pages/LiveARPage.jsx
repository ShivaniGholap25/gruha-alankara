import { useState, useRef, useEffect } from 'react';

const furnitureOptions = [
  { name: 'Sofa', icon: 'fa-couch' },
  { name: 'Chair', icon: 'fa-chair' },
  { name: 'Table', icon: 'fa-table' },
  { name: 'Lamp', icon: 'fa-lightbulb' },
  { name: 'Shelf', icon: 'fa-book-open' },
  { name: 'Bed', icon: 'fa-bed' },
];

export default function LiveARPage() {
  const videoRef = useRef(null);
  const [streamRef, setStreamRef] = useState(null);
  const [selected, setSelected] = useState('');
  const [status, setStatus] = useState('Waiting for camera permission...');
  const [cameraReady, setCameraReady] = useState(false);

  useEffect(() => {
    let stream = null;
    (async () => {
      try {
        stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' }, audio: false });
        if (videoRef.current) videoRef.current.srcObject = stream;
        setStreamRef(stream);
        setCameraReady(true);
        setStatus('Camera access granted. Select furniture and take screenshot.');
      } catch {
        setStatus('Unable to access camera. Please allow camera permissions.');
      }
    })();
    return () => { if (stream) stream.getTracks().forEach(t => t.stop()); };
  }, []);

  const takeScreenshot = () => {
    const video = videoRef.current;
    if (!video || !video.videoWidth) { setStatus('Camera feed not ready.'); return; }
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);
    if (selected) {
      ctx.fillStyle = 'rgba(124,58,237,0.85)';
      ctx.fillRect(16, 16, 280, 38);
      ctx.fillStyle = '#fff';
      ctx.font = '18px Segoe UI';
      ctx.fillText(`Placing: ${selected}`, 26, 42);
    }
    const link = document.createElement('a');
    link.download = `ar-visualizer-${Date.now()}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
    setStatus('Screenshot downloaded.');
  };

  return (
    <section style={{ maxWidth: 1200, margin: '0 auto', padding: '2rem 1.25rem' }}>
      <h1 className="gradient-text" style={{ fontSize: '2rem', fontWeight: 800 }}>Live AR Room Visualizer</h1>
      <p style={{ color: '#94a3b8', margin: '.35rem 0 1rem' }}>Preview furniture ideas live through your camera before finalizing your design.</p>

      <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', gap: '1rem' }}>
        <aside className="card">
          <h3 style={{ marginBottom: '.75rem' }}>Instructions</h3>
          <ol style={{ display: 'grid', gap: '.55rem', paddingLeft: '1.15rem', color: '#cbd5e1', lineHeight: 1.45 }}>
            <li>Allow camera access</li>
            <li>Point at your room</li>
            <li>Select furniture to place</li>
            <li>Take screenshot</li>
          </ol>

          <h4 style={{ margin: '1rem 0 .55rem' }}>Furniture Selector</h4>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '.55rem' }}>
            {furnitureOptions.map(item => (
              <button key={item.name} onClick={() => { setSelected(item.name); setStatus(`${item.name} selected. Position your camera.`); }}
                style={{ padding: '.55rem', border: `1px solid ${selected===item.name?'#7c3aed':'#334155'}`, borderRadius: 10, background: selected===item.name?'#7c3aed22':'#0f172a', color: '#e2e8f0', display: 'flex', alignItems: 'center', gap: '.45rem', justifyContent: 'center', cursor: 'pointer' }}>
                <i className={`fas ${item.icon}`}></i> {item.name}
              </button>
            ))}
          </div>

          <div style={{ display: 'grid', gap: '.55rem', marginTop: '1rem' }}>
            <button className="btn btn-primary" style={{ justifyContent: 'center' }} onClick={takeScreenshot}><i className="fas fa-camera"></i> Take Screenshot</button>
            <button className="btn btn-outline" style={{ justifyContent: 'center' }} onClick={() => { setSelected(''); setStatus('Reset done.'); }}><i className="fas fa-rotate-left"></i> Start Over</button>
          </div>
          <p style={{ marginTop: '.75rem', color: '#cbd5e1' }}>{status}</p>
        </aside>

        <article className="card" style={{ padding: '.75rem' }}>
          <div style={{ position: 'relative', borderRadius: 12, overflow: 'hidden', border: '1px solid #334155', background: '#020617' }}>
            <video ref={videoRef} autoPlay playsInline style={{ width: '100%', display: 'block', minHeight: 420, objectFit: 'cover' }}></video>
            {selected && <div style={{ position: 'absolute', right: 10, top: 10, padding: '.35rem .65rem', background: '#7c3aedcc', color: '#fff', borderRadius: 999, fontSize: '.8rem' }}>Placing: {selected}</div>}
            {!cameraReady && <div style={{ position: 'absolute', inset: 0, display: 'grid', placeItems: 'center', color: '#64748b' }}>Camera feed will appear here</div>}
          </div>
        </article>
      </div>
    </section>
  );
}
