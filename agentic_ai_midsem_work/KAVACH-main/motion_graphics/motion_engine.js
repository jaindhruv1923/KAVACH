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
  initFuzzerInteractivity();
  initMerkleTreeInteractivity();
  initAblationInteractivity();
  initMultisigInteractivity();
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
</div>`,

  "fuzzer": `<div class="fuzzer-box">
  <div class="fuzzer-chamber">
    <div class="fuzzer-emitter"><div class="emitter-core emitter-red">500</div></div>
    <div class="fuzzer-barrier"></div>
    <div class="fuzzer-emitter"><div class="emitter-core emitter-green">0.48ms</div></div>
  </div>
</div>`,

  "merkle": `<div class="merkle-box">
  <svg class="merkle-svg-wrap" viewBox="0 0 320 150">
    <circle cx="160" cy="25" r="14" fill="#0f172a" stroke="#10b981" stroke-width="2.5"/>
    <text x="160" y="29" fill="#10b981" font-size="9" text-anchor="middle">ROOT</text>
  </svg>
</div>`,

  "ablation": `<div class="ablation-meter-wrap">
  <div class="ablation-bar-track"><div class="ablation-bar-fill" style="width: 98.2%;"></div></div>
</div>`,

  "multisig": `<div class="multisig-highway-track">
  <div class="agent-circle-icon agent-adk">ADK</div>
  <div class="hsm-vault-lock">VAULT</div>
  <div class="agent-circle-icon agent-crew">CREW</div>
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

// ============================================================================
// ACADEMIC WEAPON CARD CONTROLLERS (Cards 7 - 10)
// ============================================================================

// Card 7: Genetic Adversarial Fuzzer
function initFuzzerInteractivity() {
  const burstBtn = document.getElementById("fuzzerBurstBtn");
  const catBtns = document.querySelectorAll(".fuzzer-cat-btn");
  const emitter = document.getElementById("fuzzerEmitter");
  if (!burstBtn) return;

  catBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      catBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      if (emitter) {
        emitter.textContent = btn.dataset.cat.substring(0, 3).toUpperCase();
        setTimeout(() => { emitter.textContent = "500"; }, 1500);
      }
    });
  });

  burstBtn.addEventListener("click", () => {
    burstBtn.textContent = "Mutating...";
    burstBtn.style.background = "#f59e0b";
    
    // Animate particles
    document.querySelectorAll(".fuzzer-burst-p").forEach(p => {
      p.style.animation = "none";
      p.offsetHeight; // trigger reflow
      p.style.animation = "fuzzerFly 0.8s infinite linear";
    });

    setTimeout(() => {
      burstBtn.textContent = "489/500 Intercepted";
      burstBtn.style.background = "#10b981";
      setTimeout(() => {
        burstBtn.textContent = "Execute Mutation Burst";
        burstBtn.style.background = "#ef4444";
      }, 2500);
    }, 1200);
  });
}

// Card 8: SLSA Level 3 Merkle Tree
function initMerkleTreeInteractivity() {
  const tamperBtn = document.getElementById("tamperSimBtn");
  const leaf2 = document.getElementById("merkleLeaf2");
  const leaf2Text = document.getElementById("merkleLeaf2Text");
  const rootCircle = document.getElementById("merkleRootCircle");
  const rootText = document.getElementById("merkleRootText");
  const hudText = document.getElementById("merkleStatusText");
  const lineRRight = document.getElementById("line-r-right");
  const lineL2 = document.getElementById("line-l-2");

  if (!tamperBtn) return;

  let isTampered = false;

  tamperBtn.addEventListener("click", () => {
    isTampered = !isTampered;
    if (isTampered) {
      if (leaf2) { leaf2.setAttribute("stroke", "#ef4444"); leaf2.setAttribute("fill", "rgba(239, 68, 68, 0.3)"); }
      if (leaf2Text) { leaf2Text.setAttribute("fill", "#ef4444"); }
      if (rootCircle) { rootCircle.setAttribute("stroke", "#ef4444"); rootCircle.setAttribute("fill", "rgba(239, 68, 68, 0.4)"); }
      if (rootText) { rootText.setAttribute("fill", "#ef4444"); rootText.textContent = "FAIL"; }
      if (lineRRight) { lineRRight.setAttribute("stroke", "#ef4444"); }
      if (lineL2) { lineL2.setAttribute("stroke", "#ef4444"); }
      if (hudText) {
        hudText.innerHTML = "[TAMPER DETECTED] Root Digest Mismatch (NIST SP 800-218 Broken)!";
        hudText.style.color = "#ef4444";
      }
      tamperBtn.textContent = "Re-Attest Seal";
      tamperBtn.style.background = "rgba(16, 185, 129, 0.2)";
      tamperBtn.style.borderColor = "#10b981";
      tamperBtn.style.color = "#34d399";
    } else {
      if (leaf2) { leaf2.setAttribute("stroke", "#a855f7"); leaf2.setAttribute("fill", "#0f172a"); }
      if (leaf2Text) { leaf2Text.setAttribute("fill", "#a855f7"); }
      if (rootCircle) { rootCircle.setAttribute("stroke", "#10b981"); rootCircle.setAttribute("fill", "#0f172a"); }
      if (rootText) { rootText.setAttribute("fill", "#10b981"); rootText.textContent = "ROOT"; }
      if (lineRRight) { lineRRight.setAttribute("stroke", "#334155"); }
      if (lineL2) { lineL2.setAttribute("stroke", "#334155"); }
      if (hudText) {
        hudText.innerHTML = "● MERKLE ROOT: 611689ea... [SLSA L3 VERIFIED]";
        hudText.style.color = "#10b981";
      }
      tamperBtn.textContent = "Simulate Tamper";
      tamperBtn.style.background = "rgba(239, 68, 68, 0.15)";
      tamperBtn.style.borderColor = "#ef4444";
      tamperBtn.style.color = "#f87171";
    }
  });
}

