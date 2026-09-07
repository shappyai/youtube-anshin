# -*- coding: utf-8 -*-
"""draft_v2 発音修正preview: seg 13(NFC)/17(PIN)/26(上)/32(方)/40(方) の effective textで
audio_query・synthesisを行い、accent_phrasesを確認する。"""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from episode_io import load_json, load_pronunciation_entries  # noqa: E402
from tts_voicevox import resolve_speaker, make_audio_query  # noqa: E402
from voicevox_incremental import synthesize  # noqa: E402
from voicevox_preflight import expected_reading  # noqa: E402

ENGINE = "http://127.0.0.1:50021"
BASE = ROOT / "episodes" / "007_myna_app_login"
OUT = BASE / "work" / "phase_b_review" / "pronunciation_fix_v2"
OUT.mkdir(parents=True, exist_ok=True)
data = load_json(BASE / "episode.json")
entries = load_pronunciation_entries()
segments = {int(s["id"]): s for s in data["narration_segments"]}
targets = [13, 17, 26, 32, 40]
style_id = None
for sid in targets:
    seg = segments[sid]
    effective, approvals = expected_reading(seg, entries, "007")
    if style_id is None:
        _uuid, style_id = resolve_speaker(ENGINE, "剣崎雌雄", "ノーマル")
    query = make_audio_query(ENGINE, effective, style_id)
    # accent_phrases法（NFC/PIN等）のoverrideを適用したqueryも保存・表示する
    from voicevox_incremental import apply_pronunciation_overrides  # noqa: E402
    applied = json.loads(json.dumps(query))
    apply_pronunciation_overrides(applied, episode_id="007")  # in-place
    wav = OUT / f"seg_{sid:03d}.wav"
    synthesize(ENGINE, effective, style_id, wav, episode_id="007")
    (OUT / f"seg_{sid:03d}_query_raw.json").write_text(json.dumps(query, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / f"seg_{sid:03d}_query_applied.json").write_text(json.dumps(applied, ensure_ascii=False, indent=2), encoding="utf-8")
    aps = []
    for ap in applied.get("accent_phrases", []):
        kana = "".join(m.get("text", "") for m in ap.get("moras", []))
        aps.append(f"{kana}(accent={ap.get('accent')})")
    print(f"seg {sid}: eff={effective[:48]}…")
    print(f"   approvals={approvals}")
    print(f"   applied_query={aps}")
    print(f"   saved={wav.name}")
