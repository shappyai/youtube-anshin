"""Mechanical checks for the hand-authored subtitle cues in episode.json."""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from episode_io import load_json, segment_display_text, validate_episode
from japanese_subtitle_semantics import boundary_issues

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover - requirements.txt includes Pillow
    Image = ImageDraw = ImageFont = None  # type: ignore[assignment]

DEFAULT_SAFE_WIDTH = 1800
DEFAULT_CUE_LIMIT = 120
PARTICLE_ONLY = {
    "は", "が", "を", "に", "へ", "で", "と", "の", "も", "や", "ね", "よ",
    "から", "まで", "だけ", "ほど", "しか", "ので", "のに",
}
PROTECTED_TERMS = (
    "マイナアプリ",
    "マイナポータルアプリ",
    "デジタル認証アプリ",
    "マイナンバーカード",
    "利用者証明用暗証番号",
    "Digital Agency of Japan",
    "App Store",
    "Google",
    "Googleフォト",
    "Googleアカウント",
    "Google ドライブ",
    "バックアップ",
    "バックアップ済み",
    "未バックアップ",
    "標準バックアップ",
    "自動バックアップ",
    "プレミアムバックアップ",
    "バックアップ・引き継ぎ",
    "バックアップ用の暗証番号",
    "バックアップ用のPINコード",
    "PINコード",
    "トーク履歴",
    "トークのバックアップ",
    "今すぐバックアップ",
    "メイン端末",
    "引き継ぎガイド",
    "iCloud Drive",
    "LYPプレミアム",
    "セーフティネット",
    "空き容量を増やす",
    "デバイスから削除",
    "最近削除した項目",
    "Google Play",
    "iPhone",
    "Android",
    "YouTube",
    "LINE",
    "NFC",
    "0120-95-0178",
)
INFLECTION_ENDINGS = (
    "確認しま",
    "案内しま",
    "なりま",
    "されま",
    "できま",
    "してい",
    "使え",
    "開け",
)
INFLECTION_CONTINUATIONS = ("す", "せん", "した", "すか", "る", "ない", "ます", "て")


def clean(text: str) -> str:
    return re.sub(r"\s+", "", text)


def _font_measure_context() -> tuple[Any, Any] | None:
    if Image is None or ImageDraw is None or ImageFont is None:
        return None
    candidates = (
        "C:/Windows/Fonts/YuGothB.ttc",
        "C:/Windows/Fonts/meiryob.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
    )
    for candidate in candidates:
        if Path(candidate).exists():
            try:
                font = ImageFont.truetype(candidate, size=72)
                draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
                return draw, font
            except OSError:
                continue
    return None


_MEASURE_CONTEXT = _font_measure_context()


def estimated_width(text: str) -> int:
    if _MEASURE_CONTEXT is not None:
        draw, font = _MEASURE_CONTEXT
        return round(draw.textlength(text, font=font))
    width = 0
    for char in text:
        if char.isascii():
            width += 42 if char.isalnum() else 30
        else:
            width += 72
    return width


def cue_text(subtitle: dict[str, Any]) -> str:
    return "".join(str(line) for line in subtitle.get("text_lines", []))


def check_protected_boundaries(
    subtitles: list[dict[str, Any]],
    segments: dict[int, dict[str, Any]],
    failures: list[str],
) -> None:
    by_segment: dict[int, list[dict[str, Any]]] = {}
    for subtitle in subtitles:
        by_segment.setdefault(int(subtitle["segment_id"]), []).append(subtitle)
    for segment_id, cues in by_segment.items():
        # Layout spaces are viewer-facing typography, not Japanese reading
        # characters.  Use the cleaned stream for boundary positions so an
        # official UI spelling such as 「バックアップ コード」 does not
        # shift the semantic check into the next mora.
        combined = clean("".join(cue_text(cue) for cue in cues))
        boundaries: set[int] = set()
        cursor = 0
        for cue in cues[:-1]:
            cursor += len(clean(cue_text(cue)))
            boundaries.add(cursor)
        for term in PROTECTED_TERMS:
            start = combined.find(term)
            while start >= 0:
                end = start + len(term)
                crossed = [boundary for boundary in boundaries if start < boundary < end]
                if crossed:
                    failures.append(
                        f"seg {segment_id:03d}: 固有名詞を途中分割: {term}"
                    )
                start = combined.find(term, start + 1)


