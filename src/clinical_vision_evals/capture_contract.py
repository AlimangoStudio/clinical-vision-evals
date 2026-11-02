"""Reusable synthetic capture-set validation, adapted from PAPPS capture-first patterns.

No patient identifiers, clinic procedures, storage locations, or backend routes are used.
This validates metadata only; it cannot judge clinical image quality.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence


class CaptureContractError(ValueError):
    """The supplied synthetic capture set is incomplete or inconsistent."""


def validate_capture_set(*, case_key: str, required_views: Sequence[str], captures: Sequence[Mapping]) -> dict:
    """Require one unique, saved, consent-marked capture per prescribed view, in order.

    Mirrors a *generic invariant* used by PAPPS; this is a separate Python
    implementation. case_key is a synthetic grouping token, not a patient ID.
    """
    if not isinstance(case_key, str) or not case_key.startswith("synthetic-"):
        raise CaptureContractError("case_key must be a synthetic grouping token")
    if isinstance(required_views, (str, bytes)) or not 1 <= len(required_views) <= 12:
        raise CaptureContractError("required_views must contain 1-12 entries")
    views = list(required_views)
    if any(not isinstance(v, str) or not v.strip() for v in views) or len(set(views)) != len(views):
        raise CaptureContractError("required_views must be unique nonempty strings")
    if isinstance(captures, (str, bytes)) or len(captures) != len(views):
        raise CaptureContractError("capture count does not match required views")
    seen = set()
    receipts = []
    for expected, capture in zip(views, captures):
        if not isinstance(capture, Mapping):
            raise CaptureContractError("capture must be a metadata mapping")
        allowed = {"capture_key", "case_key", "view", "saved", "synthetic", "consent_confirmed"}
        if set(capture) - allowed:
            raise CaptureContractError("capture contains unsupported fields; do not submit image bytes or identifying metadata")
        key = capture.get("capture_key")
        if not isinstance(key, str) or not key.startswith("synthetic-") or key in seen:
            raise CaptureContractError("capture keys must be unique synthetic tokens")
        seen.add(key)
        if capture.get("case_key") != case_key:
            raise CaptureContractError("capture belongs to a different synthetic case")
        if capture.get("view") != expected:
            raise CaptureContractError("capture views must match required order")
        if any(capture.get(field) is not True for field in ("saved", "synthetic", "consent_confirmed")):
            raise CaptureContractError("only saved, synthetic, consent-marked captures are accepted")
        receipts.append({"capture_key": key, "view": expected})
    return {"case_key": case_key, "complete": True, "captures": receipts,
            "clinical_quality_verified": False, "research_only": True}
