import { useState, useRef, useEffect } from 'react';
import { api } from '../api/client';
import './BuddyChat.css';

const LANG_MAP = { en: 'en-IN', hi: 'hi-IN', te: 'te-IN' };

export default function BuddyChat() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hello! I am your interior design assistant. Ask me about furniture, styles, prices or booking.' },
  ]);
  const [input, setInput] = useState('');
  const [typing, setTyping] = useState(false);
  const [language, setLanguage] = useState('en');
  const [listening, setListening] = useState(false);
  const messagesEndRef = useRef(null);
  const recognitionRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (overrideMsg) => {
    const msg = (overrideMsg || input).trim();
    if (!msg) return;
    setMessages((prev) => [...prev, { sender: 'user', text: msg }]);
    setInput('');
    setTyping(true);
    const res = await api.post('/buddy', { message: msg, language });
    setTyping(false);
    if (res.ok && (res.data.text || res.data.reply)) {
      setMessages((prev) => [
        ...prev,
        { sender: 'bot', text: res.data.text || res.data.reply },
      ]);
      if (res.data.audio_url) {
        const audioSrc = (import.meta.env.VITE_API_URL || '') + res.data.audio_url;
        new Audio(audioSrc).play().catch(() => {});
      }
    } else {
      setMessages((prev) => [...prev, { sender: 'bot', text: res.data?.text || 'Sorry, something went wrong. Please try again.' }]);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') sendMessage();
  };

  // Issue 5 — Web Speech API mic
  const toggleMic = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert('Speech recognition is not supported in this browser. Try Chrome.');
      return;
    }

    if (listening) {
      recognitionRef.current?.stop();
      setListening(false);
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = LANG_MAP[language] || 'en-IN';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = (e) => {
      const transcript = e.results[0][0].transcript;
      setInput(transcript);
      setListening(false);
      // auto-submit
      sendMessage(transcript);
    };
    recognition.onerror = () => setListening(false);
    recognition.onend = () => setListening(false);

    recognitionRef.current = recognition;
    recognition.start();
    setListening(true);
  };

  return (
    <>
      <button className="buddy-fab" onClick={() => setOpen(!open)} title="Chat with Gruha Buddy">
        <i className={`fas ${open ? 'fa-xmark' : 'fa-robot'}`}></i>
      </button>

      {open && (
        <div className="buddy-panel">
          <div className="buddy-header">
            <div className="buddy-header-left">
              <i className="fas fa-robot"></i>
              <span>Gruha Buddy</span>
              <span className="buddy-online-dot"></span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <select
                className="buddy-lang-select"
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
              >
                <option value="en">EN</option>
                <option value="hi">हिं</option>
                <option value="te">తె</option>
              </select>
              <button className="buddy-close-btn" onClick={() => setOpen(false)}>×</button>
            </div>
          </div>

          <div className="buddy-messages">
            {messages.map((m, i) => (
              <div key={i} className={`buddy-msg ${m.sender === 'user' ? 'buddy-msg-user' : 'buddy-msg-bot'}`}>
                {m.sender === 'bot' && <span className="buddy-sender">Gruha Buddy</span>}
                {m.text}
              </div>
            ))}
            {typing && <div className="buddy-typing">Buddy is typing...</div>}
            <div ref={messagesEndRef} />
          </div>

          <div className="buddy-input-bar">
            {/* Issue 5 — mic button */}
            <button
              className="buddy-mic-btn"
              onClick={toggleMic}
              title={listening ? 'Stop listening' : 'Speak'}
              style={{
                background: listening ? '#ef4444' : 'transparent',
                border: 'none',
                color: listening ? '#fff' : '#94a3b8',
                borderRadius: 8,
                padding: '0 8px',
                cursor: 'pointer',
                fontSize: '1rem',
                transition: 'all .2s',
              }}
            >
              <i className={`fas ${listening ? 'fa-stop' : 'fa-microphone'}`}></i>
            </button>
            <input
              className="buddy-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={listening ? 'Listening...' : 'Ask Buddy anything...'}
            />
            <button className="buddy-send-btn" onClick={() => sendMessage()}>
              <i className="fas fa-paper-plane"></i>
            </button>
          </div>
        </div>
      )}
    </>
  );
}
