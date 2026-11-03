path = r"c:\Users\jaind\OneDrive\Desktop\project_work\agentic_ai_midsem_work\KAVACH-main\scripts\build_teacher_flowchart_system.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace Hinglish in headings
text = text.replace('1. Ingress Action ("Humne Ye Kiya")', '1. Ingress Action (Payload Ingested)')
text = text.replace('2. System Execution ("Fir Ye Hua")', '2. System Execution (Pipeline Process)')
text = text.replace('3. Decision Verdict ("Ye Result Aya")', '3. Decision Verdict (Gate Outcome)')
text = text.replace('4. Theoretical Grounding ("Kyu Hua")', '4. Theoretical Grounding (Academic Proof)')
text = text.replace("<!-- Teacher's Causal Commentary Board (Humne Ye Kiya -> Fir Ye Hua -> Ye Result Aya) -->", "<!-- Teacher's Causal Commentary Board (Ingress -> Execution -> Verdict -> Proof) -->")

# Rename .flowchart-controls-bar to .impl-player-controls-bar to prevent style.css sticky collision
text = text.replace(".flowchart-controls-bar {", """.impl-player-controls-bar {
        position: static !important;
        top: auto !important;
        z-index: 1 !important;""")
text = text.replace('<div class="flowchart-controls-bar">', '<div class="impl-player-controls-bar">')

# Rename .flowchart-diagram-grid to .impl-diagram-grid
text = text.replace(".flowchart-diagram-grid {", """.impl-diagram-grid {
        margin-bottom: 16px;""")
text = text.replace('<div class="flowchart-diagram-grid">', '<div class="impl-diagram-grid">')

# Ensure flow-node-card does not clip bottom
text = text.replace("min-height: 140px;", """min-height: 150px;
        box-sizing: border-box;""")

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("build_teacher_flowchart_system.py updated cleanly")

