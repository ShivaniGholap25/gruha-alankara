# Gruha Alankara — Testing Checklist

## 10 Test Photos

| # | Type | Expected Result |
|---|---|---|
| 1 | Living room (modern style) | ✅ Accepted → furniture suggestions (sofa, coffee table, TV unit) |
| 2 | Bedroom (small) | ✅ Accepted → furniture suggestions (bed, wardrobe, nightstand) |
| 3 | Kitchen interior | ✅ Accepted → furniture suggestions (cabinets, dining table, chairs) |
| 4 | Bathroom interior | ✅ Accepted → furniture suggestions (vanity, mirror, storage) |
| 5 | Office/study room | ✅ Accepted → furniture suggestions (desk, chair, bookshelf) |
| 6 | Street photo | ❌ Rejected → "Please upload a photo of a room interior" |
| 7 | Landscape/outdoor photo | ❌ Rejected → "Please upload a photo of a room interior" |
| 8 | Blank white wall photo | ⚠️ Edge case → may pass with minimal suggestions |
| 9 | Dark/poorly lit room | ✅ Accepted → lighting quality = "Low" |
| 10 | Cluttered room | ✅ Accepted → complexity = "High" |

---

## Cross-Browser Test Matrix

| Feature | Chrome Desktop | Firefox Desktop | Chrome Mobile | Safari iOS |
|---|---|---|---|---|
| Upload + AI analysis | ⬜ | ⬜ | ⬜ | ⬜ |
| AR camera overlay | ⬜ | ⬜ | ⬜ | ⬜ |
| Voice input (STT) | ⬜ | ⬜ | ⬜ | ⬜ |
| Audio response (TTS) | ⬜ | ⬜ | ⬜ | ⬜ |
| Booking flow | ⬜ | ⬜ | ⬜ | ⬜ |
| 360° panorama | ⬜ | ⬜ | ⬜ | ⬜ |
| JWT auth | ⬜ | ⬜ | ⬜ | ⬜ |

---

## Demo Video Script

Record in this order (5-7 minutes total):

### 1. Registration & Login (30s)
- Open homepage at http://localhost:5173
- Click "Register" → fill form → submit
- Login with new credentials → redirected to homepage

### 2. Room Analysis with AI (90s)
- Navigate to "Analyze Room"
- Upload a living room photo
- Click "Analyze Room"
- **Show:** AI furniture suggestions with prices (₹15,000-₹80,000 range)
- **Show:** Composite preview image with labeled furniture zones
- **Show:** Dimensions, lighting quality, color palette
- Click "Proceed to Design Studio"

### 3. AR Camera Furniture Overlay (60s)
- Navigate to "Live AR"
- Allow camera permission
- **Show:** Live camera feed visible
- Select "Sofa" → **Show:** purple sofa shape appears overlaid on camera
- Drag sofa to reposition → **Show:** smooth movement
- Scroll to resize → **Show:** sofa scales up/down
- Select "Chair" → **Show:** blue chair replaces sofa
- Click "Screenshot" → **Show:** download confirmation

### 4. Voice Assistant (60s)
- Click Buddy chatbot icon (bottom-right)
- Select language: "हिं" (Hindi)
- Click microphone button
- Speak: "मुझे एक सोफा बुक करना है" (I want to book a sofa)
- **Show:** Text appears in chat input
- **Show:** Buddy responds in Hindi
- **Show:** Audio plays automatically
- Switch to English → ask "What is the price of the Luxe Comfort Sofa?"
- **Show:** Response with price ₹18,500

### 5. Furniture Booking (45s)
- Navigate to "Furniture"
- Browse catalog → click "Book" on "Sheesham Dining Table"
- **Show:** Booking modal → confirm
- **Show:** Success message
- Navigate to "My Bookings"
- **Show:** Booking appears with status badge "Confirmed" (green)

### 6. 360° Panorama View (45s)
- Navigate to "Design Studio"
- Click "3D View" tab
- Click "360° Preview" card
- **Show:** Full-screen Three.js panorama opens
- Drag to rotate view → **Show:** smooth 360° rotation
- Click "📷 Live Camera" mode → allow camera
- **Show:** Live camera feed mapped to sphere
- Click "📸 Capture This View" → **Show:** download

### 7. Error Handling (30s)
- Navigate to "Analyze Room"
- Upload a street photo (not a room)
- Click "Analyze"
- **Show:** Red error box: "Please upload a photo of a room interior"
- Upload a 10MB file
- **Show:** Error: "File too large. Maximum size is 5 MB"

### 8. Security Test (30s)
- Log out
- Try to access `/dashboard` directly
- **Show:** Redirected to login page
- Try to access `/catalog` without auth
- **Show:** Redirected to login page

