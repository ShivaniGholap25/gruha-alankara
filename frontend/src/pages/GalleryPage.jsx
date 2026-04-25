import { useState } from 'react';

const images = [
  { category: 'Living Room', style: 'Modern', src: 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400', title: 'Modern Living Serenity' },
  { category: 'Bedroom', style: 'Scandinavian', src: 'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400', title: 'Cozy Bedroom Calm' },
  { category: 'Kitchen', style: 'Contemporary', src: 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400', title: 'Bright Kitchen Flow' },
  { category: 'Office', style: 'Industrial', src: 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=400', title: 'Focused Work Nook' },
  { category: 'Bathroom', style: 'Minimalist', src: 'https://images.unsplash.com/photo-1507652313519-d4e9174996dd?w=400', title: 'Calm Bathroom Spa' },
  { category: 'Living Room', style: 'Bohemian', src: 'https://images.unsplash.com/photo-1522444195799-478538b28823?w=400', title: 'Boho Textured Lounge' },
  { category: 'Bedroom', style: 'Traditional', src: 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=400', title: 'Classic Bedroom Craft' },
  { category: 'Kitchen', style: 'Modern', src: 'https://images.unsplash.com/photo-1484154218962-a197022b5858?w=400', title: 'Sleek Kitchen Lines' },
  { category: 'Office', style: 'Scandinavian', src: 'https://images.unsplash.com/photo-1486946255434-2466348c2166?w=400', title: 'Nordic Office Desk' },
  { category: 'Bathroom', style: 'Luxury', src: 'https://images.unsplash.com/photo-1616594039964-0f6b2d5243d2?w=400', title: 'Luxury Marble Bath' },
];

const tabs = ['All', 'Living Room', 'Bedroom', 'Kitchen', 'Office', 'Bathroom'];

export default function GalleryPage() {
  const [activeTab, setActiveTab] = useState('All');
  const [lightbox, setLightbox] = useState(null);
  const [likes, setLikes] = useState(() => {
    try { return JSON.parse(localStorage.getItem('gallery_likes') || '{}'); } catch { return {}; }
  });

  const filtered = activeTab === 'All' ? images : images.filter(i => i.category === activeTab);

  const toggleLike = (title) => {
    const next = { ...likes, [title]: !likes[title] };
    setLikes(next);
    localStorage.setItem('gallery_likes', JSON.stringify(next));
  };

  const saveMood = (img) => {
    const saved = JSON.parse(localStorage.getItem('mood_board_saved_styles') || '[]');
    if (!saved.find(x => x.title === img.title)) { saved.push(img); localStorage.setItem('mood_board_saved_styles', JSON.stringify(saved)); }
  };

  return (
    <section style={{ maxWidth: 1220, margin: '0 auto', padding: '2rem 1.25rem' }}>
      <h1 className="gradient-text" style={{ fontSize: '2rem', fontWeight: 800 }}>Design Inspiration Gallery</h1>
      <p style={{ color: '#94a3b8', margin: '.35rem 0 1rem' }}>Explore visual styles, like your favorites, and send ideas to your mood board.</p>

      <div style={{ display: 'flex', gap: '.55rem', flexWrap: 'wrap', marginBottom: '1rem' }}>
        {tabs.map(tab => (
          <button key={tab} onClick={() => setActiveTab(tab)} style={{ padding: '.45rem .85rem', borderRadius: 999, border: activeTab===tab?'none':'1px solid #334155', background: activeTab===tab?'linear-gradient(135deg,#7c3aed,#a855f7)':'#111827', color: activeTab===tab?'#fff':'#cbd5e1', cursor: 'pointer' }}>{tab}</button>
        ))}
      </div>

      <div style={{ columnCount: 3, columnGap: '1rem' }}>
        {filtered.map((img, idx) => (
          <article key={idx} style={{ breakInside: 'avoid', background: '#111827', border: '1px solid #334155', borderRadius: 12, overflow: 'hidden', margin: '0 0 1rem' }}>
            <img src={img.src} alt={img.title} style={{ width: '100%', display: 'block', cursor: 'pointer' }} onClick={() => setLightbox(img)} loading="lazy" />
            <div style={{ padding: '.75rem', display: 'grid', gap: '.45rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '.4rem' }}>
                <strong style={{ fontSize: '.95rem' }}>{img.title}</strong>
                <span style={{ padding: '.2rem .5rem', borderRadius: 999, background: '#7c3aed22', border: '1px solid #7c3aed66', color: '#c4b5fd', fontSize: '.75rem' }}>{img.style}</span>
              </div>
              <div style={{ display: 'flex', gap: '.45rem', flexWrap: 'wrap' }}>
                <button onClick={() => toggleLike(img.title)} style={{ padding: '.4rem .65rem', border: '1px solid #334155', borderRadius: 8, background: likes[img.title]?'#ef444422':'transparent', color: likes[img.title]?'#fecaca':'#cbd5e1', cursor: 'pointer' }}>{likes[img.title]?'♥ Liked':'♡ Like'}</button>
                <a href={`/design?style=${encodeURIComponent(img.style)}`} className="btn btn-primary" style={{ padding: '.4rem .65rem' }}>Use Style</a>
                <button onClick={() => { saveMood(img); alert('Saved!'); }} style={{ padding: '.4rem .65rem', border: '1px solid #334155', borderRadius: 8, background: 'transparent', color: '#cbd5e1', cursor: 'pointer' }}>Save to Mood Board</button>
              </div>
            </div>
          </article>
        ))}
      </div>

      {lightbox && (
        <div style={{ position: 'fixed', inset: 0, background: 'rgba(2,6,23,.82)', zIndex: 1800, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '1rem' }} onClick={e => { if (e.target === e.currentTarget) setLightbox(null); }}>
          <div style={{ width: 'min(960px,100%)', background: '#111827', border: '1px solid #334155', borderRadius: 14, overflow: 'hidden' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '.8rem 1rem', borderBottom: '1px solid #334155' }}>
              <strong>{lightbox.title}</strong>
              <button onClick={() => setLightbox(null)} style={{ background: 'none', border: 'none', color: '#cbd5e1', cursor: 'pointer', fontSize: '1.1rem' }}>×</button>
            </div>
            <img src={lightbox.src.replace('w=400','w=1200')} alt={lightbox.title} style={{ width: '100%', maxHeight: '70vh', objectFit: 'cover', display: 'block' }} />
            <div style={{ padding: '.85rem 1rem', color: '#cbd5e1' }}><strong>{lightbox.style}</strong> • {lightbox.category}</div>
          </div>
        </div>
      )}
    </section>
  );
}
