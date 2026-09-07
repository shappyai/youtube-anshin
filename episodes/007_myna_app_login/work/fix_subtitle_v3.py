# -*- coding: utf-8 -*-
"""draft_v2 字幕再構築: 「小さくして収める」をやめ「時間分割で大きく読む」。

- 44/52px cue（SUB-012/016/020/047）を 1 narration segment → 2 display cue に分割（60px）。
- 分割は句点「。」優先・読点を低優先の意味単位。語中・助詞のみ・protected term途中NG。
- 確保後は全 cue 56px以上（font_px は 60 のみ・44/52を廃止）。
- 字幕テキストはナレーション全文（欠落なし）。
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "episodes" / "007_myna_app_login"
EPISODE = BASE / "episode.json"
LIMIT = 1800


import sys as _sys
_S = str(ROOT / "scripts")
if _S not in _sys.path:
    _sys.path.insert(0, _S)
from subtitle_preflight import estimated_width  # noqa: E402


def est(text, px=60):
    """QA（subtitle_preflight.estimated_width・72px基準1800）と同じ測り方に統一する。"""
    return round(estimated_width(text) * px / 72.0)


def tokens(text):
    out, buf, i = [], "", 0
    while i < len(text):
        ch = text[i]
        buf += ch
        if ch in "、。」":
            out.append(buf)
            buf = ""
        i += 1
    if buf:
        out.append(buf)
    return out


def split_lines(text, px):
    lines, cur = [], ""
    for tok in tokens(text):
        if cur and est(cur + tok, px) > LIMIT:
            lines.append(cur)
            cur = tok
        else:
            cur += tok
    if cur:
        lines.append(cur)
    return lines


def ensure_fit(lines, px):
    """行がLIMITを超える場合にトークン単位で再分割（いかなる行も <= LIMIT を保証）。"""
    out = []
    for line in lines:
        if est(line, px) <= LIMIT:
            out.append(line)
            continue
        cur = ""
        for tok in tokens(line):
            if cur and est(cur + tok, px) > LIMIT:
                out.append(cur)
                cur = tok
            else:
                cur += tok
        if cur:
            out.append(cur)
    return out


def split_cue_pair(text):
    """句点「。」で文節（sentence）に分け、前後のdisplay cueを両方2行以内(60px)に収める分割を選ぶ."""
    sentences = []
    cur = ""
    for ch in text:
        cur += ch
        if ch == "。":
            sentences.append(cur)
            cur = ""
    if cur:
        sentences.append(cur)
    # 前半 cue に取る文節数をスキャン（両cueの行数<=2になる最大）
    best = 1
    for n in range(1, len(sentences)):
        first_text = "".join(sentences[:n])
        second_text = "".join(sentences[n:])
        if not second_text:
            break
        if len(split_lines(first_text, 60)) <= 2 and len(split_lines(second_text, 60)) <= 2:
            best = n
    first_text = "".join(sentences[:best])
    second_text = "".join(sentences[best:])
    if not second_text:
        # 文が1つだけ: 読点境界で前後に分割（60px2行ずつ）
        toks = tokens(text)
        best_t = 1
        for n in range(1, len(toks)):
            if len(split_lines("".join(toks[:n]), 60)) <= 2 and len(split_lines("".join(toks[n:]), 60)) <= 2:
                best_t = n
        first_text = "".join(toks[:best_t])
        second_text = "".join(toks[best_t:])
    return first_text, second_text


def main():
    data = json.loads(EPISODE.read_text(encoding="utf-8"))
    nar = {int(s["id"]): str(s["narration"]) for s in data["narration_segments"]}
    # narration起点の完全再構築（idempotent）
    new_subs = []
    split_ids = []
    for sid, text in sorted(nar.items()):
        f72_lines = ensure_fit(split_lines(text, 72), 72)
        if len(f72_lines) <= 2 and all(est(l, 72) <= LIMIT for l in f72_lines):
            new_subs.append({"id": f"SUB-{sid:03d}", "text_lines": f72_lines, "segment_id": sid})
            continue
        f60_lines = ensure_fit(split_lines(text, 60), 60)
        if len(f60_lines) <= 2 and all(est(l, 60) <= LIMIT for l in f60_lines):
            new_subs.append({"id": f"SUB-{sid:03d}", "text_lines": f60_lines, "segment_id": sid, "font_px": 60})
            continue
        # 60px 2行でも収まらない長文 cue は意味単位で2つの表示cueに分割（時間方向分割）
        first_text, second_text = split_cue_pair(text)
        c1 = {"id": f"SUB-{sid:03d}_1", "text_lines": split_lines(first_text, 60) or [first_text], "segment_id": sid, "font_px": 60}
        c2 = {"id": f"SUB-{sid:03d}_2", "text_lines": split_lines(second_text, 60) or [second_text], "segment_id": sid, "font_px": 60}
        new_subs.extend([c1, c2])
        split_ids.append(sid)
    new_subs.sort(key=lambda c: (int(c["segment_id"]), c["id"]))
    data["subtitles"] = new_subs
    split_ids_out = split_ids
    EPISODE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("split cues (segment ids):", split_ids_out)
    print("total display cues:", len(new_subs))
    bad = []
    for c in new_subs:
        px = int(c.get("font_px") or 72)
        if px < 56:
            bad.append((c["id"], px))
        for l in c["text_lines"]:
            if est(l, px) > LIMIT:
                bad.append((c["id"], "width"))
    print("font<56 or width:", bad)
    # 表示cueをsegmentごとに連結してナレーション全文と一致するか検証
    mm = []
    by_seg = {}
    for c in new_subs:
        by_seg.setdefault(int(c["segment_id"]), []).append(c)
    for seg_id, cues in sorted(by_seg.items()):
        joined = "".join("".join(c["text_lines"]) for c in cues)
        if joined != nar[seg_id]:
            mm.append(seg_id)
    print("narration mismatches:", mm)


if __name__ == "__main__":
    main()
