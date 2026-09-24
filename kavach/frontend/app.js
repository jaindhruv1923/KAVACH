// Kavach Phase 8 dashboard — talks to the real FastAPI backend.
// Every panel renders whatever the backend actually returned. Nothing here
// decides "Aadhaar = blocked" — that decision is made entirely by
// backend/app/security/detector.py (Phase 4). This file only displays it.

const API_BASE = "http://127.0.0.1:8000";

const ingestBtn = document.getElementById("ingest-btn");
const repoPathInput = document.getElementById("repo-path");
const ingestStatus = document.getElementById("ingest-status");
const submitBtn = document.getElementById("submit-btn");
const requestInput = document.getElementById("request-input");
const networkError = document.getElementById("network-error");
const micBtn = document.getElementById("mic-btn");
const micStatus = document.getElementById("mic-status");
const githubBtn = document.getElementById("github-btn");
const githubUrl = document.getElementById("github-url");
const githubStatus = document.getElementById("github-status");
const reviewBtn = document.getElementById("review-btn");
const reviewInput = document.getElementById("review-input");
const reviewFilename = document.getElementById("review-filename");
const reviewResult = document.getElementById("review-result");
const liveFeed = document.getElementById("live-feed");
const liveClock = document.getElementById("live-clock");

function updateLiveClock() {
  liveClock.textContent = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
}
updateLiveClock();
setInterval(updateLiveClock, 1000);

// --- Groq Whisper STT & Audio Recording ---
const groqModal = document.getElementById("groq-modal");
const groqCfgBtn = document.getElementById("groq-cfg-btn");
const groqModalClose = document.getElementById("groq-modal-close");
const groqKeyInput = document.getElementById("groq-key-input");
const groqSaveBtn = document.getElementById("groq-save-btn");
const groqClearBtn = document.getElementById("groq-clear-btn");
const groqModalStatus = document.getElementById("groq-modal-status");

function getGroqKey() {
  return localStorage.getItem("GROQ_API_KEY") || "";
}

function updateGroqBtnState() {
  if (groqCfgBtn) {
    const hasKey = Boolean(getGroqKey());
    groqCfgBtn.textContent = hasKey ? "⚡ Groq Active" : "⚡ Groq Whisper";
    groqCfgBtn.style.color = hasKey ? "var(--safe)" : "var(--accent)";
    groqCfgBtn.style.borderColor = hasKey ? "var(--safe-border)" : "rgba(0, 210, 255, 0.3)";
  }
}
updateGroqBtnState();

if (groqCfgBtn) {
  groqCfgBtn.addEventListener("click", () => {
    if (groqModal) {
      groqModal.style.display = "flex";
      groqKeyInput.value = getGroqKey();
      groqModalStatus.textContent = getGroqKey() ? "Current key loaded." : "No key configured.";
      groqKeyInput.focus();
    }
  });
}
if (groqModalClose) {
  groqModalClose.addEventListener("click", () => {
    if (groqModal) groqModal.style.display = "none";
  });
}
if (groqSaveBtn) {
  groqSaveBtn.addEventListener("click", () => {
    const key = groqKeyInput.value.trim();
    if (!key) {
      groqModalStatus.textContent = "Please paste a valid Groq key (gsk_...).";
      groqModalStatus.style.color = "var(--blocked)";
      return;
    }
    localStorage.setItem("GROQ_API_KEY", key);
    updateGroqBtnState();
    groqModalStatus.textContent = "✓ Groq API Key saved successfully!";
    groqModalStatus.style.color = "var(--safe)";
    setTimeout(() => { if (groqModal) groqModal.style.display = "none"; }, 800);
  });
}
if (groqClearBtn) {
  groqClearBtn.addEventListener("click", () => {
    localStorage.removeItem("GROQ_API_KEY");
    groqKeyInput.value = "";
    updateGroqBtnState();
    groqModalStatus.textContent = "Groq key cleared. Using browser fallback.";
    groqModalStatus.style.color = "var(--text-dim)";
  });
}
if (groqModal) {
  groqModal.addEventListener("click", (e) => {
    if (e.target === groqModal) groqModal.style.display = "none";
  });
}

