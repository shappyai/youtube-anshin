# -*- coding: utf-8 -*-
"""第8稿 draft_v8.mp4 組み立て

- スマホは常に全体表示（インセット・クロップズームなし）
- 視線誘導は「短時間の青枠ハイライト（2〜5秒）」と「青系タップリップル（約1秒）」のみ
- 字幕 72px・安全幅 1780px・帯 y885〜1080・縦中央 y980（captions_v8.ass）
- 音声は実サンプル基準の narration_v6.mp3 と完全同期（captions_v8.srt）
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EP = Path(__file__).resolve().parents[1]
WORK = EP / "work"
ASSETS = WORK / "v8_assets"
AUDIO = EP / "audio" / "narration_v6.mp3"
OUT = EP / "output" / "draft_v8.mp4"
FONT = "font.ttc"

BG = "0xF7F5F2"
ACCENT = "0x2E6DA4"
DARK = "0x1F2A37"
GRAY = "0x5B6570"
HL = (76, 141, 224)
HEADER_MS = 1.8
PHONE_W, PHONE_H = 379, 850
PHONE_X, PHONE_Y = 770, 12


def tl() -> dict:
    return json.loads((WORK / "timeline_v8.json").read_text(encoding="utf-8"))


def dt(text: str, size: int, color: str, x, y: int, fname: str) -> str:
    (WORK / fname).write_text(text, encoding="utf-8")
    return (f"drawtext=fontfile={FONT}:textfile={fname}:"
            f"fontsize={size}:fontcolor={color}:x={x}:y={y}:expansion=none")


def dt_b(text: str, size: int, color: str, x, y: int, fname: str) -> str:
    (WORK / fname).write_text(text, encoding="utf-8")
    return (f"drawtext=fontfile={FONT}:textfile={fname}:"
            f"fontsize={size}:fontcolor={color}:x={x}:y={y}:expansion=none"
            f":box=1:boxcolor=0x000000@0.35:boxborderw=14")


def to_phone(rect: tuple) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = rect
    ox = round(x1 * PHONE_W / 1080.0)
    oy = round(y1 * PHONE_H / 2424.0)
    ow = max(round((x2 - x1) * PHONE_W / 1080.0), 8)
    oh = max(round((y2 - y1) * PHONE_H / 2424.0), 8)
    return ox, oy, ow, oh


def make_hl(px: tuple[int, int, int, int], idx: int) -> Path:
    ox, oy, ow, oh = px
    radius = max(8, min(ow, oh) // 5)
    img = Image.new("RGBA", (ow + 8, oh + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([4, 4, ow + 3, oh + 3], radius=radius, outline=HL + (255,), width=4)
    p = ASSETS / f"hl8_{idx:02d}.png"
    img.save(p)
    return p


def make_ripple() -> Path:
    """青系のタップリップル（0.4秒で広がりながら消える・1.33s ループ動画）。"""
    d = ASSETS / "ripple8"
    d.mkdir(exist_ok=True)
    for f in range(40):
        img = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
        dr = ImageDraw.Draw(img)
        t = f / 40.0
        r = int(8 + t * 30)
        alpha = int(210 * (1 - t))
        dr.ellipse([48 - r, 48 - r, 48 + r, 48 + r],
                   outline=HL + (alpha,), width=4)
        img.save(d / f"{f:02d}.png")
    mov = ASSETS / "ripple8.mov"
    if not mov.exists():
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30",
                        "-i", str(d / "%02d.png"), "-c:v", "qtrle", "-pix_fmt", "rgba",
                        str(mov)], check=True, cwd=WORK)
    return mov


def render_panel(dur: float, out: Path, still: str, label: str,
                 events: list[dict], idx: int):
    """スマホ全体＋イベント（タップリップル/短時間ハイライト）を重ねたパネル。"""
    frames = max(int(round(dur * 30)), 5)
    need_first = bool(events) or bool(label.strip())
    inputs = ["ffmpeg", "-y", "-v", "error",
              "-f", "lavfi", "-i", f"color=c={BG}:s=1920x1080:r=30:d={dur}",
              "-loop", "1", "-framerate", "30", "-t", f"{dur}", "-i", str(WORK / still)]
    fc = "[1:v]scale=379:850[ph];[0:v][ph]overlay=770:12:shortest=1"
    if need_first:
        fc += "[phx]"
    last = "phx" if need_first else None
    ext = 2
    for ev in events:
        if ev["kind"] == "hl":
            px = to_phone(ev["rect"])
            asset = make_hl(px, idx * 10 + len(events))
            inputs += ["-loop", "1", "-framerate", "30", "-t", f"{dur}", "-i", str(asset)]
            fc += (f";[{last}][{ext}:v]overlay={PHONE_X + px[0] + 4}:{PHONE_Y + px[1] + 4}:"
                   f"enable='between(t,{ev['t']:.2f},{ev['te']:.2f})'[m{ext}]")
        else:  # ripple
            inputs += ["-stream_loop", "-1", "-t", f"{dur}", "-i", str(ASSETS / "ripple8.mov")]
            fc += (f";[{last}][{ext}:v]overlay={PHONE_X + ev['x'] - 48}:{PHONE_Y + ev['y'] - 48}:"
                   f"enable='between(t,{ev['t']:.2f},{ev['te']:.2f})'[m{ext}]")
        last = f"m{ext}"
        ext += 1
    tf = []
    if label.strip():
        fn = f"txt8_{out.stem}_label.txt"
        (WORK / fn).write_text(label, encoding="utf-8")
        tf.append(f"drawtext=fontfile={FONT}:textfile={fn}:"
                  f"fontsize=40:fontcolor={DARK}:x=48:y=36:expansion=none")
    if tf:
        fc += f";[{last}]" + ",".join(tf)
    inputs += ["-filter_complex", fc, "-an", "-c:v", "libx264", "-crf", "19",
               "-preset", "medium", out.name]
    subprocess.run(inputs, check=True, cwd=WORK)
    print(f"panel {out.name} ({dur:.1f}s ev={len(events)})")


def render_static(dur: float, out: Path, texts, visual: str | None = None,
                  fullbleed: bool = False, vscale=(528, 297), vpos=(696, 118),
                  underline: bool = False, fade_out: float = 0.0):
    tf = []
    for i, (t, size, color, x, y) in enumerate(texts):
        fn = f"txt8_{out.stem}_{i}.txt"
        if i == 0 and out.stem == "v8_01_intro":
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
        fc += (",".join(tf) if fc == "[0:v]" else "," + ",".join(tf))
    if fade_out > 0:
        fc += f",fade=t=out:st={dur - fade_out:.2f}:d={fade_out}"
    inputs += ["-filter_complex", fc, "-an", "-c:v", "libx264", "-crf", "19",
               "-preset", "medium", out.name]
    subprocess.run(inputs, check=True, cwd=WORK)
    print(f"static {out.name} ({dur:.1f}s)")


def main():
    ASSETS.mkdir(exist_ok=True)
    make_ripple()
    t = tl()
    secs = t["sections"]
    sec_start = {s["name"]: round(s["start"], 2) for s in secs}
    total = round(t["total"], 2)
    cta_start = t["cta_start"]
    order = ["はじめに", "1. セキュリティ診断", "2. 再設定用の電話番号・メール",
             "3. 2段階認証とパスキー", "4. 心当たりのない端末",
             "5. Googleでログインしたサービス", "まとめ"]
    spans = []
    for i, name in enumerate(order):
        st = sec_start.get(name, 0.0)
        en = (sec_start.get(order[i + 1], cta_start)
              if i + 1 < len(order) else cta_start)
        spans.append({"name": name, "start": st, "end": en})

    parts = []
    idx = 0
    # --- 冒頭 ---
    intro_dur = spans[0]["end"] - spans[0]["start"]
    parts.append(("intro", intro_dur, [
        ("イメージ", 30, "0xF7F5F2", "(w-text_w)-140", 48),
    ], "intro_visual_v4.png", False, (1582, 890), (169, 0)))

    # --- セクション本編（スマホ全体＋短時間イベント）---
    plan = [
        {"num": "1 / 5", "span": 1, "still": ["s01_security.png", "s01_checkup.png"],
         "frac": [0.5],
         "events": [
             {"part": 0, "fr": 0.16, "kind": "ripple", "pos": (217, 177), "hold": 0.9},
             {"part": 0, "fr": 0.34, "kind": "hl", "rect": (42, 625, 1042, 856), "hold": 4.5},
             {"part": 0, "fr": 0.38, "kind": "ripple", "pos": (190, 259), "hold": 0.9},
             {"part": 1, "fr": 0.40, "kind": "hl", "rect": (120, 200, 960, 520), "hold": 4.5},
         ]},
        {"num": "2 / 5", "span": 2, "still": ["s02_phone.png", "s02b_email.png"],
         "frac": [0.5],
         "events": [
             {"part": 0, "fr": 0.30, "kind": "ripple", "pos": (190, 333), "hold": 0.9},
             {"part": 0, "fr": 0.32, "kind": "hl", "rect": (42, 520, 1042, 1400), "hold": 4.5},
             {"part": 1, "fr": 0.42, "kind": "hl", "rect": (42, 500, 1042, 1500), "hold": 4.5},
         ]},
        {"num": "3 / 5", "span": 3, "still": ["s03_top.png", "s03_methods.png"],
         "frac": [0.5],
         "events": [
             {"part": 0, "fr": 0.36, "kind": "hl", "rect": (63, 1053, 1021, 1510), "hold": 4.5},
             {"part": 1, "fr": 0.28, "kind": "hl", "rect": (273, 1864, 882, 2006), "hold": 4.5},
             {"part": 1, "fr": 0.62, "kind": "hl", "rect": (63, 2034, 1018, 2363), "hold": 4.5},
         ]},
        {"num": "4 / 5", "span": 4, "still": ["s04_devices.png", None],
         "frac": [1.0],
         "events": [
             {"part": 0, "fr": 0.28, "kind": "ripple", "pos": (228, 427), "hold": 0.9},
             {"part": 0, "fr": 0.30, "kind": "hl", "rect": (294, 1040, 1018, 1400), "hold": 4.5},
             {"part": 0, "fr": 0.72, "kind": "hl", "rect": (294, 1450, 1018, 1800), "hold": 4.5},
         ]},
        {"num": "5 / 5", "span": 5, "still": ["s05_conn.png", None],
         "frac": [1.0],
         "events": [
             {"part": 0, "fr": 0.32, "kind": "hl", "rect": (63, 380, 1021, 850), "hold": 4.5},
             {"part": 0, "fr": 0.76, "kind": "hl", "rect": (42, 1750, 1042, 2300), "hold": 4.5},
         ]},
    ]
    for sec in plan:
        span = spans[sec["span"]]
        dur = span["end"] - span["start"]
        header_dur = min(HEADER_MS, dur - 1.0)
        parts.append(("header", header_dur, [
            ("大人のデジタル安心室", 28, GRAY, "(w-text_w)/2", 292),
            (sec["num"], 120, ACCENT, "(w-text_w)/2", 368),
            (["セキュリティ診断", "再設定用の電話番号・メール", "2段階認証とパスキー",
              "ログイン中の端末", "リンク済みアプリ"][sec["span"] - 1], 58, DARK,
             "(w-text_w)/2", 570),
        ], None, True, (0, 0), (0, 0)))
        panel = dur - header_dur
        cuts = [int(round(f * panel)) for f in [0] + sec["frac"] + [1]]
        for pi, (st0, st1) in enumerate(zip(cuts[:-1], cuts[1:])):
            still = sec["still"][pi] if pi < len(sec["still"]) and sec["still"][pi] else None
            if still is None:
                continue
            seg_dur = st1 - st0
            if seg_dur <= 1.0:
                continue
            events = []
            for ev in sec["events"]:
                if ev["part"] != pi:
                    continue
                t0 = st0 + seg_dur * ev["fr"]
                te = t0 + ev["hold"]
                if ev["kind"] == "hl":
                    events.append({"kind": "hl", "rect": ev["rect"], "t": t0, "te": te})
                else:
                    events.append({"kind": "ripple", "x": ev["pos"][0],
                                   "y": ev["pos"][1], "t": t0, "te": te})
            idx += 1
            parts.append(("panel", seg_dur, (still, sec["num"], events, idx)))

    # --- まとめ（v7同様の静止切替）---
    sum_span = spans[6]
    dur = sum_span["end"] - sum_span["start"]
    header_dur = min(HEADER_MS, dur - 1.0)
    parts.append(("header", header_dur, [
        ("大人のデジタル安心室", 28, GRAY, "(w-text_w)/2", 292),
        ("まとめ", 110, ACCENT, "(w-text_w)/2", 368),
        ("5つの確認項目をおさらいしましょう", 44, DARK, "(w-text_w)/2", 570),
    ], None, True, (0, 0), (0, 0)))
    old = json.loads((WORK / "timeline.json").read_text(encoding="utf-8"))["units"]
    old_sum = [u for u in old if u["section"] == "まとめ"]
    old_total = old_sum[-1]["end"] - old_sum[0]["start"]
    new_sum_dur = dur - header_dur
    segs = []
    for u in old_sum:
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
        segs.append((((u["start"] - old_sum[0]["start"]) / old_total) * new_sum_dur,
                     ((u["end"] - old_sum[0]["start"]) / old_total) * new_sum_dur, still))
    merged = []
    for st, en, still in segs:
        if merged and merged[-1][2] == still:
            merged[-1] = (merged[-1][0], en, still)
        else:
            merged.append((st, en, still))
    cursor = 0.0
    for st, en, still in merged:
        if st < cursor:
            st = cursor
        if en <= st:
            continue
        idx += 1
        parts.append(("panel", en - st, (still, "", [], idx)))
        cursor = en

    # --- CTA / エンドカード（v7準拠）---
    parts.append(("cta", 7.9, [
        ("役に立ったら、", 58, DARK, "(w-text_w)/2", 470),
        ("チャンネル登録して", 58, DARK, "(w-text_w)/2", 548),
        ("次回も一緒に確認しましょう", 58, DARK, "(w-text_w)/2", 626),
        ("大人のデジタル安心室", 46, ACCENT, "(w-text_w)/2", 760),
    ], "cta_visual.png", False, (528, 297), (696, 118)))
    used = sum(p[1] for p in parts)
    audio_total = t["end_audio_total"]
    end_dur = round(audio_total - used, 2)
    parts.append(("endcard", end_dur, [
        ("役に立ったら", 46, DARK, "(w-text_w)/2", 560),
        ("チャンネル登録して、また次回。", 46, DARK, "(w-text_w)/2", 636),
    ], "channel_logo_google.png", False, (480, 270), (720, 100)))

    # --- レンダリング&連結 ---
    out_parts = []
    for i, part in enumerate(parts, 1):
        kind = part[0]
        d = part[1]
        p = WORK / f"v8_{i:02d}_{kind}.mp4"
        if kind == "panel":
            still, label, events, idx2 = part[2]
            render_panel(round(d, 3), p, still, label, events, idx2)
        elif kind == "header":
            render_static(round(d, 3), p, part[2], part[3], part[4], part[5], part[6],
                          underline=True)
        else:
            render_static(round(d, 3), p, part[2], part[3], part[4], part[5], part[6],
                          fade_out=0.8 if kind == "endcard" else 0.0)
        out_parts.append(p)
    lst = WORK / "v8_concat.txt"
    lst.write_text("\n".join(f"file '{p.name}'" for p in out_parts), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c", "copy", str(WORK / "v8_video.mp4")],
                   check=True, cwd=WORK)
    subprocess.run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(WORK / "v8_video.mp4"), "-i", str(AUDIO),
        "-vf", "drawbox=x=0:y=885:w=1920:h=195:color=0x08101B@0.78:t=fill,"
               "subtitles=captions_v8.ass",
        "-c:v", "libx264", "-crf", "19", "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k", "-shortest", str(OUT)],
        check=True, cwd=EP)
    print(f"draft_v8.mp4 written: {OUT}")


if __name__ == "__main__":
    main()
