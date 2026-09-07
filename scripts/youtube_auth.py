"""Small, secret-safe OAuth helper for the YouTube publisher.

The publisher deliberately keeps browser OAuth out of the normal path.  A
saved access token may be refreshed automatically, while a missing or
revoked refresh token requires an explicit ``--force-reauth`` invocation.
This module also owns the token persistence rules so that a refresh failure
cannot damage the canonical token file.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable


UTC = timezone.utc
AUTH_REAUTH_COMMAND = "python scripts/publish_youtube.py --auth-check --force-reauth"
DEFAULT_NEAR_EXPIRY_SECONDS = 300

_DIAGNOSTIC_FIELDS = (
    "auth_timestamp",
    "oauth_client_type",
    "oauth_client_id_sha256_prefix",
    "oauth_client_id_suffix",
    "has_refresh_token",
    "access_token_expiry",
    "refresh_attempted",
    "refresh_success",
    "error_class",
    "channel_id",
    "channel_guard",
    "youtube_api_auth",
    "token_exists",
    "token_saved",
    "token_backup_created",
)


class AuthError(RuntimeError):
    """Expected OAuth failure with a safe error class and diagnostics."""

    def __init__(
        self,
        message: str,
        *,
        code: str = "AUTH_ERROR",
        error_class: str = "other",
        diagnostics: dict[str, Any] | None = None,
        cause: BaseException | None = None,
    ) -> None:
        self.code = code
        self.error_class = error_class
        self.diagnostics = dict(diagnostics or {})
        self.cause = cause
        super().__init__(message)


@dataclass(frozen=True)
class ClientInfo:
    client_type: str
    client_id: str


@dataclass(frozen=True)
class GoogleComponents:
    request: Any
    credentials: Any
    installed_app_flow: Any
    build: Callable[..., Any]


@dataclass(frozen=True)
class AuthResult:
    service: Any
    credentials: Any
    diagnostics: dict[str, Any]


def _utc_now(value: datetime | None = None) -> datetime:
    result = value or datetime.now(UTC)
    if result.tzinfo is None:
        return result.replace(tzinfo=UTC)
    return result.astimezone(UTC)


def _iso_timestamp(value: datetime | None = None) -> str:
    return _utc_now(value).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def client_id_fingerprint(client_id: str) -> dict[str, str]:
    """Return only non-secret diagnostics for an OAuth client ID."""
    digest = hashlib.sha256(client_id.encode("utf-8")).hexdigest()
    return {
        "oauth_client_id_sha256_prefix": digest[:12],
        "oauth_client_id_suffix": client_id[-6:] if client_id else "",
    }


def _client_block(data: dict[str, Any]) -> tuple[str, dict[str, Any]] | None:
    for key in ("installed", "web"):
        value = data.get(key)
        if isinstance(value, dict):
            return key, value
    return None


def load_client_info(client_secret_path: Path) -> ClientInfo:
    try:
        data = json.loads(client_secret_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AuthError(
            f"OAuth client secret is missing: {client_secret_path}.",
            code="AUTH_CLIENT_MISSING",
            error_class="invalid_client",
            cause=exc,
        ) from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise AuthError(
            "OAuth client secret could not be read as JSON.",
            code="AUTH_CLIENT_INVALID",
            error_class="invalid_client",
            cause=exc,
        ) from exc

    if not isinstance(data, dict):
        raise AuthError(
            "OAuth client secret must contain a JSON object.",
            code="AUTH_CLIENT_INVALID",
            error_class="invalid_client",
        )
    block = _client_block(data)
    if block is None or not str(block[1].get("client_id") or "").strip():
        raise AuthError(
            "OAuth client secret does not contain a usable client ID.",
            code="AUTH_CLIENT_INVALID",
            error_class="invalid_client",
        )
    client_type, values = block
    return ClientInfo(client_type=client_type, client_id=str(values["client_id"]).strip())


def _read_token_data(token_path: Path) -> dict[str, Any]:
    try:
        data = json.loads(token_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AuthError(
            f"OAuth token is missing: {token_path}.",
            code="AUTH_REAUTH_REQUIRED",
            error_class="missing_refresh_token",
            cause=exc,
        ) from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise AuthError(
            "Existing OAuth token could not be loaded; browser OAuth was not started.",
            code="AUTH_TOKEN_LOAD_FAILED",
            error_class="other",
            cause=exc,
        ) from exc
    if not isinstance(data, dict):
        raise AuthError(
            "Existing OAuth token must contain a JSON object; browser OAuth was not started.",
            code="AUTH_TOKEN_LOAD_FAILED",
            error_class="other",
        )
    return data


def _check_client_consistency(
    client_info: ClientInfo,
    token_data: dict[str, Any],
    diagnostics: dict[str, Any],
    *,
    candidate_client_id: str | None = None,
) -> None:
    token_client_id = str(token_data.get("client_id") or "").strip()
    compared_client_id = token_client_id or str(candidate_client_id or "").strip()
    if compared_client_id and compared_client_id != client_info.client_id:
        diagnostics["error_class"] = "client_mismatch"
        raise AuthError(
            "AUTH_CLIENT_MISMATCH: client_secret.json and token.json were created for different OAuth clients; browser OAuth was not started.",
            code="AUTH_CLIENT_MISMATCH",
            error_class="client_mismatch",
            diagnostics=diagnostics,
        )


def _error_text(exc: BaseException) -> str:
    """Collect error markers for classification without returning them."""
    values: list[str] = [type(exc).__name__, str(exc)]
    for name in ("error", "error_details", "response", "resp"):
        value = getattr(exc, name, None)
        if value is None:
            continue
        if isinstance(value, (dict, list, tuple)):
            try:
                values.append(json.dumps(value, ensure_ascii=False, default=str))
            except Exception:
                values.append(str(value))
        else:
            values.append(str(value))
    return " ".join(values).lower()


def classify_refresh_error(exc: BaseException) -> str:
    """Classify a refresh failure without exposing Google's response body."""
    text = _error_text(exc)
    if "invalid_grant" in text:
        return "invalid_grant"
    if "invalid_client" in text:
        return "invalid_client"
    if isinstance(exc, (TimeoutError,)) or any(
        marker in text for marker in ("timeout", "timed out", "deadline exceeded")
    ):
        return "timeout"
    if isinstance(exc, (ConnectionError,)) or any(
        marker in text
        for marker in (
            "connection",
            "network",
            "dns",
            "name resolution",
            "unreachable",
            "connection reset",
            "connection refused",
            "transport error",
            "ssl error",
        )
    ):
        return "network"
    return "other"


