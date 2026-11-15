/**
 * ==============================================================================
 * KAVACH PORTAL INTEGRATIONS & EMBEDDED DASHBOARDS (v5.0.0)
 * 
 * Provides live iframe embedding + standalone launchers for:
 *  1. Autonomous AI Defense Cockpit (Port 8003) & Live Agent Swarm (Port 8000)
 *  2. Bharat Core Banking Enterprise Portal (Port 8002)
 * ==============================================================================
 */

(function () {
  'use strict';

  // Track active sub-tab for Swarm view ('cockpit' vs 'swarm')
  let activeSwarmSubTab = 'cockpit';

  // --- EMBEDDED LIVE AGENT SWARM VIEW (#swarm-view) ---
  window.renderLiveSwarmView = function () {
    const view = document.getElementById('swarm-view');
    if (!view) return;

    const cockpitUrl = window.location.port === '8001' ? '/cockpit' : 'http://127.0.0.1:8003/';
    const swarmUrl = 'http://127.0.0.1:8000/';
    const currentFrameUrl = activeSwarmSubTab === 'cockpit' ? cockpitUrl : swarmUrl;

    view.innerHTML = `
      <div style="background:#0c1324;border:1px solid rgba(0,242,254,0.3);border-radius:14px;padding:20px;margin-bottom:24px;box-shadow:0 8px 32px rgba(0,0,0,0.45);">
        <!-- TOP LAUNCHER & STATUS BAR -->
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:14px;margin-bottom:16px;padding-bottom:14px;border-bottom:1px solid rgba(255,255,255,0.08);">
          
          <!-- Sub-Tab Switcher -->
          <div style="display:flex;align-items:center;gap:8px;background:#080d1a;padding:4px;border-radius:10px;border:1px solid #1d2d4d;">
            <button type="button" id="btn-subtab-cockpit" onclick="window.switchSwarmEmbed('cockpit')" style="background:${activeSwarmSubTab === 'cockpit' ? 'linear-gradient(135deg, #0284c7, #00f2fe)' : 'transparent'}; color:${activeSwarmSubTab === 'cockpit' ? '#060913' : '#94a3b8'}; border:none; padding:7px 14px; border-radius:7px; font-weight:800; font-size:0.77rem; cursor:pointer; display:inline-flex; align-items:center; gap:6px; transition:all 0.16s ease;">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
              <span>Autonomous Cockpit (Port 8003)</span>
            </button>
            <button type="button" id="btn-subtab-swarm" onclick="window.switchSwarmEmbed('swarm')" style="background:${activeSwarmSubTab === 'swarm' ? 'linear-gradient(135deg, #7c3aed, #a855f7)' : 'transparent'}; color:${activeSwarmSubTab === 'swarm' ? '#ffffff' : '#94a3b8'}; border:none; padding:7px 14px; border-radius:7px; font-weight:800; font-size:0.77rem; cursor:pointer; display:inline-flex; align-items:center; gap:6px; transition:all 0.16s ease;">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
              <span>6-Pod Swarm Engine (Port 8000)</span>
            </button>
          </div>

          <!-- Metadata Tags -->
          <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
            <span class="badge" style="background:rgba(0,242,254,0.12);color:#38bdf8;border-color:rgba(0,242,254,0.35);font-weight:700;display:inline-flex;align-items:center;gap:6px;font-size:0.72rem;">
              <span style="width:7px;height:7px;background:#00f2fe;border-radius:50%;display:inline-block;box-shadow:0 0 6px #00f2fe;"></span>
              19 MCP TOOLS
            </span>
            <span class="badge" style="background:rgba(16,185,129,0.12);color:#34d399;border-color:rgba(16,185,129,0.35);font-weight:700;font-size:0.72rem;">
              6-STAGE INVARIANTS
            </span>
          </div>

          <!-- Action Controls -->
          <div style="display:flex;align-items:center;gap:10px;">
            <button type="button" class="btn-nav-secondary" onclick="document.getElementById('swarm-live-iframe').src=('${currentFrameUrl}?t=' + Date.now())" style="padding:7px 14px;font-size:0.75rem;cursor:pointer;background:#111c35;color:#cbd5e1;border:1px solid #1d2d4d;border-radius:7px;font-weight:600;display:inline-flex;align-items:center;gap:5px;">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"></polyline><polyline points="1 20 1 14 7 14"></polyline><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path></svg>
              Reload Frame
            </button>
            <a href="${activeSwarmSubTab === 'cockpit' ? cockpitUrl : swarmUrl}" target="_blank" style="background:linear-gradient(135deg, #00f2fe, #4facfe);color:#070b14;text-decoration:none;border-radius:8px;padding:8px 18px;font-size:0.78rem;font-weight:800;display:inline-flex;align-items:center;gap:6px;box-shadow:0 0 14px rgba(0,242,254,0.4);">
              <span>Open Standalone</span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3"/></svg>
            </a>
          </div>
        </div>

        <!-- LIVE APPLICATION IFRAME -->
        <div style="position:relative;width:100%;height:960px;background:#060913;border-radius:10px;overflow:hidden;border:1px solid rgba(0,242,254,0.25);box-shadow:inset 0 2px 14px rgba(0,0,0,0.6);">
          <iframe id="swarm-live-iframe" src="${currentFrameUrl}" style="width:100%;height:100%;border:none;display:block;" title="KAVACH Live Autonomous Defense Engine"></iframe>
        </div>
      </div>
    `;
  };

  window.switchSwarmEmbed = function (tab) {
    activeSwarmSubTab = tab;
    window.renderLiveSwarmView();
  };

  // --- EMBEDDED APPLICATIONS WORK VIEW (#apps-view) ---
  window.renderApplicationsWorkView = function () {
    const view = document.getElementById('apps-view');
    if (!view) return;

    const appsUrl = 'http://127.0.0.1:8002/';

    view.innerHTML = `
      <div style="background:#0c1324;border:1px solid rgba(16,185,129,0.35);border-radius:14px;padding:20px;margin-bottom:24px;box-shadow:0 8px 32px rgba(0,0,0,0.45);">
        <!-- TOP LAUNCHER & STATUS BAR -->
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:14px;margin-bottom:16px;padding-bottom:14px;border-bottom:1px solid rgba(255,255,255,0.08);">
          <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
            <span class="badge" style="background:rgba(16,185,129,0.15);color:#34d399;border-color:rgba(16,185,129,0.35);font-weight:700;display:inline-flex;align-items:center;gap:6px;">
              <span style="width:8px;height:8px;background:#10b981;border-radius:50%;display:inline-block;box-shadow:0 0 6px #10b981;"></span>
              BHARAT CORE BANK LIVE PORTAL (PORT 8002)
            </span>
            <span class="badge" style="background:rgba(56,189,248,0.15);color:#38bdf8;border-color:rgba(56,189,248,0.35);font-weight:700;">
              A/B COMPARATIVE SIMULATION CORE
            </span>
            <span class="badge" style="background:rgba(239,68,68,0.15);color:#f87171;border-color:rgba(239,68,68,0.35);font-weight:700;">
              5 ATTACK VECTORS ACTIVE
            </span>
          </div>

          <div style="display:flex;align-items:center;gap:10px;">
            <button type="button" class="btn-nav-secondary" onclick="document.getElementById('apps-live-iframe').src='http://127.0.0.1:8002/?t=' + Date.now()" style="padding:7px 14px;font-size:0.75rem;cursor:pointer;background:#111c35;color:#cbd5e1;border:1px solid #1d2d4d;border-radius:7px;font-weight:600;display:inline-flex;align-items:center;gap:5px;">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"></polyline><polyline points="1 20 1 14 7 14"></polyline><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path></svg>
              Reload Bank Frame
            </button>
            <a href="${appsUrl}" target="_blank" style="background:linear-gradient(135deg, #10b981, #059669);color:#060913;text-decoration:none;border-radius:8px;padding:8px 18px;font-size:0.78rem;font-weight:800;display:inline-flex;align-items:center;gap:6px;box-shadow:0 0 14px rgba(16,185,129,0.35);">
              <span>Open Standalone Bank</span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3"/></svg>
            </a>
          </div>
        </div>

        <!-- LIVE APPLICATION IFRAME -->
        <div style="position:relative;width:100%;height:940px;background:#060913;border-radius:10px;overflow:hidden;border:1px solid rgba(16,185,129,0.25);box-shadow:inset 0 2px 14px rgba(0,0,0,0.6);">
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
