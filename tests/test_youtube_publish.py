from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import publish_youtube as publisher  # noqa: E402


class YouTubePublishPureTests(unittest.TestCase):
    def _valid_metadata_plan(self):
        return {
            "title": "title",
            "description": "description",
            "tags": ["tag"],
            "category_id": "22",
            "default_language": "ja",
            "made_for_kids": False,
            "privacy": "private",
            "contains_synthetic_media": True,
        }

    def test_private_is_the_default_mode(self):
        args = argparse.Namespace(
            private=False,
            schedule=None,
            public=False,
            retry_thumbnail=False,
            retry_schedule=None,
        )
        self.assertEqual(publisher.determine_mode(args), "private")

    def test_public_is_rejected_before_any_work(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = publisher.main(["003", "--public"])
        self.assertEqual(result, 2)
        self.assertEqual(
            output.getvalue().strip(),
            "ERROR\nImmediate public publishing is disabled by policy.",
        )

    def test_jst_schedule_converts_to_utc(self):
        local, label, api_value = publisher.parse_schedule(
            "2026-09-02 19:00",
            now=datetime(2026, 8, 31, 12, 0, 0, tzinfo=publisher.JST),
        )
        self.assertEqual(local.strftime("%Y-%m-%d %H:%M"), "2026-09-02 19:00")
        self.assertEqual(label, "2026-09-02 19:00:00 JST")
        self.assertEqual(api_value, "2026-09-02T10:00:00Z")

    def test_past_schedule_is_rejected(self):
        with self.assertRaises(publisher.PublishError):
            publisher.parse_schedule(
                "2026-08-30 19:00",
                now=datetime(2026, 8, 31, 12, 0, 0, tzinfo=publisher.JST),
            )

    def test_metadata_limits_and_control_characters_fail_without_truncation(self):
        plan = {
            "title": "あ" * 101,
            "description": "あ" * 1700,
            "tags": ["tag\x00", "x" * 501],
            "category_id": "22",
            "default_language": "ja",
            "made_for_kids": False,
            "privacy": "private",
        }
        errors = publisher.validate_metadata(plan)
        self.assertTrue(any("title exceeds" in error for error in errors))
        self.assertTrue(any("description exceeds" in error for error in errors))
        self.assertTrue(any("control characters" in error for error in errors))
        self.assertTrue(any("tags exceed" in error for error in errors))
        self.assertEqual(len(plan["title"]), 101)

    def test_ai_disclosure_requires_an_explicit_boolean(self):
        plan = self._valid_metadata_plan()
        del plan["contains_synthetic_media"]
        errors = publisher.validate_metadata(plan)
        self.assertTrue(any("AI disclosure" in error for error in errors))
        plan["contains_synthetic_media"] = False
        self.assertFalse(any("AI disclosure" in error for error in publisher.validate_metadata(plan)))

    def test_insert_body_maps_true_and_false_to_api_field(self):
        for value in (True, False):
            plan = self._valid_metadata_plan()
            plan["contains_synthetic_media"] = value
            body = publisher.build_video_insert_body(plan)
            self.assertEqual(body["status"]["containsSyntheticMedia"], value)
            self.assertEqual(body["status"]["privacyStatus"], "private")

    def test_uploaded_video_verification_allows_list_omitting_ai_disclosure(self):
        class Request:
            def execute(self):
                return {
                    "items": [{
                        "id": "abc12345678",
                        "snippet": {
                            "title": "title",
                            "description": "description",
                            "channelId": "channel-id",
                        },
                        "status": {
                            "privacyStatus": "private",
                            "selfDeclaredMadeForKids": False,
                        },
                    }]
                }

        class Videos:
            def list(self, **kwargs):
                return Request()

        class YouTube:
            def videos(self):
                return Videos()

        plan = {
            "title": "title",
            "description": "description",
            "made_for_kids": False,
            "contains_synthetic_media": True,
            "schedule_api": None,
        }
        item = publisher.verify_uploaded_video(
            YouTube(), plan, "abc12345678", expected_channel_id="channel-id"
        )
        self.assertEqual(item["id"], "abc12345678")

    def test_preserved_status_keeps_schedule_and_made_for_kids(self):
        current = {
            "privacyStatus": "private",
            "publishAt": "2026-09-02T10:00:00Z",
            "license": "youtube",
            "embeddable": True,
            "publicStatsViewable": False,
            "selfDeclaredMadeForKids": False,
            "madeForKids": False,
            "uploadStatus": "processed",
            "containsSyntheticMedia": False,
        }
        preserved = publisher.build_preserved_status(current, True)
        self.assertEqual(preserved["privacyStatus"], "private")
        self.assertEqual(preserved["publishAt"], "2026-09-02T10:00:00Z")
        self.assertEqual(preserved["selfDeclaredMadeForKids"], False)
        self.assertEqual(preserved["containsSyntheticMedia"], True)
        self.assertNotIn("madeForKids", preserved)
        self.assertNotIn("uploadStatus", preserved)

    def test_ai_disclosure_can_verify_from_update_response_when_list_omits_field(self):
        before = {
            "id": "abc12345678",
            "status": {
                "privacyStatus": "private",
                "publishAt": "2026-09-02T10:00:00Z",
                "license": "youtube",
                "embeddable": True,
                "publicStatsViewable": True,
                "selfDeclaredMadeForKids": False,
                "containsSyntheticMedia": False,
            },
        }
        after = {
            "id": "abc12345678",
            "status": {
                "privacyStatus": "private",
                "publishAt": "2026-09-02T10:00:00Z",
                "license": "youtube",
                "embeddable": True,
                "publicStatsViewable": True,
                "selfDeclaredMadeForKids": False,
            },
        }
        source = publisher.verify_ai_disclosure_status(
            before,
            after,
            True,
            update_response={"status": {"containsSyntheticMedia": True}},
        )
        self.assertIn("videos.update response", source)
        self.assertIn("videos.list omitted", source)

    def test_ai_update_is_status_only_and_never_inserts(self):
        class Request:
            def __init__(self, result):
                self.result = result

            def execute(self):
                return self.result

        class Videos:
            def __init__(self):
                self.status = {
                    "privacyStatus": "private",
                    "publishAt": "2026-09-02T10:00:00Z",
                    "license": "youtube",
                    "embeddable": True,
                    "publicStatsViewable": True,
                    "selfDeclaredMadeForKids": False,
                    "containsSyntheticMedia": False,
                }
                self.update_part = None
                self.update_body = None
                self.insert_called = False

            def list(self, **kwargs):
                return Request({"items": [{"id": "abc12345678", "status": dict(self.status)}]})

            def update(self, **kwargs):
                self.update_part = kwargs["part"]
                self.update_body = kwargs["body"]
                self.status["containsSyntheticMedia"] = kwargs["body"]["status"]["containsSyntheticMedia"]
                return Request({"id": "abc12345678"})

            def insert(self, **kwargs):
                self.insert_called = True
                raise AssertionError("videos.insert must not be called")

        class YouTube:
            def __init__(self):
                self.video_api = Videos()

            def videos(self):
                return self.video_api

        with tempfile.TemporaryDirectory() as directory:
            episode_dir = Path(directory)
            (episode_dir / "work" / "youtube_publish").mkdir(parents=True)
            (episode_dir / "STATE.md").write_text(
                "# test\n\n- youtube_video_id: abc12345678\n- youtube_privacy: private\n",
                encoding="utf-8",
            )
            (episode_dir / "publish.json").write_text(
                '{"contains_synthetic_media": true}\n', encoding="utf-8"
            )
            plan = {"episode": "999_test", "episode_dir": str(episode_dir)}
            service = YouTube()
            result = publisher.execute_ai_disclosure_update(service, plan, True, "channel-id")
            self.assertFalse(service.video_api.insert_called)
            self.assertEqual(service.video_api.update_part, "status")
            self.assertEqual(service.video_api.update_body["id"], "abc12345678")
            self.assertNotIn("snippet", service.video_api.update_body)
            status_body = service.video_api.update_body["status"]
            self.assertEqual(status_body["privacyStatus"], "private")
            self.assertEqual(status_body["publishAt"], "2026-09-02T10:00:00Z")
            self.assertEqual(status_body["selfDeclaredMadeForKids"], False)
            self.assertEqual(status_body["containsSyntheticMedia"], True)
            self.assertEqual(result["verification"], "PASS")
            state = (episode_dir / "STATE.md").read_text(encoding="utf-8")
            self.assertIn("youtube_video_id: abc12345678", state)
            self.assertIn("youtube_ai_disclosure: true", state)

    def test_ai_dry_run_report_and_display_show_disclosure(self):
        plan = {
            "episode": "003_line_renewal",
            "episode_dir": str(ROOT / "episodes" / "003_line_renewal"),
            "final_path": "final.mp4",
            "thumbnail_path": "thumbnail.png",
            "title": "title",
            "description": "description",
            "tags": [],
            "privacy": "private",
            "video_sha256": "D" * 64,
            "contains_synthetic_media": True,
            "schedule_local_label": None,
            "schedule_api": None,
        }
        report = publisher.ai_disclosure_dry_run_report(plan, True, "abc12345678", [])
        self.assertTrue(report["target_containsSyntheticMedia"])
        self.assertFalse(report["videos_insert_called"])
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            publisher.print_preflight(plan, [], dry_run=True)
        self.assertIn("AI disclosure    YES", output.getvalue())

    def test_thumbnail_validation_detects_missing_and_accepts_valid_png(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            missing = publisher.validate_thumbnail(folder / "missing.png")
            self.assertTrue(any("Thumbnail missing" in error for error in missing))
            valid_path = folder / "thumbnail.png"
            Image.new("RGB", (1600, 900), (20, 80, 120)).save(valid_path, format="PNG")
            self.assertEqual(publisher.validate_thumbnail(valid_path), [])

    def test_wrong_channel_is_rejected_by_id(self):
        ok, reason = publisher.channel_matches(
            "actual-channel",
            "大人のデジタル安心室",
            "approved-channel",
            "大人のデジタル安心室",
            "大人のデジタル安心室",
        )
        self.assertFalse(ok)
        self.assertIn("ID mismatch", reason)

    def test_missing_final_is_a_gate_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            errors, digest = publisher.final_gate(Path(directory))
            self.assertTrue(errors)
            self.assertEqual(digest, "")
            self.assertTrue(any("Final video missing" in error for error in errors))

    def test_non_approved_final_is_a_gate_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            episode_dir = Path(directory)
            (episode_dir / "output" / "review").mkdir(parents=True)
            (episode_dir / "work").mkdir(parents=True)
            final = episode_dir / "output" / "final.mp4"
            final.write_bytes(b"test-final")
            digest = publisher.sha256(final)
            (episode_dir / "STATE.md").write_text(
                "# test\n\n- status: finalized\n- human_approved: true\n",
                encoding="utf-8",
            )
            (episode_dir / "work" / "human_review.json").write_text(
                json.dumps({"video": {"draft_auto_v3": "pending"}}),
                encoding="utf-8",
            )
            (episode_dir / "output" / "review" / "final_qa.md").write_text(
                f"QA PASS\nSHA-256: {digest}\n",
                encoding="utf-8",
            )
            errors, _ = publisher.final_gate(episode_dir, final)
            self.assertTrue(any("human_review.json" in error for error in errors))

    def test_duplicate_video_id_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            episode_dir = Path(directory)
            (episode_dir / "STATE.md").write_text(
                "# test\n\n- youtube_video_id: abc12345678\n",
                encoding="utf-8",
            )
            video_id, source, unknown = publisher.existing_video_id(episode_dir)
            self.assertEqual(video_id, "abc12345678")
            self.assertEqual(source, "STATE.md")
            self.assertFalse(unknown)

    def test_dry_run_report_never_marks_api_as_called(self):
        report = publisher.dry_run_report(
            {
                "episode": "003_line_renewal",
                "final_path": "final.mp4",
                "thumbnail_path": "thumbnail.png",
                "title": "title",
                "description": "description",
                "tags": ["one"],
                "privacy": "private",
                "video_sha256": "A" * 64,
            },
            [],
        )
        self.assertFalse(report["api_called"])
        self.assertFalse(report["oauth_called"])
        self.assertIn("videos.insert", report["expected_api_requests"][0])

    def test_dry_run_does_not_initialize_youtube_service(self):
        with tempfile.TemporaryDirectory() as directory:
            report_dir = Path(directory)
            plan = {
                "episode": "999_test",
                "episode_dir": str(report_dir),
                "final_path": "final.mp4",
                "thumbnail_path": "thumbnail.png",
                "title": "title",
                "description": "description",
                "tags": [],
                "privacy": "private",
                "video_sha256": "C" * 64,
                "schedule_local_label": None,
                "schedule_api": None,
            }
            with patch.object(publisher, "build_plan", return_value=(plan, [])), patch.object(
                publisher, "preflight", return_value=[]
            ), patch.object(publisher, "existing_video_id", return_value=(None, None, False)), patch.object(
                publisher, "get_youtube_service"
            ) as service:
                result = publisher.main(["999", "--private", "--dry-run"])
            self.assertEqual(result, 0)
            service.assert_not_called()
            self.assertTrue((report_dir / "work" / "youtube_publish" / "dry_run.json").exists())

    def test_auth_check_is_read_only_and_runs_channel_guard(self):
        diagnostics = {
            "has_refresh_token": True,
            "refresh_attempted": True,
            "refresh_success": True,
        }
        with patch.object(
            publisher,
            "auth_health_check",
            return_value=(object(), diagnostics, "channel-id", "channel title"),
        ) as health, patch.object(publisher, "_insert_video") as insert:
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = publisher.main(["--auth-check"])

        self.assertEqual(result, 0)
        health.assert_called_once()
        insert.assert_not_called()
        text = output.getvalue()
        self.assertIn("OAuth client: OK", text)
        self.assertIn("YouTube API auth: PASS", text)
        self.assertIn("Channel guard: PASS", text)
        self.assertIn("AUTH_HEALTH=PASS", text)
        self.assertIn("upload: 0", text)

    def test_auth_health_check_uses_read_only_channels_list_and_approved_id(self):
        class FakeChannelRequest:
            def __init__(self):
                self.kwargs = None

            def list(self, **kwargs):
                self.kwargs = kwargs
                return self

            def execute(self):
                return {"items": [{"id": "approved-channel", "snippet": {"title": "channel title"}}]}

        class FakeYouTube:
            def __init__(self):
                self.request = FakeChannelRequest()

            def channels(self):
                return self.request

        service = FakeYouTube()
        config = {"channel_name": "channel title"}
        with patch.object(publisher, "get_youtube_service", return_value=service), patch.object(
            publisher,
            "load_channel_config",
            return_value={"expected_channel_id": "approved-channel", "expected_channel_title": "channel title"},
        ):
            _, diagnostics, channel_id, title = publisher.auth_health_check(config, quiet=True)

        self.assertEqual(service.request.kwargs, {"part": "id,snippet", "mine": True, "maxResults": 1})
        self.assertEqual(channel_id, "approved-channel")
        self.assertEqual(title, "channel title")
        self.assertEqual(diagnostics["channel_guard"], "PASS")
        self.assertEqual(diagnostics["youtube_api_auth"], "PASS")

    def test_log_filters_token_and_client_secret_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            episode_dir = Path(directory)
            publisher.append_log(
                episode_dir,
                {
                    "timestamp": "now",
                    "mode": "dry-test",
                    "title": "title",
                    "token": "refresh-token-secret",
                    "client_secret": "client-secret-value",
                },
            )
            text = (episode_dir / "work" / "youtube_publish" / "youtube_upload_log.md").read_text(encoding="utf-8")
            self.assertNotIn("refresh-token-secret", text)
            self.assertNotIn("client-secret-value", text)

    def test_id_is_persisted_before_thumbnail_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            episode_dir = Path(directory)
            (episode_dir / "work" / "youtube_publish").mkdir(parents=True)
            (episode_dir / "STATE.md").write_text(
                "# test\n\n- status: finalized\n- human_approved: true\n",
                encoding="utf-8",
            )
            (episode_dir / "publish.json").write_text("{}\n", encoding="utf-8")
            plan = {
                "episode": "999_test",
                "episode_dir": str(episode_dir),
                "title": "title",
                "description": "description",
                "tags": [],
                "category_id": "22",
                "default_language": "ja",
                "made_for_kids": False,
                "privacy": "private",
                "final_path": str(episode_dir / "output" / "final.mp4"),
                "thumbnail_path": str(episode_dir / "thumbnail.png"),
                "video_sha256": "B" * 64,
                "schedule_local_label": None,
                "schedule_api": None,
            }
            with patch.object(publisher, "_insert_video", return_value="abc12345678") as insert, patch.object(
                publisher,
                "_set_thumbnail",
                side_effect=publisher.PublishError("thumbnail failed"),
            ):
                with self.assertRaises(publisher.PublishError):
                    publisher.execute_publish(object(), {}, plan, "channel-id")
            insert.assert_called_once()
            state = (episode_dir / "STATE.md").read_text(encoding="utf-8")
            self.assertIn("youtube_video_id: abc12345678", state)
            self.assertIn("youtube_upload: uploaded_private_thumbnail_failed", state)
            attempt = json.loads(
                (episode_dir / "work" / "youtube_publish" / "upload_attempt.json").read_text(encoding="utf-8")
            )
            self.assertEqual(attempt["video_id"], "abc12345678")
            self.assertEqual(publisher.existing_video_id(episode_dir)[0], "abc12345678")


if __name__ == "__main__":
    unittest.main()
