import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRONTEND_DIR = os.path.join(ROOT, "01_KAVACH_Platform", "frontend")
INDEX_PATH = os.path.join(FRONTEND_DIR, "index.html")
STYLE_PATH = os.path.join(FRONTEND_DIR, "style.css")

def update_index_html():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # Normalize line endings
    html = html.replace("\r\n", "\n")

    # 1. Check if main-nav-switcher is still inside app-header-main
    old_header_structure = re.search(
        r'(<div class="header-left-cluster">.*?</div>\s*)(<!-- Center Section:.*?<nav class="nav-switcher" id="main-nav-switcher".*?</nav>\s*)(<!-- Right Section: Actions & Review Hub -->\s*<div class="nav-actions">)',
        html,
        re.DOTALL
    )

    if old_header_structure:
        left_cluster = old_header_structure.group(1)
        nav_switcher = old_header_structure.group(2)
        nav_actions_open = old_header_structure.group(3)

        # Remove nav-switcher from between left cluster and nav-actions
        html = html.replace(old_header_structure.group(0), left_cluster + "\n    " + nav_actions_open, 1)
        print("[1] Removed main-nav-switcher from inside app-header-main")

    # 2. In nav-actions: remove Tour and Console buttons, keep hidden anchors
    # Remove Tour button
    tour_btn_pat = r'<button type="button" id="header-defense-tour-btn".*?<span>Tour</span>\s*</button>\s*'
    if re.search(tour_btn_pat, html, re.DOTALL):
        html = re.sub(tour_btn_pat, '<span id="header-defense-tour-btn" style="display:none;" onclick="if(window.startDefenseTour)window.startDefenseTour()"></span>\n', html, flags=re.DOTALL)
        print("[2] Removed Tour button from header nav-actions")

    # Remove Console button
    console_btn_pat = r'<button type="button" class="btn-console-cta.*?>\s*<span>Console</span>.*?</button>\s*'
    if re.search(console_btn_pat, html, re.DOTALL):
        html = re.sub(console_btn_pat, '<span id="btn-console-cta" style="display:none;" onclick="if(window.switchToWorkspace)window.switchToWorkspace()"></span>\n', html, flags=re.DOTALL)
        print("[3] Removed Console button from header nav-actions")

    # 3. Insert Tier 2 dedicated sub-nav right under app-header-main
    # Check if app-header-subnav already exists
    if '<div class="app-header-subnav"' not in html:
        tier2_html = """  </div>

  <!-- Tier 2: Dedicated Contextual Navigation Sub-Bar ("just usi ke niche" - full width, perfectly centered, never cropped!) -->
  <div class="app-header-subnav" id="app-header-subnav">
    <div class="subnav-container">
      <nav class="nav-switcher" id="main-nav-switcher" role="tablist" aria-label="Context Navigation Tabs">
        <button type="button" class="nav-switch-btn active" onclick="scrollToTarget('product-view', this)">Overview</button>
        <button type="button" class="nav-switch-btn" onclick="scrollToTarget('architecture-flowchart', this)">Flowchart</button>
        <button type="button" class="nav-switch-btn" onclick="scrollToTarget('terminal-results-section', this)">Checks</button>
        <button type="button" class="nav-switch-btn" onclick="switchToDefense()">Matrix</button>
        <button type="button" class="nav-switch-btn" onclick="switchToEval()">Eval</button>
        <button type="button" class="nav-switch-btn" onclick="switchToResearch()">Paper</button>
      </nav>
    </div>
  </div>"""

        # Replace closing </div> of app-header-main
        header_end_target = "    </div>\n  </div>\n\n  <div id=\"scroll-scrub-bar\""
        if header_end_target in html:
            html = html.replace(header_end_target, "    </div>\n" + tier2_html + "\n\n  <div id=\"scroll-scrub-bar\"", 1)
            print("[4] Inserted dedicated Tier 2 app-header-subnav right below app-header-main")
        else:
            # Fallback
            html = re.sub(r'(</div>\s*</div>\s*<div id="scroll-scrub-bar")', r'</div>\n' + tier2_html + r'\n\n  <div id="scroll-scrub-bar"', html, count=1)
            print("[4] (Fallback) Inserted dedicated Tier 2 app-header-subnav")

    # 4. Cache-busting bump to v4.2.0
    html = re.sub(r'style\.css\?v=[0-9a-zA-Z\.]+', 'style.css?v=4.2.0', html)
    html = re.sub(r'query_library\.js\?v=[0-9a-zA-Z\.]+', 'query_library.js?v=4.2.0', html)
    html = re.sub(r'script\.js\?v=[0-9a-zA-Z\.]+', 'script.js?v=4.2.0', html)
    html = re.sub(r'app\.js\?v=[0-9a-zA-Z\.]+', 'app.js?v=4.2.0', html)
    html = re.sub(r'improvised_controller\.js\?v=[0-9a-zA-Z\.]+', 'improvised_controller.js?v=4.2.0', html)
    html = re.sub(r'course_cockpit\.js\?v=[0-9a-zA-Z\.]+', 'course_cockpit.js?v=4.2.0', html)
    html = re.sub(r'academic_weapon\.js\?v=[0-9a-zA-Z\.]+', 'academic_weapon.js?v=4.2.0', html)
    html = re.sub(r'eli5_hub\.js\?v=[0-9a-zA-Z\.]+', 'eli5_hub.js?v=4.2.0', html)
    html = re.sub(r'gov_rules_codex\.js\?v=[0-9a-zA-Z\.]+', 'gov_rules_codex.js?v=4.2.0', html)
    html = re.sub(r'implementation_flow\.js\?v=[0-9a-zA-Z\.]+', 'implementation_flow.js?v=4.2.0', html)
    print("[5] Updated cache busting query tags to v4.2.0")

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html)

