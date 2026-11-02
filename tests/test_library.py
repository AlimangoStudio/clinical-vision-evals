import json
import tempfile
import unittest
from pathlib import Path
from clinical_vision_evals.library import LibraryError, load_query, load_references, validate_query, validate_reference
from clinical_vision_evals.matcher import compare

ROOT = Path(__file__).resolve().parents[1]

class LibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.refs = load_references(ROOT / "examples/library")
        cls.query = load_query(ROOT / "examples/queries/synthetic-itchy-rash.json")

    def test_references_loaded(self):
        self.assertEqual(len(self.refs), 5)

    def test_private_reference_rejected(self):
        with self.assertRaises(LibraryError):
            validate_reference(dict(self.refs[0], origin="clinical_patient"))

    def test_image_path_rejected(self):
        with self.assertRaises(LibraryError):
            validate_reference(dict(self.refs[0], image_paths=["patients/img.png"]))

    def test_copyright_unknown_rejected(self):
        with self.assertRaises(LibraryError):
            validate_reference(dict(self.refs[0], license="unknown"))

    def test_non_synthetic_query_rejected(self):
        with self.assertRaises(LibraryError):
            validate_query({**self.query, "synthetic": False})

    def test_patient_id_rejected(self):
        with self.assertRaises(LibraryError):
            validate_query({**self.query, "patient_id": 123})

    def test_invalid_lab_flag_rejected(self):
        with self.assertRaises(LibraryError):
            validate_query({**self.query, "lab_flags": [{"name":"cbc", "flag":"positive"}]})

    def test_duplicate_id_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            a = Path(d)
            (a / "one.json").write_text(json.dumps(self.refs[0]))
            (a / "two.json").write_text(json.dumps(self.refs[0]))
            with self.assertRaises(LibraryError):
                load_references(a)

    def test_returns_overlap_not_diagnosis(self):
        output = compare(self.query, self.refs)
        self.assertEqual(output["mode"], "non_diagnostic_reference_browse")
        self.assertTrue(output["unmatched_or_unlisted_are_not_excluded"])
        self.assertTrue(output["clinician_review_required"])
        self.assertTrue(any(c["feature_overlap"] for c in output["candidates"]))
        self.assertFalse(any("probability" in c or "diagnosis" in c or "rule_out" in c for c in output["candidates"]))

    def test_attentional_flag_is_not_triage(self):
        query = load_query(ROOT / "examples/queries/synthetic-changing-spot.json")
        result = compare(query, self.refs)
        self.assertEqual(result["attention_flags_as_reported"], ["change_over_time"])
        self.assertNotIn("priority", result)
        self.assertNotIn("cancer_risk", result)

    def test_no_matches_does_not_rule_out(self):
        result = compare({**self.query, "observed_features": ["feature_not_in_library"], "lab_flags": []}, self.refs)
        self.assertEqual(result["candidates"], [])
        self.assertTrue(result["unmatched_or_unlisted_are_not_excluded"])

    def test_max_results_only_affects_display(self):
        result = compare(self.query, self.refs, limit=1)
        self.assertEqual(len(result["candidates"]), 1)
        self.assertEqual(result["reference_count"], 5)

    def test_invalid_limit(self):
        with self.assertRaises(ValueError):
            compare(self.query, self.refs, limit=0)

if __name__ == "__main__":
    unittest.main()
