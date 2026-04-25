import { useState } from 'react';

const brands = [
  { name: 'IKEA', desc: 'Affordable Scandinavian furniture and home accessories.', site: 'https://www.ikea.com/in/en/' },
  { name: 'Pepperfry', desc: 'Wide online catalog with modern and classic furniture.', site: 'https://www.pepperfry.com/' },
  { name: 'Urban Ladder', desc: 'Contemporary furniture and curated living collections.', site: 'https://www.urbanladder.com/' },
  { name: 'HomeTown', desc: 'Home solutions, decor, and modular furniture options.', site: 'https://www.hometown.in/' },
  { name: '@Home', desc: 'Stylish decor and furniture for every room.', site: 'https://www.athome.co.in/' },
  { name: 'Godrej Interio', desc: 'Trusted Indian brand for home and office interiors.', site: 'https://www.godrejinterio.com/' },
  { name: 'Durian', desc: 'Premium furniture and ergonomic seating collections.', site: 'https://www.durian.in/' },
  { name: 'Nilkamal', desc: 'Practical and durable furniture for homes and offices.', site: 'https://www.nilkamalfurniture.com/' },
];

export default function NearbyShopsPage() {
  const [city, setCity] = useState('Hyderabad');
  const [results, setResults] = useState([]);
  const [status, setStatus] = useState('Use city search or find your live location.');
  const [gmapSrc, setGmapSrc] = useState('https://www.google.com/maps?q=furniture+shops+near+Hyderabad&output=embed');
  const [osmSrc, setOsmSrc] = useState('https://www.openstreetmap.org/export/embed.html?bbox=78.30%2C17.27%2C78.60%2C17.52&layer=mapnik');

  const searchCity = async (c) => {
    const q = c || city || 'Hyderabad';
    setStatus('Searching nearby shops...');
    setGmapSrc(`https://www.google.com/maps?q=${encodeURIComponent('furniture shops near '+q)}&output=embed`);
    try {
      const res = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent('furniture shops near '+q)}&format=json`, { headers: { Accept: 'application/json' } });
      const data = await res.json();
      setResults(Array.isArray(data) ? data.slice(0, 18) : []);
      setStatus(`Showing results for ${q}.`);
      if (data[0]) {
        const lat = Number(data[0].lat), lon = Number(data[0].lon);
        setOsmSrc(`https://www.openstreetmap.org/export/embed.html?bbox=${(lon-0.08).toFixed(4)}%2C${(lat-0.08).toFixed(4)}%2C${(lon+0.08).toFixed(4)}%2C${(lat+0.08).toFixed(4)}&layer=mapnik`);
      }
    } catch { setStatus('Could not fetch shops.'); setResults([]); }
  };

  const findLocation = () => {
    if (!navigator.geolocation) { setStatus('Geolocation not supported.'); return; }
    setStatus('Finding your location...');
    navigator.geolocation.getCurrentPosition(async (pos) => {
      const { latitude: lat, longitude: lon } = pos.coords;
      setGmapSrc(`https://www.google.com/maps?q=furniture+shops+near+${lat},${lon}&output=embed`);
      setOsmSrc(`https://www.openstreetmap.org/export/embed.html?bbox=${(lon-0.08).toFixed(4)}%2C${(lat-0.08).toFixed(4)}%2C${(lon+0.08).toFixed(4)}%2C${(lat+0.08).toFixed(4)}&layer=mapnik&marker=${lat}%2C${lon}`);
      try {
        const res = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent('furniture shops near '+lat+','+lon)}&format=json`, { headers: { Accept: 'application/json' } });
        const data = await res.json();
        setResults(Array.isArray(data) ? data.slice(0, 18) : []);
        setStatus('Nearby shops loaded.');
      } catch { setStatus('Location found, but shops failed to load.'); }
    }, () => setStatus('Unable to retrieve location.'));
  };

  return (
    <section style={{ maxWidth: 1200, margin: '0 auto', padding: '2rem 1.25rem' }}>
      <h1 className="gradient-text" style={{ fontSize: '2rem', fontWeight: 800 }}>Furniture Shops Near You</h1>
      <p style={{ color: '#94a3b8', margin: '.35rem 0 1rem' }}>Discover nearby furniture stores and explore trusted brands.</p>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
        <div>
          <label style={{ display: 'block', color: '#94a3b8', fontSize: '.88rem', marginBottom: '.4rem' }}>Search by city</label>
          <div style={{ display: 'flex', gap: '.55rem' }}>
            <input value={city} onChange={e => setCity(e.target.value)} onKeyDown={e => e.key==='Enter' && searchCity()} placeholder="Enter city name" style={{ flex: 1, background: '#111827', border: '1px solid #334155', color: '#e2e8f0', borderRadius: 10, padding: '.75rem .85rem' }} />
            <button className="btn btn-primary" onClick={() => searchCity()}>Search</button>
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'flex-end' }}>
          <button className="btn btn-outline" style={{ width: '100%', justifyContent: 'center' }} onClick={findLocation}><i className="fas fa-location-dot"></i> Find My Location</button>
        </div>
      </div>

      <p style={{ color: '#cbd5e1', marginBottom: '1rem' }}>{status}</p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
        <article className="card" style={{ padding: '.75rem' }}>
          <h3 style={{ marginBottom: '.55rem' }}>Google Maps View</h3>
          <iframe src={gmapSrc} style={{ width: '100%', height: 400, borderRadius: 12, border: 'none' }} title="Google Maps"></iframe>
        </article>
        <article className="card" style={{ padding: '.75rem' }}>
          <h3 style={{ marginBottom: '.55rem' }}>OpenStreetMap View</h3>
          <iframe src={osmSrc} style={{ width: '100%', height: 400, borderRadius: 12, border: 'none' }} title="OpenStreetMap"></iframe>
        </article>
      </div>

      <article className="card" style={{ marginBottom: '1rem' }}>
        <h3 style={{ marginBottom: '.75rem' }}>Nearby Search Results</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,minmax(0,1fr))', gap: '.75rem' }}>
          {results.length ? results.map((p, i) => (
            <article key={i} style={{ background: '#0f172a', border: '1px solid #334155', borderRadius: 12, padding: '.8rem' }}>
              <h4 style={{ marginBottom: '.35rem' }}>{(p.display_name||'').split(',')[0] || 'Store'}</h4>
              <p style={{ color: '#94a3b8', fontSize: '.85rem', lineHeight: 1.45, minHeight: 56 }}>{p.display_name || 'N/A'}</p>
            </article>
          )) : <div style={{ gridColumn: '1/-1', border: '1px dashed #334155', borderRadius: 10, padding: '1rem', color: '#94a3b8' }}>No shops found. Try another city.</div>}
        </div>
      </article>

      <article className="card">
        <h3 style={{ marginBottom: '.85rem' }}>Popular Furniture Brands</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,minmax(0,1fr))', gap: '.75rem' }}>
          {brands.map(b => (
            <article key={b.name} style={{ background: '#0f172a', border: '1px solid #334155', borderRadius: 12, padding: '.8rem', display: 'flex', flexDirection: 'column', gap: '.5rem' }}>
              <div style={{ height: 52, borderRadius: 10, border: '1px dashed #475569', display: 'grid', placeItems: 'center', color: '#a5b4fc', fontWeight: 700 }}>{b.name}</div>
              <h4>{b.name}</h4>
              <p style={{ color: '#94a3b8', fontSize: '.85rem', lineHeight: 1.45, minHeight: 56 }}>{b.desc}</p>
              <a href={b.site} target="_blank" rel="noopener noreferrer" className="btn btn-outline" style={{ justifyContent: 'center' }}>View Catalog</a>
            </article>
          ))}
        </div>
      </article>
    </section>
  );
}