def check_inflection_boundaries(
    subtitles: list[dict[str, Any]],
    failures: list[str],
) -> None:
    by_segment: dict[int, list[dict[str, Any]]] = {}
    for subtitle in subtitles:
        by_segment.setdefault(int(subtitle["segment_id"]), []).append(subtitle)
    for segment_id, cues in by_segment.items():
        for previous, following in zip(cues, cues[1:]):
            left = clean(cue_text(previous))
            right = clean(cue_text(following))
            if any(left.endswith(ending) for ending in INFLECTION_ENDINGS) and any(
                right.startswith(start) for start in INFLECTION_CONTINUATIONS
            ):
                failures.append(
                    f"seg {segment_id:03d}: 動詞活用の不自然分断: "
                    f"{previous['id']} → {following['id']} ({left[-8:]} / {right[:8]})"
                )


def check_semantic_line_breaks(
    subtitles: list[dict[str, Any]],
) -> tuple[dict[str, int], list[str]]:
    """Check every visual and temporal cue boundary with the shared policy.

    A temporal split is also a reading boundary.  It is checked together with
    the visible two-line split so an apparently harmless cue transition cannot
    leave a particle, compound, or inflection stem stranded on the next cue.
    """
    metrics = {
        "unnatural_japanese_line_break": 0,
        "word_split": 0,
        "conjugation_split": 0,
        "particle_or_auxiliary_orphan": 0,
    }
    failures: list[str] = []
    by_segment: dict[int, list[dict[str, Any]]] = {}
    for subtitle in subtitles:
        by_segment.setdefault(int(subtitle["segment_id"]), []).append(subtitle)

    for segment_id, cues in by_segment.items():
        # First scan the visible line breaks inside every cue.
        for cue in cues:
            lines = [str(line) for line in cue.get("text_lines", [])]
            if len(lines) != 2:
                continue
            full = "".join(lines)
            result = boundary_issues(full, len(clean(lines[0])))
            for key, failed in result.items():
                if failed:
                    metrics[key] += 1
                    failures.append(
                        f"{cue['id']} seg {segment_id:03d}: {key} "
                        f"({lines[0]} / {lines[1]})"
                    )

        # Then scan the temporal boundaries between consecutive cues in the
        # same narration segment.
        combined = clean("".join(cue_text(cue) for cue in cues))
        cursor = 0
        for previous in cues[:-1]:
            cursor += len(clean(cue_text(previous)))
            result = boundary_issues(combined, cursor)
            for key, failed in result.items():
                if failed:
                    metrics[key] += 1
                    failures.append(
                        f"{previous['id']} → next seg {segment_id:03d}: {key} "
                        f"({combined[:cursor]} / {combined[cursor:]})"
                    )
    return metrics, failures


def check_tts_reading_leakage(
    subtitles: list[dict[str, Any]],
    segments: dict[int, dict[str, Any]],
) -> list[str]:
    """Ensure TTS-only readings never replace canonical display text."""
    failures: list[str] = []
    by_segment: dict[int, list[dict[str, Any]]] = {}
    for subtitle in subtitles:
        by_segment.setdefault(int(subtitle["segment_id"]), []).append(subtitle)
    for segment_id, segment in segments.items():
        displayed = clean("".join(cue_text(cue) for cue in by_segment.get(segment_id, [])))
        expected_display = clean(segment_display_text(segment))
        if expected_display and displayed != expected_display:
            failures.append(
                f"seg {segment_id:03d}: display_text不一致 "
                f"(expected={segment_display_text(segment)} / actual={displayed})"
            )
        reading_entries = dict(segment.get("reading_overrides") or {})
        for surface, spec in (segment.get("accent_overrides") or {}).items():
            if isinstance(spec, dict) and spec.get("reading"):
                reading_entries[str(surface)] = str(spec["reading"])
        for surface, reading in reading_entries.items():
            reading_clean = clean(str(reading))
            surface_clean = clean(str(surface))
            if reading_clean and reading_clean != surface_clean and reading_clean in displayed:
                failures.append(
                    f"seg {segment_id:03d}: tts_reading_leakage "
                    f"({surface} → {reading})"
                )
    return failures


