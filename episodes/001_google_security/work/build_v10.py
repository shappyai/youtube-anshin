# -*- coding: utf-8 -*-
"""第10稿 draft_v10.mp4 組み立て — VOICEVOX「剣崎雌雄」ナレーション版

v9 の映像デザインを継承:
- 1920x1080 / 下部字幕帯 (y885〜) / 72px字幕（captions_v10.ass）
- 構図3種のみ: full（全体=場所確認・短く） / crop（説明対象の大きな切り抜き） / two（比較の意味がある時のみ）
- モザイク済み素材使用・青枠・タップリップルなし・冒頭5項目・1/5〜5/5見出し・エンドカード

v10 の変更点:
- タイムラインを segments_manifest.csv（VOICEVOX実尺）に全面再配置
- 全体画面は原則4秒以内、それを超える説明は full→crop に分割
- 字幕・音声は VOICEVOX 実時間（narration_kenzaki_final.wav / captions_v10.ass）
"""
from __future__ import annotations

import csv
import json
import subprocess
import sys
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FFMPEG = r"C:\Users\user\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"

EP = Path(__file__).resolve().parents[1]
WORK = EP / "work"
AUDIO = EP / "audio" / "voicevox_kenzaki" / "narration_kenzaki_final.wav"
MANIFEST = EP / "audio" / "voicevox_kenzaki" / "segments_manifest.csv"
OUT = EP / "output" / "draft_v10.mp4"
FONT = "font.ttc"
PFONT = str(WORK / "font.ttc")

DARK = "0x1F2A37"
GRAY = "0x5B6570"
BG_PIL = (247, 245, 242)
DARK_PIL = (31, 42, 55)
GRAY_PIL = (91, 101, 112)
ACCENT = "0x2E6DA4"
HEADER_MS = 1.8
AREA_Y = 885
ENDCARD_SILENCE = 8.0
FULL_MAX = 4.0   # 全体画面は原則4秒以内
FULL_SPLIT = 3.0  # 超える場合の全体表示秒数


def load(name: str):
    return Image.open(WORK / name).convert("RGB")


def fit(w: int, h: int, maxw: int, maxh: int) -> tuple[int, int]:
    r = min(maxw / w, maxh / h)
    return max(int(w * r), 1), max(int(h * r), 1)


def panel_png(out_name: str, label: str, content: list[tuple]):
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
    p = WORK / f"v10panel_{out_name}.png"
    canvas.save(p)
    return p


