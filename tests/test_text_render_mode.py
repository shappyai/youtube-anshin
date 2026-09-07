from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_image_generation_manifest import build_prompt, manifest_rows  # noqa: E402
from episode_io import canonical_text_render_mode, validate_episode  # noqa: E402
from hybrid_scene_renderer import render_episode_scenes  # noqa: E402
from scene_mode_advisor import recommend_text_render_mode  # noqa: E402
from text_qa import mark, report_scene  # noqa: E402

BASE_SCENE = {
    "id": 1,
    "layout": "layout_01_hero",
    "main_message": "今日も確認する",
    "headline": "のんびり、いこう。",
    "support_text": "今日もいい一日を。",
    "official_asset": [],
    "official_asset_crop": [],
    "start_segment": 1,
    "end_segment": 1,
}


class TextRenderModeTests(unittest.TestCase):
    def test_canonical_mapping_keeps_legacy_aliases(self):
        self.assertEqual(canonical_text_render_mode({"text_render_mode": "codex"}), "pil_overlay")
        self.assertEqual(canonical_text_render_mode({"text_render_mode": "image"}), "imagegen_native")
        self.assertEqual(canonical_text_render_mode({"text_render_mode": "imagegen_native"}), "imagegen_native")
        self.assertEqual(canonical_text_render_mode({"text_render_mode": "pil_overlay"}), "pil_overlay")
        self.assertEqual(canonical_text_render_mode({"text_render_mode": "no_text"}), "no_text")
        # 未指定は新規sceneのdefault
        self.assertEqual(canonical_text_render_mode({}), "imagegen_native")

    def test_validation_accepts_new_modes_and_rejects_unknown(self):
        for mode in ("imagegen_native", "pil_overlay", "no_text", "codex", "image"):
            scene = {**BASE_SCENE, "text_render_mode": mode}
            data = {"scenes": [scene]}
            issues = [issue for issue in validate_episode(data) if "text_render_mode" in issue]
            self.assertEqual(issues, [], mode)
        bad = {**BASE_SCENE, "text_render_mode": "bogus"}
        issues = [issue for issue in validate_episode({**{"scenes": [bad]}}) if "text_render_mode" in issue]
        self.assertTrue(issues)

    def test_imagegen_native_prompt_contains_exact_text(self):
        prompt = build_prompt({**BASE_SCENE, "render_mode": "gpt_image", "text_render_mode": "imagegen_native"})
        self.assertIn("のんびり、いこう。", prompt)
        self.assertIn("今日もいい一日を。", prompt)
        self.assertIn("line 1", prompt)
        self.assertIn("line 2", prompt)
        self.assertIn("bottom 180 pixels", prompt)

    def test_pil_overlay_prompt_does_not_authorize_generated_image_hybrid(self):
        prompt = build_prompt({**BASE_SCENE, "render_mode": "gpt_image", "text_render_mode": "pil_overlay"})
        self.assertIn("later large text overlay", prompt)
        self.assertIn("renderer-native", prompt)
        self.assertIn("Do NOT render any readable text", prompt)

    def test_no_text_prompt_forbids_readable_text(self):
        prompt = build_prompt({**BASE_SCENE, "render_mode": "gpt_image", "text_render_mode": "no_text"})
        self.assertIn("NO readable text", prompt)
        manifest = manifest_rows({"narration_segments": [], "scenes": [{**BASE_SCENE, "render_mode": "gpt_image", "text_render_mode": "no_text"}]})
        self.assertTrue(any("readable text" in item for item in manifest[0]["must_not_generate"]))

    def test_manifest_row_carries_text_spec_and_qa_state(self):
        rows = manifest_rows({"narration_segments": [], "scenes": [{**BASE_SCENE, "render_mode": "gpt_image", "text_render_mode": "imagegen_native"}]})
        row = rows[0]
        self.assertEqual(row["text_render_mode"], "imagegen_native")
        self.assertEqual(row["text_spec"]["headline"], "のんびり、いこう。")
        self.assertEqual(row["text_spec"]["support_text"], "今日もいい一日を。")
        self.assertEqual(row["text_qa"]["status"], "pending")
        self.assertEqual(row["text_qa"]["retry_count"], 0)

    def test_advisor_recommends_modes(self):
        self.assertEqual(recommend_text_render_mode({**BASE_SCENE}, "template"), "pil_overlay")
        self.assertEqual(recommend_text_render_mode({**BASE_SCENE}, "official"), "pil_overlay")
        self.assertEqual(recommend_text_render_mode({**BASE_SCENE}, "gpt_image"), "imagegen_native")
        long_text = {**BASE_SCENE, "headline": "非常に長い見出しで正確性を求められるためPILで正確に描く必要がある見出しです", "support_text": "さらに長い補足説明が続きます"}
        self.assertEqual(recommend_text_render_mode(long_text, "gpt_image"), "imagegen_native")
        digits = {**BASE_SCENE, "headline": "30日で消えます", "support_text": ""}
        self.assertEqual(recommend_text_render_mode(digits, "gpt_image"), "imagegen_native")
        pin = {**BASE_SCENE, "headline": "PINは6桁", "support_text": ""}
        self.assertEqual(recommend_text_render_mode(pin, "gpt_image"), "imagegen_native")
        empty = {**BASE_SCENE, "headline": "", "support_text": ""}
        self.assertEqual(recommend_text_render_mode(empty, "gpt_image"), "no_text")

    def test_renderer_skips_overlay_for_imagegen_native(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ai = root / "ai"
            ai.mkdir()
            source = Image.new("RGB", (1920, 1080), "#123456")
            source.save(ai / "scene_001.png")
            data = {"narration_segments": [{"id": 1, "section": "テスト"}], "scenes": [
                {**BASE_SCENE, "render_mode": "gpt_image", "text_render_mode": "imagegen_native"},
            ]}
            episode_path = root / "episode.json"
            episode_path.write_text("{}", encoding="utf-8")
            result = render_episode_scenes(episode_path, data, ai, root / "template", root / "final")
            self.assertEqual(result["status"], "PASS", result["errors"])
            rendered = root / "final" / "scene_001.png"
            self.assertEqual(Image.open(rendered).convert("RGB").getpixel((500, 250)), (0x12, 0x34, 0x56))

    def test_renderer_rejects_generated_image_pil_overlay_hybrid(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ai = root / "ai"
            ai.mkdir()
            source = Image.new("RGB", (1920, 1080), "#123456")
            source.save(ai / "scene_001.png")
            data = {"narration_segments": [{"id": 1, "section": "テスト"}], "scenes": [
                {**BASE_SCENE, "render_mode": "gpt_image", "text_render_mode": "pil_overlay"},
            ]}
            episode_path = root / "episode.json"
            episode_path.write_text("{}", encoding="utf-8")
            result = render_episode_scenes(episode_path, data, ai, root / "template", root / "final")
            self.assertEqual(result["status"], "FAIL")
            self.assertTrue(any("NO_IMAGE_TEXT_HYBRID" in error for error in result["errors"]))

    def test_text_qa_report_and_retry_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ai = root / "generated_ai"
            ai.mkdir()
            Image.new("RGB", (1920, 1080), "white").save(ai / "scene_001.png")
            scene = {**BASE_SCENE, "render_mode": "gpt_image", "text_render_mode": "imagegen_native", "image_prompt": ""}
            # custom promptをfile経由で与える
            manifest = {"scenes": [{
                "scene_id": "SCENE-001",
                "image_prompt": "line 1: \"のんびり、いこう。\" line 2: \"今日もいい一日を。\"",
                "text_qa": {"status": "pending", "retry_count": 0, "fallback": None},
            }]}
            report = report_scene(scene, manifest, ai)
            self.assertEqual(report["text_render_mode"], "imagegen_native")
            self.assertTrue(any("文言仕様" in item for item in report["auto_passed"]))
            self.assertEqual(report["auto_fail"], [])
            self.assertEqual(len(report["vision_checklist"]), 12)
            # 1回目FAIL → retry
            mark(manifest, "SCENE-001", "FAIL")
            mark(manifest, "SCENE-001", "FAIL")
            self.assertEqual(manifest["scenes"][0]["text_qa"]["status"], "renderer_only_required")
            self.assertEqual(manifest["scenes"][0]["text_qa"]["retry_count"], 2)
            self.assertEqual(manifest["scenes"][0]["text_qa"]["fallback"], "renderer_only")
            mark(manifest, "SCENE-001", "RESET")
            mark(manifest, "SCENE-001", "PASS")
            self.assertEqual(manifest["scenes"][0]["text_qa"]["status"], "passed")

    def test_text_qa_flags_missing_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "generated_ai").mkdir()
            scene = {**BASE_SCENE, "render_mode": "gpt_image", "text_render_mode": "imagegen_native"}
            report = report_scene(scene, None, root / "generated_ai")
            self.assertTrue(report["auto_fail"])


if __name__ == "__main__":
    unittest.main()
