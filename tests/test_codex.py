import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from clinical_vision_evals.codex import CODEX_MODEL, UnsafeInput, check_synthetic_fixture, codex_synthetic_observe

ROOT = Path(__file__).resolve().parents[1]
IM = ROOT / "examples/fixtures/synthetic_shape.png"
MANIFEST = ROOT / "examples/fixtures/manifest.json"

class CodexTests(unittest.TestCase):
    def test_model_is_codex_only(self):
        self.assertEqual(CODEX_MODEL, "gpt-5.3-codex")

    def test_synthetic_image_hash_matches(self):
        self.assertGreater(len(check_synthetic_fixture(IM, MANIFEST)), 100)

    def test_default_disallows_api(self):
        with self.assertRaises(UnsafeInput):
            codex_synthetic_observe(str(IM), str(MANIFEST))

    def test_disallows_arbitrary_image_path(self):
        with tempfile.TemporaryDirectory() as d:
            other = Path(d)/"other.png"
            other.write_bytes(IM.read_bytes())
            with self.assertRaises(UnsafeInput):
                check_synthetic_fixture(other, MANIFEST)

    def test_disallows_wrong_checksum(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/'synthetic_shape.png').write_bytes(IM.read_bytes() + b'injected')
            (root/'manifest.json').write_text(MANIFEST.read_text())
            with self.assertRaises(UnsafeInput):
                check_synthetic_fixture(root/'synthetic_shape.png', root/'manifest.json')

    def test_rejects_non_synthetic_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/'synthetic_shape.png').write_bytes(IM.read_bytes())
            manifest=json.loads(MANIFEST.read_text())
            manifest['synthetic'] = False
            (root/'manifest.json').write_text(json.dumps(manifest))
            with self.assertRaises(UnsafeInput):
                check_synthetic_fixture(root/'synthetic_shape.png', root/'manifest.json')

    def test_no_api_key_no_network(self):
        with patch.dict('os.environ', {}, clear=True):
            with self.assertRaises(UnsafeInput):
                codex_synthetic_observe(str(IM), str(MANIFEST), allow_api=True)

if __name__ == "__main__":
    unittest.main()
