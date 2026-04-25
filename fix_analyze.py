import os

content = """{% extends 'base.html' %}
{% block content %}
<div style="max-width:900px;margin:0 auto;padding:2rem;">

  <div style="text-align:center;margin-bottom:2rem;">
    <h1 style="font-size:2rem;font-weight:700;background:linear-gradient(135deg,#818cf8,#a855f7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Room Analysis</h1>
    <p style="color:#94a3b8;margin-top:0.5rem;">Upload your room photo and AI will analyze dimensions, lighting, colors and suggest styles</p>
  </div>

  <!-- Step 1 -->
  <div style="background:#1a1a2e;border:1px solid #2d3748;border-radius:16px;padding:2rem;margin-bottom:1.5rem;">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:1.5rem;">
      <div style="width:32px;height:32px;background:linear-gradient(135deg,#7c3aed,#a855f7);border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;color:white;font-size:0.85rem;">1</div>
      <h3 style="font-weight:700;">Upload Room Photo</h3>
    </div>
    <div id="drop-zone" onclick="openFileDialog()"
      style="border:2px dashed #2d3748;border-radius:12px;padding:2.5rem;text-align:center;cursor:pointer;transition:all 0.2s;"
      onmouseover="this.style.borderColor='#7c3aed';this.style.background='rgba(124,58,237,0.05)'"
      onmouseout="this.style.borderColor='#2d3748';this.style.background='transparent'">
      <i class="fas fa-cloud-upload-alt" style="font-size:3rem;color:#818cf8;display:block;margin-bottom:1rem;"></i>
      <p style="color:#e2e8f0;font-weight:600;margin-bottom:0.5rem;">Click to upload your room photo</p>
      <p style="color:#6b7280;font-size:0.85rem;">Supports JPG, PNG, WEBP, GIF</p>
    </div>
    <input type="file" id="file-input" accept="image/*" style="display:none" onchange="previewImage(this)">
    <div id="preview-container" style="display:none;margin-top:1rem;position:relative;">
      <img id="preview-img" style="width:100%;max-height:350px;object-fit:cover;border-radius:12px;">
      <button onclick="document.getElementById('file-input').click()"
        style="position:absolute;bottom:12px;right:12px;background:rgba(0,0,0,0.75);color:white;border:none;border-radius:8px;padding:0.5rem 1rem;cursor:pointer;">
        <i class="fas fa-sync" style="margin-right:4px;"></i>Change Photo
      </button>
    </div>
  </div>

  <!-- Step 2 -->
  <div style="background:#1a1a2e;border:1px solid #2d3748;border-radius:16px;padding:2rem;margin-bottom:1.5rem;">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:1.5rem;">
      <div style="width:32px;height:32px;background:linear-gradient(135deg,#7c3aed,#a855f7);border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;color:white;font-size:0.85rem;">2</div>
      <h3 style="font-weight:700;">Select Room Type</h3>
    </div>
    <div style="display:flex;gap:1rem;align-items:center;flex-wrap:wrap;">
      <select id="room-type" style="background:#0d0d1a;border:1px solid #2d3748;color:#e2e8f0;border-radius:8px;padding:0.6rem 1rem;font-size:0.95rem;min-width:200px;">
        <option>Living Room</option>
        <option>Bedroom</option>
        <option>Kitchen</option>
        <option>Bathroom</option>
        <option>Office</option>
        <option>Dining Room</option>
      </select>
      <button onclick="analyzeRoom()" id="analyze-btn"
        style="background:linear-gradient(135deg,#7c3aed,#a855f7);color:white;border:none;border-radius:8px;padding:0.7rem 2rem;font-size:0.95rem;font-weight:600;cursor:pointer;display:flex;align-items:center;gap:8px;transition:opacity 0.2s;">
        <i class="fas fa-search"></i> Analyze Room
      </button>
    </div>
  </div>

  <!-- Loading -->
  <div id="loading-section" style="display:none;text-align:center;padding:3rem;background:#1a1a2e;border:1px solid #2d3748;border-radius:16px;margin-bottom:1.5rem;">
    <div style="width:64px;height:64px;border:4px solid #2d3748;border-top-color:#7c3aed;border-radius:50%;animation:spin 1s linear infinite;margin:0 auto 1.5rem;"></div>
    <p style="color:#e2e8f0;font-size:1.1rem;font-weight:600;">Analyzing your room...</p>
    <p style="color:#6b7280;font-size:0.85rem;margin-top:0.5rem;">Detecting dimensions, lighting, colors and features</p>
    <div style="display:flex;justify-content:center;gap:1rem;margin-top:1.5rem;flex-wrap:wrap;">
      <span id="step-dims" style="background:#16213e;border:1px solid #2d3748;border-radius:20px;padding:4px 12px;font-size:0.8rem;color:#6b7280;">📐 Dimensions</span>
      <span id="step-light" style="background:#16213e;border:1px solid #2d3748;border-radius:20px;padding:4px 12px;font-size:0.8rem;color:#6b7280;">💡 Lighting</span>
      <span id="step-colors" style="background:#16213e;border:1px solid #2d3748;border-radius:20px;padding:4px 12px;font-size:0.8rem;color:#6b7280;">🎨 Colors</span>
      <span id="step-style" style="background:#16213e;border:1px solid #2d3748;border-radius:20px;padding:4px 12px;font-size:0.8rem;color:#6b7280;">✨ Style Match</span>
    </div>
  </div>

  <!-- Step 3: Results -->
  <div id="results-section" style="display:none;">
    <div style="background:#1a1a2e;border:1px solid #2d3748;border-radius:16px;padding:2rem;margin-bottom:1.5rem;">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:1.5rem;">
        <div style="width:32px;height:32px;background:linear-gradient(135deg,#10b981,#059669);border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;">
          <i class="fas fa-check" style="font-size:0.85rem;"></i>
        </div>
        <h3 style="font-weight:700;">Analysis Complete</h3>
        <span style="background:rgba(16,185,129,0.15);color:#10b981;border:1px solid rgba(16,185,129,0.3);border-radius:20px;padding:2px 10px;font-size:0.75rem;">AI Powered</span>
      </div>

      <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:1rem;margin-bottom:1rem;">
        <div style="background:#0d0d1a;border:1px solid #2d3748;border-radius:12px;padding:1.25rem;">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:0.75rem;">
            <i class="fas fa-ruler-combined" style="color:#818cf8;"></i>
            <h4 style="font-weight:700;font-size:0.9rem;">Dimensions</h4>
          </div>
          <div id="dim-results" style="font-size:0.88rem;color:#94a3b8;line-height:2.2;"></div>
        </div>

        <div style="background:#0d0d1a;border:2px solid #7c3aed;border-radius:12px;padding:1.25rem;">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:0.75rem;">
            <i class="fas fa-lightbulb" style="color:#818cf8;"></i>
            <h4 style="font-weight:700;font-size:0.9rem;">Lighting Analysis</h4>
          </div>
          <div id="light-results" style="font-size:0.88rem;color:#94a3b8;line-height:2.2;"></div>
        </div>

        <div style="background:#0d0d1a;border:1px solid #2d3748;border-radius:12px;padding:1.25rem;">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:0.75rem;">
            <i class="fas fa-palette" style="color:#818cf8;"></i>
            <h4 style="font-weight:700;font-size:0.9rem;">Room Color Palette</h4>
          </div>
          <div id="color-results" style="display:flex;flex-wrap:wrap;gap:10px;margin-top:0.5rem;"></div>
        </div>

        <div style="background:#0d0d1a;border:1px solid #2d3748;border-radius:12px;padding:1.25rem;">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:0.75rem;">
            <i class="fas fa-chart-bar" style="color:#818cf8;"></i>
            <h4 style="font-weight:700;font-size:0.9rem;">Room Features</h4>
          </div>
          <div id="feature-results" style="font-size:0.88rem;color:#94a3b8;line-height:2.2;"></div>
        </div>
      </div>

      <div style="background:#0d0d1a;border:1px solid #2d3748;border-radius:12px;padding:1.25rem;margin-bottom:1.5rem;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:1rem;">
          <i class="fas fa-magic" style="color:#818cf8;"></i>
          <h4 style="font-weight:700;font-size:0.9rem;">Recommended Design Styles</h4>
        </div>
        <div id="style-results" style="display:flex;gap:1rem;flex-wrap:wrap;"></div>
      </div>

      <div style="text-align:center;">
        <a id="proceed-btn" href="/design"
          style="display:inline-flex;align-items:center;gap:8px;padding:0.9rem 2.5rem;background:linear-gradient(135deg,#7c3aed,#a855f7);color:white;border-radius:8px;text-decoration:none;font-weight:600;font-size:1rem;transition:opacity 0.2s;"
          onmouseover="this.style.opacity='0.9'" onmouseout="this.style.opacity='1'">
          <i class="fas fa-arrow-right"></i> Proceed to Design Studio
        </a>
      </div>
    </div>
  </div>
</div>

<style>
@keyframes spin{to{transform:rotate(360deg)}}
.step-active{background:#16213e!important;border-color:#7c3aed!important;color:#818cf8!important;}
</style>

<script>
function previewImage(input) {
  if(input.files && input.files[0]) {
    const reader = new FileReader();
    reader.onload = e => {
      document.getElementById('preview-img').src = e.target.result;
      document.getElementById('drop-zone').style.display = 'none';
      document.getElementById('preview-container').style.display = 'block';
    };
    reader.readAsDataURL(input.files[0]);
  }
}

async function analyzeRoom() {
  const file = document.getElementById('file-input').files[0];
  if(!file) {
    alert('Please upload a room photo first!');
    return;
  }
  const btn = document.getElementById('analyze-btn');
  btn.innerHTML = "<i class='fas fa-spinner fa-spin'></i> Analyzing...";
  btn.disabled = true;
  document.getElementById('loading-section').style.display = 'block';
  document.getElementById('results-section').style.display = 'none';

  let stepIdx = 0;
  const steps = ['step-dims','step-light','step-colors','step-style'];
  const stepTimer = setInterval(() => {
    steps.forEach(s => document.getElementById(s).className = '');
    if(stepIdx < steps.length) {
      document.getElementById(steps[stepIdx]).classList.add('step-active');
      stepIdx++;
    }
  }, 600);

  const fd = new FormData();
  fd.append('image', file);
  fd.append('room_type', document.getElementById('room-type').value);

  try {
    const res = await fetch('/analyze-room', {method:'POST', body:fd});
    const data = await res.json();
    clearInterval(stepTimer);
    document.getElementById('loading-section').style.display = 'none';

    if(data.error) {
      alert('Error: ' + data.error);
      btn.innerHTML = "<i class='fas fa-search'></i> Analyze Room";
      btn.disabled = false;
      return;
    }

    const d = data.dimensions;
    document.getElementById('dim-results').innerHTML =
      "<b style='color:#e2e8f0'>Width:</b> " + d.width + " ft<br>" +
      "<b style='color:#e2e8f0'>Length:</b> " + d.length + " ft<br>" +
      "<b style='color:#e2e8f0'>Height:</b> " + d.height + " ft<br>" +
      "<b style='color:#e2e8f0'>Area:</b> <span style='color:#818cf8;font-weight:700'>" + d.area + " sq ft</span>";

    const l = data.lighting;
    const lc = l.quality==='Excellent'?'#10b981':l.quality==='Good'?'#818cf8':l.quality==='Moderate'?'#f59e0b':'#ef4444';
    document.getElementById('light-results').innerHTML =
      "<b style='color:#e2e8f0'>Quality:</b> <span style='color:" + lc + ";font-weight:700'>" + l.quality + "</span><br>" +
      "<b style='color:#e2e8f0'>Brightness:</b> " + l.brightness + "/255<br>" +
      "<p style='margin-top:6px;font-size:0.82rem;line-height:1.6;color:#94a3b8'>" + l.description + "</p>";

    document.getElementById('color-results').innerHTML = data.colors.map(c =>
      "<div style='text-align:center'>" +
      "<div style='width:48px;height:48px;border-radius:10px;background:" + c + ";border:2px solid #2d3748;margin-bottom:4px;'></div>" +
      "<span style='font-size:0.65rem;color:#94a3b8'>" + c + "</span></div>"
    ).join('');

    const f = data.features;
    document.getElementById('feature-results').innerHTML =
      "<b style='color:#e2e8f0'>Complexity:</b> " + f.complexity + "<br>" +
      "<b style='color:#e2e8f0'>Edges:</b> " + f.edges + "<br>" +
      "<b style='color:#e2e8f0'>Orientation:</b> " + f.orientation;

    const roomType = document.getElementById('room-type').value;
    const styleMap = {
      'Living Room':['Modern Minimalist','Scandinavian','Contemporary'],
      'Bedroom':['Scandinavian','Traditional','Bohemian'],
      'Kitchen':['Modern Minimalist','Industrial','Contemporary'],
      'Office':['Modern Minimalist','Industrial','Contemporary'],
      'Bathroom':['Modern Minimalist','Scandinavian','Contemporary'],
      'Dining Room':['Traditional','Contemporary','Scandinavian']
    };
    const styles = styleMap[roomType] || ['Modern Minimalist','Scandinavian','Contemporary'];
    const labels = ['Best Match','Great Fit','Good Choice'];
    const colors = ['#818cf8','#10b981','#f59e0b'];
    document.getElementById('style-results').innerHTML = styles.map((s,i) =>
      "<div onclick=\"window.location.href='/design?style=" + encodeURIComponent(s) + "'\" style='background:#16213e;border:1px solid #2d3748;border-radius:10px;padding:0.75rem 1.25rem;cursor:pointer;transition:all 0.2s;flex:1;min-width:150px;' onmouseover=\"this.style.borderColor='#7c3aed'\" onmouseout=\"this.style.borderColor='#2d3748'\">" +
      "<span style='font-size:0.72rem;color:" + colors[i] + ";display:block;margin-bottom:4px;font-weight:600'>" + labels[i] + "</span>" +
      "<span style='font-weight:600;color:#e2e8f0;font-size:0.9rem'>" + s + "</span>" +
      "<p style='font-size:0.75rem;color:#6b7280;margin-top:4px;'>Click to design</p></div>"
    ).join('');

    document.getElementById('proceed-btn').href = '/design?room_type=' + encodeURIComponent(roomType) + '&area=' + d.area;
    document.getElementById('results-section').style.display = 'block';
    document.getElementById('results-section').scrollIntoView({behavior:'smooth'});

  } catch(e) {
    clearInterval(stepTimer);
    document.getElementById('loading-section').style.display = 'none';
    alert('Analysis failed. Please try again.');
  }

  btn.innerHTML = "<i class='fas fa-search'></i> Analyze Room";
  btn.disabled = false;
}
</script>
{% endblock %}"""

with open(r"E:\gruha_alankara\templates\analyze.html", "w", encoding="utf-8") as f:
    f.write(content)
print("analyze.html rewritten successfully!")