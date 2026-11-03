"""
Test Suite for Multimodal Vision & Image Inspection (Module 7).
Tests byte decoding, PIL metadata parsing, visual entropy calculations, and security auditing.
"""

import io
import base64
import pytest
from PIL import Image, PngImagePlugin

from app.security.multimodal_vision import global_vision_auditor, MultimodalVisionAuditor
from app.agent.tools import TOOLS_REGISTRY, multimodal_inspect_image


def create_test_png(width: int = 100, height: int = 100, metadata_dict: dict = None) -> bytes:
    """Helper to generate a clean in-memory PNG with optional metadata chunks."""
    img = Image.new("RGB", (width, height), color=(73, 109, 137))
    buf = io.BytesIO()
    png_info = PngImagePlugin.PngInfo()
    if metadata_dict:
        for k, v in metadata_dict.items():
            png_info.add_text(k, str(v))
    img.save(buf, format="PNG", pnginfo=png_info)
    return buf.getvalue()


def test_clean_image_decoding_and_entropy():
    raw_png = create_test_png(120, 80, {"title": "Architecture Overview", "version": "1.0"})
    b64_str = base64.b64encode(raw_png).decode("utf-8")

    auditor = MultimodalVisionAuditor()
    res = auditor.audit_diagram_or_image(
        image_identifier="test_clean.png",
        diagram_description="Clean microservices diagram behind TLS gateway",
        base64_data=b64_str
    )

    assert res["security_verdict"] == "PASSED"
    assert res["findings_count"] == 0
    meta = res["image_metadata"]
    assert meta["is_valid_image"] is True
    assert meta["format"] == "PNG"
    assert meta["width"] == 120
    assert meta["height"] == 80
    assert meta["channels"] == 3
    assert meta["byte_size"] > 0
    assert "title" in meta["extracted_metadata_keys"]


def test_visual_credential_exposure_detection():
    # PNG with embedded secret in chunk
    raw_png = create_test_png(64, 64, {"comment": "AWS_SECRET_ACCESS_KEY=AKIA1234567890EXAMPLE"})
    b64_str = base64.b64encode(raw_png).decode("utf-8")

    auditor = MultimodalVisionAuditor()
    res = auditor.audit_diagram_or_image(
        image_identifier="compromised_diagram.png",
        diagram_description="Topology showing direct database connection",
        base64_data=b64_str
    )

    assert res["security_verdict"] == "FAILED"
    assert res["findings_count"] >= 1
    threat_names = [f["threat"] for f in res["findings"]]
    assert any("Credential Exposure" in t for t in threat_names)
    assert res["architectural_risk_score"] > 0.0


def test_multimodal_unencrypted_threat():
    auditor = MultimodalVisionAuditor()
    res = auditor.audit_diagram_or_image(
        image_identifier="insecure_edge.png",
        diagram_description="Frontend communicates over http://api.internal without encryption"
    )

    assert res["security_verdict"] == "FAILED"
    severities = [f["severity"] for f in res["findings"]]
    assert "HIGH" in severities


def test_multimodal_registered_tool():
    raw_png = create_test_png(50, 50)
    b64_str = base64.b64encode(raw_png).decode("utf-8")

    tool_func = TOOLS_REGISTRY["multimodal_inspect_image"]
    res = tool_func(
        image_path="",
        base64_data=b64_str,
        description="Payment gateway topology ingress"
    )

    assert res["success"] is True
    assert res["modality"] == "Vision / Image"
    assert res["image_metadata"]["width"] == 50
