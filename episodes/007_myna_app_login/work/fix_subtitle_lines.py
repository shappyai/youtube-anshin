# -*- coding: utf-8 -*-
"""Episode 007 字幕行の安全幅対応: estimated_width(line) <= 1800 に自然な文節折返しで再分割。

本文（ナレーション・字幕テキストの意味）は変更しない。行分割のみ更新して episode.json を書き換える。
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from episode_io import load_json  # noqa: E402
from subtitle_preflight import estimated_width  # noqa: E402

BASE = ROOT / "episodes" / "007_myna_app_login"
EPISODE = BASE / "episode.json"
LIMIT = 1800
PROTECTED = ["マイナアプリ", "マイナポータル", "マイナンバーカード", "利用者証明用電子証明書",
             "電子証明書", "スマートフォン", "iPhone", "Android", "0120-95-0178", "iOS", "NFC", "NFC"]


def split_natural(text):
    """文節（、。とprotected term）で折返し候補を作る."""
    tokens = []
    buf = ""
    i = 0
    while i < len(text):
        matched = None
        for term in sorted(PROTECTED, key=len, reverse=True):
            if text.startswith(term, i):
                matched = term
                break
        if matched:
            buf += matched
            i += len(matched)
            continue
        ch = text[i]
        buf += ch
        if ch in "、。」！？":
            tokens.append(buf)
            buf = ""
        i += 1
    if buf:
        tokens.append(buf)
    return tokens


def wrap_line(text, limit=LIMIT):
    """文節チャンクをlimit内に組み合わせ自然改行。2行に強制（それ以上は1行目を早めに切る）。"""
    tokens = split_natural(text)
    lines = []
    cur = ""
    for tok in tokens:
        if cur and estimated_width(cur + tok) > limit:
            lines.append(cur)
            cur = tok
        else:
            cur += tok
    if cur:
        lines.append(cur)
    if len(lines) > 2:
        # 2行に強制: 1行目を「等分＋文節優先」で切る
        total_est = sum(estimated_width(ln) for ln in lines)
        half = total_est / 2
        acc = 0
        first = []
        for ln in lines:
            w = estimated_width(ln)
            if acc + w > half and first:
                break
            acc += w
            first.append(ln)
        second = lines[len(first):]
        lines = ["".join(first), "".join(second)]
    # 行頭禁則（、。）を除去
    lines = [ln.lstrip("、。「」") for ln in lines if ln.strip()]
    return lines[:2]


def main():
    data = load_json(EPISODE)
    changed = []
    for sub in data.get("subtitles", []):
        new_lines = []
        for line in sub.get("text_lines", []):
            if estimated_width(line) > LIMIT:
                new_lines.extend(wrap_line(line))
                changed.append(sub["id"])
            else:
                new_lines.append(line)
        sub["text_lines"] = new_lines
    EPISODE.write_text(
        __import__("json").dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("changed cues:", sorted(set(changed)))
    print("total changed:", len(set(changed)))


if __name__ == "__main__":
    main()