def render_panel(dur: float, out: Path, png: Path):
    subprocess.run([FFMPEG, "-y", "-v", "error", "-loop", "1", "-framerate", "30",
                    "-t", f"{dur:.3f}", "-i", str(png),
                    "-vf", "scale=1920:1080", "-an", "-c:v", "libx264",
                    "-crf", "19", "-preset", "medium", "-pix_fmt", "yuv420p",
                    str(out)], check=True, cwd=WORK)


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
        fn = f"txt10_{out.stem}_{i}.txt"
        tf.append(dt_b(t, size, color, x, y, fn)
                  if visual == "intro_visual_v4.png" and i == 0
                  else dt(t, size, color, x, y, fn))
    if underline:
        tf.append(f"drawbox=x=760:y=730:w=400:h=6:color={ACCENT}:t=fill")
    inputs = [FFMPEG, "-y", "-v", "error",
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


def r(x1, y1, x2, y2):
    return (x1, y1, x2, y2)


def main():
    with MANIFEST.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    seg = {}
    for i, row in enumerate(rows):
        sid = int(row["segment_id"])
        seg[sid] = {
            "dur": float(row["duration_sec"]),
            "pad": float(row["pad_after_sec"]) if row["pad_after_sec"] else 0.0,
            "start": float(row["start_sec"]),
            "end": float(row["end_sec"]),
        }

    # 最終音声にエンドカード分の無音 8s を付加して総尺を確定
    with wave.open(str(AUDIO), "rb") as w:
        rate, ch, sw, nf = w.getframerate(), w.getnchannels(), w.getsampwidth(), w.getnframes()
    if nf / rate < seg[79]["end"] + ENDCARD_SILENCE - 0.5:
        import array
        with wave.open(str(AUDIO), "rb") as w:
            data = w.readframes(w.getnframes())
        extra = int(rate * ENDCARD_SILENCE)
        with wave.open(str(AUDIO), "wb") as w:
            w.setnchannels(ch)
            w.setsampwidth(sw)
            w.setframerate(rate)
            w.writeframes(data + b"\x00\x00" * (extra * sw // 2) * (ch if sw == 2 else 1))
    with wave.open(str(AUDIO), "rb") as w:
        audio_total = w.getnframes() / w.getframerate()
    print(f"audio total: {audio_total:.3f}s (narration {seg[79]['end']:.3f}s + endcard silence)")

    S = {s: load(f"{s}.png") for s in
         ["s01_security", "s01_checkup", "s02_phone", "s02b_email",
          "s03_top", "s03_methods", "s04_devices", "s05_conn"]}
    FULL = (0, 0, 1080, 2424)
    phone_re = r(42, 240, 1042, 950)
    email_re = r(42, 240, 1042, 1150)
    two_phone_email = {"kind": "two", "items": [
        (S["s02_phone"], phone_re, "電話番号"),
        (S["s02b_email"], email_re, "メールアドレス")]}
    two_passkey = {"kind": "two", "items": [
        (S["s03_top"], r(42, 230, 1042, 1050), "2段階認証"),
        (S["s01_security"], r(42, 2050, 1042, 2320), "パスキー")]}

    M = {}
    M[1] = {"kind": "intro"}
    M[2] = {"kind": "intro"}
    M[3] = {"kind": "intro"}
    M[4] = {"kind": "crop", "png": "s01_checkup", "rect": r(42, 380, 1042, 1150)}
    M[5] = {"kind": "crop", "png": "s01_security", "rect": r(42, 240, 1042, 720)}
    M[6] = {"kind": "full", "png": "s01_security", "fallback": r(42, 240, 1042, 720)}
    M[7] = {"kind": "crop", "png": "s01_security", "rect": r(42, 240, 1042, 720)}
    M[8] = {"kind": "crop", "png": "s01_security", "rect": r(42, 240, 1042, 720)}
    M[9] = {"kind": "crop", "png": "s01_security", "rect": r(42, 240, 1042, 720)}
    M[10] = {"kind": "crop", "png": "s01_security", "rect": r(42, 240, 1042, 720)}
    M[11] = {"kind": "crop", "png": "s01_checkup", "rect": r(42, 380, 1042, 1150)}
    M[12] = {"kind": "crop", "png": "s01_checkup", "rect": r(42, 380, 1042, 1150)}
    M[13] = {"kind": "crop", "png": "s01_checkup", "rect": r(42, 560, 1042, 2000)}
    M[14] = {"kind": "crop", "png": "s01_checkup", "rect": r(42, 560, 1042, 2000)}
    M[15] = {"kind": "crop", "png": "s01_checkup", "rect": r(42, 380, 1042, 1150)}
    M[16] = {"kind": "crop", "png": "s01_checkup", "rect": r(42, 380, 1042, 1150)}
    M[17] = {"kind": "crop", "png": "s01_checkup", "rect": r(42, 560, 1042, 2000)}
    for sid in (18, 19, 20, 21, 22, 23, 24, 25, 27):
        M[sid] = dict(two_phone_email)
    M[26] = {"kind": "crop", "png": "s02_phone", "rect": phone_re}
    M[28] = {"kind": "crop", "png": "s03_top", "rect": r(42, 230, 1042, 1050)}
    M[29] = {"kind": "crop", "png": "s03_top", "rect": r(42, 230, 1042, 1050)}
    M[30] = {"kind": "crop", "png": "s03_top", "rect": r(42, 230, 1042, 1050)}
    M[31] = {"kind": "crop", "png": "s03_top", "rect": r(42, 850, 1042, 1650)}
    M[32] = {"kind": "crop", "png": "s03_top", "rect": r(42, 850, 1042, 1650)}
    M[33] = dict(two_passkey)
    M[34] = dict(two_passkey)
    M[35] = {"kind": "crop", "png": "s03_top", "rect": r(42, 230, 1042, 1050)}
    M[36] = dict(two_phone_email)
    M[37] = dict(two_phone_email)
    M[38] = {"kind": "crop", "png": "s02b_email", "rect": email_re}
    M[39] = {"kind": "crop", "png": "s02b_email", "rect": email_re}
    M[40] = {"kind": "crop", "png": "s03_methods", "rect": r(42, 220, 1042, 1000)}
    M[41] = {"kind": "crop", "png": "s03_methods", "rect": r(42, 220, 1042, 1000)}
    M[42] = {"kind": "crop", "png": "s03_methods", "rect": r(42, 800, 1042, 1900)}
    M[43] = {"kind": "crop", "png": "s03_methods", "rect": r(42, 800, 1042, 1900)}
    M[44] = {"kind": "full", "png": "s04_devices", "fallback": r(42, 230, 1042, 950)}
    M[45] = {"kind": "crop", "png": "s04_devices", "rect": r(42, 230, 1042, 950)}
    M[46] = {"kind": "crop", "png": "s04_devices", "rect": r(42, 230, 1042, 950)}
    M[47] = {"kind": "crop", "png": "s04_devices", "rect": r(42, 230, 1042, 950)}
    for sid in range(48, 56):
        M[sid] = {"kind": "crop", "png": "s04_devices", "rect": r(42, 900, 1042, 2300)}
    M[56] = {"kind": "full", "png": "s05_conn", "fallback": r(42, 230, 1042, 1000)}
    M[57] = {"kind": "crop", "png": "s05_conn", "rect": r(42, 230, 1042, 1000)}
    M[58] = {"kind": "crop", "png": "s05_conn", "rect": r(42, 230, 1042, 1000)}
    M[59] = {"kind": "crop", "png": "s05_conn", "rect": r(42, 900, 1042, 2100)}
    M[60] = {"kind": "crop", "png": "s05_conn", "rect": r(42, 230, 1042, 1000)}
    M[61] = {"kind": "crop", "png": "s05_conn", "rect": r(42, 900, 1042, 2100)}
    M[62] = {"kind": "crop", "png": "s05_conn", "rect": r(42, 900, 1042, 2100)}
    M[63] = {"kind": "crop", "png": "s05_conn", "rect": r(42, 900, 1042, 2100)}
    M[64] = {"kind": "crop", "png": "s05_conn", "rect": r(42, 900, 1042, 2100)}
    M[65] = {"kind": "crop", "png": "s05_conn", "rect": r(42, 900, 1042, 2100)}
    M[66] = {"kind": "crop", "png": "s05_conn", "rect": r(42, 900, 1042, 2100)}
    M[67] = {"kind": "crop", "png": "s05_conn", "rect": r(42, 900, 1042, 2100)}
    M[68] = {"kind": "crop", "png": "s01_security", "rect": r(42, 240, 1042, 720)}
    M[69] = {"kind": "full", "png": "s01_checkup", "fallback": r(42, 380, 1042, 1150)}
    M[70] = dict(two_phone_email)
    M[71] = dict(two_passkey)
    M[72] = {"kind": "full", "png": "s04_devices", "fallback": r(42, 230, 1042, 950)}
    M[73] = {"kind": "full", "png": "s05_conn", "fallback": r(42, 230, 1042, 1000)}
    M[74] = {"kind": "full", "png": "s01_security", "fallback": r(42, 240, 1042, 720)}
    M[75] = {"kind": "full", "png": "s01_checkup", "fallback": r(42, 380, 1042, 1150)}
    M[76] = {"kind": "crop", "png": "s01_security", "rect": r(42, 240, 1042, 720)}
    M[77] = {"kind": "crop", "png": "s01_security", "rect": r(42, 240, 1042, 720)}
    M[78] = {"kind": "crop", "png": "s01_security", "rect": r(42, 240, 1042, 720)}
    M[79] = {"kind": "cta"}

    labels = ["1 / 5", "2 / 5", "3 / 5", "4 / 5", "5 / 5"]
    titles = ["セキュリティ診断", "再設定用の電話番号・メール", "2段階認証とパスキー",
              "ログイン中の端末", "リンク済みアプリ"]
    sections = [(4, 17, 0), (18, 27, 1), (28, 43, 2), (44, 55, 3), (56, 67, 4)]

    def content_of(e):
        if e["kind"] == "two":
            return e["items"]
        return [(S[e["png"]], e.get("rect") or FULL, None)]

    plan = []  # ("panel"|"static", dur, label|texts, content|visual, ...)

    # --- 冒頭（5項目ビジュアル） ---
    intro_dur = seg[4]["start"]
    plan.append(("static", intro_dur,
                 [("イメージ", 30, "0xF7F5F2", "(w-text_w)-140", 48)],
                 "intro_visual_v4.png", False, (1582, 890), (169, 0), False, 0.0))

    # --- セクション1〜5 ---
    for first, last, si in sections:
        plan.append(("header", HEADER_MS, [
            ("大人のデジタル安心室", 28, GRAY, "(w-text_w)/2", 292),
            (labels[si], 120, ACCENT, "(w-text_w)/2", 368),
            (titles[si], 58, DARK, "(w-text_w)/2", 570),
        ], None, True, (0, 0), (0, 0), True, 0.0))
        first_done = False
        for sid in range(first, last + 1):
            e = M[sid]
            dur = seg[sid]["dur"] + seg[sid]["pad"]
            if not first_done:
                dur -= HEADER_MS
                first_done = True
            if e["kind"] == "full" and dur > FULL_MAX:
                full_d = FULL_SPLIT
                rest_d = dur - FULL_SPLIT
                plan.append(("panel", full_d, labels[si],
                             [(S[e["png"]], FULL, None)]))
                plan.append(("panel", rest_d, labels[si],
                             [(S[e["png"]], e["fallback"], None)]))
            else:
                if dur <= 0.05:
                    continue
                plan.append(("panel", dur, labels[si], content_of(e)))

    # --- まとめ ---
    plan.append(("header", HEADER_MS, [
        ("大人のデジタル安心室", 28, GRAY, "(w-text_w)/2", 292),
        ("まとめ", 110, ACCENT, "(w-text_w)/2", 368),
        ("5つの確認項目をおさらいしましょう", 44, DARK, "(w-text_w)/2", 570),
    ], None, True, (0, 0), (0, 0), True, 0.0))
    first_done = False
    for sid in range(68, 79):
        e = M[sid]
        dur = seg[sid]["dur"] + seg[sid]["pad"]
        if not first_done:
            dur -= HEADER_MS
            first_done = True
        if e["kind"] == "full" and dur > FULL_MAX:
            plan.append(("panel", FULL_SPLIT, "",
                         [(S[e["png"]], FULL, None)]))
            plan.append(("panel", dur - FULL_SPLIT, "",
                         [(S[e["png"]], e["fallback"], None)]))
        else:
            if dur <= 0.05:
                continue
            plan.append(("panel", dur, "", content_of(e)))

    # --- CTA / エンドカード ---
    cta_dur = seg[79]["dur"] + seg[79]["pad"]
    plan.append(("static", cta_dur, [
        ("役に立ったら、", 58, DARK, "(w-text_w)/2", 470),
        ("チャンネル登録して", 58, DARK, "(w-text_w)/2", 548),
        ("次回も一緒に確認しましょう", 58, DARK, "(w-text_w)/2", 626),
        ("大人のデジタル安心室", 46, ACCENT, "(w-text_w)/2", 760),
    ], "cta_visual.png", False, (528, 297), (696, 118), False, 0.0))
    used = sum(p[1] for p in plan)
    end_dur = round(audio_total - used, 3)
    if end_dur < 2.0:
        raise SystemExit(f"endcard too short: {end_dur}s (check timing total)")
    plan.append(("static", end_dur, [
        ("役に立ったら", 46, DARK, "(w-text_w)/2", 560),
        ("チャンネル登録して、また次回。", 46, DARK, "(w-text_w)/2", 636),
    ], "channel_logo_google.png", False, (480, 270), (720, 100), False, 0.8))
    used = sum(p[1] for p in plan)
    print(f"plan clips={len(plan)} video_total={used:.3f}s audio_total={audio_total:.3f}s")
    if abs(used - audio_total) > 0.3:
        raise SystemExit(f"total mismatch: video {used:.3f} vs audio {audio_total:.3f}")

    # --- レンダリング&連結 ---
    out_parts = []
    n = 0
    for pt in plan:
        n += 1
        kind, d = pt[0], pt[1]
        fname = "panel" if kind in ("panel", "header") else "static"
        p = WORK / f"v10_{n:02d}_{fname}.mp4"
        if kind == "panel":
            label, content = pt[2], pt[3]
            png = panel_png(f"{n:02d}", label, content)
            render_panel(d, p, png)
        else:
            render_static(d, p, pt[2], pt[3], pt[4], pt[5], pt[6],
                          underline=(kind == "header"),
                          fade_out=0.8 if kind == "static" and pt[3] == "channel_logo_google.png" else 0.0)
        out_parts.append(p)
        print(f"clip {n:02d} {kind} {d:.2f}s")
    lst = WORK / "v10_concat.txt"
    lst.write_text("\n".join(f"file '{p.name}'" for p in out_parts), encoding="utf-8")
    subprocess.run([FFMPEG, "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c", "copy", str(WORK / "v10_video.mp4")],
                   check=True, cwd=WORK)
    subprocess.run([
        FFMPEG, "-y", "-v", "error",
        "-i", str(WORK / "v10_video.mp4"), "-i", str(AUDIO),
        "-vf", "drawbox=x=0:y=885:w=1920:h=195:color=0x08101B@0.78:t=fill,"
               "subtitles=captions_v10.ass",
        "-c:v", "libx264", "-crf", "19", "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k", "-shortest", str(OUT)],
        check=True, cwd=EP)
    print(f"draft_v10.mp4 written: {OUT}")


if __name__ == "__main__":
    main()
