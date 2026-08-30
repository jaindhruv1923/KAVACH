import os
import glob

print("Current directory:", os.getcwd())
phases = [
    "Phase1_RAG_Foundation",
    "Phase2_AgentOrchestrator",
    "Phase3_EvidenceGroundedGeneration",
    "Phase4_SecurityEngineHardening",
    "Phase5_ChangeImpactAnalysis"
]

found = []
for phase in phases:
    exists = os.path.isdir(phase)
    print(f"Phase folder '{phase}' exists: {exists}")
    if exists:
        pattern = os.path.join(phase, "**", "test_*.py")
        files = glob.glob(pattern, recursive=True)
        print(f"  Pattern '{pattern}' found: {len(files)} files")
        for f in files:
            found.append((phase, f))

with open("discovered_tests.txt", "w", encoding="utf-8") as f_out:
    f_out.write(f"CWD: {os.getcwd()}\n")
    for phase, f in found:
        f_out.write(f"{phase} -> {f}\n")

print(f"Total found: {len(found)}")

