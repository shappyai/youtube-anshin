from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_image_generation_manifest import COMMON_PROMPT, build_prompt  # noqa: E402
from episode_io import apply_episode_defaults  # noqa: E402
from phase2_qa import declared_visual_center_x, scene_visual_warnings  # noqa: E402


class Phase2StandardsTests(unittest.TestCase):
    def test_scene_defaults_are_safe(self):
        data = {"scenes": [{"id": 1}]}
        result = apply_episode_defaults(data)
        self.assertEqual(result["scenes"][0]["fit_mode"], "full_bleed")
        self.assertEqual(result["scenes"][0]["animation"], "static")
        self.assertNotIn("fit_mode", data["scenes"][0])

    def test_gpt_prompt_enforces_one_full_frame_scene(self):
        self.assertIn("Generate exactly ONE standalone 16:9 image for this scene.", COMMON_PROMPT)
        self.assertIn("Do not create a collage, storyboard, contact sheet, split panel, or multiple scenes.", COMMON_PROMPT)
        self.assertIn("edge-to-edge full-frame background", build_prompt({"image_prompt": "人物が確認する"}))

    def test_caution_offset_is_warn_only_balance_signal(self):
        self.assertEqual(declared_visual_center_x({"layout": "layout_06_caution", "content_offset_x": 360}), 960.0)

    def test_horizontal_pan_without_reason_warns(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "scene_001.png"
            image = Image.new("RGB", (1920, 1080), "white")
            ImageDraw.Draw(image).rectangle((800, 200, 1120, 700), fill="#2f74bb")
            image.save(path)
            warnings = scene_visual_warnings(
                {"id": 1, "render_mode": "gpt_image", "animation": "slow_pan"}, path
            )
            self.assertTrue(any("animation_reason" in item for item in warnings))


if __name__ == "__main__":
    unittest.main()
