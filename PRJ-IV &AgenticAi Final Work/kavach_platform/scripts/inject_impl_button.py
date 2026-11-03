import os

target_path = r"C:\Users\jaind\OneDrive\Desktop\project_work\agentic_ai_midsem_work\KAVACH-main\01_KAVACH_Platform\frontend\index.html"

with open(target_path, "r", encoding="utf-8") as f:
    content = f.read()

target = '<button type="button" id="eli5-academic-btn"'
btn_html = """<!-- Master System Implementation & Execution Flowchart Button -->
      <button type="button" id="kavach-implementation-btn" class="implementation-trigger-button" onclick="openImplementationModal('journey')" title="End-to-End System Implementation, Step-by-Step Execution Journey & Complete Architecture Flowchart">
        <div class="impl-btn-content">
          <div class="impl-btn-left">
            <div class="impl-icon-box">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="7" height="7"></rect>
                <rect x="14" y="3" width="7" height="7"></rect>
                <rect x="14" y="14" width="7" height="7"></rect>
                <rect x="3" y="14" width="7" height="7"></rect>
                <path d="M10 6.5h4M17.5 10v4M14 17.5h-4M6.5 14v-4"></path>
              </svg>
            </div>
            <div class="impl-text-group">
              <div class="impl-title-row">
                <span class="impl-main-title">Implementation &middot; Master Architecture Flowchart &amp; Execution Journey</span>
                <span class="badge" style="background:#ECFDF5;color:#047857;border:1px solid #A7F3D0;font-size:0.7rem;font-weight:700;padding:2px 8px;border-radius:9999px;">LIVE WORKING SYSTEM</span>
              </div>
              <span class="impl-subtitle">Step-by-Step Flow: Humne Ye Kiya &rarr; Fir Ye Hua &rarr; Fir Ye Hua &middot; Interactive Flowchart &middot; Code Grounding &middot; All Syllabus Topics</span>
            </div>
          </div>
          <div class="impl-btn-action">
            <span class="impl-action-label">Explore Flowchart</span>
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          </div>
        </div>
      </button>

      """

if target in content and "kavach-implementation-btn" not in content:
    content = content.replace(target, btn_html + target, 1)
    print("Inserted implementation button successfully!")
else:
    print("Implementation button already exists or target missing")

target_float = '<button type="button" id="floating-eli5-launcher"'
float_html = """<button type="button" id="floating-impl-launcher" class="floating-impl-btn" onclick="openImplementationModal('journey')" aria-label="Open System Implementation Flowchart" title="System Implementation: Architecture Flowchart & Execution Walkthrough">
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
    <span>Implementation Flow</span>
  </button>

  """
if target_float in content and "floating-impl-launcher" not in content:
    content = content.replace(target_float, float_html + target_float, 1)
    print("Inserted floating button successfully!")

target_script = '<script src="gov_rules_codex.js?v=3.2.0"></script>'
script_html = '<script src="gov_rules_codex.js?v=3.2.0"></script>\n<script src="implementation_flow.js?v=3.2.0"></script>'
if target_script in content and "implementation_flow.js" not in content:
    content = content.replace(target_script, script_html, 1)
    print("Inserted script tag successfully!")

with open(target_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Finished updating index.html")

