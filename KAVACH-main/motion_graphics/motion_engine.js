/**
 * KAVACH Motion Graphics Engine & Live Controller
 * Provides real-time animation control, state switching, wave oscillators,
 * and copy-ready embed snippets for KAVACH platform.
 */

document.addEventListener("DOMContentLoaded", () => {
  initWaveOscillator();
  initHashTicker();
  initControls();
  initModal();
});

// Current active speed factor
let currentSpeed = 1;

function initControls() {
  const speedBtns = document.querySelectorAll(".speed-btn");
  speedBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      speedBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentSpeed = parseFloat(btn.dataset.speed);
      document.documentElement.style.setProperty("--anim-speed-factor", currentSpeed);
    });
  });

  const stateBtns = document.querySelectorAll(".state-btn");
  stateBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      stateBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const state = btn.dataset.state;
      
      document.body.classList.remove("state-attack", "state-lockdown", "state-safe");
      if (state === "attack") {
        document.body.classList.add("state-attack");
        triggerAttackSoundFx();
      } else if (state === "lockdown") {
        document.body.classList.add("state-lockdown");
      } else if (state === "safe") {
        document.body.classList.add("state-safe");
      }
    });
  });

  const themeToggle = document.getElementById("themeToggle");
  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      document.body.classList.toggle("theme-light");
      themeToggle.classList.toggle("active");
    });
  }
}

// 1. Quantum Latency Wave Oscillator (Canvas / SVG wave)
function initWaveOscillator() {
  const canvas = document.getElementById("waveCanvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  let step = 0;

  function resize() {
    canvas.width = canvas.parentElement.clientWidth || 320;
    canvas.height = 120;
  }
  window.addEventListener("resize", resize);
  resize();

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const isAttack = document.body.classList.contains("state-attack");
    
    // Gradient line
    const grad = ctx.createLinearGradient(0, 0, canvas.width, 0);
    if (isAttack) {
      grad.addColorStop(0, "#ef4444");
      grad.addColorStop(0.5, "#f59e0b");
      grad.addColorStop(1, "#ef4444");
    } else {
      grad.addColorStop(0, "#06b6d4");
      grad.addColorStop(0.5, "#3b82f6");
      grad.addColorStop(1, "#10b981");
    }

    ctx.beginPath();
    ctx.lineWidth = 3;
    ctx.strokeStyle = grad;
    ctx.shadowBlur = 12;
    ctx.shadowColor = isAttack ? "rgba(239, 68, 68, 0.6)" : "rgba(6, 182, 212, 0.6)";

    const amplitude = isAttack ? 25 : 12;
    const frequency = isAttack ? 0.04 : 0.02;
    const speedInc = 0.05 * currentSpeed;

    for (let x = 0; x < canvas.width; x++) {
      const y = (canvas.height / 2) + Math.sin((x * frequency) + step) * amplitude * Math.cos(x * 0.005 + step * 0.5);
      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    step += speedInc;
    requestAnimationFrame(draw);
  }
  draw();
}

// 2. Real-time Cryptographic Hash Stream
function initHashTicker() {
  const ticker = document.getElementById("hashTicker");
  if (!ticker) return;

  const hex = "0123456789abcdef";
  setInterval(() => {
    let hash = "SHA256: ";
    for (let i = 0; i < 16; i++) {
      hash += hex[Math.floor(Math.random() * hex.length)];
    }
    hash += "...";
    ticker.textContent = hash;
  }, 800 / currentSpeed);
}

// 3. Attack Simulation Visual Flash
function triggerAttackSoundFx() {
  const flash = document.createElement("div");
  flash.style.position = "fixed";
  flash.style.inset = "0";
  flash.style.backgroundColor = "rgba(239, 68, 68, 0.15)";
  flash.style.pointerEvents = "none";
  flash.style.zIndex = "999";
  flash.style.transition = "opacity 0.4s ease";
  document.body.appendChild(flash);
  setTimeout(() => {
    flash.style.opacity = "0";
    setTimeout(() => flash.remove(), 400);
  }, 100);
}

// 4. Copy-Ready Embed Code Modal
const EMBED_SNIPPETS = {
  "radar": `<div class="kavach-radar-wrap">
  <div class="radar-box">
    <div class="radar-ring ring-1"></div>
    <div class="radar-ring ring-2"></div>
    <div class="radar-ring ring-3"></div>
    <div class="radar-sweep"></div>
    <div class="radar-shield-center">
      <svg viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
      </svg>
    </div>
  </div>
</div>`,

  "highway": `<div class="kavach-highway-lane">
  <div class="lane-glow-track"></div>
  <div class="highway-node-gate gate-ast">AST</div>
  <div class="highway-node-gate gate-dpdp">DPDP</div>
  <div class="highway-node-gate gate-core">CORE</div>
  <div class="packet-stream">
    <span class="packet-pill">TX: ₹4,500 [CLEARED]</span>
  </div>
</div>`,

  "interceptor": `<div class="interceptor-box">
  <div class="interceptor-core">
    <div class="hexagon-barrier"></div>
    <div class="shockwave-ring"></div>
    <div class="interceptor-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"/>
        <path d="M12 8v4M12 16h.01"/>
      </svg>
    </div>
  </div>
</div>`
};

function initModal() {
  const modal = document.getElementById("codeModal");
  const codeBox = document.getElementById("codeSnippet");
  const closeBtn = document.getElementById("closeModalBtn");
  const copyBtn = document.getElementById("copyCodeBtn");

  document.querySelectorAll(".embed-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const type = btn.dataset.snippet || "radar";
      codeBox.textContent = EMBED_SNIPPETS[type] || EMBED_SNIPPETS["radar"];
      modal.classList.add("active");
    });
  });

  if (closeBtn) {
    closeBtn.addEventListener("click", () => modal.classList.remove("active"));
  }

  modal.addEventListener("click", (e) => {
    if (e.target === modal) modal.classList.remove("active");
  });

  if (copyBtn) {
    copyBtn.addEventListener("click", () => {
      navigator.clipboard.writeText(codeBox.textContent).then(() => {
        const original = copyBtn.textContent;
        copyBtn.textContent = "Copied to Clipboard! ✓";
        copyBtn.style.background = "#10b981";
        setTimeout(() => {
          copyBtn.textContent = original;
          copyBtn.style.background = "";
        }, 2000);
      });
    });
  }
}