def _refresh_failure(
    exc: BaseException,
    diagnostics: dict[str, Any],
) -> AuthError:
    error_class = classify_refresh_error(exc)
    diagnostics["error_class"] = error_class
    diagnostics["refresh_success"] = False
    if error_class == "invalid_grant":
        message = (
            "AUTH_REAUTH_REQUIRED: refresh tokenが期限切れまたは失効しています。"
            "OAuth consent screenがTestingの場合、Google仕様によりrefresh tokenが約7日で期限切れになるため、"
            "Google Auth PlatformのPublishing statusを確認してください。"
            f"ブラウザOAuthは開始していません。人間確認後: {AUTH_REAUTH_COMMAND}"
        )
        code = "AUTH_REAUTH_REQUIRED"
    elif error_class == "invalid_client":
        message = (
            "AUTH_CLIENT_INVALID: OAuth clientが拒否されました。client_secret.jsonとGoogle Cloud側のclientを確認してください。"
            "ブラウザOAuthは開始していません。"
        )
        code = "AUTH_CLIENT_INVALID"
    elif error_class == "network":
        message = (
            "AUTH_NETWORK_ERROR: OAuth token refreshのネットワーク通信に失敗しました。"
            "ブラウザOAuthは開始していません。"
        )
        code = "AUTH_NETWORK_ERROR"
    elif error_class == "timeout":
        message = (
            "AUTH_TIMEOUT: OAuth token refreshがタイムアウトしました。"
            "ブラウザOAuthは開始していません。"
        )
        code = "AUTH_TIMEOUT"
    else:
        message = (
            "AUTH_REFRESH_FAILED: OAuth token refreshに失敗しました。"
            "ブラウザOAuthは開始していません。"
        )
        code = "AUTH_REFRESH_FAILED"
    return AuthError(
        message,
        code=code,
        error_class=error_class,
        diagnostics=diagnostics,
        cause=exc,
    )


def _load_google_components() -> GoogleComponents:
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError as exc:
        raise AuthError(
            "YouTube client libraries are not installed. Run: python -m pip install -r requirements-youtube.txt",
            code="AUTH_DEPENDENCIES_MISSING",
            error_class="other",
            cause=exc,
        ) from exc
    return GoogleComponents(
        request=Request,
        credentials=Credentials,
        installed_app_flow=InstalledAppFlow,
        build=build,
    )


