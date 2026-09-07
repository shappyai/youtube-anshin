# -*- coding: utf-8 -*-
"""v8: 字幕タイミングを「実音声のサンプル数」基準で再構築。

従来は mp3 の ffprobe 推定尺（ビットレート由来）で累積誤差が出た。
v8 では各ユニット/無音/CTA を PCM(24000Hz) にデコードし、サンプル数を数えて
タイムラインを構築する（誤差はフレーム単位以下）。

出力:
- audio/narration_v6.mp3（ユニット+間+CTA+末尾無音、atempo1.06）
- work/timeline_v8.json
- episodes/captions_v8.srt（実音声基準の時刻）
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EP = Path(__file__).resolve().parents[1]
WORK = EP / "work"
RATE = 24000
GAP_SENT, GAP_SECTION, ATEMPO = 0.20, 0.60, 1.06
END_SILENCE = 10.3
CTA_TEXT = "役に立ったら、チャンネル登録して、次回も一緒に確認しましょう。"
OLD = json.loads((WORK / "timeline.json").read_text(encoding="utf-8"))["units"]


def pcm_samples(path: Path) -> int:
    """音声を PCM f32le 24000Hz にデコードしサンプル数を返す（正確な実尺）。"""
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le",
         "-ac", "1", "-ar", str(RATE), "-"],
        capture_output=True)
    if r.returncode != 0:
        raise SystemExit(f"decode failed: {path}")
    return len(r.stdout) // 4


def to_pcm(src: Path, dst: Path) -> None:
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src),
                    "-f", "f32le", "-ac", "1", "-ar", str(RATE), str(dst)], check=True)


def make_pcm(path: Path, seconds: float) -> int:
    """無音 PCM を生成しサンプル数を返す。"""
    n = int(round(seconds * RATE))
    data = b"\x00\x00\x00\x00" * n
    path.write_bytes(data)
    return n


def to_srt(sec: float) -> str:
    ms = int(round((sec - int(sec)) * 1000))
    s = int(sec) % 60
    m = int(sec) // 60 % 60
    h = int(sec) // 3600
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    NEW_TEXT18 = "次は、再設定用の電話番号とメールアドレスを確認します。"
    items = []
    for i, u in enumerate(OLD, 1):
        if i == 19:
            continue
        text = NEW_TEXT18 if i == 18 else u["text"]
        p = EP / "audio" / f"unit_{i:03d}.mp3"
        items.append({"text": text, "section": u["section"], "idx": i,
                      "samples": pcm_samples(p)})
    sil_s = pcm_samples_make(WORK / "v8_sil_s.pcm", GAP_SENT)
    sil_x = pcm_samples_make(WORK / "v8_sil_x.pcm", GAP_SECTION)
    cta_p = EP / "audio" / "cta.mp3"
    cta_samples = pcm_samples(cta_p)
    end_n = make_pcm(WORK / "v8_sil_e.pcm", END_SILENCE)

    # タイムライン（サンプルベース）
    audio_parts = []
    timeline = []
    cursor = 0
    for i, it in enumerate(items):
        it["start"] = cursor / RATE
        cursor += it["samples"]
        it["end"] = cursor / RATE
        timeline.append({**it})
        audio_parts.append((it["idx"], "unit"))
        if i + 1 < len(items):
            gap = GAP_SECTION if items[i + 1]["section"] != it["section"] else GAP_SENT
            cursor += int(round(gap * RATE))
            audio_parts.append((int(round(gap * RATE)), "gap"))
    cursor += int(round(0.8 * RATE))
    cta_start = cursor / RATE
    cta_end = (cursor + cta_samples) / RATE
    cursor += cta_samples
    cursor += end_n
    total = cursor

    # 実音声（PCM を連結 → wav → atempo → mp3）
    pcm_all = WORK / "v8_all.pcm"
    parts = []
    for i, (a, kind) in enumerate(audio_parts):
        if kind == "unit":
            parts.append(EP / "audio" / f"unit_{a:03d}.mp3")
        else:
            parts.append(WORK / ("v8_sil_s.pcm" if a == int(round(GAP_SENT * RATE)) else "v8_sil_x.pcm"))
    parts.append(cta_p)
    parts.append(WORK / "v8_sil_e.pcm")
    pcmdir = WORK / "v8_pcm"
    pcmdir.mkdir(exist_ok=True)
    pcm_list = []
    for i, p in enumerate(parts):
        if p.suffix != ".pcm":
            dst = pcmdir / f"{i:03d}.pcm"
            to_pcm(p, dst)
            pcm_list.append(dst)
        else:
            pcm_list.append(p)
    out = EP / "audio" / "narration_v6.mp3"
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for p in pcm_list:
        cmd += ["-f", "f32le", "-ar", str(RATE), "-ac", "1", "-i", str(p)]
    n = len(pcm_list)
    fc = "".join(f"[{i}:a]" for i in range(n))
    fc += f"concat=n={n}:v=0:a=1[a];[a]atempo={ATEMPO}"
    cmd += ["-filter_complex", fc, "-c:a", "libmp3lame", "-b:a", "128k",
            "-ar", "24000", "-ac", "1", str(out)]
    subprocess.run(cmd, check=True)
    # スケーリング（時刻は 1/atempo）
    for it in timeline:
        it["start"] /= ATEMPO
        it["end"] /= ATEMPO
    cta_start_f = cta_start / ATEMPO
    cta_end_f = cta_end / ATEMPO

    # captions_v8.srt
    lines = []
    for i, it in enumerate(timeline, 1):
        end = it["end"] + 0.25
        lines += [str(i), f"{to_srt(it['start'])} --> {to_srt(end)}", it["text"], ""]
    lines += [str(len(timeline) + 1),
              f"{to_srt(cta_start_f)} --> {to_srt(cta_end_f + 0.15)}", CTA_TEXT, ""]
    (EP / "captions_v8.srt").write_text("\n".join(lines), encoding="utf-8")
    sec_bounds = []
    for it in timeline:
        if not sec_bounds or sec_bounds[-1]["name"] != it["section"]:
            sec_bounds.append({"name": it["section"], "start": it["start"]})
    # 実音声（デコード）を正として時刻を補正（エンコード損失を吸収）
    dec = subprocess.run(["ffmpeg", "-v", "error", "-i", str(out), "-f", "f32le",
                          "-ac", "1", "-ar", str(RATE), "-"], capture_output=True)
    final_sec = (len(dec.stdout) // 4) / RATE
    planned = (total / RATE) / ATEMPO
    factor = final_sec / planned
    print(f"sync factor: {factor:.6f} (final={final_sec:.3f}s planned={planned:.3f}s)")
    for it in timeline:
        it["start"] *= factor
        it["end"] *= factor
    cta_start_f *= factor
    cta_end_f *= factor

    # captions_v8.srt を補正値で書き直し
    lines = []
    for i, it in enumerate(timeline, 1):
        end = it["end"] + 0.25
        lines += [str(i), f"{to_srt(it['start'])} --> {to_srt(end)}", it["text"], ""]
    lines += [str(len(timeline) + 1),
              f"{to_srt(cta_start_f)} --> {to_srt(cta_end_f + 0.15)}", CTA_TEXT, ""]
    (EP / "captions_v8.srt").write_text("\n".join(lines), encoding="utf-8")

    # ---- 検証: silencedetect の実発話開始と字幕開始の比較 ----
    sd = subprocess.run(
        ["ffmpeg", "-i", str(out), "-af",
         "silencedetect=noise=-40dB:d=0.15", "-f", "null", "-"],
        capture_output=True, text=True)
    re_ = __import__("re")
    sil_end = [float(m) for m in re_.findall(r"silence_end: ([0-9.]+)", sd.stderr)]
    speech = [0.0] + sil_end  # 各セグメントの開始 = 直前の無音終了
    # speech[i] の前境界 = speech リストの i 番目（CTA が最後）
    checks = [30, 60, 90, 120, 180, 240, 300, 360, 420, 480]
    ver = []
    all_cues = timeline + [{"start": cta_start_f, "end": cta_end_f, "text": CTA_TEXT}]
    for cc in checks:
        # cc を含む cue を探す
        cue = next((c for c in all_cues if c["start"] <= cc < c["end"] + 0.5), None)
        if cue:
            idx = all_cues.index(cue)
            if idx < len(speech):
                ver.append((cc, round(cue["start"], 2), round(speech[idx], 2),
                            round(cue["start"] - speech[idx], 2)))
    (WORK / "v8_sync_check.txt").write_text(
        "\n".join(f"t={a}s cue={b}s speech={c}s diff={d}s" for a, b, c, d in ver),
        encoding="utf-8")
    print("\n".join(f"t={a}s cue={b}s speech={c}s diff={d}s" for a, b, c, d in ver))

    meta = {
        "total": final_sec,
        "sections": sec_bounds,
        "cta_start": cta_start_f,
        "cta_end": cta_end_f,
        "end_audio_total": final_sec,
        "factor": factor,
    }
    (WORK / "timeline_v8.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2),
                                           encoding="utf-8")
    print(f"narration_v6.mp3 total(audio): {meta['end_audio_total']:.2f}s / "
          f"timeline total: {meta['total']:.2f}s / cues: {len(timeline) + 1}")


def pcm_samples_make(path: Path, seconds: float) -> int:
    return make_pcm(path, seconds)


if __name__ == "__main__":
    main()
