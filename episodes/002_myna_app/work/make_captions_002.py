# -*- coding: utf-8 -*-
"""captions for episode 002 — VOICEVOX実測タイムライン（segments_manifest.csv）基準。

デザインは001 v10継承: Yu Gothic 72px・白・黒アウトライン3・下部専用帯
pos(960,980)・最大2行・禁則処理。長文は幅上限(1700px)で複数cueに分割し、
発話時間を幅按分で割り当てる（実測タイミングベース）。
"""
import csv
import sys
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EP = Path(__file__).resolve().parents[1]
MANIFEST = EP / "audio" / "voicevox_kenzaki" / "segments_manifest.csv"
OUT_ASS = EP / "captions_v1.ass"
OUT_SRT = EP / "captions_v1.srt"

HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Yu Gothic,72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,3,0,5,60,60,45,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
W_JP, W_AS = 72.0, 36.0
MAX_LINE = 1780
CHUNK_MAX = 1700
FORBID_START = "、。，．」』）】〕〉》！？：；ぁぃぅぇぉゃゅょっー"
FORBID_END = "（「『〔【"
PARTICLE = "はがをにでとものからよりまで、。"


def est_w(t):
    return sum(W_JP if ord(c) > 0x2E7F or c in "（）「」・!?―" else W_AS for c in t)


def cands(text):
    out = []
    n = len(text)
    for p in range(1, n):
        if text[p] in FORBID_START:
            continue
        if text[p - 1] in FORBID_END:
            continue
        if n - p < 2:
            continue
        if text[p - 1] in PARTICLE:
            out.append(p)
    return out


def split_cues(text, maxw=CHUNK_MAX):
    """単一cue幅をmaxw以下に保つよう、文を意味の切れ目で分割する。"""
    chunks = []
    rest = text
    while rest:
        if est_w(rest) <= maxw:
            chunks.append(rest)
            break
        bestp = None
        for p in cands(rest):
            if p < 6:
                continue
            w1 = est_w(rest[:p])
            if w1 > maxw:
                continue
            bestp = p  # 最後の（最も進んだ）許容境界を採用
        if bestp is None:
            acc, cut = 0.0, 0
            for i, ch in enumerate(rest):
                acc += W_JP if ord(ch) > 0x2E7F else W_AS
                if acc >= maxw * 0.9:
                    cut = i + 1
                    break
            bestp = max(cut, 1)
        chunks.append(rest[:bestp].rstrip("、。"))
        rest = rest[bestp:].lstrip()
    return chunks


def display_lines(chunk):
    """1 cue内を最大2行に分割（中央寄りの意味境界）。"""
    w = est_w(chunk)
    if w <= 1250:
        return [chunk]
    best = None
    for p in cands(chunk):
        if p < 4 or len(chunk) - p < 4:
            continue
        sc = abs(est_w(chunk[:p]) - w / 2)
        if best is None or sc < best[0]:
            best = (sc, p)
    if best:
        p = best[1]
        return [chunk[:p].rstrip("、。"), chunk[p:].lstrip()]
    return [chunk]


def ts_ass(sec):
    ms = int(round(sec * 100))
    return f"{ms // 360000}:{(ms % 360000) // 6000:02d}:{(ms % 6000) // 100:02d}.{ms % 100:02d}"


def ts_srt(sec):
    ms = int(round(sec * 1000))
    return f"{ms // 3600000:02d}:{(ms % 3600000) // 60000:02d}:{(ms % 60000) // 1000:02d},{ms % 1000:03d}"


def main() -> int:
    with MANIFEST.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    out = [HEADER]
    srt_events = []
    n_split = 0
    for r in rows:
        start = float(r["start_sec"])
        end = float(r["end_sec"])
        text = r["text"].strip()
        dur = end - start
        if dur <= 0:
            continue
        chunks = split_cues(text)
        widths = [est_w(c) for c in chunks]
        total_w = sum(widths)
        acc = 0.0
        for c, wd in zip(chunks, widths):
            st = start + dur * (acc / total_w)
            acc += wd
            en = start + dur * (acc / total_w)
            t = "\\N".join(display_lines(c))
            out.append(f"Dialogue: 0,{ts_ass(st)},{ts_ass(en)},Default,,0,0,45,,{{\\an5\\pos(960,980)}}{t}")
            srt_events.append((st, en, t.replace("\\N", "\n")))
        if len(chunks) > 1:
            n_split += len(chunks) - 1
    OUT_ASS.write_text("\n".join(out) + "\n", encoding="utf-8")
    srt_lines = []
    for i, (st, en, t) in enumerate(srt_events, 1):
        srt_lines.append(f"{i}\n{ts_srt(st)} --> {ts_srt(en)}\n{t}\n")
    OUT_SRT.write_text("\n".join(srt_lines), encoding="utf-8")
    print(f"captions_v1.ass: {len(srt_events)} cues / split={n_split}")
    print(f"captions_v1.srt: {len(srt_events)} cues")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
