#!/usr/bin/env python
"""
Run pytest suite for CSE3101 Agentic AI Mid-Sem Project Evaluation.
Faculty: Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari
"""
import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND = ROOT / "backend"
TESTS = ROOT / "tests"

env = os.environ.copy()
env["PYTHONPATH"] = str(BACKEND)

print("=" * 70)
print(" CSE3101 AGENTIC AI — MID-SEM AUTOMATED VERIFICATION SUITE")
print(" Faculty: Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari")
print("=" * 70)

# Auto-detect virtual environment Python
venv_py = ROOT.parent / ".venv" / "Scripts" / "python.exe"
py_bin = str(venv_py) if venv_py.exists() else sys.executable

cmd = [py_bin, "-m", "pytest", str(TESTS), "-v", "--tb=short"] + sys.argv[1:]
result = subprocess.run(cmd, cwd=str(ROOT), env=env)
sys.exit(result.returncode)
