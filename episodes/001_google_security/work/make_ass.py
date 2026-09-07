# -*- coding: utf-8 -*-
"""captions.srt -> captions.ass（v6仕様）

- 字幕ブロックを帯の縦中央 y=985 に固定: {\\an5\\pos(960,985)}
- 禁則処理: 2行目先頭に句読点・閉じ括弧・促音等を置かない/1行目末尾に開き括弧を残さない
- 文節・助詞・句読点・機能語の後で自然改行（単語途中は禁止）
- 安全幅 約1550px（52px・Yu Gothic Bold 前提の実描画幅ベース）
- 2行でも超過する文は TTS 区間内で2つのイベントに分割
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EP = Path(__file__).resolve().parents[1]

HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Yu Gothic,52,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,3,0,5,60,60,45,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

MAXW = 1550
W_JP = 52.0
W_AS = 27.0

# 2行目の先頭に来てはいけない文字（禁則）
FORBID_START = "、。，．」』）】〕〉》！？：；ぁぃぅぇぉゃゅょっー"
# 1行目の末尾に残してはいけない文字（開き括弧等）
FORBID_END = "（「『〔【（"
# この直後に切ると自然な文節境界になる文字（助詞・句読点）
PARTICLE = "はがをにでとものからよりまで、。"
# 機能語（この語尾で切ると自然）
SUFFIXES = [
    "されています", "されます", "できます", "あります", "なります", "います",
    "ください", "しましょう", "します", "ました", "ません", "ます", "です",
    "ないか", "こと", "もの", "ので", "から", "ため", "よう", "場合",
]


def est_w(text: str) -> float:
    w = 0.0
    for ch in text:
        w += W_JP if ord(ch) > 0x2E7F or ch in "（）「」・!?―" else W_AS
    return w


def candidates(text: str) -> list[int]:
    """自然な改行候補位置（禁則を満たすもののみ）。"""
    out = []
    n = len(text)
    for p in range(1, n):
        if text[p] in FORBID_START:
            continue
        if text[p - 1] in FORBID_END:
            continue
        if n - p < 2:
            continue  # 1文字だけ次行へ送らない
        pre = text[p - 1]
        ok = pre in PARTICLE
        if not ok:
            for sfx in SUFFIXES:
                if text[:p].endswith(sfx):
                    ok = True
                    break
        if ok:
            out.append(p)
    return out


def wrap(text: str) -> list[str] | None:
    """自然改行して最大2行。2行でも収まらない場合は None（イベント分割へ）。"""
    if est_w(text) <= MAXW:
        return [text]
    best = None
    for p in candidates(text):
        l1, l2 = text[:p], text[p:]
        w1, w2 = est_w(l1), est_w(l2)
        if w1 > MAXW or w2 > MAXW:
            continue
        score = abs(w1 - w2)
        if best is None or score < best[0]:
            best = (score, l1, l2)
    if best:
        return [best[1], best[2]]
    return None


def split_point(text: str) -> int:
    """禁則を守りつつ、なるべく半分付近で切るイベント分割用の位置。"""
    half = est_w(text) / 2.0
    cands = candidates(text)
    best = None
    for p in cands:
        score = abs(est_w(text[:p]) - half)
        if p < 4 or len(text) - p < 4:
            continue
        if best is None or score < best[0]:
            best = (score, p)
    if best:
        return best[1]
    # 保険: 幅ベースの機械分割（禁則を可能な限り尊重）
    acc = 0.0
    cut = max(1, len(text) // 2)
    for i, ch in enumerate(text):
        if acc >= half:
            while cut < len(text) and text[cut] in FORBID_START:
                cut += 1
            break
        acc += W_JP if ord(ch) > 0x2E7F else W_AS
        cut = i
    return max(cut, 1)


def ts(sec: float) -> str:
    ms = int(round(sec * 100))
    return f"{ms // 360000}:{(ms % 360000) // 6000:02d}:{(ms % 6000) // 100:02d}.{ms % 100:02d}"


def main():
    srt = (EP / "captions.srt").read_text(encoding="utf-8")
    blocks = re.split(r"\n\s*\n", srt.strip())
    out = [HEADER]
    n_split = 0
    for b in blocks:
        lines = [l for l in b.splitlines() if l.strip()]
        if len(lines) < 3 or not lines[0].strip().isdigit():
            continue
        m = re.match(r"(\d+):(\d+):(\d+),(\d+)\s*-->\s*(\d+):(\d+):(\d+),(\d+)", lines[1])
        if not m:
            continue

        def to_sec(g):
            h, mi, s, ms = map(int, g)
            return h * 3600 + mi * 60 + s + ms / 1000.0

        start = to_sec(m.groups()[:4])
        end = to_sec(m.groups()[4:])
        text = "".join(lines[2:]).strip()
        dur = end - start
        wrapped = wrap(text)
        if wrapped:
            events = [(start, end, "\\N".join(wrapped))]
        else:
            # イベント分割（元のTTS区間内で自然に時間配分）
            pos = split_point(text)
            if pos <= 0 or pos >= len(text):
                events = [(start, end, text)]
            else:
                l1 = text[:pos].rstrip("、。")
                l2 = text[pos:].lstrip()
                w1 = est_w(l1)
                frac = w1 / (w1 + est_w(l2))
                mid = start + dur * frac
                e1 = wrap(l1) or [l1]
                e2 = wrap(l2) or [l2]
                events = [
                    (start, mid, "\\N".join(e1)),
                    (mid, end, "\\N".join(e2)),
                ]
                n_split += 1
        for st, en, t in events:
            if en <= st or not t:
                continue
            out.append(
                f"Dialogue: 0,{ts(st)},{ts(en)},Default,,0,0,45,,"
                f"{{\\an5\\pos(960,985)}}{t}")
    (EP / "captions.ass").write_text("\n".join(out) + "\n", encoding="utf-8")
    dlg = sum(1 for l in out if l.startswith("Dialogue:"))
    print(f"captions.ass written ({dlg} cues / split_events={n_split})")


if __name__ == "__main__":
    main()
