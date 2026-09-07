# -*- coding: utf-8 -*-
"""第7稿 draft_v7.mp4 組み立て

- スマホは常に全体表示（旧ズーム方式を廃止）
- 説明対象は左右余白の「拡大インセット」（角丸カード・青枠・ソフトシャドウ）
  と、スマホ上の青系角丸ハイライト枠で対応表示（0.25〜0.4sフェード）
- 字幕 62px・帯 y900〜1080・縦中央 y990（{\\an5\\pos(960,990)}）
- 1:55付近の過剰説明削除済みタイムライン（timeline_v7 / narration_v5）
- エンドカード: ロゴ拡大・名称テキスト重複削除
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EP = Path(__file__).resolve().parents[1]
WORK = EP / "work"
ASSETS = WORK / "v7_assets"
AUDIO = EP / "audio" / "narration_v5.mp3"
OUT = EP / "output" / "draft_v7.mp4"
FONT = "font.ttc"

BG = "0xF7F5F2"
ACCENT = "0x2E6DA4"
DARK = "0x1F2A37"
GRAY = "0x5B6570"
HL = (76, 141, 224)
HEADER_MS = 1.8
PHONE_W, PHONE_H = 379, 850
PHONE_X, PHONE_Y = 770, 12
INSET_W = 520


def tl() -> dict:
    return json.loads((WORK / "timeline_v7.json").read_text(encoding="utf-8"))


def dt(text: str, size: int, color: str, x, y: int, fname: str) -> str:
    (WORK / fname).write_text(text, encoding="utf-8")
    return (f"drawtext=fontfile={FONT}:textfile={fname}:"
            f"fontsize={size}:fontcolor={color}:x={x}:y={y}:expansion=none")


def dt_b(text: str, size: int, color: str, x, y: int, fname: str) -> str:
    (WORK / fname).write_text(text, encoding="utf-8")
    return (f"drawtext=fontfile={FONT}:textfile={fname}:"
            f"fontsize={size}:fontcolor={color}:x={x}:y={y}:expansion=none"
            f":box=1:boxcolor=0x000000@0.35:boxborderw=14")


def make_inset(still: str, crop: tuple[int, int, int, int], idx: int) -> Path:
    """対象領域を切り出し、角丸カード（青枠+ソフトシャドウ）として保存。"""
    img = Image.open(WORK / still).convert("RGB")
    c = img.crop(crop)
    w0 = max(c.width, 1)
    h0 = round(INSET_W * c.height / w0)
    card = c.resize((INSET_W * 2, h0 * 2), Image.LANCZOS)
    radius = 22 * 2
    mask = Image.new("L", card.size, 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, card.width - 1, card.height - 1], radius=radius, fill=255)
    card.putalpha(Image.new("L", card.size, 255))
    # 角丸マスク適用
    rgba = Image.new("RGBA", card.size)
    rgba.paste(card, (0, 0), mask)
    # 青枠
    d2 = ImageDraw.Draw(rgba)
    d2.rounded_rectangle([3, 3, rgba.width - 4, rgba.height - 4], radius=radius - 2,
                         outline=HL + (255,), width=3 * 2)
    # ソフトシャドウ
    sh = Image.new("RGBA", (rgba.width + 48, rgba.height + 48), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle([24, 30, sh.width - 24, sh.height - 12], radius=radius,
                         fill=(20, 30, 40, 90))
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    out = Image.new("RGBA", sh.size, (0, 0, 0, 0))
    out.paste(sh, (0, 0), sh)
    out.paste(rgba, (24, 12), rgba)
    p = ASSETS / f"inset_{idx:02d}.png"
    out.save(p)
    return p


def make_hlight(rect: tuple[int, int, int, int] | None, idx: int) -> Path | None:
    """スマホ上の角丸ハイライト枠（青系・太さ4px）を生成。"""
    if not rect:
        return None
    x1, y1, x2, y2 = rect
    w = max(int((x2 - x1) * PHONE_W / 1080.0), 8)
    h = max(int((y2 - y1) * PHONE_H / 2424.0), 8)
    radius = max(8, min(w, h) // 6)
    img = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([4, 4, w + 3, h + 3], radius=radius, outline=HL + (255,), width=4)
    p = ASSETS / f"hl_{idx:02d}.png"
    img.save(p)
    return p


def render_scene(dur: float, out: Path, still: str, label: str,
                 crop: tuple | None = None, hl: tuple | None = None, idx: int = 0):
    """スマホ全体＋必要ならインセット＋ハイライト。"""
    frames = max(int(round(dur * 30)), 5)
    inputs = ["ffmpeg", "-y", "-v", "error",
              "-f", "lavfi", "-i", f"color=c={BG}:s=1920x1080:r=30:d={dur}",
              "-loop", "1", "-framerate", "30", "-t", f"{dur}", "-i", str(WORK / still)]
    fc = ""
    need_label = bool(hl) or bool(label.strip())
    last = "0"
    if crop:
        inset = make_inset(still, crop, idx)
        ins_img = Image.open(inset)
        iw, ih = ins_img.size
        side = "left" if idx % 2 == 0 else "right"
        ix = 110 if side == "left" else 1920 - 110 - iw
        iy = 437 - ih // 2
        fade_in, fade_out = 0.5, dur - 0.6
        inputs += ["-loop", "1", "-framerate", "30", "-t", f"{dur}", "-i", str(inset)]
        fc += (f"[2:v]zoompan=z='min(1.04,1+0.04*on/12)':d={frames}:"
               f"s={iw}x{ih}:fps=30,")
        fc += (f"fade=t=in:st={fade_in}:d=0.35,fade=t=out:st={fade_out}:d=0.4[ins];")
        if need_label:
            fc += f"[0:v][ins]overlay={ix}:{iy}[m1];"
            last = "m1"
        else:
            fc += f"[0:v][ins]overlay={ix}:{iy};"
            last = None
    else:
        fade_in, fade_out = 0.0, dur
    hlight = make_hlight(hl, idx)
    if hlight:
        x1, y1, x2, y2 = hl
        ox = round(x1 * PHONE_W / 1080.0)
        oy = round(y1 * PHONE_H / 2424.0)
        inputs += ["-loop", "1", "-framerate", "30", "-t", f"{dur}", "-i", str(hlight)]
    else:
        ox = oy = 0
    # スマホ重ね
    fc = fc.rstrip(";")
    fc += f"{';' if fc else ''}[1:v]scale={PHONE_W}:{PHONE_H}[ph]"
    if last:
        fc += f";[{last}][ph]overlay={PHONE_X}:{PHONE_Y}:shortest=1"
    else:
        fc += f";[0:v][ph]overlay={PHONE_X}:{PHONE_Y}:shortest=1"
    has_tf = bool(label.strip())
    if hlight:
        fc += "[m2]"
        if has_tf:
            fc += f";[m2][3:v]overlay={ox + 4}:{oy + 4}:enable='between(t,{fade_in},{fade_out})'[m3]"
            last = "m3"
        else:
            fc += f";[m2][3:v]overlay={ox + 4}:{oy + 4}:enable='between(t,{fade_in},{fade_out})'"
            last = None
    elif has_tf:
        fc += "[m2]"
        last = "m2"
    tf = []
    if label.strip():
        fn = f"txt7_{out.stem}_label.txt"
        (WORK / fn).write_text(label, encoding="utf-8")
        tf.append(f"drawtext=fontfile={FONT}:textfile={fn}:"
                  f"fontsize=40:fontcolor={DARK}:x=48:y=36:expansion=none")
    if tf:
        fc += f";[{last}]" + ",".join(tf)
    inputs += ["-filter_complex", fc, "-an", "-c:v", "libx264", "-crf", "19",
               "-preset", "medium", out.name]
    subprocess.run(inputs, check=True, cwd=WORK)
    print(f"scene {out.name} ({dur:.1f}s inset={bool(crop)})")


def render_static(dur: float, out: Path, texts, visual: str | None = None,
                  fullbleed: bool = False, vscale=(528, 297), vpos=(696, 118),
                  underline: bool = False, fade_out: float = 0.0):
    tf = []
    for i, (t, size, color, x, y) in enumerate(texts):
        fn = f"txt7_{out.stem}_{i}.txt"
        if i == 0 and out.stem == "v7_01_intro":
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
    t = tl()
    secs = t["sections"]
    sec_start = {s["name"]: round(s["start"], 2) for s in secs}
    total_units = round(t["total_units"], 2)
    cta_start = t["cta_start"]
    order = ["はじめに", "1. セキュリティ診断", "2. 再設定用の電話番号・メール",
             "3. 2段階認証とパスキー", "4. 心当たりのない端末",
             "5. Googleでログインしたサービス", "まとめ"]
    spans = []
    for i, name in enumerate(order):
        st = sec_start.get(name, 0.0)
        en = sec_start.get(order[i + 1], total_units) if i + 1 < len(order) else total_units
        spans.append({"name": name, "start": st, "end": en})

    parts = []
    idx = 0

    # --- 冒頭（v6維持・y0〜890）---
    intro_dur = spans[0]["end"] - spans[0]["start"]
    parts.append(("intro", intro_dur, [
        ("イメージ", 30, "0xF7F5F2", "(w-text_w)-140", 48),
    ], "intro_visual_v4.png", False, (1582, 890), (169, 0)))

    # --- セクション本編（インセット演出・文言同期は既定シーケンス）---
    plan = [
        {"num": "1 / 5", "name": "セキュリティ診断", "span": 1, "frac": [0.165, 0.5, 0.661, 1.0],
         "scenes": [
             ("s01_security.png", None, None),
             ("s01_security.png", (160, 525, 920, 955), (42, 625, 1042, 856)),
             ("s01_checkup.png", None, None),
             ("s01_checkup.png", (160, 180, 920, 610), (120, 200, 960, 520)),
         ]},
        {"num": "2 / 5", "name": "再設定用の電話番号・メール", "span": 2,
         "frac": [0.148, 0.5, 0.671, 1.0],
         "scenes": [
             ("s02_phone.png", None, None),
             ("s02_phone.png", (140, 700, 940, 1200), (42, 520, 1042, 1400)),
             ("s02b_email.png", None, None),
             ("s02b_email.png", (140, 780, 940, 1320), (42, 500, 1042, 1500)),
         ]},
        {"num": "3 / 5", "name": "2段階認証とパスキー", "span": 3,
         "frac": [0.110, 0.40, 0.514, 0.72, 1.0],
         "scenes": [
             ("s03_top.png", None, None),
             ("s03_top.png", (140, 950, 940, 1450), (63, 1053, 1021, 1510)),
             ("s03_methods.png", None, None),
             ("s03_methods.png", (240, 1800, 960, 2070), (273, 1864, 882, 2006)),
             ("s03_methods.png", (140, 2100, 940, 2400), (63, 2034, 1018, 2363)),
         ]},
        {"num": "4 / 5", "name": "ログイン中の端末", "span": 4,
         "frac": [0.228, 0.629, 1.0],
         "scenes": [
             ("s04_devices.png", None, None),
             ("s04_devices.png", (250, 1080, 1010, 1350), (294, 1040, 1018, 1400)),
             ("s04_devices.png", (260, 1500, 1020, 1820), (294, 1450, 1018, 1800)),
         ]},
        {"num": "5 / 5", "name": "リンク済みアプリ", "span": 5,
         "frac": [0.191, 0.623, 1.0],
         "scenes": [
             ("s05_conn.png", None, None),
             ("s05_conn.png", (160, 400, 920, 840), (63, 380, 1021, 850)),
             ("s05_conn.png", (140, 1820, 940, 2280), (42, 1750, 1042, 2300)),
         ]},
    ]
    for sec in plan:
        span = spans[sec["span"]]
        dur = span["end"] - span["start"]
        header_dur = min(HEADER_MS, dur - 1.0)
        parts.append(("header", header_dur, [
            ("大人のデジタル安心室", 28, GRAY, "(w-text_w)/2", 292),
            (sec["num"], 120, ACCENT, "(w-text_w)/2", 368),
            (sec["name"], 58, DARK, "(w-text_w)/2", 570),
        ], None, True, (0, 0), (0, 0)))
        panel = dur - header_dur
        prev = 0.0
        for endf, scene in zip(sec["frac"], sec["scenes"]):
            endv = panel * endf
            if endv <= prev:
                continue
            d = endv - prev
            prev = endv
            still, crop, hl = scene
            idx += 1
            parts.append(("scene", d, (still, sec["num"], crop, hl, idx)))

    # --- まとめ（静止切替・v6維持）---
    sum_span = spans[6]
    dur = sum_span["end"] - sum_span["start"]
    header_dur = min(HEADER_MS, dur - 1.0)
    parts.append(("header", header_dur, [
        ("大人のデジタル安心室", 28, GRAY, "(w-text_w)/2", 292),
        ("まとめ", 110, ACCENT, "(w-text_w)/2", 368),
        ("5つの確認項目をおさらいしましょう", 44, DARK, "(w-text_w)/2", 570),
    ], None, True, (0, 0), (0, 0)))
    segs = []
    units = json.loads((WORK / "timeline.json").read_text(encoding="utf-8"))["units"]
    # まとめの古いタイムラインは削除ユニットでずれるため、v7メタの全体比率で縮小マップ
    old_sum = [u for u in units if u["section"] == "まとめ"]
    old_total = old_sum[-1]["end"] - old_sum[0]["start"]
    new_sum_dur = dur - header_dur
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
        rel0 = (u["start"] - old_sum[0]["start"]) / old_total
        rel1 = (u["end"] - old_sum[0]["start"]) / old_total
        segs.append((rel0 * new_sum_dur, rel1 * new_sum_dur, still))
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
        parts.append(("scene", en - st, (still, "", None, None, idx)))
        cursor = en

    # --- CTA / エンドカード（ロゴ拡大・名称テキスト削除）---
    cta_dur = 7.9
    parts.append(("cta", cta_dur, [
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
        p = WORK / f"v7_{i:02d}_{kind}.mp4"
        if kind == "scene":
            still, label, crop, hl, idx2 = part[2]
            render_scene(round(d, 3), p, still, label, crop, hl, idx2)
        elif kind == "header":
            render_static(round(d, 3), p, part[2], part[3], part[4], part[5], part[6],
                          underline=True)
        else:
            render_static(round(d, 3), p, part[2], part[3], part[4], part[5], part[6],
                          fade_out=0.8 if kind == "endcard" else 0.0)
        out_parts.append(p)
    lst = WORK / "v7_concat.txt"
    lst.write_text("\n".join(f"file '{p.name}'" for p in out_parts), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c", "copy", str(WORK / "v7_video.mp4")],
                   check=True, cwd=WORK)
    subprocess.run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(WORK / "v7_video.mp4"), "-i", str(AUDIO),
        "-vf", "drawbox=x=0:y=900:w=1920:h=180:color=0x08101B@0.78:t=fill,"
               "subtitles=captions_v7.ass",
        "-c:v", "libx264", "-crf", "19", "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k", "-shortest", str(OUT)],
        check=True, cwd=EP)
    print(f"draft_v7.mp4 written: {OUT}")


if __name__ == "__main__":
    main()
