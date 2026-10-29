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

    const swarmUrl = 'http://127.0.0.1:8000/';

    view.innerHTML = `
      <div style="background:#FFFFFF;border:1px solid #BAE6FD;border-radius:14px;padding:20px;margin-bottom:24px;box-shadow:0 4px 20px rgba(2,132,199,0.08);">
        <!-- TOP LAUNCHER & STATUS BAR -->
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:14px;margin-bottom:16px;padding-bottom:14px;border-bottom:1px solid #E0F2FE;">
          <div style="display:flex;align-items:center;gap:10px;">
            <span class="badge" style="background:#E0F2FE;color:#0369A1;border-color:#BAE6FD;font-weight:700;display:inline-flex;align-items:center;gap:6px;">
              <span style="width:8px;height:8px;background:#0284C7;border-radius:50%;display:inline-block;animation:pulse 1.5s infinite;"></span>
              LIVE BACKEND ENGINE (PORT 8000)
            </span>
            <span class="badge" style="background:#ECFDF5;color:#047857;border-color:#A7F3D0;font-weight:700;">
              6 FSM SENTINELS ARMED
            </span>
            <span class="badge" style="background:#EFF6FF;color:#1D4ED8;border-color:#BFDBFE;font-weight:700;">
              SLSA LEVEL 3 CERTIFIED
            </span>
          </div>

          <div style="display:flex;align-items:center;gap:10px;">
            <button type="button" class="btn-nav-secondary" onclick="document.getElementById('swarm-live-iframe').src='http://127.0.0.1:8000/?t=' + Date.now()" style="padding:7px 14px;font-size:0.75rem;cursor:pointer;background:#F8FAFC;font-weight:600;">
              🔄 Reload Engine Frame
            </button>
            <a href="${swarmUrl}" target="_blank" style="background:#0284C7;color:#FFFFFF;text-decoration:none;border-radius:8px;padding:8px 18px;font-size:0.78rem;font-weight:700;display:inline-flex;align-items:center;gap:6px;box-shadow:0 2px 8px rgba(2,132,199,0.35);">
              <span>🚀 Open Full Standalone Window (Port 8000)</span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3"/></svg>
            </a>
          </div>
        </div>

        <!-- LIVE APPLICATION IFRAME -->
        <div style="position:relative;width:100%;height:940px;background:#0F172A;border-radius:10px;overflow:hidden;border:1px solid #CBD5E1;box-shadow:inset 0 2px 8px rgba(0,0,0,0.15);">
          <iframe id="swarm-live-iframe" src="${swarmUrl}" style="width:100%;height:100%;border:none;display:block;" title="KAVACH Live Multi-Agent Swarm Command Center"></iframe>
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
            <button type="button" class="btn-nav-secondary" onclick="document.getElementById('apps-live-iframe').src='http://127.0.0.1:8002/?t=' + Date.now()" style="padding:7px 14px;font-size:0.75rem;cursor:pointer;background:#F8FAFC;font-weight:600;">
              🔄 Reload Bank Frame
            </button>
            <a href="${appsUrl}" target="_blank" style="background:#059669;color:#FFFFFF;text-decoration:none;border-radius:8px;padding:8px 18px;font-size:0.78rem;font-weight:700;display:inline-flex;align-items:center;gap:6px;box-shadow:0 2px 8px rgba(5,150,105,0.35);">
              <span>🚀 Open Full Standalone Window (Port 8002)</span>
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
