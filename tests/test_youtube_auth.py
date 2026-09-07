from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import youtube_auth as auth  # noqa: E402


UTC = timezone.utc


class RefreshFailure(Exception):
    pass


class FakeRequest:
    calls = 0

    def __init__(self):
        type(self).calls += 1


class FakeCredentials:
    refresh_behavior = None
    refresh_calls = 0

    def __init__(self, data: dict, scopes: list[str] | None = None):
        self.token = data.get("token")
        self.refresh_token = data.get("refresh_token")
        self.client_id = data.get("client_id")
        self.client_secret = data.get("client_secret")
        self.scopes = list(scopes if scopes is not None else data.get("scopes", []))
        expiry = data.get("expiry")
        self.expiry = datetime.fromisoformat(str(expiry).replace("Z", "+00:00")) if expiry else None
        self.expired = self.expiry is not None and self.expiry <= datetime.now(UTC)
        self.valid = bool(self.token) and not self.expired

    @classmethod
    def from_authorized_user_file(cls, path: str, scopes: list[str]):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(data, scopes=scopes)

    def refresh(self, request):
        type(self).refresh_calls += 1
        if type(self).refresh_behavior is not None:
            type(self).refresh_behavior(self)
            return
        self.token = "refreshed-access-token"
        self.refresh_token = None  # Simulate a response that omits it.
        self.expiry = datetime.now(UTC) + timedelta(hours=1)
        self.expired = False
        self.valid = True

    def to_json(self):
        value = {
            "token": self.token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scopes": self.scopes,
            "expiry": self.expiry.isoformat().replace("+00:00", "Z") if self.expiry else None,
        }
        if self.refresh_token is not None:
            value["refresh_token"] = self.refresh_token
        return json.dumps(value)


class FakeFlow:
    run_kwargs = None
    returned_credentials = None

    def run_local_server(self, **kwargs):
        type(self).run_kwargs = kwargs
        return type(self).returned_credentials


class FakeInstalledAppFlow:
    from_calls = 0

    @classmethod
    def from_client_secrets_file(cls, path: str, scopes: list[str]):
        cls.from_calls += 1
        return FakeFlow()


def fake_build(*args, **kwargs):
    return {"service": "fake", "credentials": kwargs["credentials"]}


COMPONENTS = auth.GoogleComponents(
    request=FakeRequest,
    credentials=FakeCredentials,
    installed_app_flow=FakeInstalledAppFlow,
    build=fake_build,
)