def _expiry_datetime(credentials: Any) -> datetime | None:
    value = getattr(credentials, "expiry", None)
    if isinstance(value, datetime):
        return _utc_now(value)
    if isinstance(value, str) and value:
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
        return _utc_now(parsed)
    return None


def _expiry_for_diagnostics(credentials: Any) -> str | None:
    expiry = _expiry_datetime(credentials)
    return _iso_timestamp(expiry) if expiry else None


def _needs_refresh(credentials: Any, now: datetime, near_expiry_seconds: int) -> bool:
    expiry = _expiry_datetime(credentials)
    if expiry is not None and expiry <= now + timedelta(seconds=near_expiry_seconds):
        return True
    return bool(getattr(credentials, "expired", False)) or not bool(
        getattr(credentials, "valid", False)
    )


def _serialize_credentials(
    credentials: Any,
    *,
    previous_token_data: dict[str, Any],
    old_refresh_token: str | None,
    client_id: str,
) -> tuple[str, dict[str, Any], str | None]:
    try:
        data = json.loads(credentials.to_json())
    except (TypeError, ValueError, OSError) as exc:
        raise AuthError(
            "OAuth credentials could not be serialized safely; token.json was not changed.",
            code="AUTH_TOKEN_SAVE_FAILED",
            error_class="other",
            cause=exc,
        ) from exc
    if not isinstance(data, dict):
        raise AuthError(
            "OAuth credentials serialization did not return a JSON object; token.json was not changed.",
            code="AUTH_TOKEN_SAVE_FAILED",
            error_class="other",
        )

    # Google normally keeps this field on Credentials.  Preserve it
    # explicitly because some refresh responses omit refresh_token.
    serialized_refresh = str(data.get("refresh_token") or "").strip()
    if not serialized_refresh and old_refresh_token:
        data["refresh_token"] = old_refresh_token
        serialized_refresh = old_refresh_token
    if not data.get("client_id") and previous_token_data.get("client_id"):
        data["client_id"] = previous_token_data["client_id"]
    if not data.get("client_id"):
        data["client_id"] = client_id

    return (
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        data,
        serialized_refresh or None,
    )


