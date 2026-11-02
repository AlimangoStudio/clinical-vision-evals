"""Load provenance-tagged synthetic example references (no patient data)."""
from __future__ import annotations
import json
from pathlib import Path

VERSION = "0.1.0"
ALLOWED_FLAGS = {"elevated", "decreased", "within_reference", "not_reported"}

class LibraryError(ValueError):
    """A reference entry or query is malformed or unsafe to ingest."""

def _require_text(value: object, key: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LibraryError(f"{key} must be nonempty text")
    return value.strip()

def _tags(value: object, key: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise LibraryError(f"{key} must be a list of nonempty strings")
    if len(value) > 50:
        raise LibraryError(f"{key} is too long")
    return [item.strip().lower() for item in value]

def _lab_tags(value: object) -> list[str]:
    if not isinstance(value, list):
        raise LibraryError("lab_flags must be a list")
    result = []
    for item in value:
        if not isinstance(item, dict):
            raise LibraryError("lab_flags entries must be objects")
        name = _require_text(item.get("name"), "lab_flags.name").lower()
        flag = item.get("flag")
        if flag not in ALLOWED_FLAGS:
            raise LibraryError(f"lab_flags.flag must be one of {sorted(ALLOWED_FLAGS)}")
        result.append(f"{name}:{flag}")
    return result

def validate_reference(data: dict) -> dict:
    if not isinstance(data, dict):
        raise LibraryError("reference must be an object")
    if data.get("schema_version") != VERSION:
        raise LibraryError("unsupported schema_version")
    for key in ("case_id", "pattern_label", "limitations", "source_url", "source_title"):
        _require_text(data.get(key), key)
    if data.get("origin") != "synthetic":
        raise LibraryError("v0.1 public library accepts synthetic examples only")
    if data.get("review_status") != "illustrative_unvalidated":
        raise LibraryError("fixtures must be marked illustrative_unvalidated")
    if data.get("license") != "CC0-1.0":
        raise LibraryError("only explicitly CC0-licensed synthetic examples accepted")
    if not data["source_url"].startswith("https://"):
        raise LibraryError("source_url must be HTTPS")
    if data.get("image_paths") != []:
        raise LibraryError("reference cases may not carry patient or image paths in v0.1")
    _tags(data.get("features"), "features")
    _lab_tags(data.get("lab_flags", []))
    if not isinstance(data.get("context_notes", []), list):
        raise LibraryError("context_notes must be a list")
    return data

def validate_query(data: dict) -> dict:
    if not isinstance(data, dict) or data.get("schema_version") != VERSION:
        raise LibraryError("query requires schema_version 0.1.0")
    if data.get("synthetic") is not True:
        raise LibraryError("public demonstration CLI accepts synthetic queries only")
    if any(key in data for key in ("patient_id", "patient_name", "birthdate", "address", "phone", "email")):
        raise LibraryError("possible patient identifiers are disallowed")
    _tags(data.get("observed_features"), "observed_features")
    _lab_tags(data.get("lab_flags", []))
    _tags(data.get("attention_flags", []), "attention_flags")
    return data

def load_references(directory: str | Path) -> list[dict]:
    path = Path(directory)
    if not path.is_dir():
        raise LibraryError("reference directory does not exist")
    refs = []
    seen = set()
    for file in sorted(path.glob("*.json")):
        ref = validate_reference(json.loads(file.read_text(encoding="utf-8")))
        if ref["case_id"] in seen:
            raise LibraryError("duplicate case_id")
        seen.add(ref["case_id"])
        refs.append(ref)
    if not refs:
        raise LibraryError("reference library is empty")
    return refs

def load_query(file: str | Path) -> dict:
    return validate_query(json.loads(Path(file).read_text(encoding="utf-8")))
