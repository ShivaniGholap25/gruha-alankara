import os
base_dir = r"E:\gruha_alankara\templates"

base_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Gruha Alankara</title>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#0d0d1a;color:#e2e8f0;font-family:"Segoe UI",sans-serif;min-height:100vh;}
.navbar{display:flex;justify-content:space-between;align-items:center;padding:1rem 2rem;background:rgba(13,13,26,0.95);border-bottom:1px solid #2d3748;position:sticky;top:0;z-index:100;}
.nav-brand{font-size:1.3rem;font-weight:700;color:#818cf8;text-decoration:none;}
.nav-links{display:flex;gap:2rem;}
.nav-link{color:#94a3b8;text-decoration:none;font-size:0.95rem;}
.nav-link:hover{color:white;}
.flash{padding:0.75rem 1.5rem;margin:1rem 2rem;border-radius:8px;}
.flash-error{background:rgba(239,68,68,0.15);border:1px solid #ef4444;color:#ef4444;}
.flash-success{background:rgba(16,185,129,0.15);border:1px solid #10b981;color:#10b981;}
.flash-info{background:rgba(59,130,246,0.15);border:1px solid #3b82f6;color:#3b82f6;}
footer{text-align:center;padding:1.5rem;color:#94a3b8;font-size:0.85rem;border-top:1px solid #2d3748;margin-top:2rem;}
.page-wrapper{min-height:calc(100vh - 80px);display:flex;align-items:center;justify-content:center;padding:2rem;background:radial-gradient(ellipse at center,#1e1b4b 0%,#0d0d1a 60%);}
.auth-card{background:#1a1a2e;border:1px solid #2d3748;border-radius:16px;padding:2.5rem;width:100%;max-width:420px;box-shadow:0 25px 50px rgba(0,0,0,0.5);}
.auth-icon{width:64px;height:64px;background:linear-gradient(135deg,#7c3aed,#a855f7);border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 1.5rem;}
.auth-icon i{font-size:1.5rem;color:white;}
.auth-card h1{text-align:center;font-size:1.8rem;font-weight:700;margin-bottom:0.5rem;background:linear-gradient(135deg,#818cf8,#a855f7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.subtitle{text-align:center;color:#94a3b8;font-size:0.9rem;margin-bottom:2rem;}
.form-group{margin-bottom:1.25rem;}
.form-group label{display:block;font-size:0.85rem;color:#94a3b8;margin-bottom:0.5rem;font-weight:500;}
.input-wrapper{position:relative;}
.input-icon{position:absolute;left:12px;top:50%;transform:translateY(-50%);color:#6b7280;font-size:0.9rem;pointer-events:none;z-index:1;}
.form-group input{width:100%;background:#0d0d1a;border:1px solid #2d3748;color:#e2e8f0;border-radius:8px;padding:0.75rem 0.75rem 0.75rem 2.5rem;font-size:0.95rem;transition:border-color 0.2s;}
.form-group input:focus{outline:none;border-color:#7c3aed;box-shadow:0 0 0 3px rgba(124,58,237,0.1);}
.btn-submit{width:100%;padding:0.85rem;background:linear-gradient(135deg,#7c3aed,#a855f7);color:white;border:none;border-radius:8px;font-size:1rem;font-weight:600;cursor:pointer;margin-top:0.5rem;display:flex;align-items:center;justify-content:center;gap:8px;}
.btn-submit:hover{opacity:0.9;}
.divider{display:flex;align-items:center;gap:1rem;margin:1.5rem 0;}
.divider::before,.divider::after{content:"";flex:1;height:1px;background:#2d3748;}
.divider span{color:#6b7280;font-size:0.8rem;}
.auth-footer{text-align:center;font-size:0.9rem;color:#94a3b8;}
.auth-footer a{color:#818cf8;text-decoration:none;font-weight:600;}
.card{background:#1a1a2e;border:1px solid #2d3748;border-radius:12px;padding:1.5rem;}
.btn{padding:0.6rem 1.4rem;border-radius:8px;border:none;cursor:pointer;font-size:0.9rem;font-weight:600;transition:all 0.2s;text-decoration:none;display:inline-flex;align-items:center;gap:6px;}
.btn-primary{background:linear-gradient(135deg,#7c3aed,#a855f7);color:white;}
.btn-outline{background:transparent;border:1px solid #2d3748;color:#e2e8f0;}
.gradient-text{background:linear-gradient(135deg,#818cf8,#a855f7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.tabs{display:flex;gap:0;border-bottom:1px solid #2d3748;margin-bottom:1.5rem;}
.tab{padding:0.75rem 1.25rem;cursor:pointer;color:#94a3b8;border-bottom:2px solid transparent;font-size:0.9rem;display:flex;align-items:center;gap:6px;}
.tab.active{color:white;border-bottom-color:#7c3aed;}
.progress-bar{height:6px;background:#2d3748;border-radius:3px;overflow:hidden;margin:4px 0;}
.progress-fill{height:100%;background:linear-gradient(90deg,#7c3aed,#a855f7);border-radius:3px;}
.badge{padding:2px 8px;border-radius:20px;font-size:0.7rem;font-weight:700;}
.badge-high{background:#ef4444;color:white;}
.badge-medium{background:#f59e0b;color:black;}
.badge-low{background:#10b981;color:white;}
.badge-new,.badge-recommended{background:linear-gradient(135deg,#ec4899,#f43f5e);color:white;}
.badge-popular{background:#f59e0b;color:black;}
select,input[type=number],input[type=range]{background:#16213e;border:1px solid #2d3748;color:#e2e8f0;border-radius:8px;padding:0.5rem 0.75rem;width:100%;font-size:0.9rem;}
select:focus,input:focus{outline:none;border-color:#7c3aed;}
</style>
</head>
<body>
<nav class="navbar">
  <a href="/" class="nav-brand"><i class="fas fa-home" style="margin-right:8px;"></i>Gruha Alankara</a>
  <div class="nav-links">
    <a href="/" class="nav-link">Home</a>
    <a href="/analyze" class="nav-link">Analyze Room</a>
    <a href="/design" class="nav-link">Design Studio</a>
    <a href="/catalog" class="nav-link">My Catalog</a>
  </div>
</nav>
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    {% for category, message in messages %}
      <div class="flash flash-{{ category }}">{{ message }}</div>
    {% endfor %}
  {% endif %}
{% endwith %}
{% block content %}{% endblock %}
<footer><p>2025 Gruha Alankara - AI Interior Stylist. Powered by Agentic AI</p></footer>
{% block scripts %}{% endblock %}
</body>
</html>"""

login_html = """{% extends 'base.html' %}
{% block content %}
<div class="page-wrapper">
  <div class="auth-card">
    <div class="auth-icon"><i class="fas fa-user"></i></div>
    <h1>Welcome Back</h1>
    <p class="subtitle">Sign in to continue designing your dream space</p>
    <form method="POST" action="/login">
      <div class="form-group">
        <label>Email Address</label>
        <div class="input-wrapper">
          <i class="fas fa-envelope input-icon"></i>
          <input type="email" name="email" placeholder="you@example.com" required>
        </div>
      </div>
      <div class="form-group">
        <label>Password</label>
        <div class="input-wrapper">
          <i class="fas fa-lock input-icon"></i>
          <input type="password" name="password" placeholder="Enter your password" required>
        </div>
      </div>
      <button type="submit" class="btn-submit"><i class="fas fa-sign-in-alt"></i> Sign In</button>
    </form>
    <div class="divider"><span>or</span></div>
    <div class="auth-footer">Don't have an account? <a href="/register">Create one here</a></div>
  </div>
</div>
{% endblock %}"""

register_html = """{% extends 'base.html' %}
{% block content %}
<div class="page-wrapper">
  <div class="auth-card">
    <div class="auth-icon"><i class="fas fa-user-plus"></i></div>
    <h1>Create Account</h1>
    <p class="subtitle">Join Gruha Alankara and start designing your dream space</p>
    <form method="POST" action="/register">
      <div class="form-group">
        <label>Username</label>
        <div class="input-wrapper">
          <i class="fas fa-user input-icon"></i>
          <input type="text" name="username" placeholder="Your name" required>
        </div>
      </div>
      <div class="form-group">
        <label>Email Address</label>
        <div class="input-wrapper">
          <i class="fas fa-envelope input-icon"></i>
          <input type="email" name="email" placeholder="you@example.com" required>
        </div>
      </div>
      <div class="form-group">
        <label>Password</label>
        <div class="input-wrapper">
          <i class="fas fa-lock input-icon"></i>
          <input type="password" name="password" placeholder="Create a strong password" required>
        </div>
      </div>
      <button type="submit" class="btn-submit"><i class="fas fa-user-plus"></i> Create Account</button>
    </form>
    <div class="divider"><span>or</span></div>
    <div class="auth-footer">Already have an account? <a href="/login">Sign in here</a></div>
  </div>
</div>
{% endblock %}"""

for filename, content in [('base.html', base_html), ('login.html', login_html), ('register.html', register_html)]:
    path = os.path.join(base_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"{filename} written!")

print("ALL DONE! Restart Flask now.")