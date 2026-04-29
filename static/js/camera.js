/* =============================================================
   Gruha Alankara — AR Camera
   camera.js — handles both the analyze page (start-camera-btn)
               and the full AR page (ar-video / ar-canvas)
   ============================================================= */

/* ─────────────────────────────────────────────────────────────
   SHARED: stop any active stream
   ───────────────────────────────────────────────────────────── */
let activeStream = null;

function stopCamera() {
  if (activeStream) {
    activeStream.getTracks().forEach(t => t.stop());
    activeStream = null;
  }
}
window.stopCamera = stopCamera;

/* =============================================================
   ANALYZE PAGE  (start-camera-btn present)
   ============================================================= */
document.addEventListener('DOMContentLoaded', () => {
  const startBtn   = document.getElementById('start-camera-btn');
  if (!startBtn) return;   // not the analyze page

  const cameraFeed    = document.getElementById('camera-feed');
  const captureBtn    = document.getElementById('capture-room-btn');
  const captureCanvas = document.getElementById('capture-canvas');
  const spinner       = document.getElementById('upload-spinner');
  const recommendations = document.getElementById('ai-recommendations');
  const styleInput    = document.getElementById('selected-style');

  startBtn.addEventListener('click', async () => {
    if (!navigator.mediaDevices?.getUserMedia) {
      alert('Camera not supported in this browser.');
      return;
    }
    try {
      stopCamera();
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } }
      });
      activeStream = stream;
      cameraFeed.srcObject = stream;
      await cameraFeed.play();
      if (captureBtn) captureBtn.style.display = 'inline-flex';
    } catch (err) {
      alert(err.name === 'NotAllowedError'
        ? 'Camera permission denied. Allow access and retry.'
        : 'Unable to start camera.');
    }
  });

  if (captureBtn && captureCanvas) {
    captureBtn.addEventListener('click', async () => {
      if (!cameraFeed.videoWidth) {
        if (recommendations) recommendations.textContent = 'Camera not ready.';
        return;
      }
      captureCanvas.width  = cameraFeed.videoWidth;
      captureCanvas.height = cameraFeed.videoHeight;
      captureCanvas.getContext('2d').drawImage(cameraFeed, 0, 0);
      const b64 = captureCanvas.toDataURL('image/jpeg', 0.85);
      if (spinner) spinner.style.display = 'block';
      try {
        const blob = await (await fetch(b64)).blob();
        const fd   = new FormData();
        fd.append('image', blob, 'room-capture.jpg');
        if (styleInput?.value) fd.append('style_theme', styleInput.value);
        const res  = await fetch('/upload-camera', { method: 'POST', body: fd });
        if (!res.ok) throw new Error('Upload failed');
        const data = await res.json();
        if (recommendations) recommendations.textContent = data.recommendations || data.ai_output || 'Done.';
        if (data.redirect) setTimeout(() => { window.location.href = data.redirect; }, 600);
      } catch {
        if (recommendations) recommendations.textContent = 'Could not upload. Try again.';
      } finally {
        if (spinner) spinner.style.display = 'none';
      }
    });
  }

  document.querySelectorAll('.style-card').forEach(card => {
    card.addEventListener('click', () => {
      document.querySelectorAll('.style-card').forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      if (styleInput) styleInput.value = card.dataset.style || card.textContent.trim();
    });
  });
});

/* =============================================================
   AR PAGE  (ar-video / ar-canvas present)
   ============================================================= */
