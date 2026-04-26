import { useState, useRef, useEffect, useCallback } from 'react';

const FURNITURE = [
  { name: 'Sofa',  icon: 'fa-couch',     emoji: '🛋️', color: '#7c3aed' },
  { name: 'Chair', icon: 'fa-chair',     emoji: '🪑', color: '#2563eb' },
  { name: 'Table', icon: 'fa-table',     emoji: '🪵', color: '#059669' },
  { name: 'Lamp',  icon: 'fa-lightbulb', emoji: '💡', color: '#d97706' },
  { name: 'Shelf', icon: 'fa-book-open', emoji: '📚', color: '#dc2626' },
  { name: 'Bed',   icon: 'fa-bed',       emoji: '🛏️', color: '#7c3aed' },
];

// SVG-based furniture shapes drawn on canvas (no external images needed)
function drawFurnitureShape(ctx, name, x, y, w, h) {
  ctx.save();
  const shapes = {
    Sofa: () => {
      // Body
      ctx.fillStyle = '#7c3aed';
      ctx.beginPath(); ctx.roundRect(x, y + h * 0.3, w, h * 0.55, 12); ctx.fill();
      // Back
      ctx.fillStyle = '#6d28d9';
      ctx.beginPath(); ctx.roundRect(x, y, w, h * 0.38, 12); ctx.fill();
      // Armrests
      ctx.fillStyle = '#5b21b6';
      ctx.beginPath(); ctx.roundRect(x, y + h * 0.15, w * 0.12, h * 0.7, 8); ctx.fill();
      ctx.beginPath(); ctx.roundRect(x + w * 0.88, y + h * 0.15, w * 0.12, h * 0.7, 8); ctx.fill();
      // Cushions
      ctx.fillStyle = '#8b5cf6';
      ctx.beginPath(); ctx.roundRect(x + w * 0.14, y + h * 0.35, w * 0.33, h * 0.42, 8); ctx.fill();
      ctx.beginPath(); ctx.roundRect(x + w * 0.53, y + h * 0.35, w * 0.33, h * 0.42, 8); ctx.fill();
      // Legs
      ctx.fillStyle = '#4c1d95';
      ctx.fillRect(x + w * 0.1, y + h * 0.82, w * 0.08, h * 0.18);
      ctx.fillRect(x + w * 0.82, y + h * 0.82, w * 0.08, h * 0.18);
    },
    Chair: () => {
      ctx.fillStyle = '#2563eb';
      ctx.beginPath(); ctx.roundRect(x + w * 0.1, y + h * 0.35, w * 0.8, h * 0.35, 8); ctx.fill();
      ctx.fillStyle = '#1d4ed8';
      ctx.beginPath(); ctx.roundRect(x + w * 0.1, y, w * 0.8, h * 0.4, 8); ctx.fill();
      ctx.fillStyle = '#1e3a8a';
      ctx.fillRect(x + w * 0.12, y + h * 0.68, w * 0.12, h * 0.32);
      ctx.fillRect(x + w * 0.76, y + h * 0.68, w * 0.12, h * 0.32);
      ctx.fillRect(x + w * 0.12, y + h * 0.35, w * 0.08, h * 0.35);
      ctx.fillRect(x + w * 0.8, y + h * 0.35, w * 0.08, h * 0.35);
    },
    Table: () => {
      ctx.fillStyle = '#92400e';
      ctx.beginPath(); ctx.roundRect(x, y + h * 0.1, w, h * 0.18, 6); ctx.fill();
      ctx.fillStyle = '#78350f';
      ctx.fillRect(x + w * 0.08, y + h * 0.28, w * 0.1, h * 0.72);
      ctx.fillRect(x + w * 0.82, y + h * 0.28, w * 0.1, h * 0.72);
      ctx.fillStyle = '#a16207';
      ctx.beginPath(); ctx.roundRect(x, y, w, h * 0.14, 4); ctx.fill();
    },
    Lamp: () => {
      // Shade
      ctx.fillStyle = '#fbbf24';
      ctx.beginPath();
      ctx.moveTo(x + w * 0.2, y + h * 0.35);
      ctx.lineTo(x + w * 0.8, y + h * 0.35);
      ctx.lineTo(x + w * 0.65, y);
      ctx.lineTo(x + w * 0.35, y);
      ctx.closePath(); ctx.fill();
      // Glow
      ctx.fillStyle = 'rgba(251,191,36,0.25)';
      ctx.beginPath(); ctx.ellipse(x + w / 2, y + h * 0.35, w * 0.5, h * 0.2, 0, 0, Math.PI * 2); ctx.fill();
      // Pole
      ctx.fillStyle = '#78716c';
      ctx.fillRect(x + w * 0.46, y + h * 0.35, w * 0.08, h * 0.5);
      // Base
      ctx.fillStyle = '#57534e';
      ctx.beginPath(); ctx.roundRect(x + w * 0.25, y + h * 0.82, w * 0.5, h * 0.18, 6); ctx.fill();
    },
    Shelf: () => {
      ctx.fillStyle = '#92400e';
      for (let i = 0; i < 3; i++) {
        const sy = y + (h / 3) * i;
        ctx.beginPath(); ctx.roundRect(x, sy + h * 0.08, w, h * 0.1, 4); ctx.fill();
      }
      ctx.fillStyle = '#78350f';
      ctx.fillRect(x, y, w * 0.07, h);
      ctx.fillRect(x + w * 0.93, y, w * 0.07, h);
      // Books
      const bookColors = ['#ef4444','#3b82f6','#10b981','#f59e0b','#8b5cf6'];
      let bx = x + w * 0.1;
      bookColors.forEach((c, i) => {
        ctx.fillStyle = c;
        ctx.fillRect(bx + i * (w * 0.14), y + h * 0.12, w * 0.1, h * 0.22);
      });
    },
    Bed: () => {
      // Frame
      ctx.fillStyle = '#92400e';
      ctx.beginPath(); ctx.roundRect(x, y + h * 0.25, w, h * 0.65, 8); ctx.fill();
      // Headboard
      ctx.fillStyle = '#78350f';
      ctx.beginPath(); ctx.roundRect(x, y, w, h * 0.35, 10); ctx.fill();
      // Mattress
      ctx.fillStyle = '#e2e8f0';
      ctx.beginPath(); ctx.roundRect(x + w * 0.03, y + h * 0.28, w * 0.94, h * 0.5, 6); ctx.fill();
      // Pillow
      ctx.fillStyle = '#f8fafc';
      ctx.beginPath(); ctx.roundRect(x + w * 0.08, y + h * 0.3, w * 0.35, h * 0.2, 8); ctx.fill();
      ctx.beginPath(); ctx.roundRect(x + w * 0.57, y + h * 0.3, w * 0.35, h * 0.2, 8); ctx.fill();
      // Blanket
      ctx.fillStyle = '#7c3aed';
      ctx.beginPath(); ctx.roundRect(x + w * 0.03, y + h * 0.5, w * 0.94, h * 0.28, 6); ctx.fill();
      // Legs
      ctx.fillStyle = '#4c1d95';
      ctx.fillRect(x + w * 0.05, y + h * 0.88, w * 0.08, h * 0.12);
      ctx.fillRect(x + w * 0.87, y + h * 0.88, w * 0.08, h * 0.12);
    },
  };
  (shapes[name] || shapes.Chair)();

  // Label
  ctx.fillStyle = 'rgba(0,0,0,0.55)';
  ctx.beginPath(); ctx.roundRect(x + w * 0.2, y + h + 6, w * 0.6, 24, 6); ctx.fill();
  ctx.fillStyle = '#fff';
  ctx.font = `bold ${Math.max(12, w * 0.13)}px sans-serif`;
  ctx.textAlign = 'center';
  ctx.fillText(name, x + w / 2, y + h + 23);
  ctx.restore();
}

