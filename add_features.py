import os

templates = r"E:\gruha_alankara\templates"

# Read design.html
with open(os.path.join(templates, "design.html"), encoding="utf-8") as f:
    design = f.read()

# Add color theme selector - inject before Generate Design button
color_theme_html = """
<div style="margin-bottom:1.5rem;">
  <label style="font-size:0.85rem;color:#94a3b8;margin-bottom:0.75rem;display:block;font-weight:500;">
    <i class="fas fa-palette" style="color:#818cf8;margin-right:6px;"></i>Color Theme
  </label>
  <div id="color-themes" style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;">
    <div class="ctheme" onclick="selectTheme(this,'Warm Neutrals',['#F5F0E8','#D4A373','#CCD5AE','#E9EDC9'])" style="cursor:pointer;border-radius:8px;overflow:hidden;border:2px solid transparent;transition:all 0.2s;">
      <div style="display:flex;height:28px;"><div style="flex:1;background:#F5F0E8"></div><div style="flex:1;background:#D4A373"></div><div style="flex:1;background:#CCD5AE"></div><div style="flex:1;background:#E9EDC9"></div></div>
      <p style="font-size:0.6rem;color:#94a3b8;text-align:center;padding:2px;margin:0;">Warm</p>
    </div>
    <div class="ctheme" onclick="selectTheme(this,'Cool Blues',['#03045E','#0077B6','#00B4D8','#90E0EF'])" style="cursor:pointer;border-radius:8px;overflow:hidden;border:2px solid transparent;transition:all 0.2s;">
      <div style="display:flex;height:28px;"><div style="flex:1;background:#03045E"></div><div style="flex:1;background:#0077B6"></div><div style="flex:1;background:#00B4D8"></div><div style="flex:1;background:#90E0EF"></div></div>
      <p style="font-size:0.6rem;color:#94a3b8;text-align:center;padding:2px;margin:0;">Cool Blue</p>
    </div>
    <div class="ctheme" onclick="selectTheme(this,'Earth Tones',['#6B4226','#A0522D','#D2691E','#DEB887'])" style="cursor:pointer;border-radius:8px;overflow:hidden;border:2px solid transparent;transition:all 0.2s;">
      <div style="display:flex;height:28px;"><div style="flex:1;background:#6B4226"></div><div style="flex:1;background:#A0522D"></div><div style="flex:1;background:#D2691E"></div><div style="flex:1;background:#DEB887"></div></div>
      <p style="font-size:0.6rem;color:#94a3b8;text-align:center;padding:2px;margin:0;">Earth</p>
    </div>
    <div class="ctheme" onclick="selectTheme(this,'Forest Green',['#1B4332','#2D6A4F','#52B788','#B7E4C7'])" style="cursor:pointer;border-radius:8px;overflow:hidden;border:2px solid transparent;transition:all 0.2s;">
      <div style="display:flex;height:28px;"><div style="flex:1;background:#1B4332"></div><div style="flex:1;background:#2D6A4F"></div><div style="flex:1;background:#52B788"></div><div style="flex:1;background:#B7E4C7"></div></div>
      <p style="font-size:0.6rem;color:#94a3b8;text-align:center;padding:2px;margin:0;">Forest</p>
    </div>
    <div class="ctheme" onclick="selectTheme(this,'Sunset Vibes',['#FF6B6B','#FFA07A','#FFD93D','#6BCB77'])" style="cursor:pointer;border-radius:8px;overflow:hidden;border:2px solid transparent;transition:all 0.2s;">
      <div style="display:flex;height:28px;"><div style="flex:1;background:#FF6B6B"></div><div style="flex:1;background:#FFA07A"></div><div style="flex:1;background:#FFD93D"></div><div style="flex:1;background:#6BCB77"></div></div>
      <p style="font-size:0.6rem;color:#94a3b8;text-align:center;padding:2px;margin:0;">Sunset</p>
    </div>
    <div class="ctheme" onclick="selectTheme(this,'Royal Purple',['#10002B','#3C096C','#7B2FBE','#E0AAFF'])" style="cursor:pointer;border-radius:8px;overflow:hidden;border:2px solid transparent;transition:all 0.2s;">
      <div style="display:flex;height:28px;"><div style="flex:1;background:#10002B"></div><div style="flex:1;background:#3C096C"></div><div style="flex:1;background:#7B2FBE"></div><div style="flex:1;background:#E0AAFF"></div></div>
      <p style="font-size:0.6rem;color:#94a3b8;text-align:center;padding:2px;margin:0;">Royal</p>
    </div>
    <div class="ctheme" onclick="selectTheme(this,'Monochrome',['#1A1A1A','#4A4A4A','#8A8A8A','#DADADA'])" style="cursor:pointer;border-radius:8px;overflow:hidden;border:2px solid transparent;transition:all 0.2s;">
      <div style="display:flex;height:28px;"><div style="flex:1;background:#1A1A1A"></div><div style="flex:1;background:#4A4A4A"></div><div style="flex:1;background:#8A8A8A"></div><div style="flex:1;background:#DADADA"></div></div>
      <p style="font-size:0.6rem;color:#94a3b8;text-align:center;padding:2px;margin:0;">Mono</p>
    </div>
    <div class="ctheme" onclick="selectTheme(this,'Ocean Breeze',['#023E8A','#0096C7','#48CAE4','#ADE8F4'])" style="cursor:pointer;border-radius:8px;overflow:hidden;border:2px solid transparent;transition:all 0.2s;">
      <div style="display:flex;height:28px;"><div style="flex:1;background:#023E8A"></div><div style="flex:1;background:#0096C7"></div><div style="flex:1;background:#48CAE4"></div><div style="flex:1;background:#ADE8F4"></div></div>
      <p style="font-size:0.6rem;color:#94a3b8;text-align:center;padding:2px;margin:0;">Ocean</p>
    </div>
  </div>
  <p id="theme-name" style="font-size:0.78rem;color:#818cf8;margin-top:6px;text-align:center;min-height:18px;"></p>
</div>
"""

