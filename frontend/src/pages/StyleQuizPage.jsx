import { useState } from 'react';
import { Link } from 'react-router-dom';

const questions = [
  { q: 'What color mood appeals to you most?', opts: ['Neutral and Calm','Bold and Vibrant','Dark and Moody','Light and Airy'], icons: ['🤍','🌈','🖤','☀️'] },
  { q: 'Pick your ideal furniture style', opts: ['Sleek and Modern','Rustic and Warm','Classic and Elegant','Eclectic and Mixed'], icons: ['🔷','🪵','🏛️','🎨'] },
  { q: 'What material do you love most?', opts: ['Natural Wood','Metal and Glass','Fabric and Textile','Stone and Marble'], icons: ['🌿','✨','🛋️','💎'] },
  { q: 'Choose your lighting preference', opts: ['Bright Natural Light','Warm Ambient Glow','Dramatic Spotlights','Soft Diffused Light'], icons: ['☀️','🕯️','💡','🌙'] },
  { q: 'What is your space priority?', opts: ['Minimalism','Comfort','Style Statement','Functionality'], icons: ['⬜','😊','💫','⚙️'] },
];

const styleMap = { '0000':'Modern Minimalist','0001':'Scandinavian','0010':'Contemporary','0011':'Scandinavian','0100':'Industrial','0101':'Bohemian','0110':'Traditional','0111':'Bohemian','1000':'Industrial','1001':'Bohemian','1010':'Contemporary','1011':'Traditional','1100':'Industrial','1101':'Bohemian','1110':'Traditional','1111':'Bohemian' };
const styleDesc = { 'Modern Minimalist':'Clean lines, neutral colors, and functional furniture keep your space elegant and clutter-free.', 'Scandinavian':'Bright airy spaces with natural materials and cozy textures create a warm and inviting atmosphere.', 'Industrial':'Raw finishes, exposed textures, and bold accents define your urban design taste.', 'Bohemian':'Layered patterns, rich colors, and expressive decor make your space artistic and personal.', 'Traditional':'Classic elegance with timeless details and rich finishes suits your style best.', 'Contemporary':'Trend-forward forms and practical styling bring modern comfort to your room.' };
const styleColors = { 'Modern Minimalist':['#FFFFFF','#000000','#808080','#F5F5F5'], 'Scandinavian':['#F5F0E8','#2C5F2E','#D4A373','#FEFAE0'], 'Industrial':['#2E2E2E','#5A5A5A','#8C7B75','#B0A8A0'], 'Bohemian':['#E76F51','#2A9D8F','#E9C46A','#F4A261'], 'Traditional':['#7A4E2D','#C9B79C','#8B0000','#F5E6CC'], 'Contemporary':['#D9D9D9','#4A4E69','#9A8C98','#F2E9E4'] };

export default function StyleQuizPage() {
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [done, setDone] = useState(false);

  const answer = (i) => {
    const a = [...answers, i];
    setAnswers(a);
    if (current < 4) setCurrent(current + 1);
    else setDone(true);
  };

  const key = answers.slice(0,4).map(a => a>1?'1':'0').join('');
  const style = styleMap[key] || 'Modern Minimalist';
  const pct = done ? 100 : ((current+1)/5)*100;

  return (
    <div style={{ maxWidth: 860, margin: '0 auto', padding: '2rem' }}>
      <h1 className="gradient-text" style={{ textAlign: 'center', fontSize: '2rem', fontWeight: 700, marginBottom: '0.5rem' }}>Style Quiz</h1>
      <p style={{ textAlign: 'center', color: 'var(--muted)', marginBottom: '2rem' }}>Answer 5 quick questions to discover your ideal interior style.</p>

      <div style={{ background: '#1a1a2e', borderRadius: 12, padding: '0.5rem 1rem', marginBottom: '2rem', border: '1px solid #2d3748' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
          <span style={{ fontSize: '0.85rem', color: '#94a3b8' }}>{done ? 'Quiz Complete!' : `Question ${current+1} of 5`}</span>
          <span style={{ fontSize: '0.85rem', color: '#818cf8' }}>{Math.round(pct)}%</span>
        </div>
        <div className="progress-bar"><div className="progress-fill" style={{ width: pct+'%' }}></div></div>
      </div>

      {!done ? (
        <div style={{ textAlign: 'center' }} className="fade-in">
          <h2 style={{ fontSize: '1.4rem', fontWeight: 600, marginBottom: '2rem', color: '#e2e8f0' }}>{questions[current].q}</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2,1fr)', gap: '1rem' }}>
            {questions[current].opts.map((opt, i) => (
              <button key={i} onClick={() => answer(i)} style={{ background: '#16213e', border: '2px solid #2d3748', borderRadius: 12, padding: '1.5rem 1rem', cursor: 'pointer', textAlign: 'center', color: '#e2e8f0', transition: 'border-color 0.2s' }} onMouseOver={e => e.currentTarget.style.borderColor='#7c3aed'} onMouseOut={e => e.currentTarget.style.borderColor='#2d3748'}>
                <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>{questions[current].icons[i]}</div>
                <p style={{ fontWeight: 600, fontSize: '0.95rem', margin: 0 }}>{opt}</p>
              </button>
            ))}
          </div>
        </div>
      ) : (
        <div style={{ textAlign: 'center', background: '#1a1a2e', border: '1px solid #2d3748', borderRadius: 12, padding: '2rem' }} className="fade-in">
          <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>🏠</div>
          <h2 className="gradient-text" style={{ fontSize: '1.8rem', fontWeight: 700, marginBottom: '0.5rem' }}>Your Style: {style}</h2>
          <p style={{ color: '#94a3b8', marginBottom: '2rem', lineHeight: 1.7, maxWidth: 520, margin: '0 auto 2rem' }}>{styleDesc[style]}</p>
          <div style={{ display: 'flex', justifyContent: 'center', gap: 12, marginBottom: '2rem' }}>
            {(styleColors[style]||[]).map((c,i) => <div key={i} title={c} style={{ width: 48, height: 48, borderRadius: '50%', background: c, border: '2px solid #2d3748' }}></div>)}
          </div>
          <Link to="/dashboard" className="btn btn-primary" style={{ padding: '0.85rem 2rem', borderRadius: 8, fontWeight: 600 }}>
            <i className="fas fa-magic"></i> Start Designing
          </Link>
        </div>
      )}
    </div>
  );
}
