import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter(prefix="/api/ide", tags=["IDE Live Code Management"])

# Base repository roots
WORKSPACE_ROOT = Path(r"C:\Users\jaind\OneDrive\Desktop\uni\Ageentic&PRJ-IV").resolve()
MIDSEM_ROOT = (WORKSPACE_ROOT / "agentic ai mid sem").resolve()
PRJ4_ROOT = (WORKSPACE_ROOT / "PRJ-IV &AgenticAi Final Work").resolve()

ALLOWED_ROOTS = [WORKSPACE_ROOT, MIDSEM_ROOT, PRJ4_ROOT]
IGNORED_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules", ".venv", "venv", ".idea", ".vscode", "temp"}
ALLOWED_EXTS = {".py", ".js", ".html", ".css", ".json", ".md", ".bat", ".ps1", ".yml", ".yaml", ".txt", ".sh", ".sql"}

def resolve_target_path(req_path: str) -> Optional[Path]:
    """Safely resolves requested file path inside workspace boundaries."""
    if not req_path:
        return None
    
    clean_path = req_path.strip().replace("/", os.sep).replace("\\", os.sep)
    target = Path(clean_path)
    
    # 1. Direct check if absolute
    if target.is_absolute():
        try:
            resolved = target.resolve()
            if WORKSPACE_ROOT in resolved.parents or resolved == WORKSPACE_ROOT:
                if resolved.is_file():
                    return resolved
        except Exception:
            pass

    # 2. Check candidate relative paths
    candidates = [
        (WORKSPACE_ROOT / clean_path).resolve(),
        (PRJ4_ROOT / clean_path).resolve(),
        (MIDSEM_ROOT / clean_path).resolve(),
        (PRJ4_ROOT / "imp_files" / clean_path).resolve(),
        (MIDSEM_ROOT / "imp_files" / clean_path).resolve(),
        (PRJ4_ROOT / "kavach_platform" / clean_path).resolve(),
        (MIDSEM_ROOT / "kavach_platform" / clean_path).resolve(),
    ]

    for cand in candidates:
        try:
            if cand.is_file() and (WORKSPACE_ROOT in cand.parents or cand == WORKSPACE_ROOT):
                return cand
        except Exception:
            continue

    # 3. Fallback: Search by basename
    filename = Path(clean_path).name
    for root in [PRJ4_ROOT, MIDSEM_ROOT, WORKSPACE_ROOT]:
        if root.exists():
            for match in root.rglob(filename):
                try:
                    if match.is_file() and not any(part in match.parts for part in IGNORED_DIRS):
                        return match.resolve()
                except Exception:
                    continue

    return None

class SaveFileRequest(BaseModel):
    path: str
    content: str

@router.get("/file")
def get_live_file(path: str = Query(..., description="Relative or absolute path of file")):
    """Read actual live code from disk."""
    resolved = resolve_target_path(path)
    if not resolved or not resolved.is_file():
        raise HTTPException(status_code=404, detail=f"File not found on disk: {path}")

    try:
        try:
            with open(resolved, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(resolved, "r", encoding="latin-1") as f:
                content = f.read()

        total_lines = len(content.splitlines())
        size_bytes = len(content.encode("utf-8"))
        
        try:
            rel_display = str(resolved.relative_to(WORKSPACE_ROOT)).replace("\\", "/")
        except ValueError:
            rel_display = resolved.name

        ext = resolved.suffix.lower()
        lang_map = {
            ".py": "python",
            ".js": "javascript",
            ".html": "html",
            ".css": "css",
            ".json": "json",
            ".md": "markdown",
            ".bat": "bat",
            ".ps1": "powershell",
            ".yml": "yaml",
            ".yaml": "yaml"
        }

        return {
            "success": True,
            "path": str(resolved),
            "rel_path": rel_display,
            "filename": resolved.name,
            "language": lang_map.get(ext, "plaintext"),
            "total_lines": total_lines,
            "size_bytes": size_bytes,
            "content": content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read file: {str(e)}")

@router.post("/save")
def save_live_file(req: SaveFileRequest):
    """Save edited code directly back to the physical disk file."""
    resolved = resolve_target_path(req.path)
    if not resolved:
        clean_path = req.path.strip().replace("/", os.sep).replace("\\", os.sep)
        candidate = (WORKSPACE_ROOT / clean_path).resolve()
        try:
            if WORKSPACE_ROOT in candidate.parents:
                resolved = candidate
                resolved.parent.mkdir(parents=True, exist_ok=True)
            else:
                raise HTTPException(status_code=400, detail="Cannot create files outside workspace root.")
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid target path.")

    try:
        if WORKSPACE_ROOT not in resolved.parents and resolved != WORKSPACE_ROOT:
            raise HTTPException(status_code=403, detail="Security violation: Target is outside workspace boundaries.")
    except Exception:
        raise HTTPException(status_code=403, detail="Security violation.")

    try:
        with open(resolved, "w", encoding="utf-8") as f:
            f.write(req.content)

        total_lines = len(req.content.splitlines())
        size_bytes = len(req.content.encode("utf-8"))

        return {
            "success": True,
            "message": f"Saved {resolved.name} to disk successfully!",
            "path": str(resolved),
            "filename": resolved.name,
            "total_lines": total_lines,
            "size_bytes": size_bytes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

def scan_real_directory(dir_path: Path, max_depth: int = 4, current_depth: int = 0) -> List[Dict[str, Any]]:
    """Recursively scans the real directory tree for live interactive navigation."""
    if current_depth > max_depth or not dir_path.exists():
        return []
    
    entries = []
    try:
        items = sorted(list(dir_path.iterdir()), key=lambda x: (not x.is_dir(), x.name.lower()))
    except Exception:
        return []

    for item in items:
        if item.name.startswith(".") and item.name not in {".github"}:
            continue
        if item.name in IGNORED_DIRS:
            continue
            
        try:
            rel = str(item.relative_to(WORKSPACE_ROOT)).replace("\\", "/")
        except ValueError:
            rel = item.name

        if item.is_dir():
            sub = scan_real_directory(item, max_depth, current_depth + 1)
            if sub:
                entries.append({
                    "name": item.name,
                    "type": "folder",
                    "path": rel,
                    "open": current_depth < 1 or item.name in {"imp_files", "01_Google_ADK", "02_CrewAI", "03_Guardrails_And_Security", "04_Agentic_Design_Patterns", "bharat_core_banking"},
                    "children": sub
                })
        elif item.is_file():
            if item.suffix.lower() in ALLOWED_EXTS:
                size_kb = round(os.path.getsize(item) / 1024, 1)
                badge = "PY" if item.suffix == ".py" else item.suffix[1:].upper()
                entries.append({
                    "name": item.name,
                    "type": "file",
                    "path": rel,
                    "badge": badge,
                    "size_kb": size_kb
                })
    return entries

@router.get("/tree")
def get_live_project_tree():
    """Return an active navigable tree of all real files across the entire workspace."""
    tree = scan_real_directory(WORKSPACE_ROOT, max_depth=4)
    return {"success": True, "tree": tree}
