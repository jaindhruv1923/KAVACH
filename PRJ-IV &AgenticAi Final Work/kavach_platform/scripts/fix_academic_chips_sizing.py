import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRONTEND_DIR = os.path.join(ROOT, "01_KAVACH_Platform", "frontend")
INDEX_PATH = os.path.join(FRONTEND_DIR, "index.html")
STYLE_PATH = os.path.join(FRONTEND_DIR, "style.css")
ACADEMIC_JS_PATH = os.path.join(FRONTEND_DIR, "academic_weapon.js")

def update_academic_js():
    with open(ACADEMIC_JS_PATH, "r", encoding="utf-8") as f:
        code = f.read()

    code = code.replace("\r\n", "\n")

    # Add shortName to pillars if not already present
    short_names = {
        '"dp": {': '"dp": {\n      shortName: "Differential Privacy",',
        '"got": {': '"got": {\n      shortName: "Graph-of-Thoughts DAG",',
        '"watermark": {': '"watermark": {\n      shortName: "Agent Watermarking",',
        '"lattice": {': '"lattice": {\n      shortName: "Security Lattice",',
        '"pqc": {': '"pqc": {\n      shortName: "Post-Quantum Shield",',
        '"wallet": {': '"wallet": {\n      shortName: "Denial-of-Wallet Guard",',
        '"entailment": {': '"entailment": {\n      shortName: "Factuality Entailment",',
        '"saga": {': '"saga": {\n      shortName: "SAGA Compensation",',
        '"causal": {': '"causal": {\n      shortName: "Causal Counterfactual",',
        '"ablation": {': '"ablation": {\n      shortName: "Empirical Ablation",'
    }

    for key, repl in short_names.items():
        if key in code and "shortName:" not in code[code.find(key):code.find(key) + 80]:
            code = code.replace(key, repl, 1)

    # Update render loop in renderAcademicWeaponCockpit
    old_loop_pat = r'stripHtml \+= `\s*<button type="button" class="academic-pillar-chip \$\{isActive \? \'active\' : \'\'\}" onclick="window\.selectAcademicPillar\(\'\$\{key\}\'\)">\s*<span class="pillar-num-badge">\$\{p\.num\}</span>\s*<span>\$\{p\.name\}</span>\s*</button>\s*`;'
    
    new_loop = """stripHtml += `
        <button type="button" class="academic-pillar-chip ${isActive ? 'active' : ''}" onclick="window.selectAcademicPillar('${key}')" title="${p.name} (${p.badge})">
          <span class="pillar-num-badge">${p.num}</span>
          <span class="pillar-chip-name">${p.shortName || p.name}</span>
        </button>
      `;"""

    if re.search(old_loop_pat, code):
        code = re.sub(old_loop_pat, new_loop, code, count=1)
        print("[1] Updated chip rendering loop in academic_weapon.js with clean shortName & title attribute")
    else:
        # Fallback check
        code = code.replace('<span>${p.name}</span>', '<span class="pillar-chip-name">${p.shortName || p.name}</span>')
        print("[1] (Fallback) Updated chip span in academic_weapon.js")

    with open(ACADEMIC_JS_PATH, "w", encoding="utf-8") as f:
        f.write(code)

def update_index_html():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace("\r\n", "\n")

    # Remove inline style on academic-pillars-strip so CSS grid takes full control
    old_strip_tag = '<div id="academic-pillars-strip" class="academic-pillars-strip" style="display:flex;gap:8px;overflow-x:auto;padding:12px 4px 14px;margin-bottom:14px;-webkit-overflow-scrolling:touch;"></div>'
    new_strip_tag = '<div id="academic-pillars-strip" class="academic-pillars-strip"></div>'
    if old_strip_tag in html:
        html = html.replace(old_strip_tag, new_strip_tag, 1)
        print("[2] Removed conflicting inline flex style on academic-pillars-strip in index.html")
    else:
        html = re.sub(r'<div id="academic-pillars-strip" class="academic-pillars-strip"[^>]*></div>', '<div id="academic-pillars-strip" class="academic-pillars-strip"></div>', html)
        print("[2] (Regex) Standardized academic-pillars-strip tag in index.html")

    # Cache busting bump to v4.3.0
    html = re.sub(r'style\.css\?v=[0-9a-zA-Z\.]+', 'style.css?v=4.3.0', html)
    html = re.sub(r'academic_weapon\.js\?v=[0-9a-zA-Z\.]+', 'academic_weapon.js?v=4.3.0', html)
    html = re.sub(r'app\.js\?v=[0-9a-zA-Z\.]+', 'app.js?v=4.3.0', html)
    print("[3] Updated cache busting tags to v4.3.0")

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html)

def update_style_css():
    with open(STYLE_PATH, "r", encoding="utf-8") as f:
        css = f.read()

    css = css.replace("\r\n", "\n")

    # Replace old .academic-pillars-strip and .academic-pillar-chip styles
    strip_block_pat = r'\.academic-pillars-strip\s*\{[^}]*\}'
    new_strip_css = """.academic-pillars-strip {
  display: grid !important;
  grid-template-columns: repeat(5, 1fr) !important;
  gap: 10px !important;
  padding: 8px 0 16px !important;
  margin-bottom: 18px !important;
  border-bottom: 1px solid var(--border-subtle);
  width: 100% !important;
  box-sizing: border-box !important;
}

@media (max-width: 1100px) {
  .academic-pillars-strip {
    grid-template-columns: repeat(3, 1fr) !important;
  }
}

@media (max-width: 768px) {
  .academic-pillars-strip {
    grid-template-columns: repeat(2, 1fr) !important;
  }
}

@media (max-width: 480px) {
  .academic-pillars-strip {
    grid-template-columns: 1fr !important;
  }
}"""

    if re.search(strip_block_pat, css):
        css = re.sub(strip_block_pat, new_strip_css, css, count=1)
        print("[4] Replaced academic-pillars-strip with 5-column responsive grid")

    # Replace chip styles
    chip_block_pat = r'\.academic-pillar-chip\s*\{[^}]*\}'
    new_chip_css = """.academic-pillar-chip {
  padding: 8px 12px !important;
  border-radius: 9px !important;
  border: 1px solid #E2E8F0 !important;
  background: #FFFFFF !important;
  color: #334155 !important;
  font-size: 0.77rem !important;
  font-family: var(--font-sans) !important;
  font-weight: 600 !important;
  letter-spacing: -0.01em !important;
  cursor: pointer !important;
  white-space: nowrap !important;
  transition: all 0.16s cubic-bezier(0.16, 1, 0.3, 1) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: flex-start !important;
  gap: 8px !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
  height: 38px !important;
  box-sizing: border-box !important;
  min-width: 0 !important;
  overflow: hidden !important;
  margin: 0 !important;
}"""

    if re.search(chip_block_pat, css):
        css = re.sub(chip_block_pat, new_chip_css, css, count=1)
        print("[5] Replaced academic-pillar-chip with spacious left-aligned 38px button style")

    # Add pillar-chip-name CSS
    if ".pillar-chip-name {" not in css:
        name_css = """
.pillar-chip-name {
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  white-space: nowrap !important;
  flex: 1 1 auto !important;
  text-align: left !important;
}
"""
        css = css.rstrip() + "\n" + name_css
        print("[6] Appended pillar-chip-name text truncation safeguard")

    with open(STYLE_PATH, "w", encoding="utf-8") as f:
        f.write(css)

if __name__ == "__main__":
    update_academic_js()
    update_index_html()
    update_style_css()
    print("Academic pillar chips sizing and formatting completed successfully!")

