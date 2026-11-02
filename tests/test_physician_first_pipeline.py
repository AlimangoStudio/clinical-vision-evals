"""Regression tests for independently ported, synthetic-only pipeline invariants."""
import copy
import unittest
from pathlib import Path
from clinical_vision_evals.capture_contract import CaptureContractError, validate_capture_set
from clinical_vision_evals.evidence import (
    assemble_physician_first_packet, seal_physician_baseline, validate_evidence_bundle,
)
from clinical_vision_evals.library import LibraryError, load_references

ROOT = Path(__file__).resolve().parents[1]


def bundle():
    return {"synthetic": True, "case_key": "synthetic-case1", "evidence": [
        {"evidence_id": "e1", "modality": "patient_report", "origin": "patient",
         "source_title": "Fabricated complaint", "recorded_at": "2026-11-01T12:00:00+08:00",
         "observed_features": ["itch", "erythema"],
         "claims": [{"concept": "itch", "state": "present"}]},
        {"evidence_id": "e2", "modality": "lab_report", "origin": "laboratory_report",
         "source_title": "Fabricated lab", "recorded_at": "2026-11-02T12:00:00+08:00",
         "lab_flags": [{"name": "eosinophils", "flag": "elevated"}],
         "claims": [{"concept": "itch", "state": "absent"}]},
        {"evidence_id": "ai1", "modality": "clinical_photo_observation", "origin": "ai_unverified",
         "source_title": "Fabricated AI description", "recorded_at": "2026-11-02T12:00:00+08:00",
         "observed_features": ["unverified_malignant_appearance"]},
    ]}


def baseline():
    return {"synthetic": True, "case_key": "synthetic-case1", "clinician_key": "synthetic-doctor",
            "recorded_at": "2026-11-02T11:00:00+08:00",
            "initial_observations": "Fabricated patient description recorded independently.",
            "initial_impression": "Uncertain; needs professional review.",
            "reviewed_source_ids": ["e1"]}


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.refs = load_references(ROOT / "examples/library")

    def test_physician_first_gate(self):
        with self.assertRaises(LibraryError):
            assemble_physician_first_packet(bundle(), {}, self.refs)

    def test_evidence_aggregates_multiple_sources_without_diagnosis(self):
        packet = assemble_physician_first_packet(bundle(), seal_physician_baseline(baseline(), case_key="synthetic-case1"), self.refs)
        self.assertTrue(packet["physician_baseline_recorded_first"])
        self.assertTrue(packet["no_conditions_excluded"])
        self.assertEqual(packet["unverified_ai_evidence_ids_excluded_from_matching"], ["ai1"])
        self.assertEqual(packet["source_disagreements_needing_review"][0]["concept"], "itch")
        self.assertTrue(packet["illustrative_reference_overlap"])
        self.assertNotIn("probability", packet)
        self.assertNotIn("test_recommendations", packet)

    def test_baseline_cannot_be_modified_after_seal(self):
        sealed = seal_physician_baseline(baseline(), case_key="synthetic-case1")
        sealed["baseline"]["initial_impression"] = "altered"
        with self.assertRaises(LibraryError):
            assemble_physician_first_packet(bundle(), sealed, self.refs)

    def test_source_reference_must_exist(self):
        b = baseline()
        b["reviewed_source_ids"] = ["not-found"]
        with self.assertRaises(LibraryError):
            assemble_physician_first_packet(bundle(), seal_physician_baseline(b, case_key="synthetic-case1"), self.refs)

    def test_denies_real_records_and_nested_identifiers(self):
        b = bundle()
        b["synthetic"] = False
        with self.assertRaises(LibraryError):
            validate_evidence_bundle(b)
        b = bundle()
        b["evidence"][0]["patient_name"] = "DUMMY"
        with self.assertRaises(LibraryError):
            validate_evidence_bundle(b)

    def test_duplicate_evidence_identifiers_blocked(self):
        b = bundle()
        b["evidence"][1]["evidence_id"] = "e1"
        with self.assertRaises(LibraryError):
            validate_evidence_bundle(b)

    def test_capture_contract(self):
        steps = ["front", "profile"]
        captures = [{"case_key": "synthetic-case1", "capture_key": f"synthetic-c{i}",
                     "view": v, "saved": True, "synthetic": True, "consent_confirmed": True}
                    for i, v in enumerate(steps)]
        self.assertTrue(validate_capture_set(case_key="synthetic-case1", required_views=steps, captures=captures)["complete"])
        with self.assertRaises(CaptureContractError):
            validate_capture_set(case_key="synthetic-case1", required_views=steps, captures=list(reversed(captures)))
        modified = copy.deepcopy(captures)
        modified[1]["capture_key"] = "synthetic-c0"
        with self.assertRaises(CaptureContractError):
            validate_capture_set(case_key="synthetic-case1", required_views=steps, captures=modified)
        modified = copy.deepcopy(captures)
        modified[1]["case_key"] = "synthetic-other"
        with self.assertRaises(CaptureContractError):
            validate_capture_set(case_key="synthetic-case1", required_views=steps, captures=modified)
        modified = copy.deepcopy(captures)
        modified[1]["file_path"] = "/tmp/patient-photo.jpg"
        with self.assertRaises(CaptureContractError):
            validate_capture_set(case_key="synthetic-case1", required_views=steps, captures=modified)


if __name__ == "__main__":
    unittest.main()
