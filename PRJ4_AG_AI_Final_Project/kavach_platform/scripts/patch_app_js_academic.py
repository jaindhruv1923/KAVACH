"""
Patches final_project/KAVACH-main/01_KAVACH_Platform/frontend/app.js:
1. Adds 'academic-view' to ALL_APP_VIEWS array
2. Updates switchMasterView to handle 'academic-view' target and activate btnAcademic
3. Implements switchToAcademic()
4. Updates activatePathwayMode() to handle mode === 'academic' and call switchToAcademic()
5. Updates renderDynamicNavbar() to show academic nav buttons
6. Updates handleAppHashRouting() to route #academic and #academic-weapon to switchToAcademic()
7. Exports window.switchToAcademic
"""

import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
APP_JS_PATH = os.path.join(ROOT, "01_KAVACH_Platform", "frontend", "app.js")

def patch_app_js():
    with open(APP_JS_PATH, "r", encoding="utf-8") as f:
        code = f.read()

    # 1. ALL_APP_VIEWS
    old_views = """const ALL_APP_VIEWS = [
  'product-view',
  'improvised-view',
  'workspace-view',
  'defense-view',
  'eval-view',
  'usecases-view',
  'research-view'
];"""

    new_views = """const ALL_APP_VIEWS = [
  'product-view',
  'improvised-view',
  'academic-view',
  'workspace-view',
  'defense-view',
  'eval-view',
  'usecases-view',
  'research-view'
];"""

    if old_views in code:
        code = code.replace(old_views, new_views, 1)
        print("[1] Injected 'academic-view' into ALL_APP_VIEWS")

    # 2. switchMasterView mode detection and button toggle
    old_mode_sync = """  // 2. Determine and sync pathway mode
  let mode = 'midsem';
  if (targetViewId === 'improvised-view') {
    mode = 'improvised';
  } else if (targetViewId === 'workspace-view') {
    mode = window.CURRENT_PATHWAY || 'midsem';
  }
  window.CURRENT_PATHWAY = mode;

  // 3. Update header pathway selector pills
  const btnMidsem = document.getElementById('pathway-btn-midsem');
  const btnImprovised = document.getElementById('pathway-btn-improvised');"""

    new_mode_sync = """  // 2. Determine and sync pathway mode
  let mode = 'midsem';
  if (targetViewId === 'improvised-view') {
    mode = 'improvised';
  } else if (targetViewId === 'academic-view') {
    mode = 'academic';
  } else if (targetViewId === 'workspace-view') {
    mode = window.CURRENT_PATHWAY || 'midsem';
  }
  window.CURRENT_PATHWAY = mode;

  // 3. Update header pathway selector pills
  const btnMidsem = document.getElementById('pathway-btn-midsem');
  const btnImprovised = document.getElementById('pathway-btn-improvised');
  const btnAcademic = document.getElementById('pathway-btn-academic');"""

    if old_mode_sync in code:
        code = code.replace(old_mode_sync, new_mode_sync, 1)
        print("[2] Injected btnAcademic in switchMasterView")

    old_btn_toggle = """  if (btnMidsem) btnMidsem.classList.toggle('active', mode === 'midsem');
  if (btnImprovised) btnImprovised.classList.toggle('active', mode === 'improvised');"""

    new_btn_toggle = """  if (btnMidsem) btnMidsem.classList.toggle('active', mode === 'midsem');
  if (btnImprovised) btnImprovised.classList.toggle('active', mode === 'improvised');
  if (btnAcademic) btnAcademic.classList.toggle('active', mode === 'academic');"""

    if old_btn_toggle in code:
        code = code.replace(old_btn_toggle, new_btn_toggle, 1)
        print("[3] Added btnAcademic toggle in switchMasterView")

    # 3. Add switchToAcademic function before activatePathwayMode
    target_switch = "function switchToImprovised(targetSectionId = null) {"
    if "function switchToAcademic(" not in code:
        switch_academic_code = """function switchToAcademic(targetSectionId = null) {
  switchMasterView('academic-view', 'academic-weapon', null, targetSectionId || 'academic-view');
  updateSEOViewMeta('academic');
  if (typeof window.renderAcademicWeaponCockpit === 'function') {
    window.renderAcademicWeaponCockpit();
  }
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

"""
        code = code.replace(target_switch, switch_academic_code + target_switch, 1)
        print("[4] Added switchToAcademic() function")

    # 4. Update activatePathwayMode
    old_activate = """function activatePathwayMode(mode, targetId = null) {
  window.CURRENT_PATHWAY = mode;
  const btnMidsem = document.getElementById('pathway-btn-midsem');
  const btnImprovised = document.getElementById('pathway-btn-improvised');
  const scopeEarlier = document.getElementById('scope-btn-earlier');
  const scopeNew = document.getElementById('scope-btn-new');
  const scopeAll = document.getElementById('scope-btn-all');
  const scopeMatrix = document.getElementById('scope-btn-matrix');
  const pill = document.getElementById('scope-context-pill');

  if (btnMidsem) btnMidsem.classList.toggle('active', mode === 'midsem');
  if (btnImprovised) btnImprovised.classList.toggle('active', mode === 'improvised');

  [scopeAll, scopeEarlier, scopeNew, scopeMatrix].forEach(btn => {
    if (btn) btn.classList.remove('active');
  });

  if (typeof window.renderDynamicNavbar === 'function') {
    window.renderDynamicNavbar(mode);
  }

  if (mode === 'midsem') {
    if (scopeEarlier) scopeEarlier.classList.add('active');
    switchToProduct(targetId);
    if (pill) pill.innerHTML = "<strong>Active Scope: Mid-Sem Foundation (v1.0 Baseline).</strong> Taskbar adapted to earlier architecture: 8-stage air-gapped deterministic pipeline, AST blast-radius analyzer, closed-loop ReAct reflexion, and CycloneDX SBOM generator.";
  } else {
    if (scopeNew) scopeNew.classList.add('active');
    switchToImprovised(targetId);
    if (pill) pill.innerHTML = "<strong>Active Scope: Newly Added Improvised Innovations (v3.0).</strong> Highlighting 10 major gap solvers, Live Cyber War-Room Arena, Forensic Incident DVR Replay, Multi-Model Consensus Radar, and SLSA L3 / DPDP Dossier Generator.";
  }"""

    new_activate = """function activatePathwayMode(mode, targetId = null) {
  window.CURRENT_PATHWAY = mode;
  const btnMidsem = document.getElementById('pathway-btn-midsem');
  const btnImprovised = document.getElementById('pathway-btn-improvised');
  const btnAcademic = document.getElementById('pathway-btn-academic');
  const scopeEarlier = document.getElementById('scope-btn-earlier');
  const scopeNew = document.getElementById('scope-btn-new');
  const scopeAll = document.getElementById('scope-btn-all');
  const scopeMatrix = document.getElementById('scope-btn-matrix');
  const pill = document.getElementById('scope-context-pill');

  if (btnMidsem) btnMidsem.classList.toggle('active', mode === 'midsem');
  if (btnImprovised) btnImprovised.classList.toggle('active', mode === 'improvised');
  if (btnAcademic) btnAcademic.classList.toggle('active', mode === 'academic');

  [scopeAll, scopeEarlier, scopeNew, scopeMatrix].forEach(btn => {
    if (btn) btn.classList.remove('active');
  });

  if (typeof window.renderDynamicNavbar === 'function') {
    window.renderDynamicNavbar(mode);
  }

  if (mode === 'midsem') {
    if (scopeEarlier) scopeEarlier.classList.add('active');
    switchToProduct(targetId);
    if (pill) pill.innerHTML = "<strong>Active Scope: Mid-Sem Foundation (v1.0 Baseline).</strong> Taskbar adapted to earlier architecture: 8-stage air-gapped deterministic pipeline, AST blast-radius analyzer, closed-loop ReAct reflexion, and CycloneDX SBOM generator.";
  } else if (mode === 'academic') {
    switchToAcademic(targetId);
    if (pill) pill.innerHTML = "<strong>Active Scope: Academic Weapon & Research Rigor (10 Autonomous Guardrail Frontiers).</strong> Live interactive flow processors for (&epsilon;,&delta;)-Differential Privacy, Graph-of-Thoughts DAG, Kirchenbauer Watermarking, Denning Security Lattice, NIST Post-Quantum Dilithium, OWASP LLM04 Token-Bucket, NLI Cross-Entailment, SAGA Compensation, Pearl Counterfactual XAI, and Empirical Scientific Ablations.";
    return;
  } else {
    if (scopeNew) scopeNew.classList.add('active');
    switchToImprovised(targetId);
    if (pill) pill.innerHTML = "<strong>Active Scope: Newly Added Improvised Innovations (v3.0).</strong> Highlighting 10 major gap solvers, Live Cyber War-Room Arena, Forensic Incident DVR Replay, Multi-Model Consensus Radar, and SLSA L3 / DPDP Dossier Generator.";
  }"""

    if old_activate in code:
        code = code.replace(old_activate, new_activate, 1)
        print("[5] Updated activatePathwayMode() to handle 'academic' mode")

    # 5. Update renderDynamicNavbar
    old_navbar = """  } else {
    container.innerHTML = `
      <button type="button" class="nav-switch-btn active" onclick="scrollToTarget('improvised-innovations-section', this)">Innovations</button>
      <button type="button" class="nav-switch-btn" onclick="scrollToTarget('warroom-arena-card', this)">War Room</button>
      <button type="button" class="nav-switch-btn" onclick="scrollToTarget('forensic-replay-card', this)">DVR Replay</button>
      <button type="button" class="nav-switch-btn" onclick="scrollToTarget('consensus-radar-card', this)">Consensus</button>
      <button type="button" class="nav-switch-btn" onclick="scrollToTarget('comparison-matrix-section', this)">Audit Matrix</button>
    `;
  }"""

    new_navbar = """  } else if (mode === 'academic') {
    container.innerHTML = `
      <button type="button" class="nav-switch-btn active" onclick="activatePathwayMode('academic')">10 Frontiers</button>
      <button type="button" class="nav-switch-btn" onclick="scrollToTarget('academic-grounding-card', this)">KaTeX Math</button>
      <button type="button" class="nav-switch-btn" onclick="scrollToTarget('academic-flow-sim', this)">Flow Pipeline</button>
      <button type="button" class="nav-switch-btn" onclick="scrollToTarget('academic-telemetry-box', this)">Telemetry</button>
      <button type="button" class="nav-switch-btn" onclick="activatePathwayMode('midsem')">&larr; Earlier (v1.0)</button>
      <button type="button" class="nav-switch-btn" onclick="activatePathwayMode('improvised')">Improvised (v3.0) &rarr;</button>
    `;
  } else {
    container.innerHTML = `
      <button type="button" class="nav-switch-btn active" onclick="scrollToTarget('improvised-innovations-section', this)">Innovations</button>
      <button type="button" class="nav-switch-btn" onclick="scrollToTarget('warroom-arena-card', this)">War Room</button>
      <button type="button" class="nav-switch-btn" onclick="scrollToTarget('forensic-replay-card', this)">DVR Replay</button>
      <button type="button" class="nav-switch-btn" onclick="scrollToTarget('consensus-radar-card', this)">Consensus</button>
      <button type="button" class="nav-switch-btn" onclick="scrollToTarget('comparison-matrix-section', this)">Audit Matrix</button>
    `;
  }"""

    if old_navbar in code:
        code = code.replace(old_navbar, new_navbar, 1)
        print("[6] Updated renderDynamicNavbar for 'academic' pathway")

    # 6. Update handleAppHashRouting
    old_hash_route = '  } else if (hash === "#improvised") {\n    switchToImprovised();'
    new_hash_route = """  } else if (hash === "#academic" || hash === "#academic-weapon" || hash === "#academic-view") {
    switchToAcademic();
  } else if (hash === "#improvised") {
    switchToImprovised();"""

    if old_hash_route in code and "hash === \"#academic\"" not in code:
        code = code.replace(old_hash_route, new_hash_route, 1)
        print("[7] Injected #academic and #academic-weapon hash routes in handleAppHashRouting")

    # 7. Global Exports
    old_exports = "window.switchToImprovised = switchToImprovised;"
    new_exports = "window.switchToImprovised = switchToImprovised;\nwindow.switchToAcademic = switchToAcademic;"

    if old_exports in code and "window.switchToAcademic" not in code:
        code = code.replace(old_exports, new_exports, 1)
        print("[8] Exported window.switchToAcademic")

    with open(APP_JS_PATH, "w", encoding="utf-8") as f:
        f.write(code)
    print("[*] Successfully updated app.js")


if __name__ == "__main__":
    patch_app_js()

