# -*- coding: utf-8 -*-
"""第4稿 draft_v4.mp4 組み立て。

- 冒頭: ユーザー提供の intro_visual_v4.png をフルスクリーン主役に（文字は最小限）
- 本編: スマホ y10〜875 / 字幕帯 y890〜1080（濃ネイビー半透明・52px太字・下部固定）
- まとめ: ナレーション実タイミングに合わせて各項目の画面へハードカット（モザイク済み再利用）
- エンドカード: CTA後 約10秒（ナレーション・字幕なし・YouTube終了画面用の余白）
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
AUDIO = EP / "audio" / "narration_v4.mp3"
OUT = EP / "output" / "draft_v4.mp4"
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


def dt_b(text: str, size: int, color: str, x, y: int, fname: str) -> str:
    (WORK / fname).write_text(text, encoding="utf-8")
    return (
        f"drawtext=fontfile={FONT}:textfile={fname}:"
        f"fontsize={size}:fontcolor={color}:x={x}:y={y}:expansion=none"
        f":box=1:boxcolor=0x000000@0.35:boxborderw=14"
    )


def render(dur: float, out: Path, texts, phone: str | None = None,
           visual: str | None = None, underline: bool = False,
           vscale=(528, 297), vpos=(696, 118), fullbleed: bool = False,
           fade_out: float = 0.0):
    tf = []
    for i, (t, size, color, x, y) in enumerate(texts):
        if i == 0 and out.stem == "v4_01_intro":
            tf.append(dt_b(t, size, color, x, y, f"txt4_{out.stem}_{i}.txt"))
        else:
            tf.append(dt(t, size, color, x, y, f"txt4_{out.stem}_{i}.txt"))
    if underline:
        tf.append(f"drawbox=x=760:y=730:w=400:h=6:color={ACCENT}:t=fill")
    inputs = ["ffmpeg", "-y", "-v", "error",
              "-f", "lavfi", "-i", f"color=c={BG}:s=1920x1080:r=30:d={dur}"]
    if phone:
        inputs += ["-loop", "1", "-framerate", "30", "-t", f"{dur}", "-i", str(Path(phone))]
    if visual:
        inputs += ["-loop", "1", "-framerate", "30", "-t", f"{dur}", "-i", str(Path(visual))]
    if fullbleed and visual:
        fc = "[1:v]scale=1920:1080[bg];[0:v][bg]overlay=0:0"
    elif phone and not visual:
        fc = "[1:v]scale=379:850[ph];[0:v][ph]overlay=770:12:shortest=1"
    elif visual and not phone:
        fc = (f"[1:v]scale={vscale[0]}:{vscale[1]}[vs];"
              f"[0:v][vs]overlay={vpos[0]}:{vpos[1]}:shortest=1")
    else:
        fc = "[0:v]"
    if tf:
        if fc == "[0:v]":
            fc += ",".join(tf)
        else:
            fc += "," + ",".join(tf)
    if fade_out > 0:
        fc += f",fade=t=out:st={dur - fade_out:.2f}:d={fade_out}"
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

    # --- 冒頭: ユーザー提供画像を主役に（文字は最小限）---
    intro_dur = spans[0]["end"] - spans[0]["start"]
    if not (WORK / "intro_visual_v4.png").exists():
        raise SystemExit("work/intro_visual_v4.png が見つかりません（差し替え画像が未配置）")
    parts.append(("intro", intro_dur, [
        ("イメージ", 30, "0xF7F5F2", "(w-text_w)-140", 48),
    ], None, "intro_visual_v4.png", False, (1920, 1080), (0, 0), True, 0.0))

    # --- セクション（スマホ中央・小さいインジケータ）---
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
        ], None, None, True, (0, 0), (0, 0), False, 0.0))
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
            ], still, None, False, (0, 0), (0, 0), False, 0.0))

    # --- まとめ: ナレーション実タイミングで画面切り替え（モザイク済み素材の再利用）---
    sum_span = spans[6]
    dur = sum_span["end"] - sum_span["start"]
    header_dur = min(HEADER_MS, dur - 1.0)
    parts.append(("header", header_dur, [
        ("大人のデジタル安心室", 28, GRAY, "(w-text_w)/2", 292),
        ("まとめ", 110, ACCENT, "(w-text_w)/2", 368),
        ("5つの確認項目をおさらいしましょう", 44, DARK, "(w-text_w)/2", 570),
    ], None, None, True, (0, 0), (0, 0), False, 0.0))
    units = [u for u in t["units"] if u["section"] == "まとめ"]
    segs = []  # (start, end, still)
    for u in units:
        txt = u["text"]
        if "1つ目" in txt or "セキュリティ診断" in txt:
            still = "s01_checkup.png"
        elif "2つ目" in txt or "電話番号" in txt or "メール" in txt:
            still = "s02_phone.png"
        elif "3つ目" in txt or "2段階認証" in txt or "パスキー" in txt:
            still = "s03_methods.png"
        elif "4つ目" in txt or "端末" in txt:
            still = "s04_devices.png"
        elif "5つ目" in txt or "サービス" in txt:
            still = "s05_conn.png"
        else:
            still = "s01_security.png"
        segs.append((u["start"], u["end"], still))
    segs[-1] = (segs[-1][0], sum_span["end"], segs[-1][2])
    # 隣接する同一画面は結合（短いフラッシュを避ける）
    merged = []
    for st, en, still in segs:
        if merged and merged[-1][2] == still:
            merged[-1] = (merged[-1][0], en, still)
        else:
            merged.append((st, en, still))
    segs = merged
    cursor = sum_span["start"] + header_dur
    for st, en, still in segs:
        if st < cursor:
            st = cursor
        if en <= st:
            continue
        parts.append(("panel", en - st, [], still, None, False, (0, 0), (0, 0), False, 0.0))
        cursor = en

    # --- CTA（v3維持）---
    meta = json.loads((WORK / "outro_meta.json").read_text(encoding="utf-8"))
    outro_dur = meta["video_after_v2"]
    parts.append(("outro", outro_dur, [
        ("役に立ったら、", 58, DARK, "(w-text_w)/2", 470),
        ("チャンネル登録して", 58, DARK, "(w-text_w)/2", 548),
        ("次回も一緒に確認しましょう", 58, DARK, "(w-text_w)/2", 626),
        ("大人のデジタル安心室", 46, ACCENT, "(w-text_w)/2", 760),
    ], None, "cta_visual.png", False, (528, 297), (696, 118), False, 0.0))

    # --- エンドカード（約10秒・ナレーション/字幕なし・フェードアウト）---
    end_start = sum_span["end"] + outro_dur
    end_dur = round(519.98 - end_start, 2)
    parts.append(("endcard", end_dur, [
        ("大人のデジタル安心室", 56, ACCENT, "(w-text_w)/2", 430),
        ("役に立ったら", 46, DARK, "(w-text_w)/2", 560),
        ("チャンネル登録して、また次回。", 46, DARK, "(w-text_w)/2", 636),
    ], None, None, False, (0, 0), (0, 0), False, 0.8))

    # --- レンダリング＆連結 ---
    out_parts = []
    for i, (kind, d, texts, phone, visual, ul, vs, vp, fb, fo) in enumerate(parts, 1):
        p = WORK / f"v4_{i:02d}_{kind}.mp4"
        render(round(d, 3), p, texts, phone, visual, ul, vs, vp, fb, fo)
        out_parts.append(p)
    lst = WORK / "v4_concat.txt"
    lst.write_text("\n".join(f"file '{p.name}'" for p in out_parts), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c", "copy", str(WORK / "v4_video.mp4")], check=True, cwd=WORK)
    subprocess.run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(WORK / "v4_video.mp4"), "-i", str(AUDIO),
        "-vf", "drawbox=x=0:y=890:w=1920:h=190:color=0x08101B@0.78:t=fill,"
               "subtitles=captions.ass",
        "-c:v", "libx264", "-crf", "19", "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k", "-shortest", str(OUT)],
        check=True, cwd=EP)
    print(f"draft_v4.mp4 written: {OUT}")


if __name__ == "__main__":
    main()
