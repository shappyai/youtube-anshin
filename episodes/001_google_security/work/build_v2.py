# -*- coding: utf-8 -*-
"""第2稿 draft_v2.mp4 組み立て（一回限りのビルド補助）。

- 冒頭カード（5つの安全チェック一覧）
- 各セクション開始の見出しカード（1/5〜5/5）
- 左情報パネル（番号・項目名・要点）＋右にスマホ画面（モザイク済み静止画）
- 音声 narration_v2.mp3 と同期（work/timeline.json のセクション境界を使用）
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
AUDIO = EP / "audio" / "narration_v2.mp3"
OUT = EP / "output" / "draft_v2.mp4"
FONT = "font.ttc"  # work/ にコピー済み（cwd=work で解決）

BG = "0xF7F5F2"
ACCENT = "0x2E6DA4"
DARK = "0x1F2A37"
GRAY = "0x5B6570"

HEADER_MS = 1.8  # 見出しカードの表示秒


def tl() -> dict:
    return json.loads((WORK / "timeline.json").read_text(encoding="utf-8"))


def dt(text: str, size: int, color: str, x: int, y: int, fname: str) -> str:
    (WORK / fname).write_text(text, encoding="utf-8")
    return (
        f"drawtext=fontfile={FONT}:textfile={fname}:"
        f"fontsize={size}:fontcolor={color}:x={x}:y={y}:expansion=none"
    )


def render(kind: str, dur: float, out: Path, texts, phone: str | None = None,
           underline: tuple[int, int, int] | None = None):
    """kind: intro / header / panel。texts: (text,size,color,x,y) のリスト。"""
    tf = []
    for i, (t, size, color, x, y) in enumerate(texts):
        tf.append(dt(t, size, color, x, y, f"txt_{out.stem}_{i}.txt"))
    if underline:
        dx, dy, dw = underline
        tf.append(f"drawbox=x={dx}:y={dy}:w={dw}:h=6:color={ACCENT}:t=fill")
    if phone:
        cmd = [
            "ffmpeg", "-y", "-v", "error",
            "-f", "lavfi", "-i", f"color=c={BG}:s=1920x1080:r=30:d={dur}",
            "-loop", "1", "-framerate", "30", "-t", f"{dur}", "-i", str(Path(phone)),
            "-filter_complex",
            f"[1:v]scale=445:1000[ph];[0:v][ph]overlay=1350:40:shortest=1[comp];[comp]{','.join(tf)}",
            "-an", "-c:v", "libx264", "-crf", "19", "-preset", "medium", out.name,
        ]
    else:
        cmd = [
            "ffmpeg", "-y", "-v", "error",
            "-f", "lavfi", "-i", f"color=c={BG}:s=1920x1080:r=30:d={dur}",
            "-vf", ",".join(tf),
            "-an", "-c:v", "libx264", "-crf", "19", "-preset", "medium", out.name,
        ]
    subprocess.run(cmd, check=True, cwd=WORK)
    print(f"rendered {out.name} ({dur:.1f}s)")


def main():
    t = tl()
    secs = t["sections"]
    sec_start = {s["name"]: round(s["start"], 2) for s in secs}
    total = round(t["total"], 2)
    order = ["はじめに", "1. セキュリティ診断", "2. 再設定用の電話番号・メール",
             "3. 2段階認証とパスキー", "4. 心当たりのない端末",
             "5. Googleでログインしたサービス", "まとめ"]
    spans = []
    for i, name in enumerate(order):
        st = sec_start.get(name, 0.0)
        en = sec_start.get(order[i + 1], total) if i + 1 < len(order) else total
        spans.append({"name": name, "start": st, "end": en})

    parts = []  # (kind, dur, texts, phone, underline)

    # --- 冒頭カード（はじめに）---
    intro_dur = spans[0]["end"] - spans[0]["start"]
    intro_texts = [
        ("大人のデジタル安心室", 34, GRAY, 825, 140),
        ("今日はGoogleアカウントの", 64, DARK, 560, 240),
        ("5つの安全チェックを一緒に確認します", 64, DARK, 400, 330),
        ("1. セキュリティ診断", 44, DARK, 700, 520),
        ("2. 再設定用の電話番号・メール", 44, DARK, 700, 600),
        ("3. 2段階認証とパスキー", 44, DARK, 700, 680),
        ("4. ログイン中の端末", 44, DARK, 700, 760),
        ("5. リンク済みアプリ", 44, DARK, 700, 840),
        ("この5つを順番に確認していきます", 40, ACCENT, 590, 950),
    ]
    parts.append(("intro", intro_dur, intro_texts, None, None))

    # --- セクション定義 ---
    sections = [
        {"num": "1 / 5", "name": "セキュリティ診断", "key": "まずセキュリティ診断を確認",
         "still_a": "s01_security.png", "still_b": "s01_checkup.png", "split": 0.5},
        {"num": "2 / 5", "name": "再設定用の電話番号・メール", "key": "再設定用の連絡先を確認",
         "still_a": "s02_phone.png", "still_b": "s02b_email.png", "split": 0.5},
        {"num": "3 / 5", "name": "2段階認証とパスキー", "key": "2段階認証とパスキーを確認",
         "still_a": "s03_top.png", "still_b": "s03_methods.png", "split": 0.4},
        {"num": "4 / 5", "name": "ログイン中の端末", "key": "知らない端末がないか確認",
         "still_a": "s04_devices.png", "still_b": None, "split": 1.0},
        {"num": "5 / 5", "name": "リンク済みアプリ", "key": "接続中のアプリを確認",
         "still_a": "s05_conn.png", "still_b": None, "split": 1.0},
    ]

    for idx, (span, sec) in enumerate(zip(spans[1:6], sections)):
        dur = span["end"] - span["start"]
        header_dur = min(HEADER_MS, dur - 1.0)
        panel_dur = dur - header_dur
        # 見出しカード
        parts.append(("header", header_dur, [
            ("大人のデジタル安心室", 30, GRAY, 780, 160),
            (sec["num"], 132, ACCENT, 810, 280),
            (sec["name"], 62, DARK, 560, 470),
        ], None, (760, 620, 400)))
        # 本編パネル（a/b 分割）
        if sec["still_b"] is None:
            d_a, d_b = panel_dur, 0.0
        else:
            split = min(max(sec["split"], 0.25), 0.75)
            d_a = panel_dur * split
            d_b = panel_dur - d_a
        for sub in ("a", "b"):
            still = sec["still_a"] if sub == "a" else sec["still_b"]
            if still is None:
                continue
            d = d_a if sub == "a" else d_b
            if d < 1.0:
                continue
            parts.append(("panel", d, [
                ("Googleアカウント 安全チェック", 32, ACCENT, 88, 90),
                (sec["num"], 84, DARK, 84, 150),
                (sec["name"], 50, DARK, 88, 300),
                (sec["key"], 36, GRAY, 88, 430),
                ("大人のデジタル安心室", 28, GRAY, 88, 990),
            ], still, None))

    # --- まとめ ---
    sum_span = spans[6]
    dur = sum_span["end"] - sum_span["start"]
    header_dur = min(HEADER_MS, dur - 1.0)
    parts.append(("header", header_dur, [
        ("大人のデジタル安心室", 30, GRAY, 780, 160),
        ("まとめ", 120, ACCENT, 790, 300),
        ("5つの確認項目をおさらいしましょう", 46, DARK, 560, 490),
    ], None, (760, 640, 400)))
    parts.append(("panel", dur - header_dur, [
        ("Googleアカウント 安全チェック", 32, ACCENT, 88, 90),
        ("まとめ", 84, DARK, 84, 150),
        ("見覚えのないものがないか確認", 50, DARK, 88, 300),
        ("これで5項目すべての確認が終わりました", 36, GRAY, 88, 430),
        ("大人のデジタル安心室", 28, GRAY, 88, 990),
    ], "s01_checkup.png", None))

    # --- レンダリング ---
    out_parts = []
    for i, (kind, d, texts, phone, ul) in enumerate(parts, 1):
        p = WORK / f"v2_{i:02d}_{kind}.mp4"
        render(kind, round(d, 3), p, texts, phone, ul)
        out_parts.append(p)
    lst = WORK / "v2_concat.txt"
    lst.write_text("\n".join(f"file '{p.name}'" for p in out_parts), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c", "copy", str(WORK / "v2_video.mp4")], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(WORK / "v2_video.mp4"),
                    "-i", str(AUDIO), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", str(OUT)], check=True)
    print(f"draft_v2.mp4 written: {OUT}")


if __name__ == "__main__":
    main()
