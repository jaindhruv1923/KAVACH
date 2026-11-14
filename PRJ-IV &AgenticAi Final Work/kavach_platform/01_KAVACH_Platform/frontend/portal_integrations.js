/**
 * ==============================================================================
 * KAVACH PORTAL INTEGRATIONS & EMBEDDED DASHBOARDS (v4.6.0)
 * 
 * Provides live iframe embedding + standalone launchers for:
 *  1. Live Agent Swarm View (#swarm-view) - Port 8000
 *  2. Applications Work View (#apps-view) - Port 8002
 * ==============================================================================
 */

(function () {
  'use strict';

  // --- EMBEDDED LIVE AGENT SWARM VIEW (#swarm-view) ---
  window.renderLiveSwarmView = function () {
    const view = document.getElementById('swarm-view');
    if (!view) return;

    const swarmUrl = window.location.port === '8001' ? '/cockpit' : 'http://127.0.0.1:8003/';

    view.innerHTML = `
      <div style="background:#0b1120;border:1px solid rgba(0,242,254,0.3);border-radius:14px;padding:20px;margin-bottom:24px;box-shadow:0 4px 24px rgba(0,242,254,0.12);">
        <!-- TOP LAUNCHER & STATUS BAR -->
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:14px;margin-bottom:16px;padding-bottom:14px;border-bottom:1px solid rgba(255,255,255,0.08);">
          <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
            <span class="badge" style="background:rgba(0,242,254,0.15);color:#38bdf8;border-color:rgba(0,242,254,0.3);font-weight:700;display:inline-flex;align-items:center;gap:6px;">
              <span style="width:8px;height:8px;background:#00f2fe;border-radius:50%;display:inline-block;animation:pulse 1.5s infinite;"></span>
              LIVE AUTONOMOUS AGENT ENGINE (PORT 8003 / COCKPIT)
            </span>
            <span class="badge" style="background:rgba(16,185,129,0.15);color:#34d399;border-color:rgba(16,185,129,0.3);font-weight:700;">
              19 REGISTERED MCP TOOLS
            </span>
            <span class="badge" style="background:rgba(168,85,247,0.15);color:#c084fc;border-color:rgba(168,85,247,0.3);font-weight:700;">
              6-STAGE INVARIANT CERTIFIED
            </span>
          </div>

          <div style="display:flex;align-items:center;gap:10px;">
            <button type="button" class="btn-nav-secondary" onclick="document.getElementById('swarm-live-iframe').src=('${swarmUrl}?t=' + Date.now())" style="padding:7px 14px;font-size:0.75rem;cursor:pointer;background:rgba(255,255,255,0.06);color:#cbd5e1;border:1px solid rgba(255,255,255,0.12);border-radius:6px;font-weight:600;display:inline-flex;align-items:center;gap:5px;">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"></polyline><polyline points="1 20 1 14 7 14"></polyline><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path></svg>
              Reload Agent Frame
            </button>
            <a href="${swarmUrl}" target="_blank" style="background:linear-gradient(135deg, #00f2fe, #4facfe);color:#070b14;text-decoration:none;border-radius:8px;padding:8px 18px;font-size:0.78rem;font-weight:700;display:inline-flex;align-items:center;gap:6px;box-shadow:0 0 14px rgba(0,242,254,0.4);">
              <span>Open Standalone Cockpit</span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3"/></svg>
            </a>
          </div>
        </div>

        <!-- LIVE APPLICATION IFRAME -->
        <div style="position:relative;width:100%;height:960px;background:#030611;border-radius:10px;overflow:hidden;border:1px solid rgba(0,242,254,0.25);box-shadow:inset 0 2px 12px rgba(0,0,0,0.4);">
          <iframe id="swarm-live-iframe" src="${swarmUrl}" style="width:100%;height:100%;border:none;display:block;" title="KAVACH Live Autonomous Agent Defense Cockpit"></iframe>
        </div>
      </div>
    `;
  };

  // --- EMBEDDED APPLICATIONS WORK VIEW (#apps-view) ---
  window.renderApplicationsWorkView = function () {
    const view = document.getElementById('apps-view');
    if (!view) return;

    const appsUrl = 'http://127.0.0.1:8002/';

    view.innerHTML = `
      <div style="background:#FFFFFF;border:1px solid #A7F3D0;border-radius:14px;padding:20px;margin-bottom:24px;box-shadow:0 4px 20px rgba(5,150,105,0.08);">
        <!-- TOP LAUNCHER & STATUS BAR -->
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:14px;margin-bottom:16px;padding-bottom:14px;border-bottom:1px solid #ECFDF5;">
          <div style="display:flex;align-items:center;gap:10px;">
            <span class="badge" style="background:#ECFDF5;color:#047857;border-color:#A7F3D0;font-weight:700;display:inline-flex;align-items:center;gap:6px;">
              <span style="width:8px;height:8px;background:#10B981;border-radius:50%;display:inline-block;animation:pulse 1.5s infinite;"></span>
              BHARAT CORE BANK LIVE PORTAL (PORT 8002)
            </span>
            <span class="badge" style="background:#EFF6FF;color:#1D4ED8;border-color:#BFDBFE;font-weight:700;">
              A/B COMPARATIVE SIMULATION CORE
            </span>
            <span class="badge" style="background:#FEF2F2;color:#DC2626;border-color:#FECACA;font-weight:700;">
              5 ATTACK VECTORS ACTIVE
            </span>
          </div>

          <div style="display:flex;align-items:center;gap:10px;">
            <button type="button" class="btn-nav-secondary" onclick="document.getElementById('apps-live-iframe').src='http://127.0.0.1:8002/?t=' + Date.now()" style="padding:7px 14px;font-size:0.75rem;cursor:pointer;background:#F8FAFC;font-weight:600;display:inline-flex;align-items:center;gap:5px;">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"></polyline><polyline points="1 20 1 14 7 14"></polyline><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path></svg>
              Reload Bank Frame
            </button>
            <a href="${appsUrl}" target="_blank" style="background:#059669;color:#FFFFFF;text-decoration:none;border-radius:8px;padding:8px 18px;font-size:0.78rem;font-weight:700;display:inline-flex;align-items:center;gap:6px;box-shadow:0 2px 8px rgba(5,150,105,0.35);">
              <span>Open Standalone Bank</span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3"/></svg>
            </a>
          </div>
        </div>

        <!-- LIVE APPLICATION IFRAME -->
        <div style="position:relative;width:100%;height:940px;background:#FAFAFA;border-radius:10px;overflow:hidden;border:1px solid #CBD5E1;box-shadow:inset 0 2px 8px rgba(0,0,0,0.06);">
          <iframe id="apps-live-iframe" src="${appsUrl}" style="width:100%;height:100%;border:none;display:block;" title="Bharat Core Bank Comparative A/B Applications Portal"></iframe>
        </div>
      </div>
    `;
  };

    // --- BIDIRECTIONAL CROSS-TAB & IFRAME NAVIGATION LISTENER ---
  window.addEventListener('message', function (event) {
    if (event && event.data && event.data.type === 'KAVACH_NAVIGATE') {
      const pathway = event.data.pathway || 'overview';
      if (typeof window.activatePathwayMode === 'function') {
        window.activatePathwayMode(pathway);
      }
    }
  });

  // --- AUTO-INITIALIZE ON DOM LOAD ---
  function initPortals() {
    if (document.getElementById('swarm-view')) {
      window.renderLiveSwarmView();
    }
    if (document.getElementById('apps-view')) {
      window.renderApplicationsWorkView();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPortals);
  } else {
    initPortals();
  }

})();
