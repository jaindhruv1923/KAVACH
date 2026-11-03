import os

console_path = r"C:\Users\jaind\OneDrive\Desktop\project_work\agentic_ai_midsem_work\KAVACH-main\01_KAVACH_Platform\frontend\console.html"

with open(console_path, "r", encoding="utf-8") as f:
    content = f.read()

target_chat = '<button type="button" id="chatbot-launcher"'
floating_btn = """<button type="button" id="floating-impl-launcher" class="floating-impl-btn" onclick="openImplementationModal('journey')" aria-label="Open System Implementation Flowchart" title="System Implementation: Architecture Flowchart & Execution Walkthrough">
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
    <span>Implementation Flow</span>
  </button>
  """
if target_chat in content and "floating-impl-launcher" not in content:
    content = content.replace(target_chat, floating_btn + target_chat, 1)
    print("Added floating button to console.html")

target_script = '<script src="app.js?v=3.2.0"></script>'
script_tag = '<script src="app.js?v=3.2.0"></script>\n<script src="implementation_flow.js?v=3.2.0"></script>'
if target_script in content and "implementation_flow.js" not in content:
    content = content.replace(target_script, script_tag, 1)
    print("Added script tag to console.html")

with open(console_path, "w", encoding="utf-8") as f:
    f.write(content)

print("console.html update complete!")

