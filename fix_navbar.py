import os

path = r"E:\gruha_alankara\templates\base.html"
content = open(path, encoding="utf-8").read()

old_links = """    <a href="/" class="nav-link {% if request.path == '/' %}active{% endif %}">Home</a>
    <a href="/analyze" class="nav-link {% if request.path == '/analyze' %}active{% endif %}">Analyze Room</a>
    <a href="/style-quiz" class="nav-link {% if request.path == '/style-quiz' %}active{% endif %}">Style Quiz</a>
    <a href="/design" class="nav-link {% if request.path == '/design' %}active{% endif %}">Design Studio</a>
    <a href="/catalog" class="nav-link {% if request.path == '/catalog' %}active{% endif %}">My Catalog</a>"""

# Find the nav-links div and replace everything inside it
# We'll do a broader replacement
content_new = content

# Replace the entire navbar with a clean version
old_nav = content[content.find('<nav'):content.find('</nav>')+6]

new_nav = """<nav class="navbar">
  <a href="/" class="nav-brand"><i class="fas fa-home" style="margin-right:8px;"></i>Gruha Alankara</a>
  
  <div class="nav-links">
    <a href="/" class="nav-link {% if request.path == '/' %}active{% endif %}">Home</a>
    <a href="/analyze" class="nav-link {% if request.path == '/analyze' %}active{% endif %}">Analyze Room</a>
    <a href="/design" class="nav-link {% if request.path == '/design' %}active{% endif %}">Design Studio</a>
    <a href="/catalog" class="nav-link {% if request.path == '/catalog' %}active{% endif %}">My Catalog</a>
    
    <!-- More dropdown -->
    <div style="position:relative;display:inline-block;" id="more-menu">
      <button onclick="toggleMore()" style="background:none;border:1px solid #2d3748;color:#94a3b8;border-radius:8px;padding:0.4rem 0.8rem;cursor:pointer;font-size:0.9rem;display:flex;align-items:center;gap:6px;">
        More <i class="fas fa-chevron-down" style="font-size:0.7rem;"></i>
      </button>
      <div id="more-dropdown" style="display:none;position:absolute;top:110%;right:0;background:#1a1a2e;border:1px solid #2d3748;border-radius:10px;min-width:180px;z-index:200;box-shadow:0 10px 40px rgba(0,0,0,0.4);overflow:hidden;">
        <a href="/style-quiz" style="display:flex;align-items:center;gap:10px;padding:0.75rem 1rem;color:#e2e8f0;text-decoration:none;font-size:0.875rem;transition:background 0.2s;" onmouseover="this.style.background='#16213e'" onmouseout="this.style.background='transparent'">
          <i class="fas fa-magic" style="color:#818cf8;width:16px;"></i> Style Quiz
        </a>
        <a href="/gallery" style="display:flex;align-items:center;gap:10px;padding:0.75rem 1rem;color:#e2e8f0;text-decoration:none;font-size:0.875rem;transition:background 0.2s;" onmouseover="this.style.background='#16213e'" onmouseout="this.style.background='transparent'">
          <i class="fas fa-images" style="color:#818cf8;width:16px;"></i> Gallery
        </a>
        <a href="/nearby-shops" style="display:flex;align-items:center;gap:10px;padding:0.75rem 1rem;color:#e2e8f0;text-decoration:none;font-size:0.875rem;transition:background 0.2s;" onmouseover="this.style.background='#16213e'" onmouseout="this.style.background='transparent'">
          <i class="fas fa-map-marker-alt" style="color:#818cf8;width:16px;"></i> Near Me
        </a>
        <a href="/budget-calculator" style="display:flex;align-items:center;gap:10px;padding:0.75rem 1rem;color:#e2e8f0;text-decoration:none;font-size:0.875rem;transition:background 0.2s;" onmouseover="this.style.background='#16213e'" onmouseout="this.style.background='transparent'">
          <i class="fas fa-calculator" style="color:#818cf8;width:16px;"></i> Budget Calc
        </a>
        <a href="/furniture" style="display:flex;align-items:center;gap:10px;padding:0.75rem 1rem;color:#e2e8f0;text-decoration:none;font-size:0.875rem;transition:background 0.2s;" onmouseover="this.style.background='#16213e'" onmouseout="this.style.background='transparent'">
          <i class="fas fa-couch" style="color:#818cf8;width:16px;"></i> Furniture
        </a>
        {% if session.get('user_id') %}
        <a href="/my-bookings" style="display:flex;align-items:center;gap:10px;padding:0.75rem 1rem;color:#e2e8f0;text-decoration:none;font-size:0.875rem;transition:background 0.2s;" onmouseover="this.style.background='#16213e'" onmouseout="this.style.background='transparent'">
          <i class="fas fa-bookmark" style="color:#818cf8;width:16px;"></i> My Bookings
        </a>
        <a href="/dashboard" style="display:flex;align-items:center;gap:10px;padding:0.75rem 1rem;color:#e2e8f0;text-decoration:none;font-size:0.875rem;transition:background 0.2s;" onmouseover="this.style.background='#16213e'" onmouseout="this.style.background='transparent'">
          <i class="fas fa-tachometer-alt" style="color:#818cf8;width:16px;"></i> Dashboard
        </a>
        {% endif %}
      </div>
    </div>
  </div>

  <div style="display:flex;align-items:center;gap:0.75rem;">
    {% if session.get('user_id') %}
      <a href="/logout" style="background:#ef4444;color:white;padding:0.4rem 0.9rem;border-radius:6px;text-decoration:none;font-size:0.85rem;font-weight:600;">
        <i class="fas fa-sign-out-alt" style="margin-right:4px;"></i>Logout
      </a>
    {% else %}
      <a href="/login" style="color:#94a3b8;text-decoration:none;font-size:0.85rem;padding:0.4rem 0.75rem;">Login</a>
      <a href="/register" style="background:linear-gradient(135deg,#7c3aed,#a855f7);color:white;padding:0.4rem 0.9rem;border-radius:6px;text-decoration:none;font-size:0.85rem;font-weight:600;">Register</a>
    {% endif %}
  </div>
</nav>

<script>
function toggleMore() {
  const dd = document.getElementById('more-dropdown');
  dd.style.display = dd.style.display === 'none' ? 'block' : 'none';
}
document.addEventListener('click', function(e) {
  const menu = document.getElementById('more-menu');
  if(menu && !menu.contains(e.target)) {
    document.getElementById('more-dropdown').style.display = 'none';
  }
});
</script>"""

content_new = content.replace(old_nav, new_nav)

with open(path, "w", encoding="utf-8") as f:
    f.write(content_new)
print("Navbar fixed!")