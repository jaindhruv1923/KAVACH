import re

with open("README.md", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Broken paths
text = text.replace("important/kavach/artifacts/screenshots/", "01_KAVACH_Platform/artifacts/screenshots/")
text = text.replace("important/kavach/tests", "01_KAVACH_Platform/tests/test_kavach_100_suite.py")
text = text.replace("important/02_Official_Reports_and_Synopses/", "03_Documentation/02_Official_Reports_and_Synopses/")
text = text.replace("important/kavach/", "01_KAVACH_Platform/")

# 2. Badges & 9.6/10 removal
text = text.replace("badge/Tests-278%2F278%20Passing-00E599", "badge/Tests-300%2F300%20Passing-00E599")
text = text.replace("badge/CSE3101%20Agentic%20AI-9.6%2F10-F59E0B", "badge/CSE3101%20Agentic%20AI-Audited%20%26%20Verified-009688")
text = text.replace("* **Evaluation Score:** **9.6 / 10** across Rubric Criteria C1 to C5", "* **Verification Status:** **100% Deterministic Test Pass (300/300)** & **94.3% F1 on Held-Out V2 Corpus**")

# 3. Add Single Source of Truth link to header nav
old_nav = '<a href="01_KAVACH_Platform/RUNNING_KAVACH.md"><b>⚡ Running Kavach</b></a>'
new_nav = '<a href="01_KAVACH_Platform/RUNNING_KAVACH.md"><b>⚡ Running Kavach</b></a> &nbsp;•&nbsp;\n  <a href="docs/METRICS.md"><b>📈 System Metrics (SSOT)</b></a>'
text = text.replace(old_nav, new_nav)

# 4. TOC Endpoints count update
text = text.replace("REST API Reference (10 Endpoints)", "REST API Reference (120 Core / 142 Total Endpoints)")

# 5. Automated Verification & 278 Passing Tests
text = text.replace("Automated Verification & 278 Passing Tests", "Automated Verification & 300 Master Verification Tests (641 Total)")
text = text.replace("Automated Verification & 278 Tests", "Automated Verification & 300 Master Tests")
text = text.replace("278 tests", "300 deterministic verification tests (641 total repository tests)")
text = text.replace("278 Tests", "300 Deterministic Tests (641 Total)")

# 6. Add caveat to 100% interception claims
text = text.replace(
    "achieving a **100.0% Interception Rate**.",
    "achieving a **100.0% Interception Rate** across 19 vectors in the authored red-team benchmark (see [`docs/METRICS.md`](docs/METRICS.md) for full benchmark logs)."
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(text)

print("README.md updated successfully.")
