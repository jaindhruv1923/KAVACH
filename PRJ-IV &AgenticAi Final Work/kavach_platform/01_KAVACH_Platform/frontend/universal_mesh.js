/**
 * ==============================================================================
 * KAVACH UNIVERSAL ECOSYSTEM NAVIGATION MESH (v5.1.0)
 * 
 * Persistent across all 4 microservices:
 *  - Master Platform   : / or :8001
 *  - Live Agent Swarm  : /swarm/ or :8000
 *  - Bharat Core Bank  : /bank/ or :8002
 *  - Real Agent Cockpit: /cockpit/ or :8003
 * ==============================================================================
 */

(function () {
  'use strict';

  // Determine current active port & path
  const currentPort = window.location.port || (window.location.protocol === 'https:' ? '443' : '80');
  const currentPath = window.location.pathname;

  let activeService = '8001';
  if (currentPort === '8000' || currentPath.startsWith('/swarm')) activeService = '8000';
  else if (currentPort === '8002' || currentPath.startsWith('/bank')) activeService = '8002';
  else if (currentPort === '8003' || currentPath.startsWith('/cockpit')) activeService = '8003';
  else activeService = '8001';

  // Resolve URLs using KAVACH_CONFIG if available
  const masterUrl = (window.KAVACH_CONFIG && typeof window.KAVACH_CONFIG.getDashboardUrl === 'function')
    ? window.KAVACH_CONFIG.getDashboardUrl('master')
    : 'http://127.0.0.1:8001/';
  const swarmUrl = (window.KAVACH_CONFIG && typeof window.KAVACH_CONFIG.getDashboardUrl === 'function')
    ? window.KAVACH_CONFIG.getDashboardUrl('swarm')
    : 'http://127.0.0.1:8000/';
  const bankUrl = (window.KAVACH_CONFIG && typeof window.KAVACH_CONFIG.getDashboardUrl === 'function')
    ? window.KAVACH_CONFIG.getDashboardUrl('banking')
    : 'http://127.0.0.1:8002/';
  const cockpitUrl = (window.KAVACH_CONFIG && typeof window.KAVACH_CONFIG.getDashboardUrl === 'function')
    ? window.KAVACH_CONFIG.getDashboardUrl('cockpit')
    : 'http://127.0.0.1:8003/';

  const isProd = window.KAVACH_CONFIG && typeof window.KAVACH_CONFIG.isProduction === 'function' && window.KAVACH_CONFIG.isProduction();
  const masterTag = isProd ? 'PORTAL' : ':8001';
  const swarmTag = isProd ? 'SWARM' : ':8000';
  const bankTag = isProd ? 'BANK' : ':8002';
  const cockpitTag = isProd ? 'AGENT' : ':8003';

  const meshHtml = `
  <div id="kavach-universal-mesh-bar" class="kavach-mesh-bar">
    <div class="kavach-mesh-inner">
      
      <!-- Brand & Project Identity Cluster -->
      <div class="kavach-mesh-brand">
        <a href="${masterUrl}" class="kavach-mesh-brand-link" title="Return to KAVACH Master Platform">
          <div class="kavach-mesh-logo">K</div>
          <div class="kavach-mesh-titles">
            <div class="kavach-mesh-main-title">KAVACH <span>ECOSYSTEM</span></div>
            <div class="kavach-mesh-sub-title">CSE3101 Agentic AI &bull; BML Munjal Univ &bull; Dhruv Jain (230532)</div>
          </div>
        </a>
      </div>

      <!-- The 4 Core Microservice Pills -->
      <nav class="kavach-mesh-nav" aria-label="KAVACH Unified Microservices">
        
        <!-- [1] Master Platform -->
        <a href="${masterUrl}" class="kavach-mesh-pill ${activeService === '8001' ? 'active' : ''}" title="KAVACH Master Unified Platform (Architecture, 6 Stages, Checks, Paper)">
          <span class="kavach-mesh-dot" style="background:#38bdf8;"></span>
          <span class="kavach-mesh-name">Master Platform</span>
          <span class="kavach-mesh-port">${masterTag}</span>
          ${activeService === '8001' ? '<span class="kavach-mesh-active-tag">CURRENT</span>' : ''}
        </a>

        <!-- [2] Live Agent Swarm -->
        <a href="${swarmUrl}" class="kavach-mesh-pill ${activeService === '8000' ? 'active' : ''}" title="Live Multi-Agent Swarm Command Center (Blackboard & Timeline)">
          <span class="kavach-mesh-dot" style="background:#00f2fe;"></span>
          <span class="kavach-mesh-name">Live Swarm</span>
          <span class="kavach-mesh-port">${swarmTag}</span>
          ${activeService === '8000' ? '<span class="kavach-mesh-active-tag">CURRENT</span>' : ''}
        </a>

        <!-- [3] Bharat Core Bank -->
        <a href="${bankUrl}" class="kavach-mesh-pill ${activeService === '8002' ? 'active' : ''}" title="Bharat Core Banking Highway (Vulnerable vs Shielded A/B Testing)">
          <span class="kavach-mesh-dot" style="background:#10b981;"></span>
          <span class="kavach-mesh-name">Bharat Bank</span>
          <span class="kavach-mesh-port">${bankTag}</span>
          ${activeService === '8002' ? '<span class="kavach-mesh-active-tag">CURRENT</span>' : ''}
        </a>

        <!-- [4] Real Agent Cockpit -->
        <a href="${cockpitUrl}" class="kavach-mesh-pill ${activeService === '8003' ? 'active' : ''}" title="Autonomous AI Defense Cockpit (Port 8003)">
          <span class="kavach-mesh-dot" style="background:#c084fc;"></span>
          <span class="kavach-mesh-name">Agent Cockpit</span>
          <span class="kavach-mesh-port">${cockpitTag}</span>
          ${activeService === '8003' ? '<span class="kavach-mesh-active-tag">CURRENT</span>' : ''}
        </a>

      </nav>

      <!-- Right Status Chip -->
      <div class="kavach-mesh-status">
        <span class="kavach-mesh-status-dot"></span>
        <span class="kavach-mesh-status-text">4/4 NODES ONLINE</span>
      </div>

    </div>
  </div>
  `;

  // Inject once DOM is available
  // NOTE: On Port 8001 (Master Platform), the native Enterprise Clean Header is the sole authority.
  // The mesh bar is injected on external microservice dashboards (:8000, :8002, :8003 / /swarm /bank /cockpit).
  function injectMesh() {
    if ((activeService === '8001' && currentPath === '/') || document.querySelector('.app-header')) return;
    if (document.getElementById('kavach-universal-mesh-bar')) return;
    const placeholder = document.createElement('div');
    placeholder.innerHTML = meshHtml;
    document.body.insertBefore(placeholder.firstElementChild, document.body.firstChild);
    document.body.classList.add('has-universal-mesh');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectMesh);
  } else {
    injectMesh();
  }
})();