def run_preflight(
    episode_path: Path,
    report_path: Path,
    safe_width: int = DEFAULT_SAFE_WIDTH,
    cue_limit: int = DEFAULT_CUE_LIMIT,
) -> dict[str, Any]:
    data = load_json(episode_path)
    schema_issues = validate_episode(data)
    if schema_issues:
        raise SystemExit("episode.json validation failed:\n- " + "\n- ".join(schema_issues))
    subtitles = data["subtitles"]
    segments = {int(segment["id"]): segment for segment in data["narration_segments"]}
    failures: list[str] = []
    warnings: list[str] = []

    for subtitle in subtitles:
        subtitle_id = str(subtitle["id"])
        lines = [str(line) for line in subtitle.get("text_lines", [])]
        text = cue_text(subtitle)
        compact = clean(text)
        # 恒久ルール（2026-09-04）: 字幕最小56px（推奨60〜72）。44px等の縮小cueは廃止。
        fs = float(subtitle.get("font_px") or 72)
        if fs < 56:
            failures.append(f"{subtitle_id}: 字幕フォントが基準未満 ({fs:.0f}px < 56px)")
        if len(compact) == 1:
            failures.append(f"{subtitle_id}: 1文字だけのcue")
        if len(compact) <= 2 and compact in PARTICLE_ONLY:
            failures.append(f"{subtitle_id}: 助詞だけの短いcue ({text})")
        for line_index, line in enumerate(lines, 1):
            line_width = estimated_width(line) * fs / 72.0
            if line_width > safe_width:
                failures.append(
                    f"{subtitle_id}: 行長が安全幅を超過 "
                    f"(line {line_index}, estimated {line_width:.0f}px > {safe_width}px @{fs:.0f}px)"
                )
            if len(clean(line)) <= 3:
                warnings.append(f"{subtitle_id}: 1行が極端に短い ({line})")
        if len(lines) == 2:
            widths = [estimated_width(line) for line in lines]
            if max(widths) and min(widths) / max(widths) < 0.35 and len(compact) >= 10:
                warnings.append(f"{subtitle_id}: 2行の長さのバランスが悪い")

    check_protected_boundaries(subtitles, segments, failures)
    check_inflection_boundaries(subtitles, failures)
    semantic_metrics, semantic_failures = check_semantic_line_breaks(subtitles)
    # Keep the alternate wording used by the production checklist while the
    # canonical counter remains particle_or_auxiliary_orphan.
    semantic_metrics["orphan_particle_auxiliary"] = semantic_metrics["particle_or_auxiliary_orphan"]
    failures.extend(semantic_failures)
    leakage_failures = check_tts_reading_leakage(subtitles, segments)
    failures.extend(leakage_failures)
    if len(subtitles) > cue_limit:
        warnings.append(f"cue数が多い ({len(subtitles)} > {cue_limit})")

    status = "FAIL" if failures else "WARN" if warnings else "PASS"
    report_lines = [
        "# Subtitle preflight",
        "",
        f"Episode: {episode_path.parent.name}",
        f"Cues: {len(subtitles)}",
        f"Safe width: {safe_width}px (72px font measurement when available)",
        "",
        "## FAIL",
        "",
    ]
    report_lines.extend(f"- {failure}" for failure in failures) or report_lines.append("- なし")
    report_lines.extend(["", "## WARN", ""])
    report_lines.extend(f"- {warning}" for warning in warnings) or report_lines.append("- なし")
    report_lines.extend(
        [
            "",
        "## tts_reading_leakage",
            "",
            f"- result: {'PASS' if not leakage_failures else 'FAIL'}",
        f"- fail count: {len(leakage_failures)}",
        "",
        "## japanese_semantic_line_break",
        "",
        "- policy: sentence meaning > bunsetsu integrity > modifier relation > visual balance > 72px",
        "- long cues are split in time; font is not reduced to force a fit",
        f"- unnatural_japanese_line_break: {semantic_metrics['unnatural_japanese_line_break']}",
        f"- word_split: {semantic_metrics['word_split']}",
        f"- conjugation_split: {semantic_metrics['conjugation_split']}",
        f"- particle_or_auxiliary_orphan: {semantic_metrics['particle_or_auxiliary_orphan']}",
        f"- orphan_particle_auxiliary: {semantic_metrics['orphan_particle_auxiliary']}",
        f"- result: {'PASS' if not semantic_failures else 'FAIL'}",
        "",
        "## Summary",
            "",
            f"- result: {status}",
            f"- fail count: {len(failures)}",
            f"- warn count: {len(warnings)}",
            "- cue text is read from episode.json; no character-count auto-splitting is performed",
        ]
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    return {
        "status": status,
        "cue_count": len(subtitles),
        "fail_count": len(failures),
        "warn_count": len(warnings),
        "tts_reading_leakage_fail_count": len(leakage_failures),
        "tts_reading_leakage_failures": leakage_failures,
        "japanese_semantic_line_break": semantic_metrics,
        "japanese_semantic_line_break_failures": semantic_failures,
        "report_path": str(report_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("episode", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--safe-width", type=int, default=DEFAULT_SAFE_WIDTH)
    parser.add_argument("--cue-limit", type=int, default=DEFAULT_CUE_LIMIT)
    args = parser.parse_args()
    report = args.report or args.episode.parent / "work" / "subtitle_preflight.md"
    result = run_preflight(args.episode.resolve(), report.resolve(), args.safe_width, args.cue_limit)
    print(
        f"subtitles={result['status']} cues={result['cue_count']} "
        f"fail={result['fail_count']} warn={result['warn_count']}"
    )
    print(f"report={result['report_path']}")
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