class YouTubeAuthTests(unittest.TestCase):
    scopes = [
        "https://www.googleapis.com/auth/youtube.upload",
        "https://www.googleapis.com/auth/youtube.force-ssl",
    ]

    def setUp(self):
        FakeCredentials.refresh_behavior = None
        FakeCredentials.refresh_calls = 0
        FakeRequest.calls = 0
        FakeInstalledAppFlow.from_calls = 0
        FakeFlow.run_kwargs = None
        FakeFlow.returned_credentials = None

    def _files(self, *, token: dict | None = None):
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name)
        client_secret = root / "client_secret.json"
        token_path = root / "token.json"
        client_secret.write_text(
            json.dumps(
                {
                    "installed": {
                        "client_id": "client-id.apps.googleusercontent.com",
                        "client_secret": "test-client-secret",
                    }
                }
            ),
            encoding="utf-8",
        )
        if token is not None:
            token_path.write_text(json.dumps(token) + "\n", encoding="utf-8")
        return directory, client_secret, token_path

    def _token(self, *, expiry: datetime, client_id: str = "client-id.apps.googleusercontent.com"):
        return {
            "token": "old-access-token",
            "refresh_token": "old-refresh-token",
            "client_id": client_id,
            "client_secret": "test-client-secret",
            "scopes": self.scopes,
            "expiry": expiry.isoformat().replace("+00:00", "Z"),
        }

    def _authenticate(self, client_secret: Path, token_path: Path, **kwargs):
        return auth.authenticate(
            client_secret,
            token_path,
            self.scopes,
            google_components=COMPONENTS,
            now=datetime(2026, 9, 7, 12, 0, tzinfo=UTC),
            **kwargs,
        )

    def test_valid_refresh_token_uses_saved_credentials_without_browser(self):
        directory, client_secret, token_path = self._files(
            token=self._token(expiry=datetime(2026, 9, 7, 18, 0, tzinfo=UTC))
        )
        self.addCleanup(directory.cleanup)
        before = token_path.read_bytes()

        result = self._authenticate(client_secret, token_path)

        self.assertEqual(result.diagnostics["refresh_attempted"], False)
        self.assertIsNone(result.diagnostics["refresh_success"])
        self.assertEqual(FakeCredentials.refresh_calls, 0)
        self.assertEqual(FakeInstalledAppFlow.from_calls, 0)
        self.assertEqual(token_path.read_bytes(), before)

    def test_expired_access_token_refreshes_automatically_and_never_opens_browser(self):
        directory, client_secret, token_path = self._files(
            token=self._token(expiry=datetime(2026, 9, 7, 11, 0, tzinfo=UTC))
        )
        self.addCleanup(directory.cleanup)

        result = self._authenticate(client_secret, token_path)
        saved = json.loads(token_path.read_text(encoding="utf-8"))

        self.assertTrue(result.diagnostics["refresh_attempted"])
        self.assertTrue(result.diagnostics["refresh_success"])
        self.assertEqual(FakeCredentials.refresh_calls, 1)
        self.assertEqual(FakeInstalledAppFlow.from_calls, 0)
        self.assertEqual(saved["refresh_token"], "old-refresh-token")
        self.assertEqual(saved["token"], "refreshed-access-token")
        self.assertFalse((token_path.parent / ".token.json.tmp").exists())

    def test_refresh_response_without_new_refresh_token_preserves_old_value(self):
        directory, client_secret, token_path = self._files(
            token=self._token(expiry=datetime(2026, 9, 7, 11, 0, tzinfo=UTC))
        )
        self.addCleanup(directory.cleanup)

        self._authenticate(client_secret, token_path)

        saved = json.loads(token_path.read_text(encoding="utf-8"))
        self.assertEqual(saved["refresh_token"], "old-refresh-token")

    def test_invalid_grant_requires_explicit_reauth_and_leaves_token_unchanged(self):
        directory, client_secret, token_path = self._files(
            token=self._token(expiry=datetime(2026, 9, 7, 11, 0, tzinfo=UTC))
        )
        self.addCleanup(directory.cleanup)
        before = token_path.read_bytes()

        def fail(_credentials):
            raise RefreshFailure("invalid_grant: Token has been expired or revoked.")

        FakeCredentials.refresh_behavior = fail
        with self.assertRaises(auth.AuthError) as raised:
            self._authenticate(client_secret, token_path)

        error = raised.exception
        self.assertEqual(error.code, "AUTH_REAUTH_REQUIRED")
        self.assertEqual(error.error_class, "invalid_grant")
        self.assertIn("Testing", str(error))
        self.assertIn("--auth-check --force-reauth", str(error))
        self.assertEqual(token_path.read_bytes(), before)
        self.assertEqual(FakeInstalledAppFlow.from_calls, 0)
        self.assertFalse((token_path.parent / ".token.json.tmp").exists())

    def test_other_refresh_failure_leaves_token_unchanged(self):
        directory, client_secret, token_path = self._files(
            token=self._token(expiry=datetime(2026, 9, 7, 11, 0, tzinfo=UTC))
        )
        self.addCleanup(directory.cleanup)
        before = token_path.read_bytes()

        def fail(_credentials):
            raise ConnectionError("network unavailable")

        FakeCredentials.refresh_behavior = fail
        with self.assertRaises(auth.AuthError) as raised:
            self._authenticate(client_secret, token_path)

        self.assertEqual(raised.exception.error_class, "network")
        self.assertEqual(token_path.read_bytes(), before)

    def test_refresh_error_classification_covers_required_classes(self):
        self.assertEqual(auth.classify_refresh_error(Exception("invalid_client")), "invalid_client")
        self.assertEqual(auth.classify_refresh_error(TimeoutError("timed out")), "timeout")
        self.assertEqual(auth.classify_refresh_error(Exception("unexpected response")), "other")

    def test_client_mismatch_stops_before_refresh_or_browser(self):
        directory, client_secret, token_path = self._files(
            token=self._token(
                expiry=datetime(2026, 9, 7, 11, 0, tzinfo=UTC),
                client_id="different-client.apps.googleusercontent.com",
            )
        )
        self.addCleanup(directory.cleanup)
        before = token_path.read_bytes()

        with self.assertRaises(auth.AuthError) as raised:
            self._authenticate(client_secret, token_path)

        self.assertEqual(raised.exception.code, "AUTH_CLIENT_MISMATCH")
        self.assertEqual(FakeCredentials.refresh_calls, 0)
        self.assertEqual(FakeInstalledAppFlow.from_calls, 0)
        self.assertEqual(token_path.read_bytes(), before)

    def test_missing_token_without_force_reauth_never_opens_browser(self):
        directory, client_secret, token_path = self._files()
        self.addCleanup(directory.cleanup)

        with self.assertRaises(auth.AuthError) as raised:
            self._authenticate(client_secret, token_path)

        self.assertEqual(raised.exception.code, "AUTH_REAUTH_REQUIRED")
        self.assertEqual(FakeInstalledAppFlow.from_calls, 0)

    def test_missing_refresh_token_stops_even_before_access_token_expires(self):
        token = self._token(expiry=datetime(2026, 9, 7, 18, 0, tzinfo=UTC))
        token.pop("refresh_token")
        directory, client_secret, token_path = self._files(token=token)
        self.addCleanup(directory.cleanup)

        with self.assertRaises(auth.AuthError) as raised:
            self._authenticate(client_secret, token_path)

        self.assertEqual(raised.exception.code, "AUTH_REAUTH_REQUIRED")
        self.assertEqual(raised.exception.error_class, "missing_refresh_token")
        self.assertEqual(FakeCredentials.refresh_calls, 0)
        self.assertEqual(FakeInstalledAppFlow.from_calls, 0)

    def test_force_reauth_uses_offline_consent_and_saves_token(self):
        directory, client_secret, token_path = self._files()
        self.addCleanup(directory.cleanup)
        FakeFlow.returned_credentials = FakeCredentials(
            {
                "token": "new-access-token",
                "refresh_token": "new-refresh-token",
                "client_id": "client-id.apps.googleusercontent.com",
                "client_secret": "test-client-secret",
                "scopes": self.scopes,
                "expiry": "2026-09-07T13:00:00Z",
            },
            scopes=self.scopes,
        )

        result = self._authenticate(client_secret, token_path, force_reauth=True)
        saved = json.loads(token_path.read_text(encoding="utf-8"))

        self.assertIsNotNone(result.service)
        self.assertEqual(FakeInstalledAppFlow.from_calls, 1)
        self.assertEqual(FakeFlow.run_kwargs["access_type"], "offline")
        self.assertEqual(FakeFlow.run_kwargs["prompt"], "consent")
        self.assertEqual(saved["refresh_token"], "new-refresh-token")
        self.assertEqual(result.diagnostics["has_refresh_token"], True)

    def test_new_refresh_token_creates_only_one_secret_backup(self):
        directory, client_secret, token_path = self._files(
            token=self._token(expiry=datetime(2026, 9, 7, 11, 0, tzinfo=UTC))
        )
        self.addCleanup(directory.cleanup)

        def rotate(credentials):
            credentials.token = "new-access-token"
            credentials.refresh_token = "new-refresh-token"
            credentials.expiry = datetime.now(UTC) + timedelta(hours=1)
            credentials.expired = False
            credentials.valid = True

        FakeCredentials.refresh_behavior = rotate
        result = self._authenticate(client_secret, token_path)
        backups = list((token_path.parent / "backups").glob("token.*.json"))

        self.assertEqual(len(backups), 1)
        self.assertTrue(result.diagnostics["token_backup_created"])
        backup_text = backups[0].read_text(encoding="utf-8")
        self.assertIn("old-refresh-token", backup_text)
        self.assertNotIn("new-refresh-token", backup_text)

    def test_diagnostics_allowlist_does_not_write_token_values(self):
        directory, client_secret, token_path = self._files(
            token=self._token(expiry=datetime(2026, 9, 7, 18, 0, tzinfo=UTC))
        )
        self.addCleanup(directory.cleanup)
        result = self._authenticate(client_secret, token_path)
        diagnostics_path = token_path.parent / "diagnostics.json"

        auth.write_diagnostics(diagnostics_path, result.diagnostics)
        text = diagnostics_path.read_text(encoding="utf-8")
        self.assertNotIn("old-access-token", text)
        self.assertNotIn("old-refresh-token", text)
        self.assertNotIn("test-client-secret", text)
        self.assertIn("oauth_client_id_sha256_prefix", text)


if __name__ == "__main__":
    unittest.main()
