"""Build the human-review pronunciation preview for Episode 009 draft_v2."""
from __future__ import annotations

import csv
import json
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))

from episode_io import load_pronunciation_entries  # noqa: E402
from tts_voicevox import (  # noqa: E402
    apply_pronunciation_overrides,
    make_audio_query,
    refresh_mora_data,
    resolve_speaker,
    synthesize,
)

ENGINE_URL = "http://127.0.0.1:50021"
SPEAKER = "剣崎雌雄"
STYLE = "ノーマル"
EPISODE_ID = "009"
OUT_DIR = ROOT / "episodes" / "009_windows11_24h2_support" / "work" / "phase_b_review" / "pronunciation_fix_v2"

PREVIEWS = [
    ("kata_context", "Windows 11を使っているかた、こちらは人を指す『方』の読みです。", "person context override: 方→かた"),
    ("windows_representative", "Windowsの語末のズを確認します。", "approved accent: ウィンドオズ / peak=ズ"),
    ("update_representative", "Updateの語末のトを確認します。", "approved accent: アップデエト / peak=ト"),
    ("id_representative", "個人名やIDのディを確認します。", "approved accent: アイディイ / peak=ディ"),
    ("windows_update_phrase", "Windows Updateを確認します。", "Windows peak=ズ + Update peak=ト"),
]


def apply_config(query: dict) -> bool:
    changed = apply_pronunciation_overrides(query, episode_id=EPISODE_ID)
    if changed:
        refresh_mora_data(ENGINE_URL, query, 21)
    query["speedScale"] = 1.0
    query["intonationScale"] = 1.0
    query["pitchScale"] = 0.0
    return changed


def phrase_rows(query: dict) -> list[dict]:
    return [
        {
            "moras": [str(mora.get("text") or "") for mora in phrase.get("moras") or []],
            "accent": int(phrase.get("accent") or 0),
        }
        for phrase in query.get("accent_phrases") or []
    ]


def concat_wavs(paths: list[Path], output: Path) -> None:
    frames = bytearray()
    params = None
    gap = None
    for path in paths:
        with wave.open(str(path), "rb") as wav:
            current = wav.getparams()
            if params is None:
                params = current
                gap = b"\x00" * int(wav.getframerate() * 0.35) * wav.getnchannels() * wav.getsampwidth()
            frames.extend(wav.readframes(wav.getnframes()))
        frames.extend(gap or b"")
    output.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output), "wb") as wav:
        wav.setparams(params)
        wav.writeframes(bytes(frames))


def main() -> int:
    _uuid, style_id = resolve_speaker(ENGINE_URL, SPEAKER, STYLE)
    entries = load_pronunciation_entries()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    wav_paths = []
    for name, text, note in PREVIEWS:
        query = make_audio_query(ENGINE_URL, text, style_id)
        changed = apply_config(query)
        wav_path = OUT_DIR / f"{name}.wav"
        synthesize(ENGINE_URL, query, style_id, wav_path)
        query_path = OUT_DIR / f"{name}_audio_query.json"
        query_path.write_text(
            json.dumps(
                {
                    "surface_text": text,
                    "effective_text": text,
                    "speaker": SPEAKER,
                    "style": STYLE,
                    "style_id": style_id,
                    "config_applied": changed,
                    "note": note,
                    "accent_phrases": phrase_rows(query),
                    "query": query,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        wav_paths.append(wav_path)
        rows.append(
            {
                "name": name,
                "text": text,
                "wav_path": str(wav_path.relative_to(ROOT)),
                "query_path": str(query_path.relative_to(ROOT)),
                "config_applied": str(changed).lower(),
                "note": note,
                "status": "human_review_pending",
            }
        )
    all_path = OUT_DIR / "pronunciation_fix_v2_all.wav"
    concat_wavs(wav_paths, all_path)
    manifest = OUT_DIR / "pronunciation_fix_v2_manifest.csv"
    with manifest.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({"status": "PASS", "preview_count": len(rows), "manifest": str(manifest), "all_wav": str(all_path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