def update_style_css():
    with open(STYLE_PATH, "r", encoding="utf-8") as f:
        css = f.read()

    css = css.replace("\r\n", "\n")

    # 1. Body padding for two-tier header
    css = re.sub(r'body\s*\{[^}]*padding:\s*[0-9]+px\s+[0-9]+px\s+[0-9]+px;', 'body {\n  margin: 0;\n  padding: 106px 0 80px;', css, count=1)
    if "html {\n  scroll-padding-top: 106px;\n}" not in css:
        css = "html {\n  scroll-padding-top: 106px;\n  scroll-behavior: smooth;\n}\n" + css
    print("[6] Added scroll-padding-top: 106px and body padding: 106px 0 80px")

    # 2. Main header styling
    old_header_main = re.search(r'\.app-header-main\s*\{[^}]*\}', css)
    new_header_main = """.app-header-main {
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  padding: 7px 28px !important;
  gap: 16px !important;
  width: 100% !important;
  max-width: 1680px !important;
  margin: 0 auto !important;
  box-sizing: border-box !important;
  min-height: 48px !important;
}"""
    if old_header_main:
        css = css.replace(old_header_main.group(0), new_header_main, 1)
        print("[7] Refined app-header-main for Tier 1")

    # 3. Enable app-header-subnav for Tier 2
    old_subnav = re.search(r'\.app-header-subnav\s*\{[^}]*\}', css)
    new_subnav = """.app-header-subnav {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 100% !important;
  background: rgba(248, 250, 252, 0.96) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  border-top: 1px solid #E2E8F0 !important;
  padding: 5px 20px !important;
  box-sizing: border-box !important;
  min-height: 42px !important;
  overflow-x: auto !important;
  scrollbar-width: none !important;
}

.app-header-subnav::-webkit-scrollbar {
  display: none !important;
}

.subnav-container {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 100% !important;
  max-width: 1400px !important;
  margin: 0 auto !important;
}"""

    if old_subnav:
        css = css.replace(old_subnav.group(0), new_subnav, 1)
        print("[8] Configured app-header-subnav for Tier 2")

    # 4. Refine nav-switcher and nav-switch-btn
    old_switcher = re.search(r'\.nav-switcher\s*\{[^}]*\}', css)
    new_switcher = """.nav-switcher {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 10px !important;
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
  max-width: 100% !important;
  overflow-x: auto !important;
  scrollbar-width: none !important;
  -webkit-overflow-scrolling: touch !important;
  white-space: nowrap !important;
  flex: 0 1 auto !important;
  margin: 0 auto !important;
}"""
    if old_switcher:
        css = css.replace(old_switcher.group(0), new_switcher, 1)
        print("[9] Styled nav-switcher for spacious Tier 2 sub-nav")

    old_switch_btn = re.search(r'\.nav-switch-btn\s*\{[^}]*\}', css)
    new_switch_btn = """.nav-switch-btn {
  background: #FFFFFF !important;
  color: #334155 !important;
  border: 1px solid #CBD5E1 !important;
  border-radius: var(--radius-full) !important;
  padding: 5px 16px !important;
  font-size: 0.78rem !important;
  font-family: var(--font-sans) !important;
  font-weight: 600 !important;
  letter-spacing: -0.01em !important;
  cursor: pointer !important;
  margin: 0 !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
  white-space: nowrap !important;
  flex-shrink: 0 !important;
  transition: all 0.16s cubic-bezier(0.16, 1, 0.3, 1) !important;
  height: 30px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}"""
    if old_switch_btn:
        css = css.replace(old_switch_btn.group(0), new_switch_btn, 1)
        print("[10] Styled nav-switch-btn with 30px height, 16px padding, subtle shadow")

    with open(STYLE_PATH, "w", encoding="utf-8") as f:
        f.write(css)

if __name__ == "__main__":
    update_index_html()
    update_style_css()
    print("All two-tier subnav updates applied successfully!")
