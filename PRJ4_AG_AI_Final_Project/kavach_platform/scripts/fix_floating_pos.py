"""
Fix two issues:
1. Swap floating-impl-launcher to appear BELOW floating-eli5-launcher (visually above it on screen since flex-column)
   so the order top-to-bottom in DOM is: Implementation → ELI5 → Ask AI
   (which means on the bottom-right dock: Implementation Flow sits above ELI5 above Ask AI)
2. The HTML already has Implementation above ELI5, so the actual visual problem is the CSS positioning.
   The floating-impl-btn needs bottom offset to be higher than floating-eli5-btn.
   
Looking at screenshot 2: Implementation Flow is BELOW ELI5. That means the DOM order has ELI5 first.
But from the HTML we see Implementation is FIRST (line 5365) then ELI5 (line 5370).
The flexbox column with align-items:flex-end stacks top-to-bottom.
Since items are fixed positioned separately (not in the flex container actually),
we need to fix the bottom CSS values.

Actually the floating buttons are positioned with position:fixed in the CSS.
The floating-impl-btn has bottom:24px and right:170px.
The floating-eli5-btn likely has a different bottom value.

We just need to ensure Implementation Flow button has a HIGHER bottom value than ELI5.
Let's fix the CSS in implementation_flow.js.
"""

import re

path = r"C:\Users\jaind\OneDrive\Desktop\project_work\agentic_ai_midsem_work\KAVACH-main\01_KAVACH_Platform\frontend\implementation_flow.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix the floating button CSS: needs to be positioned ABOVE the ELI5 button
# ELI5 button has bottom:24px, Implementation should be higher = larger bottom value
# Also fix right value to align properly
old_css = """.floating-impl-btn {
        position: fixed;
        bottom: 24px;
        right: 170px;
        z-index: 9999;"""

new_css = """.floating-impl-btn {
        position: fixed;
        bottom: 72px;
        right: 138px;
        z-index: 9999;"""

if old_css in content:
    content = content.replace(old_css, new_css)
    print("Fixed floating button CSS position (bottom:72px to sit above ELI5).")
else:
    print("WARNING: old_css pattern not found - checking actual value...")
    # Find the floating-impl-btn CSS block
    idx = content.find(".floating-impl-btn {")
    if idx >= 0:
        print(f"Found .floating-impl-btn at char {idx}")
        print(repr(content[idx:idx+200]))
    else:
        print("Not found at all!")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done.")

