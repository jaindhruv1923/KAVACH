"""
Python utility to patch index.html and style.css in final_project/KAVACH-main/
Injects the 10 Academic Weapon Frontiers Cockpit, Pathway Tabs, and Navigation hooks.
"""

import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INDEX_PATH = os.path.join(ROOT, "01_KAVACH_Platform", "frontend", "index.html")
STYLE_PATH = os.path.join(ROOT, "01_KAVACH_Platform", "frontend", "style.css")


def patch_index_html():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add Pathway Selector Tab
    old_pathway = '<button type="button" id="pathway-btn-improvised" class="pathway-tab" onclick="activatePathwayMode(\'improvised\')" title="View Newly Added Post-Mid-Sem Innovations">\n          <span class="pulse-dot-green"></span> Improvised <span class="pathway-chip">v3.0</span>\n        </button>'
    new_pathway = old_pathway + '\n        <button type="button" id="pathway-btn-academic" class="pathway-tab" onclick="activatePathwayMode(\'academic\')" title="View 10 Academic Weapon Frontiers & Live Flow Processors">\n          <span class="pulse-dot-green" style="background:#8B5CF6;"></span> Academic Weapon <span class="pathway-chip" style="background:#EDE9FE;color:#7C3AED;font-weight:700;">10 Frontiers</span>\n        </button>'
    
    if "pathway-btn-academic" not in content and 'id="pathway-btn-improvised"' in content:
        # Flexible regex replacement
        content = re.sub(
            r'(<button\s+type="button"\s+id="pathway-btn-improvised"[^>]*>[\s\S]*?<\/button>)',
            r'\1\n        <button type="button" id="pathway-btn-academic" class="pathway-tab" onclick="activatePathwayMode(\'academic\')" title="View 10 Academic Weapon Frontiers & Live Flow Processors">\n          <span class="pulse-dot-green" style="background:#8B5CF6;"></span> Academic Weapon <span class="pathway-chip" style="background:#EDE9FE;color:#7C3AED;font-weight:700;">10 Frontiers</span>\n        </button>',
            content,
            count=1
        )
        print("[+] Injected pathway-btn-academic into header pathway selector")

    # 2. Add Header Action Button
    if "header-academic-btn" not in content and 'id="header-prof-review-btn"' in content:
        header_btn = '''      <button type="button" id="header-academic-btn" class="header-tool-btn magnetic-btn" onclick="activatePathwayMode('academic')" title="10 Academic Weapon Frontiers & Live Flow Processors" style="background:#F5F3FF;color:#7C3AED;border-color:#DDD6FE;font-weight:700;">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
        <span>10 Frontiers</span>
      </button>\n'''
        content = content.replace('<button type="button" id="header-prof-review-btn"', header_btn + '      <button type="button" id="header-prof-review-btn"', 1)
        print("[+] Injected header-academic-btn into header nav-actions")

    # 3. Patch activatePathwayMode function
    if "mode === 'academic'" not in content:
        target_clause = "if (mode === 'midsem') {"
        academic_clause = """const btnAcademic = document.getElementById('pathway-btn-academic');
  if (btnAcademic) btnAcademic.classList.toggle('active', mode === 'academic');

  if (mode === 'midsem') {"""
        content = content.replace("  if (mode === 'midsem') {", "  " + academic_clause, 1)

        target_else = "} else {\n    if (scopeNew) scopeNew.classList.add('active');"
        academic_branch = """} else if (mode === 'academic') {
    if (scopeNew) scopeNew.classList.add('active');
    switchToViewGlobal('improvised-view', null, 'academic-weapon');
    if (pill) pill.innerHTML = "<strong>Active Scope: Academic Weapon & Research Rigor (10 Autonomous Guardrail Frontiers).</strong> Live interactive flow processors for (&epsilon;,&delta;)-Differential Privacy, Graph-of-Thoughts DAG, Kirchenbauer Watermarking, Denning Security Lattice, NIST Post-Quantum Dilithium, OWASP LLM04 Token-Bucket, NLI Cross-Entailment, SAGA Compensation, Pearl Counterfactual XAI, and Empirical Scientific Ablations.";
    if (typeof window.renderAcademicWeaponCockpit === 'function') window.renderAcademicWeaponCockpit();
    targetId = targetId || 'academic-weapon-cockpit';
  } else {
    if (scopeNew) scopeNew.classList.add('active');"""
        content = content.replace(target_else, academic_branch, 1)
        print("[+] Patched activatePathwayMode to handle 'academic' mode")

    # 4. Patch renderDynamicNavbar function
    if "scrollToTarget('academic-weapon-cockpit'" not in content:
        navbar_target = "  } else {\n    container.innerHTML = `\n      <button type=\"button\" class=\"nav-switch-btn active\" onclick=\"scrollToTarget('improvised-innovations-section'"
        navbar_academic = """  } else if (mode === 'academic') {
    container.innerHTML = `
      <button type="button" class="nav-switch-btn active" onclick="scrollToTarget('academic-weapon-cockpit', this)">10 Frontiers</button>
      <button type="button" class="nav-switch-btn" onclick="scrollToTarget('academic-grounding-card', this)">KaTeX Math</button>
      <button type="button" class="nav-switch-btn" onclick="scrollToTarget('academic-flow-sim', this)">Flow Pipeline</button>
      <button type="button" class="nav-switch-btn" onclick="scrollToTarget('academic-telemetry-box', this)">Telemetry</button>
      <button type="button" class="nav-switch-btn" onclick="switchToDefense()">Matrix</button>
      <button type="button" class="nav-switch-btn" onclick="switchToEval()">Eval</button>
    `;
  } else {
    container.innerHTML = `
      <button type="button" class="nav-switch-btn active" onclick="scrollToTarget('improvised-innovations-section'"""
        content = content.replace(navbar_target, navbar_academic, 1)
        print("[+] Patched renderDynamicNavbar for 'academic' pathway")

    # 5. Patch hash change router
    if "#academic-weapon" not in content:
        hash_target = "else if (h === '#comparison-matrix') window.filterFeatureScope('matrix');"
        hash_academic = """else if (h === '#academic' || h === '#academic-weapon' || h === '#academic-weapon-cockpit') {
    window.activatePathwayMode('academic', 'academic-weapon-cockpit');
  }
  else if (h === '#comparison-matrix') window.filterFeatureScope('matrix');"""
        content = content.replace(hash_target, hash_academic, 1)
        print("[+] Patched hash router for #academic-weapon")

    # 6. Inject academic-weapon-cockpit Section into index.html
    if 'id="academic-weapon-cockpit"' not in content:
        section_html = '''
    <!-- ============================================================ -->
    <!-- SECTION: ACADEMIC WEAPON 10-FEATURE INTERACTIVE COMMAND DECK -->
    <!-- ============================================================ -->
    <section id="academic-weapon-cockpit" class="product-section reveal-on-scroll" style="margin-top:28px;margin-bottom:32px;">
      <div class="section-intro">
        <div style="display:flex;align-items:center;gap:8px;justify-content:center;margin-bottom:8px;flex-wrap:wrap;">
          <span class="badge" style="background:#EDE9FE;color:#6D28D9;border-color:#DDD6FE;font-weight:700;">CSE3101 ACADEMIC WEAPON</span>
          <span class="badge" style="background:#ECFDF5;color:#047857;border-color:#A7F3D0;font-weight:700;">10 RESEARCH FRONTIERS</span>
          <span class="badge" style="background:#EFF6FF;color:#1D4ED8;border-color:#BFDBFE;font-weight:700;">LIVE FLOW PROCESSORS</span>
        </div>
        <h2 style="font-size:1.6rem;font-weight:800;color:var(--text-primary);letter-spacing:-0.5px;">
          10 Autonomous Guardrail Frontiers: Live Flow &amp; Mathematical Processors
        </h2>
        <p style="max-width:880px;margin:8px auto 0;font-size:0.86rem;color:var(--text-secondary);line-height:1.55;">
          Directly execute, inspect, and verify all 10 academic innovations built into KAVACH. Select any frontier below to explore its theoretical equations, execute live security pipelines, trace animated micro-flow state transitions, and verify zero-day adversarial containment.
        </p>
      </div>

      <!-- Frontier Pillar Navigation Bar (10 Clickable Tab Pills) -->
      <div id="academic-pillars-strip" class="academic-pillars-strip" style="display:flex;gap:8px;overflow-x:auto;padding:12px 4px 14px;margin-top:14px;-webkit-overflow-scrolling:touch;"></div>

      <!-- Dynamic Live Execution Deck -->
      <div id="academic-pillar-workspace" class="card" style="background:#FFFFFF;border:1px solid var(--border-subtle);border-radius:var(--radius-lg);padding:24px;box-shadow:var(--shadow-sm);margin-top:8px;"></div>
    </section>
'''
        comp_target = '    <!-- Section 2: Head-to-Head Comparative Tables -->\n    <section id="comparison-matrix-section"'
        content = content.replace(comp_target, section_html + '\n' + comp_target, 1)
        print("[+] Injected academic-weapon-cockpit section into index.html")

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("[*] Successfully updated index.html")