color_theme_js = """
let selTheme = null, selColors = null;
function selectTheme(el, name, colors) {
  document.querySelectorAll('.ctheme').forEach(c => c.style.borderColor = 'transparent');
  el.style.borderColor = '#7c3aed';
  selTheme = name; selColors = colors;
  document.getElementById('theme-name').textContent = '✓ ' + name;
}
"""

# Add color theme HTML before generate button
if "Generate Design" in design and "color-themes" not in design:
    # Find generate button area and inject before it
    inject_marker = None
    for marker in ["Generate Design", "generate-design-btn", "btn-generate"]:
        if marker in design:
            # Find the surrounding div
            idx = design.find(marker)
            # Go back to find the start of that section
            inject_marker = marker
            break
    
    if inject_marker:
        # Find a good injection point - look for Room Type section end
        for search in ["</select>\n</div>\n", "room-type", "Room Type"]:
            idx = design.rfind(search)
            if idx > 0:
                insert_pos = design.find("</div>", idx) + 6
                design = design[:insert_pos] + "\n" + color_theme_html + design[insert_pos:]
                print("Color theme selector injected!")
                break

# Add JS for color theme
if "selTheme" not in design:
    design = design.replace("</script>", color_theme_js + "\n</script>", 1)
    print("Color theme JS added!")

with open(os.path.join(templates, "design.html"), "w", encoding="utf-8") as f:
    f.write(design)
print("design.html saved!")

# Read base.html
with open(os.path.join(templates, "base.html"), encoding="utf-8") as f:
    base = f.read()

