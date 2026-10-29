import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRONTEND_DIR = os.path.join(ROOT, "01_KAVACH_Platform", "frontend")
INDEX_PATH = os.path.join(FRONTEND_DIR, "index.html")
STYLE_PATH = os.path.join(FRONTEND_DIR, "style.css")
APP_JS_PATH = os.path.join(FRONTEND_DIR, "app.js")
SCRIPT_JS_PATH = os.path.join(FRONTEND_DIR, "script.js")

def update_index():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Remove interactive-particle-web canvas
    html = re.sub(r'<!-- Interactive Neural Constellation Canvas.*?-->\s*<canvas id="interactive-particle-web".*?</canvas>\s*', '', html, flags=re.DOTALL)
    # Also if standalone canvas exists:
    html = re.sub(r'<canvas id="interactive-particle-web".*?</canvas>\s*', '', html)
    print("[1] Removed interactive-particle-web canvas from index.html")

    # 2. In nav-actions: remove Motion button and move header-academic-btn to hidden fallback
    # Pattern to find header-motion-btn
    motion_pattern = r'<a href="/motion/" id="header-motion-btn".*?</a>\s*'
    html = re.sub(motion_pattern, '', html, flags=re.DOTALL)
    print("[2] Removed Motion button from header nav-actions")

    # Pattern for duplicate header-academic-btn in nav-actions: keep as hidden span fallback
    academic_btn_pattern = r'<button type="button" id="header-academic-btn".*?<span>10 Frontiers</span>\s*</button>\s*'
    if re.search(academic_btn_pattern, html, flags=re.DOTALL):
        html = re.sub(academic_btn_pattern, '<span id="header-academic-btn" style="display:none;" onclick="activatePathwayMode(\'academic\')"></span>\n', html, flags=re.DOTALL)
        print("[3] Converted duplicate right-side 10 Frontiers button into hidden compatibility anchor")

    # 3. Cache-busting bump to v4.1.0 across all CSS/JS
    html = re.sub(r'style\.css\?v=[0-9a-zA-Z\.]+', 'style.css?v=4.1.0', html)
    html = re.sub(r'query_library\.js\?v=[0-9a-zA-Z\.]+', 'query_library.js?v=4.1.0', html)
    html = re.sub(r'script\.js\?v=[0-9a-zA-Z\.]+', 'script.js?v=4.1.0', html)
    html = re.sub(r'app\.js\?v=[0-9a-zA-Z\.]+', 'app.js?v=4.1.0', html)
    html = re.sub(r'improvised_controller\.js\?v=[0-9a-zA-Z\.]+', 'improvised_controller.js?v=4.1.0', html)
    html = re.sub(r'course_cockpit\.js\?v=[0-9a-zA-Z\.]+', 'course_cockpit.js?v=4.1.0', html)
    html = re.sub(r'academic_weapon\.js\?v=[0-9a-zA-Z\.]+', 'academic_weapon.js?v=4.1.0', html)
    html = re.sub(r'eli5_hub\.js\?v=[0-9a-zA-Z\.]+', 'eli5_hub.js?v=4.1.0', html)
    html = re.sub(r'gov_rules_codex\.js\?v=[0-9a-zA-Z\.]+', 'gov_rules_codex.js?v=4.1.0', html)
    html = re.sub(r'implementation_flow\.js\?v=[0-9a-zA-Z\.]+', 'implementation_flow.js?v=4.1.0', html)
    print("[4] Updated cache busting tags to v4.1.0")

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html)