export default function LiveARPage() {
  const videoRef  = useRef(null);
  const canvasRef = useRef(null);
  const rafRef    = useRef(null);
  const posRef    = useRef({ x: 0.5, y: 0.5 }); // normalized 0-1
  const dragRef   = useRef({ dragging: false, startX: 0, startY: 0 });
  const scaleRef  = useRef(1);

  const [selected,    setSelected]    = useState('');
  const [status,      setStatus]      = useState('Waiting for camera permission...');
  const [cameraReady, setCameraReady] = useState(false);
  const [show360,     setShow360]     = useState(false);
  const [isMobile,    setIsMobile]    = useState(window.innerWidth < 768);

  // ── Resize canvas to match container ──────────────────────────────────────
  const resizeCanvas = useCallback(() => {
    const canvas = canvasRef.current;
    const video  = videoRef.current;
    if (!canvas) return;
    const parent = canvas.parentElement;
    canvas.width  = parent ? parent.clientWidth  : window.innerWidth;
    canvas.height = parent ? parent.clientHeight : window.innerHeight;
    setIsMobile(window.innerWidth < 768);
    if (video) { video.width = canvas.width; video.height = canvas.height; }
  }, []);

  // ── Render loop ────────────────────────────────────────────────────────────
  const renderLoop = useCallback(() => {
    const canvas = canvasRef.current;
    const video  = videoRef.current;
    if (!canvas || !video) { rafRef.current = requestAnimationFrame(renderLoop); return; }

    const ctx = canvas.getContext('2d');
    const W = canvas.width, H = canvas.height;

    // 1. Draw camera feed
    if (video.readyState >= 2) {
      ctx.drawImage(video, 0, 0, W, H);
    } else {
      ctx.fillStyle = '#020617';
      ctx.fillRect(0, 0, W, H);
    }

    // 2. Draw selected furniture
    if (selected) {
      const size = Math.min(W, H) * 0.32 * scaleRef.current;
      const cx   = posRef.current.x * W;
      const cy   = posRef.current.y * H;
      const fx   = cx - size / 2;
      const fy   = cy - size / 2;

      // Shadow
      ctx.save();
      ctx.shadowColor = 'rgba(0,0,0,0.5)';
      ctx.shadowBlur  = 20;
      ctx.shadowOffsetY = 8;
      drawFurnitureShape(ctx, selected, fx, fy, size, size);
      ctx.restore();

      // Drag handle ring
      ctx.strokeStyle = 'rgba(255,255,255,0.6)';
      ctx.lineWidth   = 2;
      ctx.setLineDash([6, 4]);
      ctx.strokeRect(fx - 4, fy - 4, size + 8, size + 8);
      ctx.setLineDash([]);

      // Corner drag hint
      ctx.fillStyle = 'rgba(124,58,237,0.9)';
      [[fx-4,fy-4],[fx+size+4,fy-4],[fx-4,fy+size+4],[fx+size+4,fy+size+4]].forEach(([px,py]) => {
        ctx.beginPath(); ctx.arc(px, py, 6, 0, Math.PI*2); ctx.fill();
      });
    }

    // 3. HUD overlay
    if (selected) {
      ctx.fillStyle = 'rgba(124,58,237,0.85)';
      ctx.beginPath(); ctx.roundRect(10, 10, 200, 32, 8); ctx.fill();
      ctx.fillStyle = '#fff';
      ctx.font = 'bold 14px sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText(`📍 Placing: ${selected}`, 18, 31);
    }

    // 4. Drag hint (first 3 seconds)
    if (selected && !dragRef.current.hasHinted) {
      ctx.fillStyle = 'rgba(0,0,0,0.5)';
      ctx.beginPath(); ctx.roundRect(W/2 - 110, H - 50, 220, 32, 8); ctx.fill();
      ctx.fillStyle = '#fff';
      ctx.font = '13px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('Drag to reposition • Pinch/scroll to resize', W/2, H - 29);
    }

    rafRef.current = requestAnimationFrame(renderLoop);
  }, [selected]);

  // ── Start camera ───────────────────────────────────────────────────────────
  useEffect(() => {
    let stream = null;
    (async () => {
      try {
        stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } },
          audio: false,
        });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.onloadedmetadata = () => {
            videoRef.current.play();
            resizeCanvas();
            setCameraReady(true);
            setStatus('Camera ready. Select furniture and drag to position it.');
          };
        }
      } catch {
        setStatus('Camera access denied. Please allow camera permissions.');
      }
    })();
    return () => { if (stream) stream.getTracks().forEach(t => t.stop()); };
  }, [resizeCanvas]);

  // ── Render loop lifecycle ──────────────────────────────────────────────────
  useEffect(() => {
    rafRef.current = requestAnimationFrame(renderLoop);
    return () => cancelAnimationFrame(rafRef.current);
  }, [renderLoop]);

  // ── Resize listener ────────────────────────────────────────────────────────
  useEffect(() => {
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();
    return () => window.removeEventListener('resize', resizeCanvas);
  }, [resizeCanvas]);

  // ── Drag to move furniture ─────────────────────────────────────────────────
  const getPos = (e, canvas) => {
    const r = canvas.getBoundingClientRect();
    const src = e.touches ? e.touches[0] : e;
    return { x: (src.clientX - r.left) / r.width, y: (src.clientY - r.top) / r.height };
  };

  const onPointerDown = (e) => {
    if (!selected) return;
    dragRef.current.dragging = true;
    dragRef.current.hasHinted = true;
    const p = getPos(e, canvasRef.current);
    dragRef.current.startX = p.x - posRef.current.x;
    dragRef.current.startY = p.y - posRef.current.y;
  };
  const onPointerMove = (e) => {
    if (!dragRef.current.dragging) return;
    e.preventDefault();
    const p = getPos(e, canvasRef.current);
    posRef.current = {
      x: Math.min(0.9, Math.max(0.1, p.x - dragRef.current.startX)),
      y: Math.min(0.9, Math.max(0.1, p.y - dragRef.current.startY)),
    };
  };
  const onPointerUp = () => { dragRef.current.dragging = false; };

  // ── Scroll/pinch to scale ──────────────────────────────────────────────────
  const onWheel = (e) => {
    e.preventDefault();
    scaleRef.current = Math.min(2.5, Math.max(0.3, scaleRef.current - e.deltaY * 0.001));
  };

  // ── Screenshot ─────────────────────────────────────────────────────────────
  const takeScreenshot = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const link = document.createElement('a');
    link.download = `ar-gruha-${Date.now()}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
    setStatus('Screenshot saved!');
  };

  const selectFurniture = (name) => {
    setSelected(name);
    posRef.current = { x: 0.5, y: 0.5 };
    scaleRef.current = 1;
    dragRef.current.hasHinted = false;
    setStatus(`${name} selected. Drag to reposition. Scroll to resize.`);
  };

  return (
    <section style={{ maxWidth: 1200, margin: '0 auto', padding: '2rem 1.25rem' }}>
      <h1 className="gradient-text" style={{ fontSize: '2rem', fontWeight: 800 }}>Live AR Room Visualizer</h1>
      <p style={{ color: '#94a3b8', margin: '.35rem 0 1rem' }}>
        Select furniture, drag to position, scroll to resize — all live on your camera feed.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr' : '280px 1fr', gap: '1rem' }}>

        {/* ── Sidebar ── */}
        <aside className="card" style={{ display: 'flex', flexDirection: 'column', gap: '.75rem' }}>
          <div>
            <h3 style={{ marginBottom: '.5rem' }}>How to use</h3>
            <ol style={{ paddingLeft: '1.1rem', color: '#cbd5e1', lineHeight: 1.6, fontSize: '.88rem' }}>
              <li>Allow camera access</li>
              <li>Select a furniture item</li>
              <li>Drag it to position</li>
              <li>Scroll/pinch to resize</li>
              <li>Take a screenshot</li>
            </ol>
          </div>

          <div>
            <h4 style={{ marginBottom: '.5rem' }}>Furniture</h4>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '.45rem' }}>
              {FURNITURE.map(item => (
                <button key={item.name}
                  onClick={() => selectFurniture(item.name)}
                  style={{
                    padding: '.5rem .4rem',
                    border: `2px solid ${selected === item.name ? item.color : '#334155'}`,
                    borderRadius: 10,
                    background: selected === item.name ? `${item.color}22` : '#0f172a',
                    color: '#e2e8f0',
                    display: 'flex', alignItems: 'center', gap: '.4rem',
                    justifyContent: 'center', cursor: 'pointer',
                    fontSize: '.85rem', fontWeight: selected === item.name ? 700 : 400,
                    transition: 'all .15s',
                  }}>
                  <i className={`fas ${item.icon}`} style={{ color: selected === item.name ? item.color : '#94a3b8' }}></i>
                  {item.name}
                </button>
              ))}
            </div>
          </div>

          {/* Scale slider */}
          {selected && (
            <div>
              <h4 style={{ marginBottom: '.4rem', fontSize: '.85rem' }}>Size</h4>
              <input type="range" min="30" max="250" defaultValue="100"
                style={{ width: '100%', accentColor: '#7c3aed' }}
                onChange={e => { scaleRef.current = e.target.value / 100; }} />
            </div>
          )}

          <div style={{ display: 'grid', gap: '.45rem' }}>
            <button className="btn btn-primary" style={{ justifyContent: 'center' }} onClick={takeScreenshot}>
              <i className="fas fa-camera"></i> Screenshot
            </button>
            <button className="btn btn-outline" style={{ justifyContent: 'center' }}
              onClick={() => { setSelected(''); setStatus('Reset. Select furniture to start.'); }}>
              <i className="fas fa-rotate-left"></i> Reset
            </button>
            <button className="btn btn-outline" style={{ justifyContent: 'center', borderColor: '#0ea5e9', color: '#0ea5e9' }}
              onClick={() => setShow360(true)}>
              <i className="fas fa-cube"></i> 360° View
            </button>
          </div>

          <p style={{ color: '#94a3b8', fontSize: '.85rem', marginTop: 'auto' }}>{status}</p>
        </aside>

        {/* ── Canvas AR view ── */}
        <article className="card" style={{ padding: '.75rem' }}>
          <div style={{ position: 'relative', borderRadius: 12, overflow: 'hidden',
            border: '1px solid #334155', background: '#020617',
            minHeight: isMobile ? 300 : 480 }}>

            {/* Hidden video — source for canvas */}
            <video ref={videoRef} autoPlay playsInline muted
              style={{ position: 'absolute', opacity: 0, pointerEvents: 'none', width: 1, height: 1 }} />

            {/* Canvas — the actual AR display */}
            <canvas ref={canvasRef}
              style={{ display: 'block', width: '100%', height: '100%', cursor: selected ? 'grab' : 'default', touchAction: 'none' }}
              onMouseDown={onPointerDown}
              onMouseMove={onPointerMove}
              onMouseUp={onPointerUp}
              onMouseLeave={onPointerUp}
              onTouchStart={onPointerDown}
              onTouchMove={onPointerMove}
              onTouchEnd={onPointerUp}
              onWheel={onWheel}
            />

            {!cameraReady && (
              <div style={{ position: 'absolute', inset: 0, display: 'grid', placeItems: 'center',
                color: '#64748b', flexDirection: 'column', gap: '.5rem' }}>
                <i className="fas fa-camera" style={{ fontSize: '2rem' }}></i>
                <span>Camera feed will appear here</span>
              </div>
            )}
          </div>
          <p style={{ color: '#475569', fontSize: '.78rem', marginTop: '.5rem', textAlign: 'center' }}>
            Drag furniture to reposition • Scroll to resize • Screenshot to save
          </p>
        </article>
      </div>

      {/* ── 360° Modal ── */}
      {show360 && (
        <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.85)', zIndex: 9999,
          display: 'grid', placeItems: 'center' }} onClick={() => setShow360(false)}>
          <div style={{ background: '#1a1a2e', border: '1px solid #334155', borderRadius: 16,
            padding: '2rem', maxWidth: 480, width: '90%', textAlign: 'center' }}
            onClick={e => e.stopPropagation()}>
            <h2 style={{ marginBottom: '.75rem' }}>360° Room View</h2>
            <p style={{ color: '#94a3b8', marginBottom: '1.5rem', fontSize: '.9rem' }}>
              Full 360° AR visualization requires a WebXR-compatible device.<br />
              Use the Live AR view above for real-time furniture placement.
            </p>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '.75rem', marginBottom: '1.5rem' }}>
              {FURNITURE.map(f => (
                <div key={f.name} style={{ background: '#0f172a', borderRadius: 10, padding: '.75rem',
                  border: '1px solid #334155', fontSize: '1.5rem', textAlign: 'center' }}>
                  {f.emoji}<br />
                  <span style={{ fontSize: '.75rem', color: '#94a3b8' }}>{f.name}</span>
                </div>
              ))}
            </div>
            <button className="btn btn-primary" style={{ justifyContent: 'center', width: '100%' }}
              onClick={() => setShow360(false)}>
              <i className="fas fa-times"></i> Close
            </button>
          </div>
        </div>
      )}
    </section>
  );
}
