def normalize_path(path: str) -> str:
    path = path.replace("\\", "/")
    if path.startswith("app/"):
        path = path[len("app/"):]
    path = path.lstrip("./")
    return path.lower()

paths = [
    "security/detector.py",
    "app/security/detector.py",
    "agent\\orchestrator.py",
    "app\\agent\\orchestrator.py"
]
normalized = [normalize_path(p) for p in paths]
print(f"Original: {paths}")
print(f"Normalized: {normalized}")