def update_css():
    with open(STYLE_PATH, "r", encoding="utf-8") as f:
        css = f.read()

    # Disable particle canvas in CSS
    if "#interactive-particle-web {" in css:
        css = re.sub(r'#interactive-particle-web\s*\{[^}]*\}', '#interactive-particle-web { display: none !important; }', css)

    # Modern spacious header layout replacement
    old_header_main = """.app-header-main {
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  padding: 6px 16px !important;
  gap: 12px !important;
  width: 100% !important;
  max-width: 1560px !important;
  margin: 0 auto !important;
  box-sizing: border-box !important;
  min-height: 48px !important;
}"""

    new_header_main = """.app-header-main {
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  padding: 8px 24px !important;
  gap: 16px !important;
  width: 100% !important;
  max-width: 1680px !important;
  margin: 0 auto !important;
  box-sizing: border-box !important;
  min-height: 54px !important;
}"""

    if old_header_main in css:
        css = css.replace(old_header_main, new_header_main, 1)
        print("[5] Upgraded app-header-main to spacious 54px height with 24px padding")

    # Clean nav-switcher so buttons are NEVER truncated (...eplay fix)
    old_nav_switcher = """.nav-switcher {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  justify-content: safe center;
  gap: 5px;
  background: transparent;
  border: none;
  padding: 0 4px;
  border-radius: 0;
  max-width: 100%;
  overflow-x: auto;
  scrollbar-width: none;
  -webkit-overflow-scrolling: touch;
  flex: 0 1 auto;
  margin: 0 10px;
  white-space: nowrap;
}"""

    new_nav_switcher = """.nav-switcher {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: transparent;
  border: none;
  padding: 0 10px;
  border-radius: 0;
  max-width: 100%;
  overflow-x: auto;
  scrollbar-width: none;
  -webkit-overflow-scrolling: touch;
  flex: 1 1 auto;
  margin: 0 12px;
  white-space: nowrap;
}"""

    if old_nav_switcher in css:
        css = css.replace(old_nav_switcher, new_nav_switcher, 1)
        print("[6] Fixed nav-switcher: removed 'safe center' truncation, enabled spacious gap: 8px")

    # Clean nav-actions with unified spacious buttons
    old_nav_actions = """.nav-actions {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  flex-shrink: 0;
  flex-wrap: nowrap;
  margin: 0 !important;
}"""

    new_nav_actions = """.nav-actions {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  flex-shrink: 0;
  flex-wrap: nowrap;
  margin: 0 !important;
}"""

    if old_nav_actions in css:
        css = css.replace(old_nav_actions, new_nav_actions, 1)
        print("[7] Updated nav-actions with gap: 9px")

    # Pathway Selector container and tab styling
    old_selector = """.header-pathway-selector {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 3px;
  background: #F1F5F9;
  border: 1px solid #CBD5E1;
  border-radius: var(--radius-full);
  padding: 2px;
  height: 33px;
  box-sizing: border-box;
  flex-shrink: 0;
  margin: 0 !important;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.04);
  transition: all var(--transition-normal);
}"""

    new_selector = """.header-pathway-selector {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: var(--radius-full);
  padding: 3px 5px;
  height: 35px;
  box-sizing: border-box;
  flex-shrink: 0;
  margin: 0 !important;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.03);
  transition: all var(--transition-normal);
}"""

    if old_selector in css:
        css = css.replace(old_selector, new_selector, 1)
        print("[8] Enhanced header-pathway-selector with clean background and spacious padding")

    # Update pathway tab styles
    old_tab = """.pathway-tab,
.pathway-tab#pathway-btn-midsem,
.pathway-tab#pathway-btn-improvised {
  background: transparent;
  color: #475569;
  border: 1px solid transparent;
  border-radius: var(--radius-full);
  padding: 0 9px;
  height: 27px;
  font-size: 0.75rem;
  font-family: var(--font-sans);
  font-weight: 600;
  letter-spacing: -0.01em;
  cursor: pointer;
  transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  box-sizing: border-box;
  gap: 5px;
  margin: 0 !important;
}"""

    new_tab = """.pathway-tab,
.pathway-tab#pathway-btn-midsem,
.pathway-tab#pathway-btn-improvised {
  background: transparent;
  color: #475569;
  border: 1px solid transparent;
  border-radius: var(--radius-full);
  padding: 0 13px;
  height: 29px;
  font-size: 0.78rem;
  font-family: var(--font-sans);
  font-weight: 600;
  letter-spacing: -0.01em;
  cursor: pointer;
  transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  box-sizing: border-box;
  gap: 6px;
  margin: 0 !important;
}"""

    if old_tab in css:
        css = css.replace(old_tab, new_tab, 1)
        print("[9] Enhanced pathway tabs with height: 29px, padding: 0 13px, font: 0.78rem")

    # Academic Weapon button dedicated idle & active style
    academic_tab_css = """
/* Academic Weapon Pathway Tab - Spacious & High-Contrast */
.pathway-tab#pathway-btn-academic {
  color: #6D28D9;
  font-weight: 600;
  background: transparent;
  border: 1px solid transparent;
  border-radius: var(--radius-full);
  padding: 0 14px;
  height: 29px;
  font-size: 0.78rem;
  gap: 6px;
  cursor: pointer;
  transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
}
.pathway-tab#pathway-btn-academic:hover:not(.active) {
  background: #F5F3FF;
  border-color: #DDD6FE;
  color: #5B21B6;
}
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
    if "/* Academic Weapon Pathway Tab - Spacious & High-Contrast */" not in css:
        css = css.rstrip() + "\n" + academic_tab_css
        print("[10] Appended dedicated high-contrast Academic Weapon tab styling")

    with open(STYLE_PATH, "w", encoding="utf-8") as f:
        f.write(css)

def neutralize_particle_canvas():
    # Make initInteractiveParticleWeb a no-op in app.js and script.js
    for path, name in [(APP_JS_PATH, "app.js"), (SCRIPT_JS_PATH, "script.js")]:
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()

        # Replace particle canvas logic with clean no-op
        pattern = r'function initInteractiveParticleWeb\(\)\s*\{[\s\S]*?requestAnimationFrame\(renderParticles\);\s*\}'
        clean_func = 'function initInteractiveParticleWeb() {\n  const canvas = document.getElementById("interactive-particle-web");\n  if (canvas) canvas.remove();\n}'

        if re.search(pattern, code):
            code = re.sub(pattern, clean_func, code)
            with open(path, "w", encoding="utf-8") as f:
                f.write(code)
            print(f"[11] Neutralized initInteractiveParticleWeb in {name}")
        else:
            print(f"[11] initInteractiveParticleWeb already clean or pattern not found in {name}")

if __name__ == "__main__":
    update_index()
    update_css()
    neutralize_particle_canvas()
    print("Spacious taskbar and motion cleanup applied cleanly!")

