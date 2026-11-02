import unittest
from pathlib import Path
from clinical_vision_evals.library import load_query, load_references
from clinical_vision_evals.review import make_blank_review_sheet
ROOT=Path(__file__).resolve().parents[1]

class ReviewTests(unittest.TestCase):
    def test_review_sheet_is_blank_and_non_diagnostic(self):
        result=make_blank_review_sheet(
            load_query(ROOT/'examples/queries/synthetic-changing-spot.json'),
            load_references(ROOT/'examples/library'))
        self.assertTrue(result['research_only'])
        self.assertEqual(result['auto_exclusions'], [])
        self.assertTrue(result['clinician_review_required'])
        self.assertGreaterEqual(len(result['rows']), 1)
        for row in result['rows']:
            self.assertEqual(row['clinician_assessment'], 'unreviewed')
            self.assertEqual(row['clinician_rationale'], '')
            self.assertEqual(row['needs_verification'], '')
