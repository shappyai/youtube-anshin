import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from episode_io import asset_path_from_item, load_json, validate_episode  # noqa: E402


class EpisodePipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.episode_path = ROOT / "episodes" / "002_myna_app" / "episode.json"
        cls.episode = load_json(cls.episode_path)

    def test_episode_json_matches_schema_contract(self):
        self.assertEqual(validate_episode(self.episode), [])
        self.assertEqual(len(self.episode["sources"]), 15)
        self.assertEqual(len(self.episode["narration_segments"]), 80)
        self.assertEqual(len(self.episode["subtitles"]), 97)
        self.assertEqual(len(self.episode["scenes"]), 35)

    def test_subtitles_are_explicit_one_or_two_lines(self):
        for subtitle in self.episode["subtitles"]:
            self.assertIn(len(subtitle["text_lines"]), (1, 2), subtitle["id"])
            self.assertTrue(all(line.strip() for line in subtitle["text_lines"]), subtitle["id"])

    def test_scene_templates_and_declared_assets_exist(self):
        episode_dir = self.episode_path.parent
        for scene in self.episode["scenes"]:
            template = ROOT / "templates" / "scenes" / f"{scene['layout']}.html"
            self.assertTrue(template.exists(), scene["layout"])
            for asset in scene["official_asset"]:
                if asset.get("kind") == "image":
                    self.assertTrue(
                        asset_path_from_item(asset, episode_dir).exists(),
                        f"scene {scene['id']}: {asset.get('path')}",
                    )

    def test_generated_contact_sheet_and_scene_dimensions(self):
        output_dir = ROOT / "episodes" / "002_myna_app" / "work" / "efficiency_test"
        self.assertTrue((output_dir / "scene_contact_sheet.png").exists())
        pngs = sorted(output_dir.glob("scene_[0-9][0-9][0-9].png"))
        self.assertEqual(len(pngs), 35)
        for path in pngs:
            data = path.read_bytes()
            self.assertGreater(len(data), 24, path.name)
            self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n", path.name)
            width = int.from_bytes(data[16:20], "big")
            height = int.from_bytes(data[20:24], "big")
            self.assertEqual((width, height), (1920, 1080), path.name)


if __name__ == "__main__":
    unittest.main()
