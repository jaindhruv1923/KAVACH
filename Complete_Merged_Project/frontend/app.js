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
  hideAllResultCards();

  try {
    const data = await safeFetch(`${API_BASE}/agent/request`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ request_text: requestText }),
    });
    renderWorkflowResult(data);
  } catch (err) {
    showNetworkError(err.message);
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Initiate Kavach Workflow";
  }
});

function hideAllResultCards() {
  ["security-card", "pipeline-card", "rag-card", "impact-card",
   "generation-card", "validation-card", "history-card"].forEach(id => {
    document.getElementById(id).style.display = "none";
  });
}

// --- Render everything from the actual backend response ---
function renderWorkflowResult(data) {
  renderSecurityStatus(data);
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
    verdictHtml = `<div class="security-verdict" style="color:var(--blocked)">🚫 BLOCKED — Sensitive information detected</div>`;
  } else if (isReview) {
    verdictHtml = `<div class="security-verdict" style="color:var(--review)">⚠ NEEDS REVIEW — Sensitive information found in retrieved context</div>`;
  } else if (findings.length > 0) {
    verdictHtml = `<div class="security-verdict" style="color:var(--review)">⚠ Findings detected but workflow proceeded (redact/audit-level)</div>`;
  } else {
    verdictHtml = `<div class="security-verdict" style="color:var(--safe)">✓ SAFE — No sensitive information detected</div>`;
  }

  let findingsHtml = "";
  if (findings.length > 0) {
    findingsHtml = findings.map(f => {
      // Never display the raw sensitive value — category, severity, and
      // reason only, per Kavach's own explainability + privacy principle.
      return `<div class="finding-item ${f.severity || ''}">
        <strong>${escapeHtml(f.category)}</strong> — severity: ${escapeHtml(f.severity || 'n/a')},
        action: ${escapeHtml(f.action)}${f.confidence !== undefined ? `, confidence: ${f.confidence}` : ''}
        ${f.reason ? `<div style="margin-top:4px;color:var(--text-dim)">${escapeHtml(f.reason)}</div>` : ''}
      </div>`;
    }).join("");
  } else {
    findingsHtml = `<p class="empty-note">No sensitive-data findings in this request or its retrieved context.</p>`;
  }

  el.innerHTML = verdictHtml + findingsHtml;
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