// Microphone Speech-To-Text: Groq Whisper (with native MediaRecorder) + Browser Fallback
let mediaRecorder = null;
let audioChunks = [];
let mediaStream = null;

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const speechRecognition = SpeechRecognition ? new SpeechRecognition() : null;
let voiceBaseText = "";
let finalVoiceText = "";
let voiceStopRequested = false;

if (speechRecognition) {
  speechRecognition.continuous = true;
  speechRecognition.interimResults = true;
  speechRecognition.lang = navigator.language || "en-US";
  speechRecognition.onstart = () => {
    micBtn.classList.add("recording");
    micBtn.setAttribute("aria-label", "Stop voice input");
    micBtn.title = "Stop voice input";
    micStatus.textContent = "Listening (browser mic). Speak now...";
  };
  speechRecognition.onresult = event => {
    let interimVoiceText = "";
    for (let index = event.resultIndex; index < event.results.length; index += 1) {
      const transcript = event.results[index][0].transcript;
      if (event.results[index].isFinal) finalVoiceText += transcript;
      else interimVoiceText += transcript;
    }
    const spokenText = `${finalVoiceText} ${interimVoiceText}`.trim();
    requestInput.value = [voiceBaseText, spokenText].filter(Boolean).join(" ");
    requestInput.dispatchEvent(new Event("input", { bubbles: true }));
    requestInput.scrollTop = requestInput.scrollHeight;
  };
  speechRecognition.onerror = event => {
    const messages = {
      "not-allowed": "Microphone permission was denied. Allow microphone access and try again.",
      "audio-capture": "No microphone was found. Check your microphone and try again.",
      "network": "Speech recognition needs an internet connection in this browser.",
      "no-speech": "No speech detected. Keep speaking after pressing the microphone.",
    };
    micStatus.textContent = messages[event.error] || `Voice input error: ${event.error}`;
    if (["not-allowed", "service-not-allowed", "audio-capture", "network"].includes(event.error)) {
      voiceStopRequested = true;
    }
  };
  speechRecognition.onend = () => {
    if (!voiceStopRequested && micBtn.classList.contains("recording")) {
      try {
        speechRecognition.start();
        return;
      } catch (error) {}
    }
    micBtn.classList.remove("recording");
    micBtn.setAttribute("aria-label", "Start voice input");
    micBtn.title = "Start voice input";
    if (requestInput.value.trim()) micStatus.textContent = "Voice captured. Press Enter to run it.";
  };
}

