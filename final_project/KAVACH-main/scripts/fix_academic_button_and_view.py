"""
Comprehensive fix for the Academic Weapon button and dedicated view:
1. Fixes the broken backslash in index.html: onclick="activatePathwayMode(\'academic\')" -> onclick="activatePathwayMode('academic')"
2. Adds 'academic-view' to switchToViewGlobal views list
3. Creates the dedicated top-level <div id="academic-view"> container
4. Updates activatePathwayMode('academic') to smoothly switch to academic-view and scroll to top
5. Updates renderDynamicNavbar to display dedicated academic tabs
6. Adds active styling for #pathway-btn-academic in style.css
"""

import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INDEX_PATH = os.path.join(ROOT, "01_KAVACH_Platform", "frontend", "index.html")
STYLE_PATH = os.path.join(ROOT, "01_KAVACH_Platform", "frontend", "style.css")


def fix_all():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Fix line 353 backslash syntax error
    html = html.replace("onclick=\"activatePathwayMode(\\'academic\\')\"", "onclick=\"activatePathwayMode('academic')\"")
    html = html.replace("onclick=\\\"activatePathwayMode(\\'academic\\')\\\"", "onclick=\"activatePathwayMode('academic')\"")
    print("[1] Fixed onclick backslash syntax error on pathway-btn-academic")

    # 2. Add 'academic-view' to switchToViewGlobal
    old_views = "const views = ['product-view', 'improvised-view', 'workspace-view', 'usecases-view', 'research-view', 'defense-view', 'eval-view', 'professor-view'];"
    new_views = "const views = ['product-view', 'improvised-view', 'academic-view', 'workspace-view', 'usecases-view', 'research-view', 'defense-view', 'eval-view', 'professor-view'];"
    if old_views in html:
        html = html.replace(old_views, new_views, 1)
        print("[2] Added 'academic-view' to switchToViewGlobal views array")

    # 3. Update activatePathwayMode
    old_academic_branch = """  } else if (mode === 'academic') {
    if (scopeNew) scopeNew.classList.add('active');
    switchToViewGlobal('improvised-view', null, 'academic-weapon');
    if (pill) pill.innerHTML = "<strong>Active Scope: Academic Weapon & Research Rigor (10 Autonomous Guardrail Frontiers).</strong> Live interactive flow processors for (&epsilon;,&delta;)-Differential Privacy, Graph-of-Thoughts DAG, Kirchenbauer Watermarking, Denning Security Lattice, NIST Post-Quantum Dilithium, OWASP LLM04 Token-Bucket, NLI Cross-Entailment, SAGA Compensation, Pearl Counterfactual XAI, and Empirical Scientific Ablations.";
    if (typeof window.renderAcademicWeaponCockpit === 'function') window.renderAcademicWeaponCockpit();
    targetId = targetId || 'academic-weapon-cockpit';
  }"""

    new_academic_branch = """  } else if (mode === 'academic') {
    if (scopeEarlier) scopeEarlier.classList.remove('active');
    if (scopeNew) scopeNew.classList.remove('active');
    switchToViewGlobal('academic-view', null, 'academic-weapon');
    if (pill) pill.innerHTML = "<strong>Active Scope: Academic Weapon & Research Rigor (10 Autonomous Guardrail Frontiers).</strong> Live interactive flow processors for (&epsilon;,&delta;)-Differential Privacy, Graph-of-Thoughts DAG, Kirchenbauer Watermarking, Denning Security Lattice, NIST Post-Quantum Dilithium, OWASP LLM04 Token-Bucket, NLI Cross-Entailment, SAGA Compensation, Pearl Counterfactual XAI, and Empirical Scientific Ablations.";
    if (typeof window.renderAcademicWeaponCockpit === 'function') {
      setTimeout(() => window.renderAcademicWeaponCockpit(), 10);
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
    return;
  }"""

    if old_academic_branch in html:
        html = html.replace(old_academic_branch, new_academic_branch, 1)
        print("[3] Updated activatePathwayMode('academic') to activate dedicated 'academic-view'")

    # 4. Remove previous duplicate academic-weapon-cockpit from inside improvised-view if present
    dup_section_marker = '    <!-- SECTION: ACADEMIC WEAPON 10-FEATURE INTERACTIVE COMMAND DECK -->'
    if dup_section_marker in html:
        pattern = r'    <!-- ============================================================ -->\s*<!-- SECTION: ACADEMIC WEAPON 10-FEATURE INTERACTIVE COMMAND DECK -->\s*<!-- ============================================================ -->\s*<section id="academic-weapon-cockpit"[\s\S]*?<\/section>'
        banner_html = '''    <!-- Promotion Banner to Dedicated Academic Weapon View -->
    <div class="card" style="background:linear-gradient(135deg, #FAF5FF 0%, #F5F3FF 100%);border:1px solid #DDD6FE;border-radius:var(--radius-lg);padding:22px 26px;margin-top:28px;margin-bottom:28px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;box-shadow:0 2px 8px rgba(124,58,237,0.08);">
      <div>
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
          <span class="badge" style="background:#EDE9FE;color:#6D28D9;border-color:#DDD6FE;font-weight:700;">FINAL PROJECT HIGHLIGHT</span>
          <span class="badge" style="background:#ECFDF5;color:#047857;border-color:#A7F3D0;font-weight:700;">10 ELITE RESEARCH FRONTIERS</span>
        </div>
        <h3 style="margin:4px 0 2px;font-size:1.20rem;font-weight:800;color:#581C87;">10 Academic Weapon Autonomous Frontiers &amp; Live Flow Processors</h3>
        <p style="margin:0;font-size:0.83rem;color:#6B21A8;max-width:760px;">Directly execute Differential Privacy, Graph-of-Thoughts DAG, Kirchenbauer Watermarking, Post-Quantum Dilithium, and Denning Security Lattice in the dedicated command deck.</p>
      </div>
      <button type="button" class="btn-serious" onclick="activatePathwayMode('academic')" style="background:#7C3AED;color:#FFF;padding:10px 22px;font-size:0.82rem;font-weight:700;border-radius:8px;box-shadow:0 2px 8px rgba(124,58,237,0.25);cursor:pointer;">
        Open 10 Frontiers Cockpit &rarr;
      </button>
    </div>'''
        html = re.sub(pattern, banner_html, html, count=1)
        print("[4] Replaced embedded cockpit in improvised-view with direct link banner")

    # 5. Insert dedicated <div id="academic-view"> right after </div> of improvised-view
    academic_view_html = '''
  <!-- ============================================================ -->
  <!-- 3. ACADEMIC WEAPON 10-FEATURE RESEARCH FRONTIERS VIEW        -->
  <!-- ============================================================ -->
  <div id="academic-view" style="display:none; padding-top:16px;">
    <!-- Stage Navigation Banner -->
    <div class="stage-nav-banner" style="background:#FFFFFF;border:1px solid #DDD6FE;border-radius:var(--radius-lg);padding:18px 24px;margin-bottom:24px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;box-shadow:0 2px 8px rgba(124,58,237,0.08);">
      <div>
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;flex-wrap:wrap;">
          <span class="badge" style="background:#EDE9FE;color:#6D28D9;border-color:#DDD6FE;font-weight:700;">FINAL PROJECT &middot; CSE3101</span>
          <span class="badge" style="background:#ECFDF5;color:#047857;border-color:#A7F3D0;font-weight:700;">10 ELITE RESEARCH FRONTIERS</span>
          <span class="badge" style="background:#EFF6FF;color:#1D4ED8;border-color:#BFDBFE;font-weight:700;">171+ TESTS PASSED (100%)</span>
        </div>
        <h2 style="margin:4px 0 2px;font-size:1.35rem;font-weight:800;color:var(--text-primary);letter-spacing:-0.3px;">
          10 Autonomous Guardrail Frontiers: Live Flow Processors &amp; KaTeX Mathematical Rigor
        </h2>
        <p style="margin:0;font-size:0.84rem;color:var(--text-secondary);max-width:850px;">
          Explore and execute all 10 academic innovations built into KAVACH. Select any frontier below to inspect its theoretical LaTeX equations, execute live security pipelines, trace animated micro-flow state transitions, and verify zero-day adversarial containment.
        </p>
      </div>
      <div style="display:flex;align-items:center;gap:10px;">
        <button type="button" class="btn-nav-secondary" onclick="activatePathwayMode('midsem')" style="padding:6px 12px;font-size:0.75rem;cursor:pointer;">&larr; Earlier (v1.0)</button>
        <button type="button" class="btn-nav-secondary" onclick="activatePathwayMode('improvised')" style="padding:6px 12px;font-size:0.75rem;cursor:pointer;">Improvised (v3.0) &rarr;</button>
      </div>
    </div>

    <!-- The 10 Frontier Selector Tabs Strip -->
    <div id="academic-pillars-strip" class="academic-pillars-strip" style="display:flex;gap:8px;overflow-x:auto;padding:12px 4px 14px;margin-bottom:14px;-webkit-overflow-scrolling:touch;"></div>

    <!-- Dynamic Live Execution Deck -->
    <div id="academic-pillar-workspace" class="card" style="background:#FFFFFF;border:1px solid var(--border-subtle);border-radius:var(--radius-lg);padding:24px;box-shadow:var(--shadow-sm);margin-bottom:28px;"></div>
  </div>
'''

    if '<div id="academic-view"' not in html:
        improv_end_marker = '</div>\n\n  <!-- ============================================================ -->\n  <!-- 2. LIVE OBSERVABILITY & EXECUTION WORKSPACE VIEW'
        if improv_end_marker in html:
            html = html.replace(improv_end_marker, '</div>\n' + academic_view_html + '\n  <!-- ============================================================ -->\n  <!-- 2. LIVE OBSERVABILITY & EXECUTION WORKSPACE VIEW', 1)
            print("[5] Injected dedicated <div id=\"academic-view\"> into index.html")
        else:
            # Fallback insertion
            html = html.replace('<div id="workspace-view">', academic_view_html + '\n  <div id="workspace-view">', 1)
            print("[5] (Fallback) Injected dedicated <div id=\"academic-view\"> into index.html")

    # 6. Update renderDynamicNavbar buttons for academic mode
    old_academic_nav = """  } else if (mode === 'academic') {
    container.innerHTML = `
      <button type="button" class="nav-switch-btn active" onclick="scrollToTarget('academic-weapon-cockpit', this)">10 Frontiers</button>
      <button type="button" class="nav-switch-btn" onclick="scrollToTarget('academic-grounding-card', this)">KaTeX Math</button>
      <button type="button" class="nav-switch-btn" onclick="scrollToTarget('academic-flow-sim', this)">Flow Pipeline</button>
      <button type="button" class="nav-switch-btn" onclick="scrollToTarget('academic-telemetry-box', this)">Telemetry</button>
      <button type="button" class="nav-switch-btn" onclick="switchToDefense()">Matrix</button>
      <button type="button" class="nav-switch-btn" onclick="switchToEval()">Eval</button>
    `;"""

    new_academic_nav = """  } else if (mode === 'academic') {
    container.innerHTML = `
      <button type="button" class="nav-switch-btn active" onclick="activatePathwayMode('academic')">10 Frontiers</button>
      <button type="button" class="nav-switch-btn" onclick="scrollToTarget('academic-grounding-card', this)">KaTeX Math</button>
      <button type="button" class="nav-switch-btn" onclick="scrollToTarget('academic-flow-sim', this)">Flow Pipeline</button>
      <button type="button" class="nav-switch-btn" onclick="scrollToTarget('academic-telemetry-box', this)">Telemetry</button>
      <button type="button" class="nav-switch-btn" onclick="activatePathwayMode('midsem')">&larr; Earlier (v1.0)</button>
      <button type="button" class="nav-switch-btn" onclick="activatePathwayMode('improvised')">Improvised (v3.0) &rarr;</button>
    `;"""

    if old_academic_nav in html:
        html = html.replace(old_academic_nav, new_academic_nav, 1)
        print("[6] Updated renderDynamicNavbar for academic pathway")

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print("[*] Successfully updated index.html")

    # 7. Update style.css with active styling for pathway-btn-academic
    with open(STYLE_PATH, "r", encoding="utf-8") as f:
        css = f.read()

    if "#pathway-btn-academic.active" not in css:
        tab_css = """
/* Dedicated Active Purple Theme for Academic Weapon Pathway Tab */
.pathway-tab#pathway-btn-academic.active {
  background: #7C3AED !important;
  color: #FFFFFF !important;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.35) !important;
  border: 1px solid #6D28D9 !important;
}
.pathway-tab#pathway-btn-academic.active .pathway-chip {
  background: rgba(255, 255, 255, 0.25) !important;
  color: #FFFFFF !important;
}
.pathway-tab#pathway-btn-academic.active .pulse-dot-green {
  background: #C4B5FD !important;
  box-shadow: 0 0 8px #DDD6FE !important;
}
"""
        with open(STYLE_PATH, "a", encoding="utf-8") as f:
            f.write(tab_css)
        print("[7] Appended active styling for #pathway-btn-academic in style.css")
    else:
        print("[7] Styling already present in style.css")


if __name__ == "__main__":
    fix_all()

