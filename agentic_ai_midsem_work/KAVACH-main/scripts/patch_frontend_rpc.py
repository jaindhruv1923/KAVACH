path = 'agentic_ai_midsem_work/KAVACH-main/01_KAVACH_Platform/frontend/implementation_flow.js'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Update Header Badge
badge_code = '              <span id="kavach-live-rpc-badge" class="impl-badge-pill" style="background:#059669;color:#fff;margin-left:6px;font-weight:700;">● LIVE MICROSERVICE CLUSTER (PORT 8000)</span>\n'
for i, line in enumerate(lines):
    if 'CSE3101 AGENTIC AI' in line and 'kavach-live-rpc-badge' not in lines[i+1]:
        lines.insert(i+1, badge_code)
        break

# 2. Update evaluateStep1Live
for i, line in enumerate(lines):
    if 'if (editor) editor.value = ctrlState.inputPayload;' in line and 'window.evaluateStep1Live' in "".join(lines[i-25:i]):
        rpc_snippet = '''
    // Asynchronous Live FastAPI RPC Endpoint
    try {
      const t0 = performance.now();
      const apiUrl = (window.location.port === "8000" || window.location.pathname.startsWith("/api"))
        ? "/api/v1/sentinel/evaluate"
        : "http://localhost:8000/api/v1/sentinel/evaluate";

      fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code: payload, scenario_id: ctrlState.selectedPreset1 })
      })
      .then(res => res.json())
      .then(data => {
        const roundTrip = Math.round(performance.now() - t0);
        const badge = document.getElementById("kavach-live-rpc-badge");
        if (badge) {
          badge.style.background = "#059669";
          badge.innerHTML = `● LIVE RPC CONNECTED &bull; ${data.execution_time_ms}ms (RTT: ${roundTrip}ms)`;
        }
        const term = document.querySelector(".step-terminal-body");
        if (term && data && !term.innerText.includes("[Live FastAPI RPC]")) {
          term.innerText += `\\n[+${roundTrip}ms] [Live FastAPI RPC: Port 8000] Status: ${data.status} • Shannon H: ${data.shannon_entropy} • Secrets: ${data.secrets_count} • AST Threats: ${(data.ast_threats || []).length}`;
        }
      })
      .catch(() => {
        const badge = document.getElementById("kavach-live-rpc-badge");
        if (badge) {
          badge.style.background = "#475569";
          badge.innerHTML = "○ STANDALONE SANDBOX RUNTIME";
        }
      });
    } catch (e) {}
'''
        lines.insert(i+1, rpc_snippet)
        break

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Successfully injected Live RPC connection & Status Pill into implementation_flow.js!")
