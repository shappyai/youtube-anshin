# -*- coding: utf-8 -*-
"""第3稿 draft_v3.mp4 組み立て。

- 冒頭: 仮ビジュアル（intro_visual.png・差し替え可能）+ 5項目一覧
- 見出しカード: 完全中央揃え（drawtext の x=(w-text_w)/2 を利用）
- 本編: スマホ画面を中央に大きく配置（左パネルなし）+ 左上に小さく「n / 5」のみ
- エンディングCTA（cta_visual.png + 文言 + チャンネル名）
- 字幕帯（下部・半透明）＋ captions.srt 全80コマを焼き込み
- 音声: audio/narration_v3.mp3
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
AUDIO = EP / "audio" / "narration_v3.mp3"
OUT = EP / "output" / "draft_v3.mp4"
FONT = "font.ttc"

BG = "0xF7F5F2"
ACCENT = "0x2E6DA4"
DARK = "0x1F2A37"
GRAY = "0x5B6570"
HEADER_MS = 1.8


def tl() -> dict:
    return json.loads((WORK / "timeline.json").read_text(encoding="utf-8"))


def dt(text: str, size: int, color: str, x, y: int, fname: str) -> str:
    (WORK / fname).write_text(text, encoding="utf-8")
    return (
        f"drawtext=fontfile={FONT}:textfile={fname}:"
        f"fontsize={size}:fontcolor={color}:x={x}:y={y}:expansion=none"
    )


def render(dur: float, out: Path, texts, phone: str | None = None,
           visual: str | None = None, underline: bool = False,
           vscale=(528, 297), vpos=(696, 118)):
    tf = []
    for i, (t, size, color, x, y) in enumerate(texts):
        tf.append(dt(t, size, color, x, y, f"txt3_{out.stem}_{i}.txt"))
    if underline:
        tf.append(f"drawbox=x=760:y=730:w=400:h=6:color={ACCENT}:t=fill")
    inputs = ["ffmpeg", "-y", "-v", "error",
              "-f", "lavfi", "-i", f"color=c={BG}:s=1920x1080:r=30:d={dur}"]
    if phone:
        inputs += ["-loop", "1", "-framerate", "30", "-t", f"{dur}", "-i", str(Path(phone))]
    if visual:
        inputs += ["-loop", "1", "-framerate", "30", "-t", f"{dur}", "-i", str(Path(visual))]
    # 合成（phone / visual のオーバーレイ → テキスト）
    fc = ""
    tail = ", ".join(tf)
    if phone and not visual:
        fc = f"[1:v]scale=414:930[ph];[0:v][ph]overlay=753:15:shortest=1[comp];[comp]{','.join(tf)}"
    elif visual and not phone:
        fc = (f"[1:v]scale={vscale[0]}:{vscale[1]}[vs];"
              f"[0:v][vs]overlay={vpos[0]}:{vpos[1]}:shortest=1[comp];[comp]{','.join(tf)}")
    else:
        fc = f"[0:v]{','.join(tf)}"
    inputs += ["-filter_complex", fc, "-an", "-c:v", "libx264", "-crf", "19",
               "-preset", "medium", out.name]
    subprocess.run(inputs, check=True, cwd=WORK)
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

    parts = []

    # --- 冒頭（ビジュアル＋5項目一覧）---
    intro_dur = spans[0]["end"] - spans[0]["start"]
    intro_texts = [
        ("大人のデジタル安心室", 30, GRAY, "(w-text_w)/2", 62),
        ("今日はGoogleアカウントの", 58, DARK, "(w-text_w)/2", 392),
        ("5つの安全チェックを一緒に確認します", 58, DARK, "(w-text_w)/2", 466),
        ("1. セキュリティ診断", 40, DARK, "(w-text_w)/2", 556),
        ("2. 再設定用の電話番号・メール", 40, DARK, "(w-text_w)/2", 624),
        ("3. 2段階認証とパスキー", 40, DARK, "(w-text_w)/2", 692),
        ("4. ログイン中の端末", 40, DARK, "(w-text_w)/2", 760),
        ("5. リンク済みアプリ", 40, DARK, "(w-text_w)/2", 828),
        ("この5つを順番に確認していきます", 38, ACCENT, "(w-text_w)/2", 908),
    ]
    parts.append(("intro", intro_dur, intro_texts, None, "intro_visual.png", False,
                  (470, 264), (725, 104)))

    # --- セクション ---
    sections = [
        {"num": "1 / 5", "name": "セキュリティ診断",
         "still_a": "s01_security.png", "still_b": "s01_checkup.png", "split": 0.5},
        {"num": "2 / 5", "name": "再設定用の電話番号・メール",
         "still_a": "s02_phone.png", "still_b": "s02b_email.png", "split": 0.5},
        {"num": "3 / 5", "name": "2段階認証とパスキー",
         "still_a": "s03_top.png", "still_b": "s03_methods.png", "split": 0.4},
        {"num": "4 / 5", "name": "ログイン中の端末",
         "still_a": "s04_devices.png", "still_b": None, "split": 1.0},
        {"num": "5 / 5", "name": "リンク済みアプリ",
         "still_a": "s05_conn.png", "still_b": None, "split": 1.0},
    ]
    for span, sec in zip(spans[1:6], sections):
        dur = span["end"] - span["start"]
        header_dur = min(HEADER_MS, dur - 1.0)
        panel_dur = dur - header_dur
        parts.append(("header", header_dur, [
            ("大人のデジタル安心室", 28, GRAY, "(w-text_w)/2", 292),
            (sec["num"], 120, ACCENT, "(w-text_w)/2", 368),
            (sec["name"], 58, DARK, "(w-text_w)/2", 570),
        ], None, None, True))
        if sec["still_b"] is None:
            d_a, d_b = panel_dur, 0.0
        else:
            split = min(max(sec["split"], 0.25), 0.75)
            d_a = panel_dur * split
            d_b = panel_dur - d_a
        for sub, d, still in (("a", d_a, sec["still_a"]), ("b", d_b, sec["still_b"])):
            if still is None or d < 1.0:
                continue
            parts.append(("panel", d, [
                (sec["num"], 40, DARK, 48, 36),
            ], still, None, False))

    # --- まとめ ---
    sum_span = spans[6]
    dur = sum_span["end"] - sum_span["start"]
    header_dur = min(HEADER_MS, dur - 1.0)
    parts.append(("header", header_dur, [
        ("大人のデジタル安心室", 28, GRAY, "(w-text_w)/2", 292),
        ("まとめ", 110, ACCENT, "(w-text_w)/2", 368),
        ("5つの確認項目をおさらいしましょう", 44, DARK, "(w-text_w)/2", 570),
    ], None, None, True))
    parts.append(("panel", dur - header_dur, [
        ("まとめ", 40, DARK, 48, 36),
    ], "s01_checkup.png", None, False))

    # --- エンディングCTA（ナレーション後）---
    meta = json.loads((WORK / "outro_meta.json").read_text(encoding="utf-8"))
    outro_dur = meta["video_after_v2"]
    parts.append(("outro", outro_dur, [
        ("役に立ったら、", 58, DARK, "(w-text_w)/2", 470),
        ("チャンネル登録して", 58, DARK, "(w-text_w)/2", 548),
        ("次回も一緒に確認しましょう", 58, DARK, "(w-text_w)/2", 626),
        ("大人のデジタル安心室", 46, ACCENT, "(w-text_w)/2", 760),
    ], None, "cta_visual.png", False))

    # --- レンダリング＆連結 ---
    out_parts = []
    for i, (kind, d, texts, phone, visual, ul, *vx) in enumerate(parts, 1):
        p = WORK / f"v3_{i:02d}_{kind}.mp4"
        vs = vx[0] if len(vx) > 0 else (528, 297)
        vp = vx[1] if len(vx) > 1 else (696, 118)
        render(round(d, 3), p, texts, phone, visual, ul, vs, vp)
        out_parts.append(p)
    lst = WORK / "v3_concat.txt"
    lst.write_text("\n".join(f"file '{p.name}'" for p in out_parts), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c", "copy", str(WORK / "v3_video.mp4")], check=True, cwd=WORK)
    # 字幕帯＋全字幕焼き込み＋音声
    subprocess.run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(WORK / "v3_video.mp4"), "-i", str(AUDIO),
        "-vf", "drawbox=x=0:y=945:w=1920:h=135:color=0x1F2A37@0.45:t=fill,"
               "subtitles=captions.srt:force_style='FontName=Yu Gothic,FontSize=35,"
               "PrimaryColour=&H00FFFFFF,Outline=1,Shadow=0,Alignment=2,MarginV=30'",
        "-c:v", "libx264", "-crf", "19", "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k", "-shortest", str(OUT)],
        check=True, cwd=EP)
    print(f"draft_v3.mp4 written: {OUT}")


if __name__ == "__main__":
    main()