buddy_widget = """
<!-- Buddy Chat Widget -->
<div id="buddy-btn" onclick="toggleBuddy()" style="position:fixed;bottom:24px;right:24px;width:56px;height:56px;background:linear-gradient(135deg,#7c3aed,#a855f7);border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 20px rgba(124,58,237,0.4);z-index:9999;transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">
  <i class="fas fa-robot" style="color:white;font-size:1.3rem;"></i>
</div>
<div id="buddy-panel" style="position:fixed;bottom:90px;right:24px;width:320px;height:440px;background:#1a1a2e;border:1px solid #2d3748;border-radius:16px;box-shadow:0 20px 60px rgba(0,0,0,0.5);z-index:9999;display:none;flex-direction:column;overflow:hidden;">
  <div style="padding:1rem;background:linear-gradient(135deg,#7c3aed,#a855f7);display:flex;justify-content:space-between;align-items:center;flex-shrink:0;">
    <div style="display:flex;align-items:center;gap:8px;">
      <i class="fas fa-robot" style="color:white;"></i>
      <span style="color:white;font-weight:700;font-size:0.95rem;">Gruha Buddy</span>
      <span style="width:8px;height:8px;background:#10b981;border-radius:50%;display:inline-block;"></span>
    </div>
    <div style="display:flex;align-items:center;gap:8px;">
      <select id="buddy-lang" style="background:rgba(255,255,255,0.2);border:none;color:white;border-radius:6px;padding:2px 6px;font-size:0.75rem;cursor:pointer;">
        <option value="en">English</option>
        <option value="hi">Hindi</option>
        <option value="te">Telugu</option>
      </select>
      <button onclick="toggleBuddy()" style="background:none;border:none;color:white;cursor:pointer;font-size:1.2rem;line-height:1;">×</button>
    </div>
  </div>
  <div id="buddy-messages" style="flex:1;overflow-y:auto;padding:1rem;display:flex;flex-direction:column;gap:0.75rem;">
    <div style="background:#16213e;border-radius:12px 12px 12px 2px;padding:0.75rem;font-size:0.85rem;color:#e2e8f0;max-width:85%;">
      <span style="font-size:0.7rem;color:#818cf8;display:block;margin-bottom:4px;">Gruha Buddy</span>
      Hello! I am your interior design assistant. Ask me about furniture, styles, colors or booking!
    </div>
  </div>
  <div id="buddy-typing" style="display:none;padding:0 1rem 0.5rem;">
    <span style="font-size:0.8rem;color:#94a3b8;font-style:italic;">Buddy is typing...</span>
  </div>
  <div style="padding:0.75rem;border-top:1px solid #2d3748;display:flex;gap:8px;flex-shrink:0;">
    <input id="buddy-input" type="text" placeholder="Ask Buddy anything..." onkeypress="if(event.key==='Enter')sendBuddy()" style="flex:1;background:#0d0d1a;border:1px solid #2d3748;color:#e2e8f0;border-radius:8px;padding:0.5rem 0.75rem;font-size:0.85rem;outline:none;">
    <button onclick="sendBuddy()" style="background:linear-gradient(135deg,#7c3aed,#a855f7);border:none;color:white;border-radius:8px;padding:0.5rem 0.9rem;cursor:pointer;font-size:0.9rem;">
      <i class="fas fa-paper-plane"></i>
    </button>
  </div>
</div>
<script>
let buddyOpen=false;
function toggleBuddy(){
  buddyOpen=!buddyOpen;
  const p=document.getElementById('buddy-panel');
  p.style.display=buddyOpen?'flex':'none';
  if(buddyOpen)document.getElementById('buddy-input').focus();
}
async function sendBuddy(){
  const inp=document.getElementById('buddy-input');
  const msg=inp.value.trim();
  if(!msg)return;
  addMsg(msg,'user');
  inp.value='';
  document.getElementById('buddy-typing').style.display='block';
  try{
    const r=await fetch('/buddy',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg,language:document.getElementById('buddy-lang').value})});
    const d=await r.json();
    document.getElementById('buddy-typing').style.display='none';
    if(d.text)addMsg(d.text,'buddy');
    if(d.audio_url){new Audio(d.audio_url).play().catch(()=>{});}
  }catch(e){
    document.getElementById('buddy-typing').style.display='none';
    addMsg('Sorry, could not connect. Try again!','buddy');
  }
}
function addMsg(text,sender){
  const m=document.getElementById('buddy-messages');
  const d=document.createElement('div');
  if(sender==='user'){
    d.style.cssText='background:linear-gradient(135deg,#7c3aed,#a855f7);border-radius:12px 12px 2px 12px;padding:0.75rem;font-size:0.85rem;color:white;max-width:85%;align-self:flex-end;margin-left:auto;';
    d.textContent=text;
  }else{
    d.style.cssText='background:#16213e;border-radius:12px 12px 12px 2px;padding:0.75rem;font-size:0.85rem;color:#e2e8f0;max-width:85%;';
    d.innerHTML='<span style="font-size:0.7rem;color:#818cf8;display:block;margin-bottom:4px;">Gruha Buddy</span>'+text;
  }
  m.appendChild(d);
  m.scrollTop=m.scrollHeight;
}
</script>
"""

if "buddy-btn" not in base:
    base = base.replace("</body>", buddy_widget + "\n</body>")
    print("Buddy widget added to base.html!")
else:
    print("Buddy widget already exists in base.html")

with open(os.path.join(templates, "base.html"), "w", encoding="utf-8") as f:
    f.write(base)
print("base.html saved!")

