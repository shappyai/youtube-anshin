# -*- coding: utf-8 -*-
"""第9稿 draft_v9.mp4 組み立て

v9 の変更点:
- 青枠ハイライト・タップリップルを完全撤去（演出での視線誘導をやめる）
- 構図は3種類のみ:
  A. full  : ページ全体（遷移・全体構成の確認、短め）
  B. crop  : 説明対象UIの大きな切り抜き（基本構図）
  C. two   : 関連2項目の左右2カラム
- 切り抜きは「モザイク済み素材 (work/s0X_*.png)」から行う
- 字幕・音声は v8 を維持（captions_v8.ass / narration_v6.mp3 / timeline_v8.json）
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EP = Path(__file__).resolve().parents[1]
WORK = EP / "work"
AUDIO = EP / "audio" / "narration_v6.mp3"
OUT = EP / "output" / "draft_v9.mp4"
FONT = "font.ttc"  # ffmpeg フィルタ用（cwd=WORK 実行のため相対パス）
PFONT = str(WORK / "font.ttc")  # PIL 用

DARK = "0x1F2A37"  # ffmpeg 色
GRAY = "0x5B6570"
BG_PIL = (247, 245, 242)  # PIL 色
DARK_PIL = (31, 42, 55)
GRAY_PIL = (91, 101, 112)
ACCENT = "0x2E6DA4"
HEADER_MS = 1.8
AREA_Y = 885  # 字幕帯（y885〜1080）と重ならない映像領域


def tl() -> dict:
    return json.loads((WORK / "timeline_v8.json").read_text(encoding="utf-8"))


def load(name: str):
    return Image.open(WORK / name).convert("RGB")


def fit(w: int, h: int, maxw: int, maxh: int) -> tuple[int, int]:
    r = min(maxw / w, maxh / h)
    return max(int(w * r), 1), max(int(h * r), 1)


def panel_png(out_name: str, label: str, content: list[tuple]):
    """1920x1080 パネルフレームを PIL で生成。
    content: (image, rect, item_label|None) のリスト。rect は 1080x2424 座標。
    """
    canvas = Image.new("RGB", (1920, 1080), BG_PIL)
    d = ImageDraw.Draw(canvas)
    f_label = ImageFont.truetype(PFONT, 40)
    f_item = ImageFont.truetype(PFONT, 44)
    if label:
        d.text((48, 36), label, font=f_label, fill=GRAY_PIL)
    if len(content) == 1:
        im, rect, item_label = content[0]
        c = im.crop(rect)
        w, h = fit(c.width, c.height, 1800, AREA_Y - 80)
        c = c.resize((w, h), Image.LANCZOS)
        canvas.paste(c, ((1920 - w) // 2, (AREA_Y - 40 - h) // 2 + 20))
    elif len(content) == 2:
        cw_each = 800
        gap = 60
        x0 = (1920 - (cw_each * 2 + gap)) // 2
        for i, (im, rect, item_label) in enumerate(content):
            c = im.crop(rect)
            w, h = fit(c.width, c.height, cw_each, AREA_Y - 110)
            c = c.resize((w, h), Image.LANCZOS)
            x = x0 + i * (cw_each + gap) + (cw_each - w) // 2
            y = (AREA_Y - 40 - h) // 2 + 40
            canvas.paste(c, (x, y))
            if item_label:
                iw = d.textlength(item_label, font=f_item)
                d.text((x + (w - iw) // 2, y - 14), item_label,
                       font=f_item, fill=DARK_PIL)
    p = WORK / f"v9panel_{out_name}.png"
    canvas.save(p)
    return p


def render_panel(dur: float, out: Path, png: Path):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", "30",
                    "-t", f"{dur:.3f}", "-i", str(png),
                    "-vf", "scale=1920:1080", "-an", "-c:v", "libx264",
                    "-crf", "19", "-preset", "medium", "-pix_fmt", "yuv420p",
                    str(out)], check=True, cwd=WORK)
    print(f"panel {out.name} ({dur:.1f}s)")


def dt(text: str, size: int, color: str, x, y: int, fname: str) -> str:
    (WORK / fname).write_text(text, encoding="utf-8")
    return (f"drawtext=fontfile={FONT}:textfile={fname}:"
            f"fontsize={size}:fontcolor={color}:x={x}:y={y}:expansion=none")


def dt_b(text: str, size: int, color: str, x, y: int, fname: str) -> str:
    (WORK / fname).write_text(text, encoding="utf-8")
    return (f"drawtext=fontfile={FONT}:textfile={fname}:"
            f"fontsize={size}:fontcolor={color}:x={x}:y={y}:expansion=none"
            f":box=1:boxcolor=0x000000@0.35:boxborderw=14")


def render_static(dur: float, out: Path, texts, visual: str | None = None,
                  fullbleed: bool = False, vscale=(528, 297), vpos=(696, 118),
                  underline: bool = False, fade_out: float = 0.0):
    tf = []
    for i, (t, size, color, x, y) in enumerate(texts):
        fn = f"txt9_{out.stem}_{i}.txt"
        if i == 0 and out.stem == "v9_01_intro":
            tf.append(dt_b(t, size, color, x, y, fn))
        else:
            tf.append(dt(t, size, color, x, y, fn))
    if underline:
        tf.append(f"drawbox=x=760:y=730:w=400:h=6:color={ACCENT}:t=fill")
    inputs = ["ffmpeg", "-y", "-v", "error",
              "-f", "lavfi", "-i", f"color=c=0xF7F5F2:s=1920x1080:r=30:d={dur}"]
    if visual:
        inputs += ["-loop", "1", "-framerate", "30", "-t", f"{dur}", "-i",
                   str(WORK / visual)]
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


def r(x1, y1, x2, y2):
    return (x1, y1, x2, y2)


def main():
    t = tl()
    secs = t["sections"]
    sec_start = {s["name"]: s["start"] for s in secs}
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

    S = {s: load(f"{s}.png") for s in
         ["s01_security", "s01_checkup", "s02_phone", "s02b_email",
          "s03_top", "s03_methods", "s04_devices", "s05_conn"]}
    FULL = (0, 0, 1080, 2424)
    phone_re = r(42, 240, 1042, 950)
    email_re = r(42, 240, 1042, 1150)
    phone_email = {"kind": "two", "items": [
        (S["s02_phone"], phone_re, "電話番号"),
        (S["s02b_email"], email_re, "メールアドレス")]}

    plan = []

    # --- 冒頭（v8維持） ---
    intro_dur = spans[0]["end"] - spans[0]["start"]
    plan.append(["static", intro_dur, [
        ("イメージ", 30, "0xF7F5F2", "(w-text_w)-140", 48),
    ], "intro_visual_v4.png", False, (1582, 890), (169, 0)])

    labels = ["1 / 5", "2 / 5", "3 / 5", "4 / 5", "5 / 5"]
    titles = ["セキュリティ診断", "再設定用の電話番号・メール", "2段階認証とパスキー",
              "ログイン中の端末", "リンク済みアプリ"]

    # 各セクションのパネルプラン（ナレーション内容に連動）
    secs_plan = [
        [  # 1: セキュリティ診断
            ("crop", spans[1]["start"] + HEADER_MS, 28.97, S["s01_checkup"],
             r(42, 380, 1042, 1150)),
            ("full", 28.97, 39.77, S["s01_security"], FULL),
            ("crop", 39.77, 50.95, S["s01_security"], r(42, 240, 1042, 720)),
            ("crop", 50.95, 65.28, S["s01_checkup"], r(42, 380, 1042, 1150)),
            ("crop", 65.28, 82.66, S["s01_checkup"], r(42, 560, 1042, 2000)),
            ("crop", 82.66, 95.43, S["s01_checkup"], r(42, 380, 1042, 1150)),
            ("full", 95.43, spans[1]["end"], S["s01_checkup"], FULL),
        ],
        [  # 2: 再設定用の電話番号・メール
            ("two", spans[2]["start"] + HEADER_MS, 117.91, None, None, phone_email),
            ("crop", 117.91, 150.64, S["s02_phone"], phone_re),
            ("two", 150.64, 158.74, None, None, phone_email),
            ("crop", 158.74, 166.75, S["s02_phone"], phone_re),
            ("two", 166.75, spans[2]["end"], None, None, phone_email),
        ],
        [  # 3: 2段階認証とパスキー
            ("crop", spans[3]["start"] + HEADER_MS, 191.73, S["s03_top"],
             r(42, 230, 1042, 1050)),
            ("crop", 191.73, 215.42, S["s03_top"], r(42, 850, 1042, 1650)),
            ("two", 215.42, 229.18, None, None,
             {"kind": "two", "items": [
                 (S["s03_top"], r(42, 230, 1042, 1050), "2段階認証"),
                 (S["s01_security"], r(42, 2050, 1042, 2320), "パスキー")]}),
            ("two", 229.18, 243.50, None, None, phone_email),
            ("crop", 243.50, 253.03, S["s02b_email"], email_re),
            ("crop", 253.03, 263.92, S["s02b_email"], email_re),
            ("crop", 263.92, 275.46, S["s03_methods"], r(42, 220, 1042, 1000)),
            ("crop", 275.46, spans[3]["end"], S["s03_methods"], r(42, 800, 1042, 1900)),
        ],
        [  # 4: 心当たりのない端末
            ("full", spans[4]["start"] + HEADER_MS, 295.63, S["s04_devices"], FULL),
            ("crop", 295.63, 307.60, S["s04_devices"], r(42, 230, 1042, 950)),
            ("crop", 307.60, 338.09, S["s04_devices"], r(42, 900, 1042, 2300)),
            ("crop", 338.09, 349.54, S["s04_devices"], r(42, 900, 1042, 2300)),
            ("crop", 349.54, 356.33, S["s04_devices"], r(42, 900, 1042, 2300)),
            ("crop", 356.33, spans[4]["end"], S["s04_devices"], r(42, 900, 1042, 2300)),
        ],
        [  # 5: リンク済みアプリ
            ("full", spans[5]["start"] + HEADER_MS, 370.38, S["s05_conn"], FULL),
            ("crop", 370.38, 383.39, S["s05_conn"], r(42, 230, 1042, 1000)),
            ("crop", 383.39, 402.40, S["s05_conn"], r(42, 900, 1042, 2100)),
            ("crop", 402.40, 411.92, S["s05_conn"], r(42, 230, 1042, 1000)),
            ("crop", 411.92, 417.76, S["s05_conn"], r(42, 900, 1042, 2100)),
            ("crop", 417.76, 422.86, S["s05_conn"], r(42, 230, 1042, 1000)),
            ("crop", 422.86, 430.96, S["s05_conn"], r(42, 900, 1042, 2100)),
            ("crop", 430.96, 437.37, S["s05_conn"], r(42, 230, 1042, 1000)),
            ("crop", 437.37, spans[5]["end"], S["s05_conn"], r(42, 900, 1042, 2100)),
        ],
    ]
    for si, ps in enumerate(secs_plan):
        plan.append(["header", HEADER_MS, [
            ("大人のデジタル安心室", 28, GRAY, "(w-text_w)/2", 292),
            (labels[si], 120, ACCENT, "(w-text_w)/2", 368),
            (titles[si], 58, DARK, "(w-text_w)/2", 570),
        ], None, True, (0, 0), (0, 0)])
        for row in ps:
            kind = row[0]
            t0, t1 = row[1], row[2]
            if kind == "two":
                plan.append(["two", t1 - t0, labels[si], row[5]["items"]])
            else:
                plan.append([kind, t1 - t0, labels[si],
                             [(row[3], row[4], None)]])

    # --- まとめ（v8と同じ静止切替・全体画面） ---
    sum_span = spans[6]
    dur = sum_span["end"] - sum_span["start"]
    header_dur = min(HEADER_MS, dur - 1.0)
    plan.append(["header", header_dur, [
        ("大人のデジタル安心室", 28, GRAY, "(w-text_w)/2", 292),
        ("まとめ", 110, ACCENT, "(w-text_w)/2", 368),
        ("5つの確認項目をおさらいしましょう", 44, DARK, "(w-text_w)/2", 570),
    ], None, True, (0, 0), (0, 0)])
    old = json.loads((WORK / "timeline.json").read_text(encoding="utf-8"))["units"]
    old_sum = [u for u in old if u["section"] == "まとめ"]
    old_total = old_sum[-1]["end"] - old_sum[0]["start"]
    new_sum_dur = dur - header_dur
    segs = []
    for u in old_sum:
        txt = u["text"]
        if "1つ目" in txt or "セキュリティ診断" in txt:
            still = S["s01_checkup"]
        elif "2つ目" in txt or "電話番号" in txt or "メール" in txt:
            still = S["s02_phone"]
        elif "3つ目" in txt or "2段階認証" in txt or "パスキー" in txt:
            still = S["s03_methods"]
        elif "4つ目" in txt or "端末" in txt:
            still = S["s04_devices"]
        elif "5つ目" in txt or "サービス" in txt:
            still = S["s05_conn"]
        else:
            still = S["s01_security"]
        segs.append((((u["start"] - old_sum[0]["start"]) / old_total) * new_sum_dur,
                     ((u["end"] - old_sum[0]["start"]) / old_total) * new_sum_dur,
                     still))
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
        plan.append(["full", en - st, "", [(still, FULL, None)]])
        cursor = en

    # --- CTA / エンドカード（v8準拠） ---
    plan.append(["static", 7.9, [
        ("役に立ったら、", 58, DARK, "(w-text_w)/2", 470),
        ("チャンネル登録して", 58, DARK, "(w-text_w)/2", 548),
        ("次回も一緒に確認しましょう", 58, DARK, "(w-text_w)/2", 626),
        ("大人のデジタル安心室", 46, ACCENT, "(w-text_w)/2", 760),
    ], "cta_visual.png", False, (528, 297), (696, 118)])
    used = sum(p[1] for p in plan)
    audio_total = t["end_audio_total"]
    end_dur = round(audio_total - used, 2)
    plan.append(["static", end_dur, [
        ("役に立ったら", 46, DARK, "(w-text_w)/2", 560),
        ("チャンネル登録して、また次回。", 46, DARK, "(w-text_w)/2", 636),
    ], "channel_logo_google.png", False, (480, 270), (720, 100)])

    # --- レンダリング&連結 ---
    out_parts = []
    n = 0
    for pt in plan:
        n += 1
        kind = pt[0]
        d = pt[1]
        fname = "panel" if kind in ("crop", "full", "two") else "static"
        p = WORK / f"v9_{n:02d}_{fname}.mp4"
        if kind in ("crop", "full", "two"):
            label = pt[2]
            content = pt[3]
            png = panel_png(f"{n:02d}", label, content)
            render_panel(d, p, png)
        else:
            render_static(d, p, pt[2], pt[3], pt[4], pt[5], pt[6],
                          underline=(kind == "header"),
                          fade_out=0.8 if kind == "endcard" else 0.0)
        out_parts.append(p)
    lst = WORK / "v9_concat.txt"
    lst.write_text("\n".join(f"file '{p.name}'" for p in out_parts), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c", "copy", str(WORK / "v9_video.mp4")],
                   check=True, cwd=WORK)
    subprocess.run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(WORK / "v9_video.mp4"), "-i", str(AUDIO),
        "-vf", "drawbox=x=0:y=885:w=1920:h=195:color=0x08101B@0.78:t=fill,"
               "subtitles=captions_v8.ass",
        "-c:v", "libx264", "-crf", "19", "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k", "-shortest", str(OUT)],
        check=True, cwd=EP)
    print(f"draft_v9.mp4 written: {OUT}")


if __name__ == "__main__":
    main()
