/**
 * Interactive Neural Constellation Canvas (Particle Mesh / Constellation Web)
 * High-performance Vanilla HTML5 Canvas simulation in STRICT MONOCHROME (Pure White & Space Black).
 * High-DPI scaling, dynamic distance linking, mouse magnetism, and laser tracking.
 */
function initInteractiveParticleWeb() {
  if (window.__particleWebInitialized) return;
  const canvas = document.getElementById("interactive-particle-web");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  if (!ctx) return;
  window.__particleWebInitialized = true;

  // Enforce fixed full-screen overlay styles directly on element (z-index: 0 so it stays behind UI cards)
  canvas.style.position = "fixed";
  canvas.style.top = "0";
  canvas.style.left = "0";
  canvas.style.inset = "0";
  canvas.style.pointerEvents = "none";
  canvas.style.zIndex = "0";
  canvas.style.opacity = "0.75";
  canvas.style.display = "block";

  let width = window.innerWidth;
  let height = window.innerHeight;
  const dpr = Math.min(window.devicePixelRatio || 1, 2);

  function resize() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = width + "px";
    canvas.style.height = height + "px";
  }
  resize();
  window.addEventListener("resize", resize, { passive: true });

  // Dynamic particle count based on display viewport
  const PARTICLE_COUNT = Math.min(120, Math.max(70, Math.floor((width * height) / 12500)));
  const particles = [];

  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const isBright = Math.random() > 0.35;
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.45,
      vy: (Math.random() - 0.5) * 0.45,
      radius: Math.random() * 1.8 + 1.8,
      color: isBright ? "rgba(255, 255, 255, 0.92)" : "rgba(230, 230, 240, 0.55)",
      pulse: Math.random() * Math.PI * 2
    });
  }

  const mouse = { x: -1000, y: -1000, active: false };

  window.addEventListener("mousemove", (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
    mouse.active = true;
  }, { passive: true });

  window.addEventListener("mouseleave", () => {
    mouse.active = false;
  });

  window.addEventListener("touchstart", (e) => {
    if (e.touches && e.touches[0]) {
      mouse.x = e.touches[0].clientX;
      mouse.y = e.touches[0].clientY;
      mouse.active = true;
    }
  }, { passive: true });

  window.addEventListener("touchmove", (e) => {
    if (e.touches && e.touches[0]) {
      mouse.x = e.touches[0].clientX;
      mouse.y = e.touches[0].clientY;
      mouse.active = true;
    }
  }, { passive: true });

  window.addEventListener("touchend", () => {
    mouse.active = false;
  });

  function renderParticles() {
    ctx.save();
    ctx.scale(dpr, dpr);
    ctx.clearRect(0, 0, width, height);

    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.pulse += 0.03;

      // Wrap around screen boundaries
      if (p.x < 0) p.x = width;
      else if (p.x > width) p.x = 0;
      if (p.y < 0) p.y = height;
      else if (p.y > height) p.y = 0;

      // 1. Mouse Interactive Laser Link (Pure White & Silver)
      if (mouse.active) {
        const dxM = p.x - mouse.x;
        const dyM = p.y - mouse.y;
        const distM = Math.sqrt(dxM * dxM + dyM * dyM);

        if (distM < 200) {
          const mAlpha = (1 - distM / 200) * 0.70;
          ctx.strokeStyle = `rgba(255, 255, 255, ${mAlpha.toFixed(2)})`;
          ctx.lineWidth = 1.2;
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(mouse.x, mouse.y);
          ctx.stroke();

          // Magnetic attraction effect
          if (distM > 15) {
            p.x -= (dxM / distM) * 0.45;
            p.y -= (dyM / distM) * 0.45;
          }
        }
      }

      // 2. Pure White Particle Dot (with subtle pulsing breath)
      const rad = p.radius + Math.sin(p.pulse) * 0.35;
      ctx.fillStyle = p.color;
      ctx.beginPath();
      ctx.arc(p.x, p.y, rad, 0, Math.PI * 2);
      ctx.fill();

      // 3. Connect neighboring dots with Pure White Laser lines
      for (let j = i + 1; j < particles.length; j++) {
        const p2 = particles[j];
        const dx = p.x - p2.x;
        const dy = p.y - p2.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 140) {
          const alpha = (1 - dist / 140) * 0.32;
          ctx.strokeStyle = `rgba(255, 255, 255, ${alpha.toFixed(2)})`;
          ctx.lineWidth = 0.9;
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.stroke();
        }
      }
    }

    // 4. Cursor Halo (Monochrome Glow Ring)
    if (mouse.active && mouse.x > 0 && mouse.y > 0) {
      ctx.fillStyle = "rgba(255, 255, 255, 0.95)";
      ctx.beginPath();
      ctx.arc(mouse.x, mouse.y, 3.5, 0, Math.PI * 2);
      ctx.fill();

      ctx.strokeStyle = "rgba(255, 255, 255, 0.45)";
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.arc(mouse.x, mouse.y, 9, 0, Math.PI * 2);
      ctx.stroke();
    }

    ctx.restore();
    requestAnimationFrame(renderParticles);
  }

  requestAnimationFrame(renderParticles);
}

// Window export & auto-start
window.initInteractiveParticleWeb = initInteractiveParticleWeb;
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initInteractiveParticleWeb);
} else {
  initInteractiveParticleWeb();
}
