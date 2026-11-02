"""Explicit opt-in OpenAI Codex-only synthetic vision research connector.

This Codex model is intended for code, NOT clinically validated.
NEVER use on patient images or medical screening.
"""
from __future__ import annotations
import base64
import hashlib
import json
import os
from pathlib import Path
import urllib.request

CODEX_MODEL = "gpt-5.3-codex"
OPENAI_API = "https://api.openai.com/v1/responses"
DEMO_FIXTURE = Path(__file__).resolve().parents[2] / "examples/fixtures/synthetic_shape.png"
DEMO_MANIFEST = Path(__file__).resolve().parents[2] / "examples/fixtures/manifest.json"
DEMO_SHA256 = "aa52d439aab3e49afe8d58452db21e4d1922495255ad32eb720e6352ffff163d"

class UnsafeInput(ValueError):
    pass

def check_synthetic_fixture(image_path: str | Path, manifest_path: str | Path) -> bytes:
    image = Path(image_path).resolve(strict=True)
    manifest_file = Path(manifest_path).resolve(strict=True)
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    if image != DEMO_FIXTURE.resolve(strict=True) or manifest_file != DEMO_MANIFEST.resolve(strict=True):
        raise UnsafeInput("only the built-in synthetic demo fixture is authorized")
    if image.parent != manifest_file.parent:
        raise UnsafeInput("fixture must be alongside manifest")
    if image.name != manifest.get("filename"):
        raise UnsafeInput("filename not allowlisted in fixture manifest")
    if manifest.get("synthetic") is not True or manifest.get("approved_for_remote_demo") is not True:
        raise UnsafeInput("only explicitly approved synthetic demonstration images allowed")
    if manifest.get("license") != "CC0-1.0":
        raise UnsafeInput("fixture must declare its redistribution license")
    if image.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
        raise UnsafeInput("unsupported fixture file type")
    raw = image.read_bytes()
    if len(raw) > 5_000_000:
        raise UnsafeInput("fixture too large")
    if hashlib.sha256(raw).hexdigest() != manifest.get("sha256") or hashlib.sha256(raw).hexdigest() != DEMO_SHA256:
        raise UnsafeInput("synthetic file checksum mismatch")
    return raw

def _parse_output(response: dict) -> str:
    parts = []
    for item in response.get("output", []):
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                parts.append(content.get("text", ""))
    return "\n".join(parts) if parts else "No textual observation returned"

def codex_synthetic_observe(image_path: str, manifest_path: str, *, allow_api: bool = False) -> dict:
    if not allow_api:
        raise UnsafeInput("add --allow-api to explicitly authorize an external API call")
    raw = check_synthetic_fixture(image_path, manifest_path)
    token = os.environ.get("OPENAI_API_KEY", "")
    if not token:
        raise UnsafeInput("OPENAI_API_KEY required; never commit secrets")
    suffix = Path(image_path).suffix.lower()
    mime = "image/png" if suffix == ".png" else ("image/webp" if suffix == ".webp" else "image/jpeg")
    data_url = "data:" + mime + ";base64," + base64.b64encode(raw).decode("ascii")
    request_data = {
        "model": CODEX_MODEL,
        "store": False,
        "max_output_tokens": 300,
        "input": [{"role": "user", "content": [
            {"type": "input_text", "text": (
                "This is a deliberately artificial, synthetic non-patient diagram for a software test. "
                "Describe only obvious visual attributes (color, shape, pattern) in plain language. "
                "Do not infer or suggest a medical condition, cancer risk, treatment, urgency, or rule-out. "
                "Say the image is artificial and that this is not a medical interpretation."
            )},
            {"type": "input_image", "image_url": data_url, "detail": "low"},
        ]}],
    }
    body = json.dumps(request_data).encode("utf-8")
    req = urllib.request.Request(OPENAI_API, data=body, headers={
        "Authorization": f"Bearer {token}", "Content-Type": "application/json"
    }, method="POST")
    with urllib.request.urlopen(req, timeout=30) as reply:
        result = json.loads(reply.read(2_000_000))
    return {"model": CODEX_MODEL, "observation": _parse_output(result),
            "research_only": True, "synthetic_input": True, "clinical_validation": "none"}
