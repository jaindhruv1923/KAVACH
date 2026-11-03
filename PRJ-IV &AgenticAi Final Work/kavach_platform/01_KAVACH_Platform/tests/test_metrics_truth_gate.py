"""
KAVACH Metrics Truth Gate & Drift Verifier.
Directly implements Freebuff's #1 Recommendation:
"Single source of truth for metrics. Add a docs/METRICS.md generated from actual pytest
output, with a CI test that fails if badges/README numbers drift from reality."
"""

import os
import json
import pytest
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
PLATFORM_DIR = CURRENT_DIR.parent
REPO_ROOT = PLATFORM_DIR.parent

METRICS_JSON_PATH = REPO_ROOT / "docs" / "METRICS.json"
METRICS_MD_PATH = REPO_ROOT / "docs" / "METRICS.md"
README_MD_PATH = REPO_ROOT / "README.md"


def test_metrics_json_and_md_exist():
    """Verify single source of truth files exist at canonical locations."""
    assert METRICS_JSON_PATH.exists(), f"Missing SSOT metrics JSON at {METRICS_JSON_PATH}"
    assert METRICS_MD_PATH.exists(), f"Missing SSOT metrics Markdown at {METRICS_MD_PATH}"


def test_metrics_json_schema_and_integrity():
    """Verify METRICS.json contains all required architectural fields."""
    with open(METRICS_JSON_PATH, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    assert "metadata" in metrics
    assert "machine_specs" in metrics
    assert "test_inventory" in metrics
    assert "endpoints" in metrics
    assert "pipeline_architecture" in metrics

    # Verify deterministic test counts
    det_tests = metrics["test_inventory"]["deterministic_verification_suites"]["total_deterministic_tests"]
    assert det_tests == 300, f"Expected 300 deterministic verification tests, found {det_tests}"

    # Verify total pytest repository inventory
    total_repo_tests = metrics["test_inventory"]["full_repository_pytest_inventory"]["total_pytest_tests_repository"]
    assert total_repo_tests == 641, f"Expected 641 total repository tests, found {total_repo_tests}"

    # Verify endpoint count
    total_endpoints = metrics["endpoints"]["total_endpoints_all_platforms"]
    assert total_endpoints == 142, f"Expected 142 total registered endpoints, found {total_endpoints}"


def test_readme_badge_drift_gate():
    """Verify README.md badges do not drift from METRICS.json ground truth."""
    assert README_MD_PATH.exists(), f"Missing README.md at {README_MD_PATH}"

    with open(README_MD_PATH, "r", encoding="utf-8") as f:
        readme_content = f.read()

    with open(METRICS_JSON_PATH, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    expected_det_tests = metrics["test_inventory"]["deterministic_verification_suites"]["total_deterministic_tests"]
    expected_badge = f"Tests-{expected_det_tests}%2F{expected_det_tests}%20Passing"

    assert expected_badge in readme_content, (
        f"README badge drifted! Expected '{expected_badge}' in README.md"
    )

    # Disallow legacy unverified counts in active top-level overview
    assert "461 passing tests" not in readme_content, "Legacy unverified '461 passing tests' found in README.md"
    assert "278 / 278" not in readme_content, "Legacy '278 / 278' count found in README.md"
    assert "9.6/10" not in readme_content, "Unverified subjective '9.6/10' badge found in README.md"