def atomic_write_text(path: Path, text: str) -> None:
    """Write and fsync a file before replacing the canonical path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    try:
        with temporary.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(str(temporary), str(path))
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def backup_previous_token(
    token_path: Path,
    *,
    backups_dir: Path | None = None,
    timestamp: datetime | None = None,
) -> Path | None:
    """Keep one timestamped copy of the token immediately before rotation."""
    if not token_path.exists():
        return None
    destination_dir = backups_dir or token_path.parent / "backups"
    destination_dir.mkdir(parents=True, exist_ok=True)
    stamp = _utc_now(timestamp).strftime("%Y%m%dT%H%M%SZ")
    destination = destination_dir / f"token.{stamp}.json"
    if destination.exists():
        destination = destination_dir / f"token.{stamp}-{os.getpid()}.json"
    temporary = destination.with_name(f".{destination.name}.tmp")
    try:
        with token_path.open("rb") as source, temporary.open("wb") as target:
            shutil.copyfileobj(source, target)
            target.flush()
            os.fsync(target.fileno())
        os.replace(str(temporary), str(destination))
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass

    # The request is intentionally one generation, not an archive.  Keep the
    # newest backup and remove only older files in this dedicated directory.
    backups = sorted(destination_dir.glob("token.*.json"), key=lambda item: item.stat().st_mtime)
    for old in backups[:-1]:
        try:
            old.unlink()
        except FileNotFoundError:
            pass
    return destination


def write_diagnostics(path: Path, diagnostics: dict[str, Any]) -> None:
    """Persist allow-listed, secret-free auth diagnostics."""
    safe = {key: diagnostics.get(key) for key in _DIAGNOSTIC_FIELDS if key in diagnostics}
    atomic_write_text(path, json.dumps(safe, ensure_ascii=False, indent=2) + "\n")


def _persist_credentials(
    token_path: Path,
    credentials: Any,
    *,
    previous_token_data: dict[str, Any],
    old_refresh_token: str | None,
    client_id: str,
    timestamp: datetime,
    diagnostics: dict[str, Any],
) -> None:
    serialized, data, new_refresh_token = _serialize_credentials(
        credentials,
        previous_token_data=previous_token_data,
        old_refresh_token=old_refresh_token,
        client_id=client_id,
    )
    if new_refresh_token and new_refresh_token != old_refresh_token:
        try:
            backup_previous_token(token_path, timestamp=timestamp)
        except OSError as exc:
            diagnostics["error_class"] = "other"
            raise AuthError(
                "AUTH_TOKEN_SAVE_FAILED: token backup could not be created; token.json was not changed.",
                code="AUTH_TOKEN_SAVE_FAILED",
                error_class="other",
                diagnostics=diagnostics,
                cause=exc,
            ) from exc
        diagnostics["token_backup_created"] = True
    current = token_path.read_bytes() if token_path.exists() else None
    encoded = serialized.encode("utf-8")
    if current != encoded:
        try:
            atomic_write_text(token_path, serialized)
        except OSError as exc:
            diagnostics["error_class"] = "other"
            raise AuthError(
                "AUTH_TOKEN_SAVE_FAILED: token.json could not be written atomically.",
                code="AUTH_TOKEN_SAVE_FAILED",
                error_class="other",
                diagnostics=diagnostics,
                cause=exc,
            ) from exc
        diagnostics["token_saved"] = True
    else:
        diagnostics["token_saved"] = False
    diagnostics["has_refresh_token"] = bool(data.get("refresh_token"))


def authenticate(
    client_secret_path: Path,
    token_path: Path,
    scopes: list[str],
    *,
    force_reauth: bool = False,
    near_expiry_seconds: int = DEFAULT_NEAR_EXPIRY_SECONDS,
    now: datetime | None = None,
    google_components: GoogleComponents | None = None,
) -> AuthResult:
    """Load, refresh, or explicitly re-authorize YouTube credentials."""
    timestamp = _utc_now(now)
    client_info = load_client_info(client_secret_path)
    token_exists = token_path.exists()
    token_data: dict[str, Any] = {}
    if token_exists:
        token_data = _read_token_data(token_path)

    diagnostics: dict[str, Any] = {
        "auth_timestamp": _iso_timestamp(timestamp),
        "oauth_client_type": client_info.client_type,
        **client_id_fingerprint(client_info.client_id),
        "has_refresh_token": bool(token_data.get("refresh_token")),
        "access_token_expiry": token_data.get("expiry"),
        "refresh_attempted": False,
        "refresh_success": None,
        "error_class": None,
        "channel_id": None,
        "channel_guard": None,
        "youtube_api_auth": None,
        "token_exists": token_exists,
        "token_saved": False,
        "token_backup_created": False,
    }

    if token_exists:
        _check_client_consistency(client_info, token_data, diagnostics)
    elif not force_reauth:
        diagnostics["error_class"] = "missing_refresh_token"
        raise AuthError(
            "AUTH_REAUTH_REQUIRED: token.jsonがありません。ブラウザOAuthは開始していません。"
            f"人間確認後: {AUTH_REAUTH_COMMAND}",
            code="AUTH_REAUTH_REQUIRED",
            error_class="missing_refresh_token",
            diagnostics=diagnostics,
        )

    components = google_components or _load_google_components()
    requested_scopes = {str(scope) for scope in scopes}
    credentials: Any | None = None

    if token_exists and not force_reauth:
        try:
            credentials = components.credentials.from_authorized_user_file(
                str(token_path), scopes=list(scopes)
            )
        except Exception as exc:
            diagnostics["error_class"] = "other"
            raise AuthError(
                "AUTH_TOKEN_LOAD_FAILED: existing OAuth token could not be loaded; browser OAuth was not started.",
                code="AUTH_TOKEN_LOAD_FAILED",
                error_class="other",
                diagnostics=diagnostics,
                cause=exc,
            ) from exc

        _check_client_consistency(
            client_info,
            token_data,
            diagnostics,
            candidate_client_id=str(getattr(credentials, "client_id", None) or "").strip() or None,
        )
        candidate_scopes = {str(scope) for scope in (getattr(credentials, "scopes", None) or [])}
        if not requested_scopes.issubset(candidate_scopes):
            diagnostics["error_class"] = "scope_mismatch"
            raise AuthError(
                "AUTH_SCOPE_MISMATCH: existing OAuth token scopes are insufficient; browser OAuth was not started.",
                code="AUTH_SCOPE_MISMATCH",
                error_class="scope_mismatch",
                diagnostics=diagnostics,
            )

        old_refresh_token = str(
            getattr(credentials, "refresh_token", None) or token_data.get("refresh_token") or ""
        ).strip() or None
        diagnostics["has_refresh_token"] = bool(old_refresh_token)
        diagnostics["access_token_expiry"] = _expiry_for_diagnostics(credentials) or token_data.get(
            "expiry"
        )
        if not old_refresh_token:
            diagnostics["error_class"] = "missing_refresh_token"
            raise AuthError(
                "AUTH_REAUTH_REQUIRED: token.jsonにrefresh tokenがありません。"
                f"ブラウザOAuthは開始していません。人間確認後: {AUTH_REAUTH_COMMAND}",
                code="AUTH_REAUTH_REQUIRED",
                error_class="missing_refresh_token",
                diagnostics=diagnostics,
            )
        needs_refresh = _needs_refresh(credentials, timestamp, near_expiry_seconds)
        if needs_refresh:
            diagnostics["refresh_attempted"] = True
            try:
                credentials.refresh(components.request())
            except Exception as exc:
                raise _refresh_failure(exc, diagnostics) from exc
            diagnostics["refresh_success"] = True
            diagnostics["access_token_expiry"] = _expiry_for_diagnostics(credentials)
            try:
                if not getattr(credentials, "refresh_token", None):
                    credentials.refresh_token = old_refresh_token
            except Exception:
                # Serialization below still injects the old value.
                pass
            _persist_credentials(
                token_path,
                credentials,
                previous_token_data=token_data,
                old_refresh_token=old_refresh_token,
                client_id=client_info.client_id,
                timestamp=timestamp,
                diagnostics=diagnostics,
            )
    else:
        # This branch is reachable only when --force-reauth was explicitly
        # supplied.  Offline access is mandatory, and consent is requested
        # only in this browser flow.
        try:
            flow = components.installed_app_flow.from_client_secrets_file(
                str(client_secret_path), scopes=list(scopes)
            )
            credentials = flow.run_local_server(
                port=0,
                access_type="offline",
                prompt="consent",
            )
        except Exception as exc:
            diagnostics["error_class"] = classify_refresh_error(exc)
            raise AuthError(
                "AUTH_REAUTH_FAILED: explicit browser OAuth authentication failed.",
                code="AUTH_REAUTH_FAILED",
                error_class=diagnostics["error_class"],
                diagnostics=diagnostics,
                cause=exc,
            ) from exc
        _check_client_consistency(
            client_info,
            token_data,
            diagnostics,
            candidate_client_id=str(getattr(credentials, "client_id", None) or "").strip() or None,
        )
        new_refresh_token = str(getattr(credentials, "refresh_token", None) or "").strip()
        if not new_refresh_token:
            diagnostics["error_class"] = "missing_refresh_token"
            raise AuthError(
                "AUTH_REAUTH_REQUIRED: explicit OAuth flow did not return a refresh token; token.json was not changed.",
                code="AUTH_REAUTH_REQUIRED",
                error_class="missing_refresh_token",
                diagnostics=diagnostics,
            )
        diagnostics["has_refresh_token"] = True
        diagnostics["access_token_expiry"] = _expiry_for_diagnostics(credentials)
        _persist_credentials(
            token_path,
            credentials,
            previous_token_data=token_data,
            old_refresh_token=str(token_data.get("refresh_token") or "").strip() or None,
            client_id=client_info.client_id,
            timestamp=timestamp,
            diagnostics=diagnostics,
        )

    if credentials is None or not bool(getattr(credentials, "valid", False)):
        diagnostics["error_class"] = diagnostics.get("error_class") or "other"
        raise AuthError(
            "AUTH_REAUTH_REQUIRED: OAuth credentials are not valid after refresh; browser OAuth was not started.",
            code="AUTH_REAUTH_REQUIRED",
            error_class=str(diagnostics["error_class"]),
            diagnostics=diagnostics,
        )

    try:
        service = components.build(
            "youtube", "v3", credentials=credentials, cache_discovery=False
        )
    except Exception as exc:
        diagnostics["error_class"] = "other"
        raise AuthError(
            "AUTH_API_CLIENT_INIT: YouTube API client could not be initialized.",
            code="AUTH_API_CLIENT_INIT",
            error_class="other",
            diagnostics=diagnostics,
            cause=exc,
        ) from exc
    diagnostics["has_refresh_token"] = bool(getattr(credentials, "refresh_token", None)) or bool(
        token_data.get("refresh_token")
    )
    return AuthResult(service=service, credentials=credentials, diagnostics=diagnostics)
