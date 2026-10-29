import os

root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for name in ["app.js", "script.js"]:
    fn = os.path.join(root, "01_KAVACH_Platform", "frontend", name)
    with open(fn, "r", encoding="utf-8") as f:
        c = f.read()

    # Normalize line breaks
    c = c.replace("\r\n", "\n")
    target = "if (canvas) canvas.remove();\n}\n\n  requestAnimationFrame(renderParticles);\n}"
    replacement = "if (canvas) canvas.remove();\n}"
    if target in c:
        c = c.replace(target, replacement)
        print(f"Fixed {name}")
    else:
        print(f"Target not found in {name}")

    with open(fn, "w", encoding="utf-8") as f:
        f.write(c)

