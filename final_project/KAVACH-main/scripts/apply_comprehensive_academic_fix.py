import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRONTEND_DIR = os.path.join(ROOT, "01_KAVACH_Platform", "frontend")
INDEX_PATH = os.path.join(FRONTEND_DIR, "index.html")
STYLE_PATH = os.path.join(FRONTEND_DIR, "style.css")
APP_JS_PATH = os.path.join(FRONTEND_DIR, "app.js")
ACADEMIC_JS_PATH = os.path.join(FRONTEND_DIR, "academic_weapon.js")

def update_style():
    with open(STYLE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    addition = """
/* Safeguard pointer-events so clicks on inner spans/dots bubble to pathway buttons */
.pathway-tab * {
  pointer-events: none !important;
}

/* Header right-side 10 Frontiers tool button active styling */
.header-tool-btn#header-academic-btn.active {
  background: #7C3AED !important;
  color: #FFFFFF !important;
  border-color: #6D28D9 !important;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.35) !important;
}
.header-tool-btn#header-academic-btn.active svg {
  stroke: #FFFFFF !important;
}
"""
    if "header-academic-btn.active" not in content:
        content = content.rstrip() + "\n" + addition
        with open(STYLE_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print("[STYLE] Added pointer-events safeguard and header-academic-btn active style")
    else:
        print("[STYLE] Already has header-academic-btn.active")

def update_index_html():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # Cache busting
    html = re.sub(r'style\.css\?v=[0-9a-zA-Z\.]+', 'style.css?v=4.0.0', html)
    html = re.sub(r'query_library\.js\?v=[0-9a-zA-Z\.]+', 'query_library.js?v=4.0.0', html)
    html = re.sub(r'script\.js\?v=[0-9a-zA-Z\.]+', 'script.js?v=4.0.0', html)
    html = re.sub(r'app\.js\?v=[0-9a-zA-Z\.]+', 'app.js?v=4.0.0', html)
    html = re.sub(r'improvised_controller\.js\?v=[0-9a-zA-Z\.]+', 'improvised_controller.js?v=4.0.0', html)
    html = re.sub(r'course_cockpit\.js\?v=[0-9a-zA-Z\.]+', 'course_cockpit.js?v=4.0.0', html)
    html = re.sub(r'academic_weapon\.js\?v=[0-9a-zA-Z\.]+', 'academic_weapon.js?v=4.0.0', html)
    html = re.sub(r'eli5_hub\.js\?v=[0-9a-zA-Z\.]+', 'eli5_hub.js?v=4.0.0', html)
    html = re.sub(r'gov_rules_codex\.js\?v=[0-9a-zA-Z\.]+', 'gov_rules_codex.js?v=4.0.0', html)
    html = re.sub(r'implementation_flow\.js\?v=[0-9a-zA-Z\.]+', 'implementation_flow.js?v=4.0.0', html)

    # In top inline script activatePathwayMode: toggle header-academic-btn
    target_btn = "const btnAcademic = document.getElementById('pathway-btn-academic');\n  if (btnAcademic) btnAcademic.classList.toggle('active', mode === 'academic');"
    repl_btn = """const btnAcademic = document.getElementById('pathway-btn-academic');
  if (btnAcademic) btnAcademic.classList.toggle('active', mode === 'academic');
  const headerAcademicBtn = document.getElementById('header-academic-btn');
  if (headerAcademicBtn) headerAcademicBtn.classList.toggle('active', mode === 'academic');"""

    if target_btn in html:
        html = html.replace(target_btn, repl_btn, 1)
        print("[INDEX] Added headerAcademicBtn sync in top inline activatePathwayMode")

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print("[INDEX] Updated cache-busting versions to ?v=4.0.0")

def update_app_js():
    with open(APP_JS_PATH, "r", encoding="utf-8") as f:
        code = f.read()

    # Ensure headerAcademicBtn is synced in switchMasterView
    old_switch = "  if (btnAcademic) btnAcademic.classList.toggle('active', mode === 'academic');"
    new_switch = """  if (btnAcademic) btnAcademic.classList.toggle('active', mode === 'academic');
  const headerAcademicBtn = document.getElementById('header-academic-btn');
  if (headerAcademicBtn) headerAcademicBtn.classList.toggle('active', mode === 'academic');"""

    if old_switch in code and "headerAcademicBtn" not in code:
        code = code.replace(old_switch, new_switch, 1)
        print("[APP_JS] Added headerAcademicBtn to switchMasterView")

    # Add explicit button click binding at bottom of app.js
    binder_code = """
// Academic Weapon pathway button click safeguard
function bindAcademicButtonsGlobally() {
  const btnAcademic = document.getElementById('pathway-btn-academic');
  if (btnAcademic && !btnAcademic._kavachAcademicBound) {
    btnAcademic._kavachAcademicBound = true;
    btnAcademic.addEventListener('click', function(e) {
      if (typeof window.activatePathwayMode === 'function') {
        window.activatePathwayMode('academic');
      }
    });
  }
  const headerAcademicBtn = document.getElementById('header-academic-btn');
  if (headerAcademicBtn && !headerAcademicBtn._kavachAcademicBound) {
    headerAcademicBtn._kavachAcademicBound = true;
    headerAcademicBtn.addEventListener('click', function(e) {
      if (typeof window.activatePathwayMode === 'function') {
        window.activatePathwayMode('academic');
      }
    });
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', bindAcademicButtonsGlobally);
} else {
  bindAcademicButtonsGlobally();
}
"""
    if "bindAcademicButtonsGlobally" not in code:
        code = code.rstrip() + "\n" + binder_code
        print("[APP_JS] Appended bindAcademicButtonsGlobally")

    with open(APP_JS_PATH, "w", encoding="utf-8") as f:
        f.write(code)

def update_academic_js():
    with open(ACADEMIC_JS_PATH, "r", encoding="utf-8") as f:
        code = f.read()

    binder_code = """
  // Guarantee Academic Weapon button binds even if loaded after app.js
  function bindAcademicWeaponTriggers() {
    const btnAcademic = document.getElementById('pathway-btn-academic');
    if (btnAcademic && !btnAcademic._kavachTrigBound) {
      btnAcademic._kavachTrigBound = true;
      btnAcademic.addEventListener('click', function() {
        if (typeof window.activatePathwayMode === 'function') {
          window.activatePathwayMode('academic');
        }
      });
    }
    const headerAcademicBtn = document.getElementById('header-academic-btn');
    if (headerAcademicBtn && !headerAcademicBtn._kavachTrigBound) {
      headerAcademicBtn._kavachTrigBound = true;
      headerAcademicBtn.addEventListener('click', function() {
        if (typeof window.activatePathwayMode === 'function') {
          window.activatePathwayMode('academic');
        }
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindAcademicWeaponTriggers);
  } else {
    bindAcademicWeaponTriggers();
  }
"""
    if "bindAcademicWeaponTriggers" not in code:
        # Insert before closing (function () { ... })();
        last_paren = code.rfind("})();")
        if last_paren != -1:
            code = code[:last_paren] + binder_code + "\n" + code[last_paren:]
            print("[ACADEMIC_JS] Injected bindAcademicWeaponTriggers into IIFE")
            with open(ACADEMIC_JS_PATH, "w", encoding="utf-8") as f:
                f.write(code)

if __name__ == "__main__":
    update_style()
    update_index_html()
    update_app_js()
    update_academic_js()
    print("All updates applied cleanly!")
