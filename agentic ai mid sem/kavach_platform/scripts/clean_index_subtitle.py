path = r"C:\Users\jaind\OneDrive\Desktop\project_work\agentic_ai_midsem_work\KAVACH-main\01_KAVACH_Platform\frontend\index.html"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_subtitle = '<span class="impl-subtitle">Step-by-Step Flow: Humne Ye Kiya &rarr; Fir Ye Hua &rarr; Fir Ye Hua &middot; Interactive Flowchart &middot; Code Grounding &middot; All Syllabus Topics</span>'
new_subtitle = '<span class="impl-subtitle">End-to-End Autonomous Pipeline &middot; 10 Sequential Stages &middot; Deterministic Gate &middot; Bounded ReAct &middot; SAGA Escrow &middot; Merkle Non-Repudiation</span>'

if old_subtitle in content:
    content = content.replace(old_subtitle, new_subtitle)
    print("Replaced subtitle in index.html with English.")
else:
    print("Old subtitle not found in index.html.")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

