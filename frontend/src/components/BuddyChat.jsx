import { useState, useRef, useEffect } from 'react';
import { api } from '../api/client';
import './BuddyChat.css';

export default function BuddyChat() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hello! I am your interior design assistant. Ask me about furniture, styles, prices or booking.' },
  ]);
  const [input, setInput] = useState('');
  const [typing, setTyping] = useState(false);
  const [language, setLanguage] = useState('en');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    const msg = input.trim();
    if (!msg) return;
    setMessages((prev) => [...prev, { sender: 'user', text: msg }]);
    setInput('');
    setTyping(true);
    const res = await api.post('/buddy', { message: msg, language });
    setTyping(false);
    if (res.ok) {
      setMessages((prev) => [
        ...prev,
        { sender: 'bot', text: res.data.text || res.data.reply || 'I am here to help!' },
      ]);
      if (res.data.audio_url) {
        new Audio(res.data.audio_url).play().catch(() => {});
      }
    } else {
      const errorMsg = res.status === 401
        ? 'Please login to chat with Buddy.'
        : 'Sorry, could not connect. Try again.';
      setMessages((prev) => [...prev, { sender: 'bot', text: errorMsg }]);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') sendMessage();
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
                <option value="en">English</option>
                <option value="hi">Hindi</option>
                <option value="te">Telugu</option>
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
            {typing && (
              <div className="buddy-typing">Buddy is typing...</div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="buddy-input-bar">
            <input
              className="buddy-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask Buddy anything..."
            />
            <button className="buddy-send-btn" onClick={sendMessage}>
              <i className="fas fa-paper-plane"></i>
            </button>
          </div>
        </div>
      )}
    </>
  );
}