(function initARPage() {
  const videoEl  = document.getElementById('ar-video');
  if (!videoEl) return;   // not the AR page

  /* ── DOM refs ── */
  const arCanvas      = document.getElementById('ar-canvas');
  const frozenImg     = document.getElementById('ar-frozen');
  const errorDiv      = document.getElementById('ar-error');
  const errorMsg      = document.getElementById('ar-error-msg');
  const hintEl        = document.getElementById('ar-hint');
  const furnPanel     = document.getElementById('furn-panel');
  const captureBtn    = document.getElementById('capture-btn');
  const retakeBtn     = document.getElementById('retake-btn');
  const enableARBtn   = document.getElementById('enable-ar-btn');
  const modeToggle    = document.getElementById('ar-mode-toggle');
  const loadingEl     = document.getElementById('ar-loading');
  const analyseOverlay = document.getElementById('analyse-overlay');
  const vp            = document.getElementById('ar-viewport');

  /* ── State ── */
  let arEnabled       = false;
  let capturedDataUrl = null;
  let selectedType    = null;
  let isDragging      = false;
  let dragMesh        = null;
  let dragStartX      = 0, dragStartZ = 0;
  let pointerStartX   = 0, pointerStartY = 0;
  const placedMeshes  = [];

  /* ── Three.js ── */
  let scene, threeCamera, renderer, raycaster, floorPlane;

  function initThree() {
    if (typeof THREE === 'undefined') {
      console.warn('Three.js not loaded');
      return;
    }
    scene       = new THREE.Scene();
    threeCamera = new THREE.PerspectiveCamera(60, vp.clientWidth / vp.clientHeight, 0.1, 100);
    threeCamera.position.set(0, 1.6, 3);
    threeCamera.lookAt(0, 0, 0);

    renderer = new THREE.WebGLRenderer({ canvas: arCanvas, alpha: true, antialias: true, preserveDrawingBuffer: true });
    renderer.setClearColor(0x000000, 0);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(vp.clientWidth, vp.clientHeight);

    scene.add(new THREE.AmbientLight(0xffffff, 0.9));
    const dir = new THREE.DirectionalLight(0xffffff, 0.8);
    dir.position.set(3, 6, 3);
    scene.add(dir);

    raycaster = new THREE.Raycaster();

    // Invisible floor plane for tap-to-place
    const floorGeo = new THREE.PlaneGeometry(20, 20);
    const floorMat = new THREE.MeshBasicMaterial({ visible: false, side: THREE.DoubleSide });
    floorPlane = new THREE.Mesh(floorGeo, floorMat);
    floorPlane.rotation.x = -Math.PI / 2;
    floorPlane.position.y = -1.5;
    scene.add(floorPlane);

    window.addEventListener('resize', () => {
      renderer.setSize(vp.clientWidth, vp.clientHeight);
      threeCamera.aspect = vp.clientWidth / vp.clientHeight;
      threeCamera.updateProjectionMatrix();
    });

    animate();
  }

  function animate() {
    requestAnimationFrame(animate);
    if (arEnabled && renderer) renderer.render(scene, threeCamera);
  }

  /* ── Furniture definitions ── */
  const FURN_DEFS = {
    sofa: () => {
      const g = new THREE.BoxGeometry(2, 0.8, 1);
      const m = new THREE.MeshPhongMaterial({ color: 0x8B4513, transparent: true, opacity: 0.85 });
      return new THREE.Mesh(g, m);
    },
    table: () => {
      const group = new THREE.Group();
      const top = new THREE.Mesh(
        new THREE.BoxGeometry(1.5, 0.05, 0.8),
        new THREE.MeshPhongMaterial({ color: 0xDEB887, transparent: true, opacity: 0.85 })
      );
      top.position.y = 0.75;
      group.add(top);
      const legMat = new THREE.MeshPhongMaterial({ color: 0xA0522D, transparent: true, opacity: 0.85 });
      [[-0.65, -0.35], [0.65, -0.35], [-0.65, 0.35], [0.65, 0.35]].forEach(([x, z]) => {
        const leg = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.75, 0.06), legMat);
        leg.position.set(x, 0.375, z);
        group.add(leg);
      });
      return group;
    },
    lamp: () => {
      const group = new THREE.Group();
      const pole = new THREE.Mesh(
        new THREE.CylinderGeometry(0.04, 0.04, 1.5, 8),
        new THREE.MeshPhongMaterial({ color: 0xFFD700, transparent: true, opacity: 0.85 })
      );
      pole.position.y = 0.75;
      group.add(pole);
      const shade = new THREE.Mesh(
        new THREE.ConeGeometry(0.3, 0.4, 12),
        new THREE.MeshPhongMaterial({ color: 0xFFF8DC, transparent: true, opacity: 0.85 })
      );
      shade.position.y = 1.65;
      group.add(shade);
      return group;
    },
    shelf: () => {
      const g = new THREE.BoxGeometry(1.2, 0.1, 0.3);
      const m = new THREE.MeshPhongMaterial({ color: 0x808080, transparent: true, opacity: 0.85 });
      const shelf = new THREE.Mesh(g, m);
      shelf.position.y = 1.2;
      return shelf;
    }
  };

  function buildMesh(type) {
    const fn = FURN_DEFS[type];
    if (!fn) return null;
    const mesh = fn();
    mesh.userData.type = type;
    return mesh;
  }

  /* ── Camera init ── */
  function showError(msg) {
    if (errorMsg) errorMsg.textContent = msg;
    if (errorDiv) errorDiv.classList.add('show');
  }

  async function startCamera() {
    const isMobile = /Mobi|Android/i.test(navigator.userAgent);
    const constraints = {
      video: isMobile ? { facingMode: { ideal: 'environment' } } : true,
      audio: false
    };
    try {
      let stream;
      try {
        stream = await navigator.mediaDevices.getUserMedia(constraints);
      } catch (_) {
        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
      }
      activeStream = stream;
      videoEl.srcObject = stream;
      videoEl.style.display = 'block';
      frozenImg.style.display = 'none';
      if (hintEl) { hintEl.textContent = 'Point camera at your room'; hintEl.style.opacity = '1'; }
      setTimeout(() => { if (hintEl) hintEl.style.opacity = '0'; }, 3000);
    } catch (err) {
      showError(err.name === 'NotAllowedError'
        ? 'Camera permission denied. Please allow camera access and try again.'
        : 'No camera found on this device.');
    }
  }

  window.retryCamera = function () {
    if (errorDiv) errorDiv.classList.remove('show');
    startCamera();
  };

  /* ── Capture ── */
  window.capturePhoto = function () {
    if (!videoEl.videoWidth) return;
    const canvas = document.createElement('canvas');
    canvas.width  = videoEl.videoWidth;
    canvas.height = videoEl.videoHeight;
    canvas.getContext('2d').drawImage(videoEl, 0, 0);
    capturedDataUrl = canvas.toDataURL('image/jpeg', 0.9);

    // Freeze frame
    frozenImg.src = capturedDataUrl;
    frozenImg.style.display = 'block';
    videoEl.style.display = 'none';
    stopCamera();

    // Swap UI
    captureBtn.style.display = 'none';
    retakeBtn.style.display  = '';
    enableARBtn.style.display = '';

    // Show analyse overlay
    if (analyseOverlay) analyseOverlay.classList.add('show');
  };

  window.retakePhoto = function () {
    frozenImg.style.display = 'none';
    frozenImg.src = '';
    capturedDataUrl = null;
    captureBtn.style.display = '';
    retakeBtn.style.display  = 'none';
    enableARBtn.style.display = 'none';
    if (modeToggle) modeToggle.style.display = 'none';
    if (furnPanel) furnPanel.style.display = 'none';
    if (analyseOverlay) analyseOverlay.classList.remove('show');
    disableAR();
    startCamera();
  };

  /* ── Analyse room ── */
  window.sendToAnalyse = async function () {
    if (!capturedDataUrl) return;
    if (analyseOverlay) analyseOverlay.classList.remove('show');
    if (loadingEl) loadingEl.classList.add('show');
    try {
      const blob = await (await fetch(capturedDataUrl)).blob();
      const fd   = new FormData();
      fd.append('image', blob, 'room-capture.jpg');
      const res  = await fetch('/analyze-room', { method: 'POST', body: fd });
      const data = await res.json();
      if (loadingEl) loadingEl.classList.remove('show');
      if (!res.ok || data.error) {
        showError(data.error || 'Analysis failed. Please try again.');
        return;
      }
      sessionStorage.setItem('lastAnalysis', JSON.stringify(data));
      window.location.href = '/analyze';
    } catch {
      if (loadingEl) loadingEl.classList.remove('show');
      showError('Analysis failed. Check your connection.');
    }
  };

  window.closeAnalyseOverlay = function () {
    if (analyseOverlay) analyseOverlay.classList.remove('show');
  };

  /* ── AR mode ── */
  function disableAR() {
    arEnabled = false;
    arCanvas.classList.remove('interactive');
    if (modeToggle) { modeToggle.textContent = 'AR OFF'; modeToggle.classList.remove('active'); }
    if (furnPanel) furnPanel.style.display = 'none';
    // Clear meshes
    placedMeshes.forEach(m => scene && scene.remove(m));
    placedMeshes.length = 0;
    if (renderer) renderer.clear();
  }

  window.enableAR = function () {
    if (!renderer) initThree();
    arEnabled = true;
    arCanvas.classList.add('interactive');
    if (modeToggle) { modeToggle.textContent = 'AR ON'; modeToggle.classList.add('active'); modeToggle.style.display = ''; }
    if (furnPanel) furnPanel.style.display = 'block';
    if (analyseOverlay) analyseOverlay.classList.remove('show');
  };

  window.toggleARMode = function () {
    if (arEnabled) disableAR(); else window.enableAR();
  };

  /* ── Furniture selection ── */
  window.selectFurniture = function (type) {
    selectedType = type;
    document.querySelectorAll('.furn-btn').forEach(b => b.classList.toggle('selected', b.dataset.type === type));
    if (hintEl) { hintEl.textContent = 'Tap to place ' + type; hintEl.style.opacity = '1'; }
    setTimeout(() => { if (hintEl) hintEl.style.opacity = '0'; }, 2500);
  };

  /* ── Tap to place ── */
  function getPointerNDC(e) {
    const rect = arCanvas.getBoundingClientRect();
    const src  = e.touches ? e.touches[0] : e;
    return {
      x:  ((src.clientX - rect.left)  / rect.width)  * 2 - 1,
      y: -((src.clientY - rect.top)   / rect.height) * 2 + 1
    };
  }

  function snapToWall(mesh) {
    const p = mesh.position;
    if (p.x >  3) p.x =  3;
    if (p.x < -3) p.x = -3;
    if (p.z >  3) p.z =  3;
    if (p.z < -3) p.z = -3;
  }

  arCanvas.addEventListener('pointerdown', e => {
    if (!arEnabled || !selectedType) return;
    const ndc = getPointerNDC(e);
    raycaster.setFromCamera(ndc, threeCamera);
    const hits = raycaster.intersectObject(floorPlane);
    if (!hits.length) return;

    const pt   = hits[0].point;
    const mesh = buildMesh(selectedType);
    if (!mesh) return;
    mesh.position.set(pt.x, pt.y + 0.4, pt.z);
    snapToWall(mesh);
    scene.add(mesh);
    placedMeshes.push(mesh);

    // Start drag on this mesh
    dragMesh    = mesh;
    isDragging  = true;
    dragStartX  = pt.x;
    dragStartZ  = pt.z;
    pointerStartX = e.clientX || (e.touches && e.touches[0].clientX) || 0;
    pointerStartY = e.clientY || (e.touches && e.touches[0].clientY) || 0;
    arCanvas.setPointerCapture(e.pointerId);
    e.preventDefault();
  }, { passive: false });

  arCanvas.addEventListener('pointermove', e => {
    if (!isDragging || !dragMesh) return;
    const dx = ((e.clientX || 0) - pointerStartX) * 0.01;
    const dz = ((e.clientY || 0) - pointerStartY) * 0.01;
    dragMesh.position.x = dragStartX + dx;
    dragMesh.position.z = dragStartZ + dz;
    snapToWall(dragMesh);
    e.preventDefault();
  }, { passive: false });

  arCanvas.addEventListener('pointerup', () => {
    isDragging = false;
    dragMesh   = null;
  });

  /* ── Init ── */
  initThree();
  startCamera();

  window.addEventListener('beforeunload', stopCamera);
})();