// Card 9: Scientific Ablation Study Comparator
function initAblationInteractivity() {
  const toggleProx = document.getElementById("toggleProximity");
  const toggleEnt = document.getElementById("toggleEntropy");
  const toggleObf = document.getElementById("toggleObfuscation");
  const f1Text = document.getElementById("ablationF1Score");
  const barFill = document.getElementById("ablationBarFill");

  if (!toggleProx || !toggleEnt || !toggleObf) return;

  function updateAblation() {
    const pOn = toggleProx.classList.contains("active");
    const eOn = toggleEnt.classList.contains("active");
    const oOn = toggleObf.classList.contains("active");

    let f1 = 0.982;
    let delta = 0.0;

    if (!oOn) { f1 -= 0.218; delta -= 0.218; }
    if (!pOn) { f1 -= 0.070; delta -= 0.070; }
    if (!eOn) { f1 -= 0.095; delta -= 0.095; }

    f1 = Math.max(0.450, f1);

    if (f1Text) {
      const deltaStr = delta === 0 ? "ΔF1: 0.000" : `ΔF1: ${delta.toFixed(3)}`;
      f1Text.textContent = `${f1.toFixed(3)} (${deltaStr})`;
      f1Text.style.color = f1 >= 0.90 ? "#10b981" : f1 >= 0.80 ? "#f59e0b" : "#ef4444";
    }

    if (barFill) {
      const pct = (f1 * 100).toFixed(1);
      barFill.style.width = `${pct}%`;
      if (f1 >= 0.90) {
        barFill.style.background = "linear-gradient(90deg, #10b981, #06b6d4)";
      } else if (f1 >= 0.80) {
        barFill.style.background = "linear-gradient(90deg, #f59e0b, #fbbf24)";
      } else {
        barFill.style.background = "linear-gradient(90deg, #ef4444, #f87171)";
      }
    }
  }

  [toggleProx, toggleEnt, toggleObf].forEach(t => {
    t.addEventListener("click", () => {
      t.classList.toggle("active");
      updateAblation();
    });
  });
}

// Card 10: Multi-Agent Dual-Custody Multi-Sig Highway
function initMultisigInteractivity() {
  const btnDual = document.getElementById("btnDualSigned");
  const btnRogue = document.getElementById("btnRogueBlocked");
  const beamRight = document.getElementById("multisigBeamRight");
  const lock = document.getElementById("hsmVaultLock");
  const statusBadge = document.getElementById("hsmStatusBadge");

  if (!btnDual || !btnRogue) return;

  btnDual.addEventListener("click", () => {
    btnDual.classList.add("active");
    btnRogue.classList.remove("active");
    if (beamRight) beamRight.style.display = "block";
    if (lock) {
      lock.style.borderColor = "#10b981";
      lock.style.background = "linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(6, 182, 212, 0.3))";
      lock.style.color = "#34d399";
    }
    if (statusBadge) {
      statusBadge.textContent = "2-of-2 SIGNED: CLEARED (₹7,50,000)";
      statusBadge.style.color = "#34d399";
    }
  });

  btnRogue.addEventListener("click", () => {
    btnRogue.classList.add("active");
    btnDual.classList.remove("active");
    if (beamRight) beamRight.style.display = "none";
    if (lock) {
      lock.style.borderColor = "#ef4444";
      lock.style.background = "linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(185, 28, 28, 0.3))";
      lock.style.color = "#f87171";
    }
    if (statusBadge) {
      statusBadge.textContent = "BLOCKED: RBI CSF (Missing Auditor Sig)";
      statusBadge.style.color = "#f87171";
    }
  });
}

