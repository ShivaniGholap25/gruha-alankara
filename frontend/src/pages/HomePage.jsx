import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';

function useAnimatedCounter(target, duration = 2000) {
  const [value, setValue] = useState(0);
  const ref = useRef(null);
  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        let start = 0;
        const step = target / (duration / 16);
        const timer = setInterval(() => {
          start += step;
          if (start >= target) { start = target; clearInterval(timer); }
          setValue(Math.floor(start));
        }, 16);
        observer.disconnect();
      }
    }, { threshold: 0.3 });
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, [target, duration]);
  return [value, ref];
}

const faqs = [
  { id: 'Q01', question: 'What is Gruha Alankara?', answer: 'Gruha Alankara is an AI-powered interior design platform that helps you visualize and plan your perfect home. Upload a room photo, choose a style, and get instant AI-generated design recommendations.' },
  { id: 'Q02', question: 'Do I need design experience to use this?', answer: 'Not at all! Gruha Alankara is designed for everyone. Simply upload your room photo, take our Style Quiz, and let the AI handle the rest. No design experience needed.' },
  { id: 'Q03', question: 'Is the Buddy AI chatbot free?', answer: 'Yes! The Gruha Buddy AI chatbot is completely free and supports English, Hindi and Telugu. It can help you with furniture selection, booking, pricing and design tips.' },
  { id: 'Q04', question: 'How accurate is the room analysis?', answer: 'Our AI analyzes your room photo to extract dimensions, lighting quality, dominant colors and structural features. Results are estimates based on image analysis and improve with better quality photos.' },
  { id: 'Q05', question: 'Can I book furniture directly from the app?', answer: 'Yes! Browse our furniture catalog, select items that match your design, and book them directly. You can track all your bookings in the My Bookings section.' },
];

const tools = [
  { icon: 'fa-brain', title: 'AI Style Engine', desc: 'Generates thematic spaces from your room preferences in seconds.' },
  { icon: 'fa-camera', title: 'Room Analysis', desc: 'Detects dimensions, lighting, and color composition from photos.' },
  { icon: 'fa-couch', title: 'Furniture Planning', desc: 'Creates practical furniture layouts for movement and comfort.' },
  { icon: 'fa-wallet', title: 'Budget Split', desc: 'Distributes spending across furniture, decor, paint, and labor.' },
  { icon: 'fa-cubes', title: '3D + AR View', desc: 'Preview your concept in a spatial walkthrough before execution.' },
  { icon: 'fa-bookmark', title: 'Catalog Save', desc: 'Store and compare multiple design concepts in one place.' },
];

