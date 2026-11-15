/**
 * ==============================================================================
 * KAVACH UNIVERSAL ECOSYSTEM NAVIGATION MESH (v5.0.0)
 * 
 * Persistent across all 4 microservices:
 *  - Master Platform   : http://127.0.0.1:8001/
 *  - Live Agent Swarm  : http://127.0.0.1:8000/
 *  - Bharat Core Bank  : http://127.0.0.1:8002/
 *  - Real Agent Cockpit: http://127.0.0.1:8003/ (or /cockpit on 8001)
 * ==============================================================================
 */

(function () {
  'use strict';

  // Determine current active port
  const currentPort = window.location.port || (window.location.protocol === 'https:' ? '443' : '80');
  const currentPath = window.location.pathname;

  let activeService = '8001';
  if (currentPort === '8000') activeService = '8000';
  else if (currentPort === '8002') activeService = '8002';
  else if (currentPort === '8003' || currentPath.startsWith('/cockpit')) activeService = '8003';
  else activeService = '8001';

  const meshHtml = `
  <div id="kavach-universal-mesh-bar" class="kavach-mesh-bar">
    <div class="kavach-mesh-inner">
      
      <!-- Brand & Project Identity Cluster -->
      <div class="kavach-mesh-brand">
        <a href="http://127.0.0.1:8001/" class="kavach-mesh-brand-link" title="Return to KAVACH Master Platform">
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
        <a href="http://127.0.0.1:8001/" class="kavach-mesh-pill ${activeService === '8001' ? 'active' : ''}" title="KAVACH Master Unified Platform (Architecture, 6 Stages, Checks, Paper)">
          <span class="kavach-mesh-dot" style="background:#38bdf8;"></span>
          <span class="kavach-mesh-name">Master Platform</span>
          <span class="kavach-mesh-port">:8001</span>
          ${activeService === '8001' ? '<span class="kavach-mesh-active-tag">CURRENT</span>' : ''}
        </a>

        <!-- [2] Live Agent Swarm -->
        <a href="http://127.0.0.1:8000/" class="kavach-mesh-pill ${activeService === '8000' ? 'active' : ''}" title="Live Multi-Agent Swarm Command Center (Blackboard & Timeline)">
          <span class="kavach-mesh-dot" style="background:#00f2fe;"></span>
          <span class="kavach-mesh-name">Live Swarm</span>
          <span class="kavach-mesh-port">:8000</span>
          ${activeService === '8000' ? '<span class="kavach-mesh-active-tag">CURRENT</span>' : ''}
        </a>

        <!-- [3] Bharat Core Bank -->
        <a href="http://127.0.0.1:8002/" class="kavach-mesh-pill ${activeService === '8002' ? 'active' : ''}" title="Bharat Core Banking Highway (Vulnerable vs Shielded A/B Testing)">
          <span class="kavach-mesh-dot" style="background:#10b981;"></span>
          <span class="kavach-mesh-name">Bharat Bank</span>
          <span class="kavach-mesh-port">:8002</span>
          ${activeService === '8002' ? '<span class="kavach-mesh-active-tag">CURRENT</span>' : ''}
        </a>

        <!-- [4] Real Agent Cockpit -->
        <a href="http://127.0.0.1:8003/" class="kavach-mesh-pill ${activeService === '8003' ? 'active' : ''}" title="Real Autonomous Agent Cockpit (ReAct Engine, 19 MCP Tools, KaTeX Math)">
          <span class="kavach-mesh-dot" style="background:#a855f7;"></span>
          <span class="kavach-mesh-name">Agent Cockpit</span>
          <span class="kavach-mesh-port">:8003</span>
          ${activeService === '8003' ? '<span class="kavach-mesh-active-tag">CURRENT</span>' : ''}
        </a>

      </nav>

      <!-- System Health Indicator -->
      <div class="kavach-mesh-health">
        <span class="kavach-mesh-pulse"></span>
        <span class="kavach-mesh-status-text">4/4 NODES ONLINE</span>
      </div>

    </div>
  </div>
  `;

  // Inject once DOM is available
  function injectMesh() {
    if (document.getElementById('kavach-universal-mesh-bar')) return;
    const placeholder = document.createElement('div');
    placeholder.innerHTML = meshHtml;
    document.body.insertBefore(placeholder.firstElementChild, document.body.firstChild);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectMesh);
  } else {
    injectMesh();
  }
})();
