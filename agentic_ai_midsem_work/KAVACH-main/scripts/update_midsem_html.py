import os

midsem_path = r"C:\Users\jaind\OneDrive\Desktop\project_work\agentic_ai_midsem_work\KAVACH-main\01_KAVACH_Platform\frontend\midsem.html"

with open(midsem_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add button to nav-actions
target_nav = '<button type="button" class="btn-serious magnetic-btn" onclick="window.openProfessorReviewModal()"'
nav_btn = """<button type="button" class="btn-serious magnetic-btn" onclick="window.openImplementationModal('journey')" style="text-decoration:none; display:inline-flex; align-items:center; gap:5px; background:linear-gradient(135deg, #065F46 0%, #047857 100%); color:#6EE7B7; font-weight:700; border:1px solid #059669; box-shadow:0 0 16px rgba(5,150,105,0.35); cursor:pointer;" title="End-to-End System Implementation, Step-by-Step Execution Journey & Complete Architecture Flowchart">
      ⚡ Implementation Flow
    </button>
    """
if target_nav in content and "openImplementationModal" not in content:
    content = content.replace(target_nav, nav_btn + target_nav, 1)
    print("Added nav button to midsem.html")

# Add floating button before chatbot launcher
target_chat = '<button type="button" id="chatbot-launcher"'
floating_btn = """<button type="button" id="floating-impl-launcher" class="floating-impl-btn" onclick="openImplementationModal('journey')" aria-label="Open System Implementation Flowchart" title="System Implementation: Architecture Flowchart & Execution Walkthrough">
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
    <span>Implementation Flow</span>
  </button>
  """
if target_chat in content and "floating-impl-launcher" not in content:
    content = content.replace(target_chat, floating_btn + target_chat, 1)
    print("Added floating button to midsem.html")

# Add script tag
target_script = '<script src="improvised_controller.js?v=3.2.0"></script>'
script_tag = '<script src="improvised_controller.js?v=3.2.0"></script>\n<script src="implementation_flow.js?v=3.2.0"></script>'
if target_script in content and "implementation_flow.js" not in content:
    content = content.replace(target_script, script_tag, 1)
    print("Added script tag to midsem.html")

with open(midsem_path, "w", encoding="utf-8") as f:
    f.write(content)

print("midsem.html update completed successfully!")

