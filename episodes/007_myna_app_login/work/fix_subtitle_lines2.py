# -*- coding: utf-8 -*-
"""Episode 007 字幕 cue の2行化＋長文cueのみ font_px=60。

- 現状の3〜4行 cue（SUB-012/016/047/051 等）を2行へ。
- 72px換算で2行(50字)に収まらない長文cueは font_px=60（60px×30字=1800px）で2行に収める。
- 本文（ナレーションとの一致）は不変。行分割のみ変更し、長文cueに font_px を付与する。
"""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "episodes" / "007_myna_app_login"
EPISODE = BASE / "episode.json"
LIMIT = 1800
PROTECTED = ["マイナアプリ", "マイナポータル", "マイナンバーカード", "利用者証明用電子証明書",
             "電子証明書", "スマートフォン", "iPhone", "Android", "0120-95-0178", "iOS", "NFC"]


def est(text, px=72):
    w = 0
    for ch in text:
        if ch.isascii():
            w += int(42 * px / 72) if ch.isalnum() else int(30 * px / 72)
        else:
            w += px
    return w


def tokens(text):
    out, buf, i = [], "", 0
    while i < len(text):
        m = None
        for term in sorted(PROTECTED, key=len, reverse=True):
            if text.startswith(term, i):
                m = term
                break
        if m:
            buf += m
            i += len(m)
            continue
        ch = text[i]
        buf += ch
        if ch in "、。」！？":
            out.append(buf)
            buf = ""
        i += 1
    if buf:
        out.append(buf)
    return out


def split_into_lines(text, px):
    """文節トークンを積み、行幅<=LIMIT（px基準）で分割。行は多くても3は避け、pxが60なら2行目標."""
    toks = tokens(text)
    lines = []
    cur = ""
    for tok in toks:
        if not tok:
            continue
        if cur and est(cur + tok, px) > LIMIT:
            lines.append(cur)
            cur = tok
        elif not cur and est(tok, px) > LIMIT:
            # 1チャンク自体が超過 → 文字単位分割（ASCII token保護）
            sub = ""
            for c in tok:
                if sub and est(sub + c, px) > LIMIT and not (c.isascii() and sub[-1].isascii()):
                    lines.append(sub)
                    sub = c
                else:
                    sub += c
            if sub:
                cur = sub
        else:
            cur += tok
    if cur:
        lines.append(cur)
    return lines


def main():
    data = json.loads(EPISODE.read_text(encoding="utf-8"))
    changed = []
    nar_by_id = {int(s["id"]): str(s["narration"]) for s in data["narration_segments"]}
    for sub in data.get("subtitles", []):
        # 字幕はナレーション全文が正（過去の分割バグで欠落したcueを修復するためnarrationから再構築）
        text = nar_by_id.get(int(sub.get("segment_id") or -1), "".join(str(l) for l in sub.get("text_lines", [])))
        current = sub.get("text_lines", [])
        # 現状で2行以内・各行72px基準OK・ナレーションと完全一致なら維持（欠落・改変の自動検知）
        current_text = "".join(str(l) for l in current)
        if len(current) <= 2 and all(est(l) <= LIMIT for l in current) and current_text == text:
            sub.pop("font_px", None)
            continue
        # 72pxで2行に収まるか
        lines72 = split_into_lines(text, 72)
        if len(lines72) <= 2 and all(est(l) <= LIMIT for l in lines72):
            sub["text_lines"] = lines72
            sub.pop("font_px", None)
            changed.append(sub["id"])
            continue
        # 60pxで2行に収める：文節トークン境界で分割し、両行ともにest<=LIMITになる位置を選ぶ（行頭句点なし・欠落なし）
        toks = tokens(text)
        acc = 0
        candidates = []
        for t in toks:
            acc += len(t)
            candidates.append(acc)
        best = None
        px = 60
        for trial_px in (60, 52, 44):
            found = None
            for pos in candidates:
                if est(text[:pos], trial_px) <= LIMIT and est(text[pos:], trial_px) <= LIMIT and 0 < pos < len(text):
                    found = pos
                    break
            if found is not None:
                best, px = found, trial_px
                break
        if best is None:
            # 最終手段: 52pxでも不可なら30字境界（字幕表示上は帯内に収める）
            ok = [p for p in candidates if p <= 40]
            best = max(ok) if ok else 30
            px = 44
        sub["text_lines"] = [text[:best], text[best:]]
        sub["font_px"] = px
        changed.append(sub["id"])
    EPISODE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("adjusted cues:", changed)
    # 検証
    bad = []
    for c in data["subtitles"]:
        px = int(c.get("font_px") or 72)
        for l in c["text_lines"]:
            if est(l, px) > LIMIT:
                bad.append((c["id"], l, est(l, px)))
    print("over-limit:", bad)
    nar = {int(s["id"]): re.sub(r"\s", "", s["narration"]) for s in data["narration_segments"]}
    mm = []
    for c in data["subtitles"]:
        joined = re.sub(r"\s", "", "".join(c["text_lines"]))
        if joined != nar[int(c["segment_id"])]:
            mm.append(c["id"] + ":" + joined[:12] + " != " + nar[int(c["segment_id"])][:12])
    print("narration mismatches:", mm)


if __name__ == "__main__":
    main()