async function startGroqRecording() {
  voiceBaseText = requestInput.value.trim();
  audioChunks = [];
  micStatus.textContent = "Requesting microphone permission...";
  try {
    mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
  } catch (err) {
    micStatus.textContent = "Microphone access denied: " + err.message;
    return;
  }
  
  let options = {};
  if (MediaRecorder.isTypeSupported("audio/webm;codecs=opus")) {
    options = { mimeType: "audio/webm;codecs=opus" };
  } else if (MediaRecorder.isTypeSupported("audio/webm")) {
    options = { mimeType: "audio/webm" };
  } else if (MediaRecorder.isTypeSupported("audio/mp4")) {
    options = { mimeType: "audio/mp4" };
  }
  
  try {
    mediaRecorder = new MediaRecorder(mediaStream, options);
  } catch (e) {
    mediaRecorder = new MediaRecorder(mediaStream);
  }
  
  mediaRecorder.ondataavailable = (event) => {
    if (event.data && event.data.size > 0) {
      audioChunks.push(event.data);
    }
  };
  
  mediaRecorder.onstart = () => {
    micBtn.classList.add("recording");
    micBtn.setAttribute("aria-label", "Stop recording and transcribe with Groq Whisper");
    micBtn.title = "Stop recording and transcribe with Groq Whisper";
    micStatus.textContent = "Recording audio... Click mic to finish & transcribe with Whisper AI.";
  };
  
  mediaRecorder.onstop = async () => {
    micBtn.classList.remove("recording");
    micBtn.setAttribute("aria-label", "Start voice input");
    micBtn.title = "Start voice input";
    if (mediaStream) {
      mediaStream.getTracks().forEach(track => track.stop());
      mediaStream = null;
    }
    
    if (audioChunks.length === 0) {
      micStatus.textContent = "No audio recorded.";
      return;
    }
    
    micStatus.textContent = "Transcribing with Groq Whisper AI...";
    const audioBlob = new Blob(audioChunks, { type: mediaRecorder.mimeType || "audio/webm" });
    const groqKey = getGroqKey();
    
    try {
      const formData = new FormData();
      formData.append("file", audioBlob, "audio.webm");
      formData.append("model", "whisper-large-v3-turbo");
      formData.append("response_format", "json");
      formData.append("temperature", "0");
      
      const response = await fetch("https://api.groq.com/openai/v1/audio/transcriptions", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${groqKey}`
        },
        body: formData
      });
      
      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        const errMsg = errData.error && errData.error.message ? errData.error.message : `HTTP ${response.status}`;
        throw new Error(errMsg);
      }
      
      const data = await response.json();
      const transcript = (data.text || "").trim();
      if (transcript) {
        requestInput.value = [voiceBaseText, transcript].filter(Boolean).join(" ");
        requestInput.dispatchEvent(new Event("input", { bubbles: true }));
        requestInput.scrollTop = requestInput.scrollHeight;
        micStatus.textContent = `Whisper: "${transcript.slice(0, 45)}${transcript.length > 45 ? '...' : ''}" captured!`;
      } else {
        micStatus.textContent = "Whisper detected no speech. Try speaking closer to mic.";
      }
    } catch (err) {
      micStatus.textContent = `Groq Whisper error: ${err.message}`;
    }
  };
  
  mediaRecorder.start(250);
}

function stopGroqRecording() {
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
  }
}

micBtn.addEventListener("click", () => {
  const groqKey = getGroqKey();
  
  if (groqKey) {
    if (micBtn.classList.contains("recording")) {
      stopGroqRecording();
    } else {
      startGroqRecording();
    }
    return;
  }
  
  if (speechRecognition) {
    if (micBtn.classList.contains("recording")) {
      voiceStopRequested = true;
      speechRecognition.stop();
      return;
    }
    if (!window.isSecureContext && location.hostname !== "localhost" && location.hostname !== "127.0.0.1") {
      micStatus.textContent = "Voice input requires HTTPS or localhost.";
      return;
    }
    voiceBaseText = requestInput.value.trim();
    finalVoiceText = "";
    voiceStopRequested = false;
    micStatus.textContent = "Requesting microphone permission...";
    try {
      speechRecognition.start();
    } catch (error) {
      micStatus.textContent = "Microphone is already starting. Try again in a moment.";
    }
    return;
  }
  
  if (groqModal) {
    groqModal.style.display = "flex";
    groqModalStatus.textContent = "Enter your Groq API key to enable Whisper speech-to-text.";
    groqKeyInput.focus();
  } else {
    micStatus.textContent = "Voice input requires Groq API key or Chrome/Edge speech recognition.";
  }
});


// The full intended pipeline order, per docs/AGENT_SPEC.md's WorkflowStage
// enum. Used only to render the pipeline visualization — the actual stage
// reached comes from the backend's `history` and `final_stage` fields.
const PIPELINE_STAGES = [
  "REQUEST_RECEIVED",
  "PLANNING",
  "CONTEXT_RETRIEVAL",
  "SECURITY_CHECK",
  "IMPACT_ANALYSIS",
  "GENERATION",
  "COMPLETE",
];

// --- Safe fetch helper: never blindly calls response.json() on a bad response ---
async function safeFetch(url, options) {
  let response;
  try {
    response = await fetch(url, options);
  } catch (networkErr) {
    throw new Error(
      "Could not reach the Kavach backend at " + API_BASE +
      ". Is the server running (uvicorn app.main:app --reload)? " +
      "Raw error: " + networkErr.message
    );
  }

  const rawText = await response.text();
  let data = null;
  if (rawText) {
    try {
      data = JSON.parse(rawText);
    } catch (parseErr) {
      throw new Error(
        `Backend returned a non-JSON response (HTTP ${response.status}). ` +
        `Raw body: ${rawText.slice(0, 200)}`
      );
    }
  }

  if (!response.ok) {
    const detail = data && data.detail ? JSON.stringify(data.detail) : rawText;
    throw new Error(`Backend returned HTTP ${response.status}: ${detail}`);
  }

  return data;
}

function showNetworkError(message) {
  networkError.textContent = "⚠ " + message;
  networkError.style.display = "block";
}

function clearNetworkError() {
  networkError.style.display = "none";
}

function animateCounter(elementId, targetValue, duration = 400) {
  const el = document.getElementById(elementId);
  if (!el) return;
  const start = parseInt(el.textContent, 10) || 0;
  const end = Number(targetValue) || 0;
  if (start === end) { el.textContent = end; return; }
  const startTime = performance.now();
  function update(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const easeOut = 1 - Math.pow(1 - progress, 3);
    const current = Math.round(start + (end - start) * easeOut);
    el.textContent = current;
    if (progress < 1) requestAnimationFrame(update);
    else el.textContent = end;
  }
  requestAnimationFrame(update);
}

async function loadCommandCenter() {
  try {
    const config = await safeFetch(`${API_BASE}/config/status`);
    const dot = document.getElementById("gemini-dot");
    document.getElementById("gemini-status").textContent = config.gemini_configured
      ? `Gemini connected · ${config.gemini_model}`
      : "Gemini not configured · using safe stub";
    dot.classList.toggle("online", config.gemini_configured);
    dot.classList.toggle("offline", !config.gemini_configured);
    const runs = await safeFetch(`${API_BASE}/agent/runs`);
    const runList = runs.runs || [];
    animateCounter("run-count", runList.length);
    animateCounter("review-count", runList.filter(run => run.stage === "NEEDS_REVIEW").length);
    animateCounter("block-count", runList.filter(run => run.stage === "BLOCKED").length);
  } catch (error) {
    document.getElementById("gemini-status").textContent = "Backend unavailable";
  }
}

githubBtn.addEventListener("click", async () => {
  const repositoryUrl = githubUrl.value.trim();
  if (!repositoryUrl) {
    githubStatus.textContent = "Enter a public GitHub URL first.";
    githubStatus.className = "status-line status-blocked";
    return;
  }
  githubBtn.disabled = true;
  liveFeed.textContent = "Live · scanning GitHub repository";
  githubStatus.textContent = "Scanning repository and building its evidence index...";
  githubStatus.className = "status-line status-neutral";
  try {
    const data = await safeFetch(`${API_BASE}/github/ingest`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ repository_url: repositoryUrl }),
    });
    githubStatus.textContent = `${data.repository}: scanned ${data.files_scanned} files, indexed ${data.chunks_indexed} chunks, found ${data.finding_count} security signals.`;
    githubStatus.className = data.finding_count ? "status-line status-review" : "status-line status-safe";
    liveFeed.textContent = `Live · ${data.repository} indexed and ready for analysis`;
  } catch (error) {
    githubStatus.textContent = error.message;
    githubStatus.className = "status-line status-blocked";
    liveFeed.textContent = "Live · repository scan needs attention";
  } finally {
    githubBtn.disabled = false;
  }
});

reviewBtn.addEventListener("click", async () => {
  const code = reviewInput.value.trim();
  if (!code) {
    reviewResult.innerHTML = `<p class="empty-note">Paste code before starting a review.</p>`;
    return;
  }
  reviewBtn.disabled = true;
  reviewBtn.textContent = "Reviewing...";
  liveFeed.textContent = "Live · security review in progress";
  try {
    const data = await safeFetch(`${API_BASE}/review`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code, filename: reviewFilename.value.trim() || "pasted-code.txt" }),
    });
    const policy = data.policy_decision || {};
    const verdictClass = policy.decision === "BLOCK" ? "status-blocked" : policy.decision === "ALLOW" ? "status-safe" : "status-review";
    const findings = data.findings.length
      ? data.findings.map(f => `<div class="finding-item ${escapeHtml(f.severity || "")}"><strong>${escapeHtml(f.category)}</strong><span>${escapeHtml(f.reason || "Signal detected")}</span></div>`).join("")
      : `<p class="empty-note">No findings detected.</p>`;
    reviewResult.innerHTML = `<p class="status-line ${verdictClass}">${escapeHtml(policy.decision || "REVIEW")} · ${data.finding_count} finding(s) · risk ${policy.risk_score ?? "n/a"}</p>${findings}<div class="recommendations"><strong>Next action</strong><ul>${data.recommendations.map(item => `<li>${escapeHtml(item)}</li>`).join("")}</ul></div>`;
    liveFeed.textContent = `Live · review complete · ${policy.decision || "REVIEW"} decision`;
  } catch (error) {
    reviewResult.innerHTML = `<p class="status-line status-blocked">${escapeHtml(error.message)}</p>`;
    liveFeed.textContent = "Live · review failed to reach the backend";
  } finally {
    reviewBtn.disabled = false;
    reviewBtn.textContent = "Run review";
  }
});

loadCommandCenter();

window.setRequest = function(text) {
  requestInput.value = text;
  requestInput.focus();
};

function maskValue(val) {
  if (!val) return "";
  const s = String(val).trim();
  if (s.length <= 4) return "****";
  const start = s.slice(0, Math.min(4, Math.floor(s.length / 3)));
  const end = s.slice(-Math.min(3, Math.floor(s.length / 3)));
  const maskLen = Math.max(3, s.length - start.length - end.length);
  return `${start}${"*".repeat(maskLen)}${end}`;
}

// --- Ingest ---
ingestBtn.addEventListener("click", async () => {
  const repoPath = repoPathInput.value.trim() || "app";
  ingestBtn.disabled = true;
  ingestStatus.textContent = "Indexing in progress...";
  ingestStatus.className = "status-line status-neutral";

  try {
    const data = await safeFetch(`${API_BASE}/ingest`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ repo_path: repoPath }),
    });
    ingestStatus.textContent =
      `Indexed successfully — ${data.chunks_indexed} chunks from "${data.repo_path}".`;
    ingestStatus.className = "status-line status-safe";
  } catch (err) {
    ingestStatus.textContent = err.message;
    ingestStatus.className = "status-line status-blocked";
  } finally {
    ingestBtn.disabled = false;
  }
});

// --- Submit request ---
submitBtn.addEventListener("click", async () => {
  const requestText = requestInput.value.trim();
  clearNetworkError();

  if (!requestText) {
    showNetworkError("Enter a request before submitting.");
    return;
  }

  submitBtn.disabled = true;
  submitBtn.textContent = "Running Kavach workflow...";
  liveFeed.textContent = "Live · Kavach agent is processing your request";
  hideAllResultCards();

  try {
    const data = await safeFetch(`${API_BASE}/agent/request`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ request_text: requestText }),
    });
    renderWorkflowResult(data);
    loadCommandCenter();
    liveFeed.textContent = `Live · workflow completed with ${data.final_stage}`;
  } catch (err) {
    showNetworkError(err.message);
    liveFeed.textContent = "Live · workflow needs attention";
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Initiate Kavach Workflow";
  }
});

requestInput.addEventListener("keydown", event => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    submitBtn.click();
  }
});

function hideAllResultCards() {
  ["security-card", "policy-card", "pipeline-card", "rag-card", "impact-card",
   "generation-card", "validation-card", "history-card"].forEach(id => {
    document.getElementById(id).style.display = "none";
  });
}

// --- Render everything from the actual backend response ---
function renderWorkflowResult(data) {
  renderSecurityStatus(data);
  renderPolicyDecision(data);
  renderPipeline(data);
  renderRagEvidence(data);
  renderImpactAnalysis(data);
  renderGeneration(data);
  renderValidation(data);
  renderHistory(data);
}

function renderSecurityStatus(data) {
  const card = document.getElementById("security-card");
  const el = document.getElementById("security-status");
  card.style.display = "block";

  const findings = data.security_findings || [];
  const stage = data.final_stage;
  const isBlocked = stage === "BLOCKED";
  const isReview = stage === "NEEDS_REVIEW";

  let verdictHtml;
  if (isBlocked) {
    verdictHtml = `<div class="security-verdict" style="color:var(--blocked)">🚫 BLOCKED — Sensitive identifier detected</div>`;
  } else if (isReview) {
    verdictHtml = `<div class="security-verdict" style="color:var(--review)">⚠ NEEDS REVIEW — Sensitive identifier detected & flagged</div>`;
  } else if (findings.length > 0) {
    verdictHtml = `<div class="security-verdict" style="color:var(--review)">⚠ Findings detected but workflow proceeded (redact/audit-level)</div>`;
  } else {
    verdictHtml = `<div class="security-verdict" style="color:var(--safe)">✓ SAFE — No sensitive information detected</div>`;
  }

  let findingsHtml = "";
  if (findings.length > 0) {
    findingsHtml = findings.map(f => {
      const masked = f.value ? maskValue(f.value) : "";
      return `<div class="finding-item ${f.severity || ''}">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;gap:8px;flex-wrap:wrap;">
          <strong>${escapeHtml(f.category)}</strong>
          ${masked ? `<span class="masked-badge">Identified: <code>${escapeHtml(masked)}</code></span>` : ""}
        </div>
        <div>
          severity: <strong>${escapeHtml(f.severity || 'n/a')}</strong>,
          action: <strong>${escapeHtml(f.action)}</strong>${f.confidence !== undefined ? `, confidence: ${f.confidence}` : ''}
        </div>
        ${f.reason ? `<div style="margin-top:4px;color:var(--text-dim)">${escapeHtml(f.reason)}</div>` : ''}
      </div>`;
    }).join("");
  } else {
    findingsHtml = `<p class="empty-note">No sensitive-data findings in this request or its retrieved context.</p>`;
  }

  el.innerHTML = verdictHtml + findingsHtml;
}

function renderPolicyDecision(data) {
  const card = document.getElementById("policy-card");
  const el = document.getElementById("policy-decision");
  const policy = data.policy_decision;

  if (!policy || Object.keys(policy).length === 0) {
    card.style.display = "block";
    el.innerHTML = `<p class="empty-note">No policy evaluation recorded for this run.</p>`;
    return;
  }

  card.style.display = "block";
  const decisionColor = {
    "ALLOW": "var(--safe)",
    "REDACT": "var(--review)",
    "REVIEW": "var(--review)",
    "BLOCK": "var(--blocked)",
  }[policy.decision] || "var(--neutral)";

  el.innerHTML = `
    <div class="security-verdict" style="color:${decisionColor}">
      ${escapeHtml(policy.decision)} — risk score: ${policy.risk_score}
    </div>
    <div class="finding-item">
      <strong>Requested action risk:</strong> ${escapeHtml(policy.action_risk_classification || "n/a")}
      <div style="margin-top:4px;color:var(--text-dim)">${escapeHtml(policy.explanation || "")}</div>
    </div>
  `;
}

function renderPipeline(data) {
  const card = document.getElementById("pipeline-card");
  const el = document.getElementById("pipeline");
  card.style.display = "block";

  // Determine which stages were actually reached from the history log.
  const history = data.history || [];
  const reachedStages = new Set(["REQUEST_RECEIVED"]);
  history.forEach(line => {
    const match = line.match(/->\s*WorkflowStage\.(\w+)/);
    if (match) reachedStages.add(match[1]);
  });

  const stoppedAt = data.final_stage;
  const stoppedEarly = stoppedAt === "BLOCKED" || stoppedAt === "NEEDS_REVIEW";

  el.innerHTML = PIPELINE_STAGES.map(stage => {
    const reached = reachedStages.has(stage) || stage === stoppedAt;
    let cls = "not-reached";
    let icon = "○";
    if (reached) { cls = "reached"; icon = "✓"; }
    return `<div class="pipeline-step ${cls}">${icon} ${stage.replace(/_/g, " ")}</div>`;
  }).join("") + (stoppedEarly
    ? `<div class="pipeline-step stopped">🚫 ${stoppedAt.replace(/_/g, " ")}</div>`
    : "");
}

function renderRagEvidence(data) {
  const card = document.getElementById("rag-card");
  const el = document.getElementById("rag-evidence");
  const context = data.retrieved_context || [];

  if (context.length === 0) {
    card.style.display = "block";
    el.innerHTML = `<p class="empty-note">No repository evidence retrieved (repository may not be indexed yet — use "Ingest Repository" above).</p>`;
    return;
  }

  card.style.display = "block";
  el.innerHTML = context.map(chunk => `
    <div class="evidence-chunk">
      <span class="file-path">${escapeHtml(chunk.file_path)}</span>
      <span class="score">score: ${chunk.score.toFixed(3)}</span>
      <div class="snippet">${escapeHtml((chunk.text || "").slice(0, 300))}${chunk.text && chunk.text.length > 300 ? "..." : ""}</div>
    </div>
  `).join("");
}

function renderImpactAnalysis(data) {
  const card = document.getElementById("impact-card");
  const el = document.getElementById("impact-report");
  const report = data.impact_report || [];

  card.style.display = "block";
  if (report.length === 0) {
    el.innerHTML = `<p class="empty-note">No impact analysis performed (workflow may have stopped before this stage, or no relevant files were found).</p>`;
    return;
  }

  el.innerHTML = report.map(item => `
    <div class="impact-item">
      <span>${escapeHtml(item.file_path)}</span>
      <span class="impact-score">${item.relevance_score}</span>
    </div>
    <div class="empty-note" style="margin:-6px 0 6px;">${escapeHtml(item.reason || "")}</div>
  `).join("");
}

function renderGeneration(data) {
  const card = document.getElementById("generation-card");
  const el = document.getElementById("generation-result");
  const gen = data.generation_result;

  if (!gen || Object.keys(gen).length === 0) {
    card.style.display = "block";
    el.innerHTML = `<p class="empty-note">Generation was not reached for this request (workflow stopped earlier, or evidence was insufficient).</p>`;
    return;
  }

  card.style.display = "block";
  const configNote = gen.llm_configured
    ? `<p class="status-line status-safe">Real LLM generation (Gemini)</p>`
    : `<p class="status-line status-review">Stub response — no GEMINI_API_KEY configured on the backend</p>`;

  el.innerHTML = configNote + `<pre class="code-block">${escapeHtml(gen.generated_output || "(no output)")}</pre>`;
}

function renderValidation(data) {
  const card = document.getElementById("validation-card");
  const el = document.getElementById("validation-result");
  const val = data.validation_result;

  if (!val || Object.keys(val).length === 0) {
    card.style.display = "block";
    el.innerHTML = `<p class="empty-note">Validation was not reached for this request.</p>`;
    return;
  }

  card.style.display = "block";
  if (val.valid_syntax) {
    el.innerHTML = `<p class="status-line status-safe">✓ Syntax validation passed</p>`;
  } else {
    el.innerHTML = `<p class="status-line status-blocked">✗ Validation failed — ${escapeHtml(val.error || "unknown error")}</p>`;
  }
}

function renderHistory(data) {
  const card = document.getElementById("history-card");
  const list = document.getElementById("history-list");
  const history = data.history || [];

  card.style.display = "block";
  list.innerHTML = history.map(line => `<li>${escapeHtml(line)}</li>`).join("")
    || `<li class="empty-note">No history recorded.</li>`;
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
