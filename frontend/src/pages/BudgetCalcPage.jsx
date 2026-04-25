import { useState, useEffect, useCallback } from 'react';

const qualityFactor = { budget: 0.8, standard: 1.0, premium: 1.35, luxury: 1.85 };
const roomTypeFactor = { 'Living Room': 1.0, 'Bedroom': 0.95, 'Kitchen': 1.25, 'Office': 1.1, 'Bathroom': 1.2, 'Dining Room': 1.05 };
const components = [
  { key: 'furniture', label: 'Furniture cost estimate', base: 850, color: '#a78bfa' },
  { key: 'painting', label: 'Painting cost', base: 95, color: '#22d3ee' },
  { key: 'flooring', label: 'Flooring cost', base: 210, color: '#34d399' },
  { key: 'lighting', label: 'Lighting cost', base: 140, color: '#fbbf24' },
  { key: 'labor', label: 'Labor cost', base: 180, color: '#fb7185' },
];
const inr = (v) => `Rs. ${Math.round(v).toLocaleString('en-IN')}`;

export default function BudgetCalcPage() {
  const [size, setSize] = useState(450);
  const [quality, setQuality] = useState('standard');
  const [roomType, setRoomType] = useState('Living Room');
  const [roomCount, setRoomCount] = useState(1);

  const calc = useCallback(() => {
    const factor = (qualityFactor[quality]||1) * (roomTypeFactor[roomType]||1) * Math.max(1,roomCount);
    const breakdown = components.map(c => ({ ...c, amount: c.base * size * factor }));
    const total = breakdown.reduce((s,c) => s+c.amount, 0);
    return { breakdown, total, min: total*0.88, max: total*1.18, perSqft: total / (size * Math.max(1,roomCount)) };
  }, [size, quality, roomType, roomCount]);

  const { breakdown, total, min, max, perSqft } = calc();

  return (
    <section style={{ maxWidth: 1100, margin: '0 auto', padding: '2rem 1.25rem' }}>
      <h1 className="gradient-text" style={{ fontSize: '2rem', fontWeight: 800 }}>Interior Design Budget Calculator</h1>
      <p style={{ color: '#94a3b8', margin: '.35rem 0 1.2rem' }}>Estimate realistic costs for Indian market and plan your room confidently.</p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
        <article className="card">
          <div style={{ display: 'grid', gap: '.9rem' }}>
            <div>
              <label style={{ display: 'block', color: '#94a3b8', fontSize: '.88rem', marginBottom: '.35rem' }}>Room size (sq ft)</label>
              <input type="range" min={100} max={2000} value={size} onChange={e => setSize(Number(e.target.value))} />
              <div style={{ display: 'flex', justifyContent: 'space-between', color: '#cbd5e1', marginTop: '.25rem' }}><span>100</span><strong>{size} sq ft</strong><span>2000</span></div>
            </div>
            <div>
              <label style={{ display: 'block', color: '#94a3b8', fontSize: '.88rem', marginBottom: '.35rem' }}>Quality level</label>
              <select value={quality} onChange={e => setQuality(e.target.value)}><option value="budget">Budget</option><option value="standard">Standard</option><option value="premium">Premium</option><option value="luxury">Luxury</option></select>
            </div>
            <div>
              <label style={{ display: 'block', color: '#94a3b8', fontSize: '.88rem', marginBottom: '.35rem' }}>Room type</label>
              <select value={roomType} onChange={e => setRoomType(e.target.value)}>{Object.keys(roomTypeFactor).map(r => <option key={r}>{r}</option>)}</select>
            </div>
            <div>
              <label style={{ display: 'block', color: '#94a3b8', fontSize: '.88rem', marginBottom: '.35rem' }}>Number of rooms</label>
              <input type="number" min={1} max={20} value={roomCount} onChange={e => setRoomCount(Number(e.target.value))} />
            </div>
            <button className="btn btn-primary" style={{ justifyContent: 'center' }} onClick={() => window.location.href=`/design?budget=${Math.round(total)}&room_type=${roomType}`}>Plan This Design</button>
          </div>
        </article>

        <article className="card">
          <h3 style={{ marginBottom: '.75rem' }}>Cost Breakdown</h3>
          <div style={{ display: 'grid', gap: '.7rem' }}>
            {breakdown.map(item => {
              const pct = Math.round((item.amount / total) * 100);
              return (
                <div key={item.key} style={{ background: '#0f172a', border: '1px solid #334155', borderRadius: 10, padding: '.65rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '.4rem' }}>
                    <span style={{ color: '#cbd5e1', fontSize: '.9rem' }}>{item.label}</span>
                    <strong style={{ color: '#e2e8f0' }}>{inr(item.amount)}</strong>
                  </div>
                  <div style={{ height: 10, background: '#1e293b', borderRadius: 999, overflow: 'hidden' }}>
                    <div style={{ height: '100%', width: pct+'%', background: `linear-gradient(90deg,${item.color},#a855f7)`, transition: 'width .4s ease' }}></div>
                  </div>
                </div>
              );
            })}
          </div>
          <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid #334155' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ color: '#94a3b8' }}>Estimated Total</span>
              <strong style={{ fontSize: '1.35rem', color: '#ddd6fe' }}>{inr(total)}</strong>
            </div>
            <div style={{ color: '#cbd5e1', marginTop: '.35rem' }}>Range: {inr(min)} - {inr(max)}</div>
          </div>
          <div style={{ marginTop: '1rem', background: '#0f172a', border: '1px solid #334155', borderRadius: 12, padding: '.75rem' }}>
            <h4 style={{ marginBottom: '.45rem' }}>Indian Market Benchmark</h4>
            <div style={{ color: '#94a3b8', fontSize: '.9rem', lineHeight: 1.5 }}>Approx {inr(perSqft)}/sq ft for {quality} {roomType.toLowerCase()} interiors.</div>
          </div>
        </article>
      </div>
    </section>
  );
}
