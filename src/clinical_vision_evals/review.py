"""Blank clinician-owned comparison worksheet for synthetic demonstration cases."""
from __future__ import annotations
from .matcher import compare

def make_blank_review_sheet(query: dict, references: list[dict]) -> dict:
    result = compare(query, references, limit=100)
    return {
        "schema_version": "0.1.0",
        "research_only": True,
        "synthetic_only": True,
        "auto_exclusions": [],
        "not_a_diagnosis": True,
        "clinician_review_required": True,
        "attention_flags_as_reported": result["attention_flags_as_reported"],
        "rows": [{
            "reference_id": c["reference_id"],
            "reference_pattern": c["reference_pattern"],
            "supporting_observations": c["feature_overlap"],
            "lab_flag_overlap": c["lab_flag_overlap"],
            "source": c["source"],
            "clinician_assessment": "unreviewed",
            "clinician_rationale": "",
            "needs_verification": "",
            "unresolved_questions": [],
        } for c in result["candidates"]],
        "limitations": "Template only. A reviewing clinician may document their own assessment; AI cannot exclude diagnoses or determine tests.",
    }
