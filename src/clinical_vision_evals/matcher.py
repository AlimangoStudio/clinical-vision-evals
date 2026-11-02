"""Non-diagnostic descriptive overlap; no probability, exclusion or advice."""
from __future__ import annotations
from .library import _tags, _lab_tags, validate_query, validate_reference
NOTICE = (
    "RESEARCH DEMO ONLY. Pattern overlaps are not diagnoses, disease probabilities, "
    "risk estimates or clinical rules. Unmatched patterns are NOT ruled out. "
    "A clinician must review original evidence and decide whether further "
    "evaluation or testing is indicated."
)

def compare(query: dict, references: list[dict], limit: int = 10) -> dict:
    validate_query(query)
    if not 1 <= limit <= 100:
        raise ValueError("limit must be 1..100")
    qfeatures = set(_tags(query["observed_features"], "observed_features"))
    qlabs = set(_lab_tags(query.get("lab_flags", [])))
    candidates = []
    for ref in references:
        validate_reference(ref)
        features = set(_tags(ref["features"], "features"))
        labs = set(_lab_tags(ref.get("lab_flags", [])))
        common = sorted(features & qfeatures)
        lab_common = sorted(labs & qlabs)
        if not common and not lab_common:
            continue
        candidates.append({
            "reference_id": ref["case_id"],
            "reference_pattern": ref["pattern_label"],
            "feature_overlap": common,
            "lab_flag_overlap": lab_common,
            "unobserved_reference_features": sorted(features - qfeatures),
            "source": {"title": ref["source_title"], "url": ref["source_url"]},
            "reference_limitations": ref["limitations"],
            "review_status": ref["review_status"],
        })
    candidates.sort(key=lambda c: (-(len(c["feature_overlap"]) + len(c["lab_flag_overlap"])), c["reference_id"]))
    return {
        "schema_version": "0.1.0",
        "mode": "non_diagnostic_reference_browse",
        "research_only": True,
        "candidates": candidates[:limit],
        "reference_count": len(references),
        "display_count": min(len(candidates), limit),
        "unmatched_or_unlisted_are_not_excluded": True,
        "ordering": "descriptive overlap, never calibrated likelihood",
        "attention_flags_as_reported": _tags(query.get("attention_flags", []), "attention_flags"),
        "clinician_review_required": True,
        "notice": NOTICE,
    }