# Create style quiz page
quiz_html = """{% extends 'base.html' %}
{% block content %}
<div style="max-width:800px;margin:0 auto;padding:2rem;">
  <h1 style="text-align:center;font-size:2rem;font-weight:700;margin-bottom:0.5rem;background:linear-gradient(135deg,#818cf8,#a855f7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Style Quiz</h1>
  <p style="text-align:center;color:#94a3b8;margin-bottom:2rem;">Answer 5 questions to discover your perfect interior design style</p>
  
  <div style="background:#1a1a2e;border-radius:12px;padding:0.5rem 1rem;margin-bottom:2rem;">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
      <span id="q-label" style="font-size:0.85rem;color:#94a3b8;">Question 1 of 5</span>
      <span id="q-pct" style="font-size:0.85rem;color:#818cf8;">20%</span>
    </div>
    <div style="height:6px;background:#2d3748;border-radius:3px;overflow:hidden;">
      <div id="progress-bar" style="height:100%;background:linear-gradient(90deg,#7c3aed,#a855f7);border-radius:3px;width:20%;transition:width 0.3s;"></div>
    </div>
  </div>

  <div id="quiz-container">
    <div id="question-box" style="text-align:center;">
      <h2 id="q-text" style="font-size:1.4rem;font-weight:600;margin-bottom:2rem;color:#e2e8f0;"></h2>
      <div id="options" style="display:grid;grid-template-columns:repeat(2,1fr);gap:1rem;"></div>
    </div>
  </div>

  <div id="result-box" style="display:none;text-align:center;">
    <div style="font-size:4rem;margin-bottom:1rem;">🏠</div>
    <h2 style="font-size:1.8rem;font-weight:700;margin-bottom:0.5rem;background:linear-gradient(135deg,#818cf8,#a855f7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Your Style: <span id="result-style"></span></h2>
    <p id="result-desc" style="color:#94a3b8;margin-bottom:2rem;line-height:1.7;max-width:500px;margin-left:auto;margin-right:auto;"></p>
    <div id="result-colors" style="display:flex;justify-content:center;gap:12px;margin-bottom:2rem;"></div>
    <a id="start-designing" href="/design" style="display:inline-flex;align-items:center;gap:8px;padding:0.85rem 2rem;background:linear-gradient(135deg,#7c3aed,#a855f7);color:white;border-radius:8px;text-decoration:none;font-weight:600;font-size:1rem;">
      <i class="fas fa-magic"></i> Start Designing
    </a>
  </div>
</div>

<script>
const questions = [
  {q:"What color mood appeals to you?", opts:["Neutral & Calm","Bold & Vibrant","Dark & Moody","Light & Airy"], icons:["🤍","🌈","🖤","☀️"]},
  {q:"Pick your ideal furniture style", opts:["Sleek & Modern","Rustic & Warm","Classic & Elegant","Eclectic & Mixed"], icons:["🔷","🪵","🏛️","🎨"]},
  {q:"What material do you love most?", opts:["Natural Wood","Metal & Glass","Fabric & Textile","Stone & Marble"], icons:["🌿","✨","🛋️","💎"]},
  {q:"Choose your lighting preference", opts:["Bright Natural Light","Warm Ambient Glow","Dramatic Spotlights","Soft Diffused Light"], icons:["☀️","🕯️","💡","🌙"]},
  {q:"What is your space priority?", opts:["Minimalism","Comfort","Style Statement","Functionality"], icons:["⬜","😊","💫","⚙️"]}
];

const styleMap = {
  "0000":"Modern Minimalist","0001":"Scandinavian","0010":"Contemporary","0011":"Scandinavian",
  "0100":"Industrial","0101":"Bohemian","0110":"Traditional","0111":"Bohemian",
  "1000":"Industrial","1001":"Bohemian","1010":"Contemporary","1011":"Traditional",
  "1100":"Industrial","1101":"Bohemian","1110":"Traditional","1111":"Bohemian"
};

const styleDesc = {
  "Modern Minimalist":"Clean lines, neutral colors, and functional furniture. Your space is intentional and clutter-free.",
  "Scandinavian":"Bright airy spaces with natural materials and cozy textures. Hygge is your design language.",
  "Industrial":"Raw materials, exposed textures, and urban character. You appreciate authenticity and edge.",
  "Bohemian":"Layered patterns, rich colors, and handcrafted pieces. Your space tells a story.",
  "Traditional":"Classic elegance with timeless finishes. You value quality and enduring beauty.",
  "Contemporary":"Trend-forward and flexible. You love current aesthetics with personal touches."
};

const styleColors = {
  "Modern Minimalist":["#FFFFFF","#000000","#808080","#F5F5F5"],
  "Scandinavian":["#F5F0E8","#2C5F2E","#D4A373","#FEFAE0"],
  "Industrial":["#2E2E2E","#5A5A5A","#8C7B75","#B0A8A0"],
  "Bohemian":["#E76F51","#2A9D8F","#E9C46A","#F4A261"],
  "Traditional":["#7A4E2D","#C9B79C","#8B0000","#F5E6CC"],
  "Contemporary":["#D9D9D9","#4A4E69","#9A8C98","#F2E9E4"]
};

let current=0, answers=[];

function showQuestion(n){
  const q=questions[n];
  document.getElementById('q-text').textContent=q.q;
  document.getElementById('q-label').textContent='Question '+(n+1)+' of 5';
  const pct=((n+1)/5*100);
  document.getElementById('q-pct').textContent=Math.round(pct)+'%';
  document.getElementById('progress-bar').style.width=pct+'%';
  const opts=document.getElementById('options');
  opts.innerHTML='';
  q.opts.forEach((opt,i)=>{
    const d=document.createElement('div');
    d.style.cssText='background:#16213e;border:2px solid #2d3748;border-radius:12px;padding:1.5rem 1rem;cursor:pointer;transition:all 0.2s;text-align:center;';
    d.innerHTML='<div style="font-size:2rem;margin-bottom:0.5rem;">'+q.icons[i]+'</div><p style="color:#e2e8f0;font-weight:600;font-size:0.95rem;margin:0;">'+opt+'</p>';
    d.onmouseover=()=>d.style.borderColor='#7c3aed';
    d.onmouseout=()=>d.style.borderColor='#2d3748';
    d.onclick=()=>answer(i);
    opts.appendChild(d);
  });
}

function answer(i){
  answers.push(i);
  if(current<4){current++;showQuestion(current);}
  else showResult();
}

function showResult(){
  const key=answers.slice(0,4).map(a=>a>1?'1':'0').join('');
  const style=styleMap[key]||'Modern Minimalist';
  document.getElementById('quiz-container').style.display='none';
  document.getElementById('result-box').style.display='block';
  document.getElementById('result-style').textContent=style;
  document.getElementById('result-desc').textContent=styleDesc[style];
  document.getElementById('start-designing').href='/design?style='+encodeURIComponent(style);
  const colors=styleColors[style]||[];
  const rc=document.getElementById('result-colors');
  rc.innerHTML=colors.map(c=>'<div style="width:48px;height:48px;border-radius:50%;background:'+c+';border:2px solid #2d3748;" title="'+c+'"></div>').join('');
  document.getElementById('progress-bar').style.width='100%';
  document.getElementById('q-label').textContent='Quiz Complete!';
  document.getElementById('q-pct').textContent='100%';
}

showQuestion(0);
</script>
{% endblock %}"""