---

## API Endpoints to Test

| Endpoint | Method | Auth | Expected Response |
|---|---|---|---|
| `/health` | GET | No | `{"status":"ok","db":"connected","counts":{...}}` |
| `/register` | POST | No | `{"success":true}` |
| `/login` | POST | No | `{"success":true,"token":"...","user":{...}}` |
| `/api/me` | GET | Yes | `{"authenticated":true,"user":{...}}` |
| `/analyze-room` | POST | No | `{"dimensions":{...},"furniture_suggestions":[...]}` |
| `/preview-composite` | POST | No | `{"preview_url":"/uploads/previews/..."}` |
| `/generate-design` | POST | No | `{"style_theme":"...","furniture_list":[...]}` |
| `/save-design` | POST | Yes | `{"success":true,"design_id":123}` |
| `/get-designs` | GET | Yes | `[{...},{...}]` |
| `/book-furniture` | POST | Yes | `{"success":true,"status":"confirmed"}` |
| `/my-bookings` | GET | Yes | `[{...}]` |
| `/buddy` | POST | Yes | `{"text":"...","audio_url":"/static/audio/..."}` |
| `/seed-db` | GET | No | `{"success":true,"count":10}` |

---

## Environment Variables Required

### Local Development
```bash
# Optional — enables Claude vision
export ANTHROPIC_API_KEY=sk-ant-...
```

### Render Backend
```
SECRET_KEY=<random-string>
FLASK_ENV=production
FRONTEND_URL=https://gruha-alankara.vercel.app
ANTHROPIC_API_KEY=sk-ant-...  # optional
```

### Vercel Frontend
```
VITE_API_URL=https://gruha-alankara-9ku2.onrender.com
```

---

## Known Limitations

1. **SQLite on Render** — database resets on every deploy (ephemeral disk). For production, migrate to PostgreSQL.
2. **Claude API** — if `ANTHROPIC_API_KEY` is not set, falls back to PIL-based analysis (less accurate).
3. **gTTS audio** — generated files are stored in `static/audio/` which is ephemeral on Render. Consider S3 for production.
4. **AR camera** — requires HTTPS in production for `getUserMedia()` to work.
5. **Web Speech API** — only works in Chrome/Edge. Safari iOS requires user gesture to start recognition.

---

## Performance Benchmarks

| Operation | Target | Acceptable |
|---|---|---|
| Room analysis (PIL) | < 2s | < 5s |
| Room analysis (Claude) | < 5s | < 10s |
| Design generation | < 1s | < 3s |
| Buddy response | < 2s | < 4s |
| AR camera init | < 1s | < 3s |
| 360° panorama load | < 2s | < 5s |

---

## Security Checklist

- [x] Passwords hashed with `werkzeug.security.generate_password_hash`
- [x] Session cookies: `HttpOnly=True`, `SameSite=Lax/None`
- [x] JWT tokens for cross-domain auth
- [x] File upload size limit: 5 MB
- [x] File type validation: JPEG, PNG, WEBP only
- [x] Minimum image dimensions: 100×100px
- [x] Protected routes check `_get_user_id()` (session or JWT)
- [ ] CSRF protection (flask-wtf) — not yet implemented
- [x] SQL injection prevented (SQLAlchemy ORM)
- [x] XSS prevented (React escapes by default, Jinja2 autoescapes)

---

## Deployment Checklist

### Before Deploy
- [ ] Run `pip install -r requirements.txt`
- [ ] Run `npm install` in `frontend/`
- [ ] Test locally: backend on :5000, frontend on :5173
- [ ] Verify `/health` returns counts
- [ ] Verify login → dashboard works
- [ ] Verify AR camera opens
- [ ] Verify Buddy chat responds

### Render Backend
- [ ] Set `FLASK_ENV=production`
- [ ] Set `SECRET_KEY` (random 32-char string)
- [ ] Set `FRONTEND_URL` (Vercel URL)
- [ ] Optional: Set `ANTHROPIC_API_KEY`
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

### Vercel Frontend
- [ ] Root directory: `frontend`
- [ ] Build command: `npm run build`
- [ ] Output directory: `dist`
- [ ] Set `VITE_API_URL` (Render backend URL)

---

## Post-Deploy Smoke Test

1. Open Vercel URL → homepage loads
2. Register new account → success
3. Login → redirected to homepage
4. Navigate to Analyze Room → upload photo → AI responds
5. Navigate to Live AR → camera opens → furniture visible
6. Click Buddy → send message → response + audio plays
7. Navigate to Furniture → book item → check My Bookings → status = Confirmed
8. Logout → try /dashboard → redirected to login

**If all pass → deployment successful ✅**
