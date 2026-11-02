"""Synthetic-only evidence aggregation with a physician-first disclosure barrier.

This offline module contains no AI inference, diagnostic probabilities or test orders.
It assembles provenance-tagged observations and delegates illustrative reference
matching to the existing non-diagnostic matcher.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any

from .library import LibraryError, validate_reference
from .matcher import compare

MODALITIES = frozenset({
    "patient_report", "medical_history", "physician_observation", "lab_report",
    "pathology_report", "biopsy_report", "xray_report", "ct_report",
    "mri_report", "clinical_photo_observation", "specialist_report",
})
ORIGINS = frozenset({"patient", "physician", "laboratory_report", "radiology_report",
                     "pathology_report", "specialist_report", "ai_unverified"})
STATES = frozenset({"present", "absent", "unknown"})
FORBIDDEN_KEYS = frozenset({
    "patient_id", "patient_name", "birthdate", "date_of_birth", "phone",
    "email", "address", "mrn", "medical_record_number", "image_path", "file_path",
    "image_bytes", "raw_image", "base64", "api_key", "access_token", "tenant_id",
})


def _time(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise LibraryError(f"{field} must be a timezone-aware timestamp")
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None or dt.utcoffset() is None:
            raise ValueError("timezone required")
    except (ValueError, TypeError) as exc:
        raise LibraryError(f"{field} must be a timezone-aware ISO-8601 timestamp") from exc
    return value


def _nonempty(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 600:
        raise LibraryError(f"{field} must be nonempty text of at most 600 characters")
    return value.strip()


def _no_identifiers(value: Any) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str) or key.lower() in FORBIDDEN_KEYS:
                raise LibraryError("patient identifiers, file paths and secrets are not allowed")
            _no_identifiers(child)
    elif isinstance(value, list):
        for child in value:
            _no_identifiers(child)


def validate_evidence_bundle(bundle: dict) -> dict:
    """Validate structured, synthetic research inputs; no patient data or raw files."""
    if not isinstance(bundle, dict):
        raise LibraryError("evidence bundle must be an object")
    _no_identifiers(bundle)
    if bundle.get("synthetic") is not True:
        raise LibraryError("the public toolkit accepts synthetic data only")
    case_key = _nonempty(bundle.get("case_key"), "case_key")
    if not case_key.startswith("synthetic-"):
        raise LibraryError("case_key must begin with synthetic-")
    items = bundle.get("evidence")
    if not isinstance(items, list) or not 1 <= len(items) <= 100:
        raise LibraryError("evidence must have 1-100 records")
    seen: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            raise LibraryError("evidence records must be objects")
        evidence_id = _nonempty(item.get("evidence_id"), "evidence_id")
        if evidence_id in seen:
            raise LibraryError("duplicate evidence_id")
        seen.add(evidence_id)
        if item.get("modality") not in MODALITIES or item.get("origin") not in ORIGINS:
            raise LibraryError("unsupported modality or origin")
        _nonempty(item.get("source_title"), "source_title")
        _time(item.get("recorded_at"), "recorded_at")
        features = item.get("observed_features", [])
        if not isinstance(features, list) or len(features) > 50 or any(
            not isinstance(v, str) or not v.strip() or len(v) > 120 for v in features
        ):
            raise LibraryError("observed_features must be short structured tags")
        claims = item.get("claims", [])
        if not isinstance(claims, list) or len(claims) > 50:
            raise LibraryError("claims must be a list of structured observations")
        for claim in claims:
            if not isinstance(claim, dict) or claim.get("state") not in STATES:
                raise LibraryError("claims need a valid state")
            _nonempty(claim.get("concept"), "concept")
        labs = item.get("lab_flags", [])
        if not isinstance(labs, list):
            raise LibraryError("lab_flags must be a list")
        for lab in labs:
            if not isinstance(lab, dict) or lab.get("flag") not in {"elevated", "decreased", "within_reference", "not_reported"}:
                raise LibraryError("invalid lab flag")
            _nonempty(lab.get("name"), "lab name")
    return bundle


def seal_physician_baseline(baseline: dict, *, case_key: str) -> dict:
    """A demonstrative digest, not a cryptographic signature or EHR audit log."""
    _no_identifiers(baseline)
    if not isinstance(baseline, dict) or baseline.get("synthetic") is not True:
        raise LibraryError("a synthetic physician baseline is required")
    if baseline.get("case_key") != case_key:
        raise LibraryError("physician baseline is for another case")
    _nonempty(baseline.get("clinician_key"), "clinician_key")
    if not baseline["clinician_key"].startswith("synthetic-"):
        raise LibraryError("clinician_key must be synthetic")
    _time(baseline.get("recorded_at"), "physician recorded_at")
    _nonempty(baseline.get("initial_observations"), "initial_observations")
    _nonempty(baseline.get("initial_impression"), "initial_impression")
    if baseline.get("reviewed_source_ids") is None or not isinstance(baseline["reviewed_source_ids"], list):
        raise LibraryError("reviewed_source_ids must be present")
    sealed = json.loads(json.dumps(baseline))  # snapshot to avoid mutated caller dictionaries
    digest = hashlib.sha256(json.dumps(sealed, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {"baseline": sealed, "sha256": digest, "sealed_before_ai": True}


def assemble_physician_first_packet(bundle: dict, sealed_baseline: dict, references: list[dict]) -> dict:
    """Return descriptive research overlaps only after validating a sealed baseline.

    Physician's initial *impression* is deliberately withheld from reference matching
    so the matcher does not merely echo diagnostic anchoring. Explicit observations
    in evidence items may contribute to the synthetic reference comparison.
    """
    validate_evidence_bundle(bundle)
    if not isinstance(sealed_baseline, dict) or sealed_baseline.get("sealed_before_ai") is not True:
        raise LibraryError("AI candidates are blocked until physician baseline is sealed")
    baseline = sealed_baseline.get("baseline")
    if not isinstance(baseline, dict) or baseline.get("case_key") != bundle["case_key"]:
        raise LibraryError("baseline is missing or from another case")
    expected = seal_physician_baseline(baseline, case_key=bundle["case_key"])["sha256"]
    if expected != sealed_baseline.get("sha256"):
        raise LibraryError("physician baseline has changed since sealing")
    for ref in references:
        validate_reference(ref)
    source_ids = {e["evidence_id"] for e in bundle["evidence"]}
    if any(x not in source_ids for x in baseline["reviewed_source_ids"]):
        raise LibraryError("physician baseline cites unavailable evidence")
    features = set()
    lab_flags = set()
    unsupported = []
    contradictions: dict[str, dict[str, set[str]]] = {}
    for item in bundle["evidence"]:
        eid = item["evidence_id"]
        if item["origin"] == "ai_unverified":
            unsupported.append(eid)
            continue  # unverified AI output never becomes ground truth for matching
        features.update(x.strip().lower() for x in item.get("observed_features", []))
        lab_flags.update((x["name"].strip().lower(), x["flag"]) for x in item.get("lab_flags", []))
        for claim in item.get("claims", []):
            concept = claim["concept"].strip().lower()
            if claim["state"] in {"present", "absent"}:
                contradictions.setdefault(concept, {}).setdefault(claim["state"], set()).add(eid)
    query = {"schema_version": "0.1.0", "synthetic": True,
             "observed_features": sorted(features),
             "lab_flags": [{"name": n, "flag": f} for n, f in sorted(lab_flags)],
             "attention_flags": []}
    matches = compare(query, references)
    return {
        "schema_version": "0.2.0", "research_only": True, "synthetic_only": True,
        "case_key": bundle["case_key"], "physician_baseline_sha256": sealed_baseline["sha256"],
        "physician_baseline_recorded_first": True,
        "provenance": [{"evidence_id": e["evidence_id"], "modality": e["modality"],
                        "origin": e["origin"], "source_title": e["source_title"],
                        "recorded_at": e["recorded_at"]} for e in bundle["evidence"]],
        "unverified_ai_evidence_ids_excluded_from_matching": unsupported,
        "source_disagreements_needing_review": [
            {"concept": c, "present_evidence_ids": sorted(v["present"]),
             "absent_evidence_ids": sorted(v["absent"])}
            for c, v in sorted(contradictions.items()) if "present" in v and "absent" in v
        ],
        "unavailable_modalities_in_supplied_bundle": sorted(MODALITIES - {e["modality"] for e in bundle["evidence"]}),
        "illustrative_reference_overlap": matches["candidates"],
        "not_a_diagnosis": True, "not_a_prognosis": True, "no_test_orders": True,
        "no_conditions_excluded": True, "clinical_verification_required": True,
        "limitations": "Synthetic reference overlap only; missing modalities are not indications for tests. "
                       "Conflicting observations may reflect different times or contexts. "
                       "No causal inference or validation of medical image interpretation.",
    }
