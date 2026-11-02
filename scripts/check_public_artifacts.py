"""Simple public-release fail-closed file checks; not a comprehensive DLP scanner."""
from __future__ import annotations
import pathlib
import re
import sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
FORBIDDEN_PARTS = {"private", "patients", "patient-data", "clinical-uploads", "uploads", "secrets", ".env"}
FORBIDDEN_EXT = {".dcm", ".dicom", ".nii", ".xlsx", ".csv", ".sqlite", ".db", ".p12", ".pem"}
SECRET_REGEX = re.compile(r"\b(sk-[A-Za-z0-9_-]{12,}|org-[A-Za-z0-9]{12,})\b")
errors = []
for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts or ".egg-info" in str(path):
        continue
    rel = path.relative_to(ROOT)
    if any(part.lower() in FORBIDDEN_PARTS for part in rel.parts) and rel.name != ".env.example":
        errors.append(f"disallowed path: {rel}")
    if path.suffix.lower() in FORBIDDEN_EXT:
        errors.append(f"disallowed file type: {rel}")
    if path.stat().st_size > 5_000_000:
        errors.append(f"oversized file: {rel}")
    if path.suffix.lower() in {".py", ".md", ".json", ".yml", ".yaml", ".txt", ".sh", ".js", ".mjs"}:
        if SECRET_REGEX.search(path.read_text(encoding="utf-8")):
            errors.append(f"secret-like token found in: {rel}")
if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print("Public artifact checks passed (NOT a full privacy audit).")