def patch_style_css():
    with open(STYLE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    if ".academic-pillars-strip" not in content:
        academic_styles = """
/* ==========================================================================
   ACADEMIC WEAPON 10-FEATURE INTERACTIVE COMMAND DECK STYLES
   ========================================================================== */

.academic-pillars-strip {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding: 10px 4px 14px;
  border-bottom: 1px solid var(--border-subtle);
  scrollbar-width: thin;
}

.academic-pillar-chip {
  padding: 8px 14px;
  border-radius: 8px;
  border: 1px solid var(--border-medium);
  background: #FFFFFF;
  color: var(--text-secondary);
  font-size: 0.76rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.15s ease;
  display: flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}

.academic-pillar-chip:hover {
  background: #F8FAFC;
  border-color: #A855F7;
  color: #6D28D9;
}

.academic-pillar-chip.active {
  background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
  color: #FFFFFF !important;
  border-color: #6D28D9;
  box-shadow: 0 2px 8px rgba(109, 40, 217, 0.25);
}

.academic-pillar-chip.active .pillar-num-badge {
  background: rgba(255,255,255,0.25);
  color: #FFFFFF;
}

.pillar-num-badge {
  font-size: 0.65rem;
  padding: 2px 6px;
  border-radius: 4px;
  background: #F1F5F9;
  color: #64748B;
  font-weight: 700;
}

.academic-workspace-grid {
  display: grid;
  grid-template-columns: 1.05fr 1fr;
  gap: 22px;
}

@media (max-width: 992px) {
  .academic-workspace-grid {
    grid-template-columns: 1fr;
  }
}

.academic-subcard {
  background: #FFFFFF;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 18px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.02);
  margin-bottom: 16px;
}

.academic-subcard-title {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.academic-math-box {
  background: #FAF5FF;
  border: 1px solid #E9D5FF;
  border-radius: 8px;
  padding: 12px 14px;
  font-family: var(--font-mono);
  font-size: 0.80rem;
  color: #581C87;
  margin-bottom: 12px;
  overflow-x: auto;
}

.academic-flow-diagram {
  display: flex;
  align-items: center;
  gap: 8px;
  overflow-x: auto;
  padding: 12px 8px;
  background: #F8FAFC;
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  margin-bottom: 14px;
}

.academic-flow-step {
  flex: 1;
  min-width: 110px;
  background: #FFFFFF;
  border: 1px solid #CBD5E1;
  border-radius: 6px;
  padding: 8px 10px;
  text-align: center;
  font-size: 0.70rem;
  transition: all 0.2s ease;
}

.academic-flow-step.pulse {
  border-color: #7C3AED;
  background: #F5F3FF;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.18);
}

.academic-flow-step.verified {
  border-color: #10B981;
  background: #ECFDF5;
  color: #065F46;
}

.academic-flow-step strong {
  display: block;
  font-size: 0.74rem;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.academic-flow-arrow {
  color: #94A3B8;
  font-size: 0.85rem;
  font-weight: 700;
}

.academic-telemetry-screen {
  background: #0F172A;
  border-radius: 8px;
  padding: 14px;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: #E2E8F0;
  max-height: 240px;
  overflow-y: auto;
  line-height: 1.5;
  border: 1px solid #1E293B;
}

.academic-telemetry-line {
  margin-bottom: 3px;
  word-break: break-all;
}

.telemetry-time { color: #64748B; margin-right: 6px; }
.telemetry-tag { color: #38BDF8; font-weight: 600; margin-right: 6px; }
.telemetry-pass { color: #34D399; font-weight: 700; }
.telemetry-veto { color: #F87171; font-weight: 700; }
.telemetry-warn { color: #FBBF24; font-weight: 700; }
.telemetry-info { color: #94A3B8; }
"""
        with open(STYLE_PATH, "a", encoding="utf-8") as f:
            f.write(academic_styles)
        print("[+] Appended Academic Weapon styles to style.css")
    else:
        print("[*] Academic Weapon styles already present in style.css")


if __name__ == "__main__":
    patch_index_html()
    patch_style_css()