const styles = [
  { name: 'Modern Minimalist', desc: 'Clean lines with balanced neutral palettes.', img: 'https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=900&q=80' },
  { name: 'Scandinavian', desc: 'Light wood tones and cozy layered textures.', img: 'https://images.unsplash.com/photo-1519710164239-da123dc03ef4?auto=format&fit=crop&w=900&q=80' },
  { name: 'Industrial', desc: 'Raw finishes with strong architectural character.', img: 'https://images.unsplash.com/photo-1493666438817-866a91353ca9?auto=format&fit=crop&w=900&q=80' },
  { name: 'Bohemian', desc: 'Eclectic layering and expressive decor accents.', img: 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80' },
  { name: 'Traditional', desc: 'Classic forms and rich timeless materials.', img: 'https://images.unsplash.com/photo-1505691938895-1758d7feb511?auto=format&fit=crop&w=900&q=80' },
  { name: 'Contemporary', desc: 'Trend-forward forms with sleek contrast.', img: 'https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=900&q=80' },
  { name: 'Mid-Century', desc: 'Retro silhouettes and warm wood texture.', img: 'https://images.unsplash.com/photo-1503174971373-b1f69850bded?auto=format&fit=crop&w=900&q=80' },
  { name: 'Coastal Calm', desc: 'Airy interiors with soft sea-inspired tones.', img: 'https://images.unsplash.com/photo-1505692794403-35fb6b6fcb32?auto=format&fit=crop&w=900&q=80' },
];

const marqueeText = 'Modern Minimalist \u00a0•\u00a0 Scandinavian \u00a0•\u00a0 Industrial \u00a0•\u00a0 Bohemian \u00a0•\u00a0 Traditional \u00a0•\u00a0 Contemporary \u00a0•\u00a0 AR Visualization \u00a0•\u00a0 AI Design \u00a0•\u00a0 Budget Planner \u00a0•\u00a0 Style Quiz \u00a0•\u00a0 ';

export default function HomePage() {
  const particlesRef = useRef(null);
  const [roomDays, setRoomDays] = useState(0);
  const [openFaq, setOpenFaq] = useState(null);

  const [count1, ref1] = useAnimatedCounter(500);
  const [count2, ref2] = useAnimatedCounter(6, 1000);
  const [count3, ref3] = useAnimatedCounter(10, 1500);
  const [count4, ref4] = useAnimatedCounter(3, 800);

  useEffect(() => {
    const container = particlesRef.current;
    if (container) {
      for (let i = 0; i < 20; i++) {
        const p = document.createElement('div');
        const size = Math.random() * 4 + 2;
        p.style.cssText = `position:absolute;width:${size}px;height:${size}px;background:rgba(124,58,237,${Math.random() * 0.3 + 0.1});border-radius:50%;left:${Math.random() * 100}%;top:${Math.random() * 100}%;animation:float ${Math.random() * 10 + 5}s ease-in-out infinite;animation-delay:${-Math.random() * 10}s;`;
        container.appendChild(p);
      }
    }
  }, []);

  useEffect(() => {
    const timer = setInterval(() => setRoomDays((d) => d + 1), 4000);
    return () => clearInterval(timer);
  }, []);

  return (
    <>
      <section className="hero">
        <div id="particles" ref={particlesRef}></div>
        <div className="hero-inner">
          <p className="hero-tag">— the platform</p>
          <h1 className="gradient-text">गृह अलंकार • Gruha Alankara</h1>
          <p>Premium AI design intelligence for beautiful homes. Upload your room, pick a vibe, and generate refined concepts in seconds.</p>
          <div className="live-counter">
            <span className="live-dot"></span>
            <span>Days since our AI designed <strong>{roomDays}</strong> rooms</span>
          </div>
          <div className="hero-actions">
            <Link to="/dashboard" className="btn btn-primary" style={{ padding: '0.9rem 1.4rem', borderRadius: 10, fontWeight: 700 }}>
              <i className="fas fa-wand-magic-sparkles"></i> Start Designing
            </Link>
            <Link to="/analyze" className="btn btn-outline" style={{ padding: '0.9rem 1.4rem', borderRadius: 10, fontWeight: 700 }}>
              <i className="fas fa-binoculars"></i> Learn More
            </Link>
          </div>
          <div className="hero-highlights">
            <span>🏪 Nearby Shops</span>
            <span>📊 Budget Calc</span>
            <span>🖼️ Gallery</span>
            <span>📷 AR Camera</span>
            <span>🤖 AI Buddy</span>
          </div>
          <div className="hero-stats">
            <div style={{ textAlign: 'center' }} ref={ref1}><div className="stat-number">{count1}+</div><p>Designs Created</p></div>
            <div style={{ textAlign: 'center' }} ref={ref2}><div className="stat-number">{count2}+</div><p>Styles Available</p></div>
            <div style={{ textAlign: 'center' }} ref={ref3}><div className="stat-number">{count3}+</div><p>AI Tools</p></div>
            <div style={{ textAlign: 'center' }} ref={ref4}><div className="stat-number">{count4}</div><p>Languages</p></div>
          </div>

          <div className="terminal-panel">
            <p style={{ color: '#10b981' }}>root@gruha-alankara:~$ show_stats --live</p>
            <p>Loading AI models... <span style={{ color: '#10b981' }}>✓ Done</span></p>
            <p>Styles available: <span style={{ color: '#818cf8' }}>6 themes</span></p>
            <p>Analysis tools: <span style={{ color: '#818cf8' }}>Active</span></p>
            <p>Buddy agent: <span style={{ color: '#10b981' }}>Online ●</span></p>
            <p>Status: <span style={{ color: '#10b981' }}>Ready for design</span></p>
          </div>

          <div className="marquee-wrap">
            <div className="marquee-track">{marqueeText}{marqueeText}</div>
          </div>
        </div>
      </section>

      <section className="home-section">
        <p className="section-label">— the tools</p>
        <h2>Intelligent Design Tools</h2>
        <div className="tool-grid">
          {tools.map((t) => (
            <article className="tool-card" key={t.title}>
              <i className={`fas ${t.icon}`}></i>
              <h3>{t.title}</h3>
              <p>{t.desc}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="home-section">
        <p className="section-label">— the styles</p>
        <h2>Popular Design Styles</h2>
        <div className="styles-grid">
          {styles.map((s) => (
            <article className="style-card" key={s.name}>
              <img src={s.img} alt={s.name} loading="lazy" />
              <div className="style-body">
                <h4>{s.name}</h4>
                <p>{s.desc}</p>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="faq-section">
        <p className="section-label" style={{ textAlign: 'center' }}>— the answers</p>
        <h2 className="gradient-text" style={{ textAlign: 'center', fontSize: '2rem', fontWeight: 700, marginBottom: '3rem' }}>Frequently Asked Questions</h2>
        <div className="faq-container">
          {faqs.map((faq) => (
            <div className="faq-item" key={faq.id}>
              <button className="faq-header" onClick={() => setOpenFaq(openFaq === faq.id ? null : faq.id)}>
                <span>
                  <span style={{ color: '#10b981' }}>root@faq:~$ </span>
                  <span style={{ color: '#818cf8', marginLeft: 8 }}>DISPLAY_ANSWER --id {faq.id}</span>
                </span>
                <span style={{ color: '#94a3b8' }}>{openFaq === faq.id ? '▲' : '▼'}</span>
              </button>
              {openFaq === faq.id && (
                <div className="faq-content fade-in">
                  <p style={{ fontFamily: 'monospace', color: '#94a3b8', fontSize: '0.8rem', marginBottom: '0.5rem' }}>Status: Active | Encoding: UTF-8</p>
                  <p style={{ fontWeight: 600, color: '#e2e8f0', marginBottom: '0.5rem' }}>{faq.question}</p>
                  <p style={{ color: '#94a3b8', fontSize: '0.9rem', lineHeight: 1.7 }}>{faq.answer}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      </section>
    </>
  );
}
