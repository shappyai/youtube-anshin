"""Verify the PIN accent override before narration regeneration."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from tts_voicevox import (  # noqa: E402
    apply_pronunciation_overrides,
    make_audio_query,
    refresh_mora_data,
    resolve_speaker,
)

ENGINE = "http://127.0.0.1:50021"
SEGS = {
    7: "三つ、バックアップ用の暗証番号、PINです。",
    39: "三つ目の確認は、バックアップ用の暗証番号、PINコードです。",
    40: "PINコードは、引き継ぎのときに、トーク履歴を復元するための、6桁の暗証番号です。",
    45: "PINの設定は、「トークのバックアップ」の画面から、できます。",
    66: "三つ、バックアップ用の暗証番号、PIN。直近14日間の、セーフティネットです。",
}


def main() -> None:
    _uuid, sid = resolve_speaker(ENGINE, "剣崎雌雄", "ノーマル")
    lines: list[str] = []
    for seg_id, text in SEGS.items():
        query = make_audio_query(ENGINE, text, sid)
        changed = apply_pronunciation_overrides(query, episode_id="006")
        if changed:
            refresh_mora_data(ENGINE, query, sid)
        lines.append(f"seg {seg_id} changed={changed}")
        for phrase in query.get("accent_phrases", []):
            mora_text = "".join(str(m.get("text") or "") for m in phrase.get("moras", []))
            pitch_text = " ".join(
                f"{m.get('text')}:{m.get('pitch', 0):.3f}" for m in phrase.get("moras", [])
            )
            lines.append(f"  accent={phrase.get('accent')} moras={mora_text}")
            lines.append(f"    pitches: {pitch_text}")
    report = ROOT / "work_tmp_pin_verify.txt"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("done")


if __name__ == "__main__":
    main()
