from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
import wave
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from build_episode import apply_pronunciation_review, check_scene_modes, gate_overall
from build_subtitle_timeline import write_subtitles
from hybrid_scene_renderer import render_episode_scenes, validate_ai_images
from phase2_qa import finalize_allowed, unresolved_placeholders
from phase2_video import build_video
from scene_mode_advisor import recommend_scene_mode
from tts_voicevox import apply_pronunciation_pitch_patterns
from voicevox_incremental import segment_hash


class Phase2PipelineTests(unittest.TestCase):
    def test_render_mode_advisor_and_validation(self):
        scene = {"id": 1, "layout": "layout_07_summary", "headline": "まとめ", "support_text": "", "main_message": ""}
        self.assertEqual(recommend_scene_mode(scene)["recommended_mode"], "template")
        self.assertEqual(check_scene_modes({"scenes": [{**scene, "render_mode": "bad"}]})[0], "FAIL")

    def test_all_four_render_modes_produce_final_scenes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            episode_path = root / "episode.json"
            episode_path.write_text("{}", encoding="utf-8")
            ai = root / "ai"
            ai.mkdir()
            for scene_id in (2, 4):
                Image.new("RGB", (1920, 1080), "white").save(ai / f"scene_{scene_id:03d}.png")
            base = {"start_segment": 1, "end_segment": 1, "layout": "layout_03_visual_text", "headline": "確認", "support_text": "安全に確認", "main_message": "慌てず確認します", "subtitle_ids": []}
            quote = [{"kind": "quote", "text": "公式説明", "source": "公式"}]
            data = {
                "narration_segments": [{"id": 1, "section": "テスト"}],
                "scenes": [
                    {**base, "id": 1, "render_mode": "template"},
                    {**base, "id": 2, "render_mode": "gpt_image"},
                    {**base, "id": 3, "render_mode": "official", "official_asset": quote},
                    {**base, "id": 4, "render_mode": "hybrid", "official_asset": quote},
                ],
            }
            result = render_episode_scenes(episode_path, data, ai, root / "template", root / "final")
            self.assertEqual(result["status"], "PASS", result["errors"])
            self.assertEqual(len(result["rendered"]), 4)

    def test_missing_gpt_image_stops_then_continue_can_pass(self):
        data = {"scenes": [{"id": 1, "render_mode": "gpt_image"}]}
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            self.assertEqual(validate_ai_images(data, folder)["status"], "MISSING")
            Image.new("RGB", (1920, 1080), "white").save(folder / "scene_001.png")
            self.assertEqual(validate_ai_images(data, folder)["status"], "PASS")

    def test_pronunciation_review_needs_explicit_approval(self):
        result = {"status": "REVIEW", "review_count": 1, "reviews": [{"segment_id": 7, "term": "例"}]}
        self.assertEqual(apply_pronunciation_review(result, {})["status"], "REVIEW")
        approved = {"pronunciation": {"approved_segments": [7]}}
        self.assertEqual(apply_pronunciation_review(result, approved)["status"], "PASS")

    def test_subtitle_fail_or_warn_stops_gate(self):
        self.assertEqual(gate_overall([{"status": "FAIL"}]), "FAIL")
        self.assertEqual(gate_overall([{"status": "WARN"}]), "REVIEW")

    def test_incremental_hash_only_changes_modified_segment(self):
        base = {"id": 1, "narration": "同じ文", "reading_overrides": {}}
        digest = segment_hash(base, "同じ文")
        self.assertEqual(digest, segment_hash(dict(base), "同じ文"))
        changed = {**base, "narration": "変更した文"}
        self.assertNotEqual(digest, segment_hash(changed, "変更した文"))

    def test_human_pitch_shape_keeps_credit_plateau_and_following_o_equal(self):
        query = {
            "accent_phrases": [
                {"moras": [
                    {"text": "シ", "pitch": 5.0},
                    {"text": "ン", "pitch": 5.2},
                    {"text": "ヨ", "pitch": 5.0},
                    {"text": "オ", "pitch": 4.8},
                ], "pause_mora": None},
                {"moras": [{"text": "オ", "pitch": 4.6}], "pause_mora": None},
            ]
        }
        records = apply_pronunciation_pitch_patterns(query, episode_id="008")
        pitches = [mora["pitch"] for mora in query["accent_phrases"][0]["moras"]]
        self.assertEqual(records[0]["following_same_mora_pitch_delta"], 0.0)
        self.assertLess(pitches[0], pitches[1])
        self.assertEqual(pitches[1:], [pitches[1]] * 3)
        self.assertEqual(query["accent_phrases"][1]["moras"][0]["pitch"], pitches[1])

    def test_placeholder_is_a_hard_failure(self):
        data = {"scenes": [{"id": 3, "headline": "GPT IMAGE HERE", "official_asset": []}]}
        self.assertTrue(unresolved_placeholders(data))

    def test_finalize_requires_video_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "human_review.json"
            self.assertFalse(finalize_allowed(path)[0])
            path.write_text(json.dumps({"video": {"draft_auto_v1": "approved"}}), encoding="utf-8")
            self.assertTrue(finalize_allowed(path)[0])

    @unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg not installed")
    def test_ffmpeg_pipeline_builds_1080p_draft(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            scenes = root / "scenes"
            scenes.mkdir()
            Image.new("RGB", (1920, 1080), "white").save(scenes / "scene_001.png")
            audio = root / "narration.wav"
            with wave.open(str(audio), "wb") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(48000)
                wav.writeframes(b"\x00\x00" * 48000)
            timing = root / "timing.json"
            timing.write_text(json.dumps({"duration": 1.0, "segments": [{"segment_id": 1, "start_sec": 0, "end_sec": 1.0, "pause_after": 0}]}), encoding="utf-8")
            ass = root / "captions.ass"
            write_subtitles([{"start_sec": 0, "end_sec": 1.0, "text_lines": ["確認します"]}], root / "captions.srt", ass)
            data = {"scenes": [{"id": 1, "start_segment": 1, "end_segment": 1, "animation": "none"}]}
            result = build_video(data, scenes, timing, audio, ass, root / "work", root / "draft.mp4")
            self.assertEqual(result["status"], "PASS", result)
            self.assertTrue((root / "draft.mp4").exists())


if __name__ == "__main__":
    unittest.main()
