# -*- coding: utf-8 -*-
"""第6稿 draft_v6.mp4 組み立て

- 字幕: 禁則・安全幅1550px・縦中央固定（{\\an5\\pos(960,985)}）は captions.ass 側
- 本編パネル: 説明に合わせて「全体 → ズーム（1.3〜1.7倍・0.5s）→ 対象を青枠ハイライト」
  のシーン構成（スマホ内の視線誘導）へ変更
- 他（冒頭・見出し・まとめ・CTA・エンドカード・帯・ナレーション）は v5 を維持
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
OUT = EP / "output" / "draft_v6.mp4"
FONT = "font.ttc"

BG = "0xF7F5F2"
ACCENT = "0x2E6DA4"
DARK = "0x1F2A37"
GRAY = "0x5B6570"
HL = "0x4C8DE0"
HEADER_MS = 1.8
PHONE_W, PHONE_H = 379, 850
PHONE_X, PHONE_Y = 770, 12


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


def project_hl(hl: tuple[int, int, int, int] | None, z: float, cx: float, cy: float):
    """入力座標(1080x2424)のハイライト矩形をスマホ描画空間(379x850)へ投影。"""
    if not hl:
        return None
    x1, y1, x2, y2 = hl
    if z <= 1.0:
        ox1 = x1 * PHONE_W / 1080.0
        oy1 = y1 * PHONE_H / 2424.0
        ow = (x2 - x1) * PHONE_W / 1080.0
        oh = (y2 - y1) * PHONE_H / 2424.0
    else:
        win_x = cx - 1080.0 / (2 * z)
        win_y = cy - 2424.0 / (2 * z)
        sx = PHONE_W * z / 1080.0
        sy = PHONE_H * z / 2424.0
        ox1 = (x1 - win_x) * sx
        oy1 = (y1 - win_y) * sy
        ow = (x2 - x1) * sx
        oh = (y2 - y1) * sy
    if ow < 6 or oh < 6:
        return None
    ox1 = max(0.0, min(ox1, PHONE_W - 4))
    oy1 = max(0.0, min(oy1, PHONE_H - 4))
    ow = min(ow, PHONE_W - ox1)
    oh = min(oh, PHONE_H - oy1)
    return ox1, oy1, ow, oh


def render_scene(dur: float, out: Path, still: str, z: float, cx: float, cy: float,
                 hl: tuple | None, label: str):
    """スマホ静止画をズーム・ハイライト付きでレンダリング（1シーン=1クリップ）。"""
    frames = max(int(round(dur * 30)), 5)
    tf = []
    if label.strip():
        fn = f"txt6_{out.stem}_label.txt"
        (WORK / fn).write_text(label, encoding="utf-8")
        tf.append(f"drawtext=fontfile={FONT}:textfile={fn}:"
                  f"fontsize=40:fontcolor={DARK}:x=48:y=36:expansion=none")
    if z > 1.001:
        fc = (
            f"[1:v]scale=2160:4848[big];"
            f"[big]zoompan=z='min({z:.3f},1+({z:.3f}-1)*on/15)':"
            f"x='{cx * 2:.1f}':y='{cy * 2:.1f}':d={frames}:s={PHONE_W}x{PHONE_H}:fps=30[ph]"
        )
    else:
        fc = f"[1:v]scale={PHONE_W}:{PHONE_H}[ph]"
    pr = project_hl(hl, z, cx, cy)
    if pr:
        ox, oy, ow, oh = pr
        fc += (f";[ph]drawbox=x={ox:.1f}:y={oy:.1f}:w={ow:.1f}:h={oh:.1f}:"
               f"color={HL}@0.9:t=3[ph2];[0:v][ph2]overlay={PHONE_X}:{PHONE_Y}:shortest=1")
    else:
        fc += f";[0:v][ph]overlay={PHONE_X}:{PHONE_Y}:shortest=1"
    if tf:
        if fc == "[0:v]":
            fc += ",".join(tf)
        else:
            fc += "," + ",".join(tf)
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-f", "lavfi", "-i", f"color=c={BG}:s=1920x1080:r=30:d={dur}",
        "-loop", "1", "-framerate", "30", "-t", f"{dur}", "-i", str(WORK / still),
        "-filter_complex", fc,
        "-an", "-c:v", "libx264", "-crf", "19", "-preset", "medium", out.name,
    ]
    subprocess.run(cmd, check=True, cwd=WORK)
    print(f"scene {out.name} ({dur:.1f}s z={z})")


def render_static(dur: float, out: Path, texts, visual: str | None = None,
                  fullbleed: bool = False, vscale=(528, 297), vpos=(696, 118),
                  underline: bool = False, fade_out: float = 0.0):
    """v5互換の静止カード（見出し・まとめ・CTA・エンドカード・冒頭）。"""
    tf = []
    for i, (t, size, color, x, y) in enumerate(texts):
        fn = f"txt6_{out.stem}_{i}.txt"
        if i == 0 and out.stem == "v6_01_intro":
            tf.append(dt_b(t, size, color, x, y, fn))
        else:
            tf.append(dt(t, size, color, x, y, fn))
    if underline:
        tf.append(f"drawbox=x=760:y=730:w=400:h=6:color={ACCENT}:t=fill")
    inputs = ["ffmpeg", "-y", "-v", "error",
              "-f", "lavfi", "-i", f"color=c={BG}:s=1920x1080:r=30:d={dur}"]
    if visual:
        inputs += ["-loop", "1", "-framerate", "30", "-t", f"{dur}", "-i", str(WORK / visual)]
    if fullbleed and visual:
        fc = "[1:v]scale=1920:1080[bg];[0:v][bg]overlay=0:0"
    elif visual:
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
    print(f"static {out.name} ({dur:.1f}s)")


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

    # --- 冒頭（v5維持・画像は y0〜890）---
    intro_dur = spans[0]["end"] - spans[0]["start"]
    if not (WORK / "intro_visual_v4.png").exists():
        raise SystemExit("work/intro_visual_v4.png が見つかりません")
    parts.append(("intro", intro_dur, [
        ("イメージ", 30, "0xF7F5F2", "(w-text_w)-140", 48),
    ], "intro_visual_v4.png", False, (1582, 890), (169, 0)))

    # --- セクション（見出し + ズームシーン）---
    sections = [
        {"num": "1 / 5", "name": "セキュリティ診断", "panel_span_idx": 1,
         "scenes": [
             (14.0, "s01_security.png", 1.0, 540, 1200, None),
             (42.35, "s01_security.png", 1.5, 540, 740, (42, 625, 1042, 856)),
             (56.0, "s01_checkup.png", 1.0, 540, 1200, None),
             (84.7, "s01_checkup.png", 1.5, 540, 360, (120, 200, 960, 520)),
         ]},
        {"num": "2 / 5", "name": "再設定用の電話番号・メール", "panel_span_idx": 2,
         "scenes": [
             (11.0, "s02_phone.png", 1.0, 540, 1200, None),
             (37.25, "s02_phone.png", 1.5, 540, 950, (42, 520, 1042, 1400)),
             (50.0, "s02b_email.png", 1.0, 540, 1200, None),
             (74.5, "s02b_email.png", 1.5, 540, 1050, (42, 500, 1042, 1500)),
         ]},
        {"num": "3 / 5", "name": "2段階認証とパスキー", "panel_span_idx": 3,
         "scenes": [
             (11.8, "s03_top.png", 1.0, 540, 1200, None),
             (42.8, "s03_top.png", 1.5, 540, 1200, (63, 1053, 1021, 1510)),
             (55.0, "s03_methods.png", 1.0, 540, 1200, None),
             (77.0, "s03_methods.png", 1.65, 577, 1935, (273, 1864, 882, 2006)),
             (107.0, "s03_methods.png", 1.6, 540, 2300, (63, 2034, 1018, 2363)),
         ]},
        {"num": "4 / 5", "name": "ログイン中の端末", "panel_span_idx": 4,
         "scenes": [
             (17.0, "s04_devices.png", 1.0, 540, 1200, None),
             (47.0, "s04_devices.png", 1.6, 650, 1220, (294, 1040, 1018, 1400)),
             (74.7, "s04_devices.png", 1.7, 660, 1700, (294, 1450, 1018, 1800)),
         ]},
        {"num": "5 / 5", "name": "リンク済みアプリ", "panel_span_idx": 5,
         "scenes": [
             (15.5, "s05_conn.png", 1.0, 540, 1200, None),
             (50.5, "s05_conn.png", 1.6, 540, 620, (63, 380, 1021, 850)),
             (81.1, "s05_conn.png", 1.55, 540, 2050, (42, 1750, 1042, 2300)),
         ]},
    ]

    def scene_parts(scenes, total_window):
        prev = 0.0
        out = []
        for endv, still, z, cx, cy, hl in scenes:
            e0 = prev
            e1 = min(endv, total_window)
            if e1 <= e0:
                continue
            out.append((e1 - e0, still, z, cx, cy, hl))
            prev = e1
        return out

    for sec in sections:
        span = spans[sec["panel_span_idx"]]
        dur = span["end"] - span["start"]
        header_dur = min(HEADER_MS, dur - 1.0)
        parts.append(("header", header_dur, [
            ("大人のデジタル安心室", 28, GRAY, "(w-text_w)/2", 292),
            (sec["num"], 120, ACCENT, "(w-text_w)/2", 368),
            (sec["name"], 58, DARK, "(w-text_w)/2", 570),
        ], None, True, (0, 0), (0, 0)))
        total_scene = dur - header_dur
        for d, still, z, cx, cy, hl in scene_parts(sec["scenes"], total_scene):
            parts.append(("scene", d, (still, z, cx, cy, hl, sec["num"])))

    # --- まとめ（v5維持: 実タイミングで静止切替）---
    sum_span = spans[6]
    dur = sum_span["end"] - sum_span["start"]
    header_dur = min(HEADER_MS, dur - 1.0)
    parts.append(("header", header_dur, [
        ("大人のデジタル安心室", 28, GRAY, "(w-text_w)/2", 292),
        ("まとめ", 110, ACCENT, "(w-text_w)/2", 368),
        ("5つの確認項目をおさらいしましょう", 44, DARK, "(w-text_w)/2", 570),
    ], None, True, (0, 0), (0, 0)))
    units = [u for u in t["units"] if u["section"] == "まとめ"]
    segs = []
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
    merged = []
    for st, en, still in segs:
        if merged and merged[-1][2] == still:
            merged[-1] = (merged[-1][0], en, still)
        else:
            merged.append((st, en, still))
    cursor = sum_span["start"] + header_dur
    for st, en, still in merged:
        if st < cursor:
            st = cursor
        if en <= st:
            continue
        parts.append(("scene", en - st, (still, 1.0, 540, 1200, None, "")))
        cursor = en

    # --- CTA / エンドカード（v5維持）---
    meta = json.loads((WORK / "outro_meta.json").read_text(encoding="utf-8"))
    parts.append(("cta", meta["video_after_v2"], [
        ("役に立ったら、", 58, DARK, "(w-text_w)/2", 470),
        ("チャンネル登録して", 58, DARK, "(w-text_w)/2", 548),
        ("次回も一緒に確認しましょう", 58, DARK, "(w-text_w)/2", 626),
        ("大人のデジタル安心室", 46, ACCENT, "(w-text_w)/2", 760),
    ], "cta_visual.png", False, (528, 297), (696, 118)))
    end_start = sum_span["end"] + meta["video_after_v2"]
    end_dur = round(519.98 - end_start, 2)
    parts.append(("endcard", end_dur, [
        ("大人のデジタル安心室", 56, ACCENT, "(w-text_w)/2", 430),
        ("役に立ったら", 46, DARK, "(w-text_w)/2", 560),
        ("チャンネル登録して、また次回。", 46, DARK, "(w-text_w)/2", 636),
    ], "channel_logo_google.png", False, (409, 230), (755, 110)))

    # --- レンダリング ---
    out_parts = []
    for i, part in enumerate(parts, 1):
        kind = part[0]
        d = part[1]
        p = WORK / f"v6_{i:02d}_{kind}.mp4"
        if kind == "scene":
            still, z, cx, cy, hl, label = part[2]
            render_scene(round(d, 3), p, still, z, cx, cy, hl, label)
        elif kind == "header":
            render_static(round(d, 3), p, part[2], part[3], part[4], part[5], part[6],
                          underline=True)
        else:
            render_static(round(d, 3), p, part[2], part[3], part[4], part[5], part[6],
                          fade_out=0.8 if (kind in ("endcard",)) else 0.0)
        out_parts.append(p)
    lst = WORK / "v6_concat.txt"
    lst.write_text("\n".join(f"file '{p.name}'" for p in out_parts), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c", "copy", str(WORK / "v6_video.mp4")],
                   check=True, cwd=WORK)
    subprocess.run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(WORK / "v6_video.mp4"), "-i", str(AUDIO),
        "-vf", "drawbox=x=0:y=890:w=1920:h=190:color=0x08101B@0.78:t=fill,"
               "subtitles=captions.ass",
        "-c:v", "libx264", "-crf", "19", "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k", "-shortest", str(OUT)],
        check=True, cwd=EP)
    print(f"draft_v6.mp4 written: {OUT}")


if __name__ == "__main__":
    main()