quiz_path = os.path.join(templates, "style_quiz.html")
with open(quiz_path, "w", encoding="utf-8") as f:
    f.write(quiz_html)
print("style_quiz.html created!")

# Add route to app.py
app_path = r"E:\gruha_alankara\app.py"
with open(app_path, encoding="utf-8") as f:
    app_code = f.read()

if "style-quiz" not in app_code:
    route = """
    @app.route("/style-quiz")
    def style_quiz():
        return render_template("style_quiz.html")
"""
    app_code = app_code.replace(
        '@app.route("/seed-db")',
        route + '\n    @app.route("/seed-db")'
    )
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(app_code)
    print("Style quiz route added to app.py!")

# Add Style Quiz link to navbar in base.html
with open(os.path.join(templates, "base.html"), encoding="utf-8") as f:
    base = f.read()

if "style-quiz" not in base:
    base = base.replace(
        '<a href="/catalog" class="nav-link">My Catalog</a>',
        '<a href="/catalog" class="nav-link">My Catalog</a>\n    <a href="/style-quiz" class="nav-link">Style Quiz</a>'
    )
    with open(os.path.join(templates, "base.html"), "w", encoding="utf-8") as f:
        f.write(base)
    print("Style Quiz link added to navbar!")

print("\nALL FEATURES ADDED SUCCESSFULLY!")
print("Restart Flask: E:\\gruha_alankara\\.venv\\Scripts\\python.exe run.py")
