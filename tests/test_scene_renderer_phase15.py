import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from scene_renderer import LAYOUT_TEMPLATES  # noqa: E402


class SceneRendererPhase15Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.episode_dir = ROOT / "episodes" / "002_myna_app"
        cls.output_dir = cls.episode_dir / "work" / "efficiency_test_v2"
        cls.episode = json.loads((cls.episode_dir / "episode.json").read_text(encoding="utf-8"))

    def test_all_eight_layout_templates_are_present(self):
        self.assertEqual(len(LAYOUT_TEMPLATES), 8)
        for filename in LAYOUT_TEMPLATES.values():
            self.assertTrue((ROOT / "templates" / "scenes" / filename).exists(), filename)

    def test_phase15_render_has_all_scenes_and_comparisons(self):
        pngs = sorted(self.output_dir.glob("scene_[0-9][0-9][0-9].png"))
        self.assertEqual(len(pngs), len(self.episode["scenes"]))
        self.assertTrue((self.output_dir / "scene_contact_sheet.png").exists())
        self.assertTrue((self.output_dir / "golden_comparison.png").exists())
        self.assertTrue((self.output_dir / "scene_quality_report.md").exists())
        for path in pngs:
            data = path.read_bytes()
            self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n", path.name)
            self.assertEqual((int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")), (1920, 1080))

    def test_quality_report_contains_mechanical_warnings(self):
        report = (self.output_dir / "scene_quality_report.md").read_text(encoding="utf-8")
        self.assertIn("WARN", report)
        self.assertIn("公式素材率", report)
        self.assertIn("<40px", report)
        self.assertIn("人間確認ポイント", report)


if __name__ == "__main__":
    unittest.main()
