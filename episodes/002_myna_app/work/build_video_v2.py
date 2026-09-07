# -*- coding: utf-8 -*-
"""Episode 002 draft_v2 builder.

ChatGPT生成の完成画像（assets/generated_scenes/scene_*.png）をフルスクリーンで使用し、
公式素材を空スロットへ合成する。Codexはレイアウトを新規デザインしない。

1) 合成: work/v2_composed/scene_XXX.png（公式crop・アイコン・FAQ引用テキスト）
2) クリップ: scene_planのanimationに沿って zoompan（none/slow_zoom/slow_pan）
3) 連結: xfadeチェーン（既定0.5s／セクション境界0.3s／SCENE-033は033→033bへ切り替え）
4) 最終: ナレーション＋captions_v2.ass（97cue・下部濃紺帯 y900-1080）を焼き込み
"""
from __future__ import annotations

import csv
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[3]
EP = ROOT / "episodes" / "002_myna_app"
GEN = EP / "assets" / "generated_scenes"
OFF = EP / "assets" / "official"
BROWSER = OFF / "browser"
WORK = EP / "work"
COMPOSED = WORK / "v2_composed"
CLIPS = WORK / "v2_clips"
OUT = EP / "output"
NARRATION = EP / "audio" / "voicevox_kenzaki" / "narration_kenzaki.wav"
MANIFEST = EP / "audio" / "voicevox_kenzaki" / "segments_manifest.csv"

BAND_Y = 900
BAND = (22, 38, 63)
BAND_EDGE = (60, 86, 128)
NAVY = (26, 42, 74)
GRAY = (110, 122, 140)
WHITE = (255, 255, 255)
SUBTITLE_MAX_W = 1800  # 1920px画面で左右60pxを確保した72px相当の上限

FONT_PATH = r"C:\Windows\Fonts\yugothb.ttc"

# timeline: scene id -> (start, end)  [source: timeline_plan.csv]
SCENES = {
    "SCENE-001": (0.000, 10.545), "SCENE-002": (10.545, 18.889),
    "SCENE-003": (18.889, 25.174), "SCENE-004": (25.174, 36.357),
    "SCENE-005": (36.357, 52.364), "SCENE-006": (52.364, 70.707),
    "SCENE-007": (70.707, 80.974), "SCENE-008": (80.974, 95.866),
    "SCENE-009": (95.866, 115.647), "SCENE-010": (115.647, 135.078),
    "SCENE-011": (135.078, 149.082), "SCENE-012": (149.082, 165.521),
    "SCENE-013": (166.205, 179.730), "SCENE-014": (179.730, 196.468),
    "SCENE-015": (196.468, 206.319), "SCENE-016": (206.319, 227.042),
    "SCENE-017": (227.042, 234.267), "SCENE-018": (234.267, 254.889),
    "SCENE-019": (254.889, 263.950), "SCENE-020": (263.950, 271.767),
    "SCENE-021": (271.767, 284.724), "SCENE-022": (284.724, 305.275),
    "SCENE-023": (305.275, 319.397), "SCENE-024": (319.397, 339.455),
    "SCENE-025": (339.455, 352.639), "SCENE-026": (352.639, 366.392),
    "SCENE-027": (366.392, 384.568), "SCENE-028": (384.568, 391.034),
    "SCENE-029": (391.034, 406.288), "SCENE-030": (406.288, 414.073),
    "SCENE-031": (414.073, 428.771), "SCENE-032": (428.771, 440.838),
    "SCENE-033": (440.838, 456.421), "SCENE-034": (456.421, 466.467),
    "SCENE-035": (466.467, 475.142),
}

ANIM = {
    1: "slow_zoom", 4: "slow_pan", 5: "slow_zoom", 6: "slow_pan",
    9: "slow_zoom", 12: "slow_pan", 16: "slow_zoom", 18: "slow_pan",
    23: "slow_zoom",
}

# transition seconds AFTER each visual clip (0.3=静的切替, 0.5=crossfade)
# clip order: 1..32, 33A, 33B, 34, 35
def transitions() -> list[float]:
    t: list[float] = []
    for i in range(1, 33):
        t.append(0.3 if i in (6, 12, 19, 25, 31) else 0.5)
    t.append(0.5)  # 33A -> 33B
    t.append(0.5)  # 33B -> 34
    t.append(0.5)  # 34 -> 35
    t.append(0.0)  # end
    return t


TRANS = transitions()

# composite specs: scene_no -> [ (slot_box, kind, asset, crop or lines) ]
ICON_ROUNDED = OFF / "official_icon_rounded_3x.png"
ICON_LIMITED = OFF / "official_icon_limited_3x.png"

COMPOSITES: dict[int, list] = {
    1: [((95, 180, 515, 600), "icon", ICON_ROUNDED, None)],
    5: [((1000, 220, 1720, 650), "image", OFF / "official_screen_card.png", None)],
    8: [((310, 250, 740, 680), "icon", ICON_ROUNDED, None),
        ((1180, 250, 1610, 680), "icon", ICON_LIMITED, None)],
    9: [((1210, 220, 1770, 640), "crop", BROWSER / "br_03_news_20260825.png", (143, 240, 1297, 760))],
    10: [((1120, 160, 1710, 420), "crop", BROWSER / "br_02_svc_top_faq.png", (0, 5300, 1440, 5680)),
         ((1120, 480, 1710, 740), "crop", BROWSER / "br_02_svc_top_faq.png", (0, 5680, 1440, 6080))],
    13: [((1180, 240, 1650, 760), "crop", BROWSER / "br_09_gplay.png", (80, 100, 1240, 560))],
    14: [((1160, 280, 1770, 660), "quote",
          ["App StoreやGoogle Playの自動更新設定を", "ご利用の場合は、自動的に更新される", "場合があります。"],
          "出典：マイナアプリ よくある質問")],
    15: [((1130, 250, 1730, 650), "crop", BROWSER / "br_09_gplay.png", (80, 100, 1240, 560))],
    17: [((1130, 280, 1740, 650), "quote",
          ["Q. アプリを入れ直したら、", "マイナアプリが開かなくなりました。"],
          "出典：マイナアプリ よくある質問")],
    18: [((1160, 230, 1770, 670), "quote",
          ["A. 後からインストールしたアプリが", "優先して開く仕組みになっています。"],
          "出典：マイナアプリ よくある質問")],
    21: [((1450, 660, 1780, 850), "crop", BROWSER / "br_06_sysreq.png", (0, 300, 1440, 1150))],
    22: [((1030, 210, 1330, 720), "image", OFF / "official_screen_register_card_auth.png", None),
         ((1440, 210, 1740, 720), "image", OFF / "official_screen_register_biometric.png", None)],
    23: [((1090, 220, 1580, 600), "image", OFF / "official_screen_register_device_lock.png", None),
         ((1630, 280, 1840, 600), "crop", BROWSER / "br_06_sysreq.png", (0, 1500, 1440, 2350))],
    27: [((120, 240, 900, 650), "crop", BROWSER / "br_08_appstore.png", (250, 60, 1440, 620)),
         ((1020, 240, 1800, 650), "crop", BROWSER / "br_09_gplay.png", (80, 100, 1240, 560))],
    28: [((735, 240, 1185, 690), "icon", ICON_ROUNDED, None)],
    29: [((1160, 240, 1770, 670), "crop", BROWSER / "br_10_notice_fakeapp.png", (0, 380, 1440, 1000))],
    30: [((1180, 280, 1740, 650), "crop", BROWSER / "br_11_notice_phishing.png", (0, 400, 1440, 1150))],
    31: [((1240, 270, 1780, 650), "crop", BROWSER / "br_10_notice_fakeapp.png", (0, 1000, 1440, 1600))],
}

# SCENE-033: split A(seg74) / B(seg75). switch point from manifest.
SWITCH_033 = 446.127


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size, index=0)


def fit_box(src_w: int, src_h: int, box) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    scale = min(bw / src_w, bh / src_h)
    dw, dh = int(src_w * scale), int(src_h * scale)
    x = x0 + (bw - dw) // 2
    y = y0 + (bh - dh) // 2
    return x, y, x + dw, y + dh


def paste_contain(canvas: Image.Image, img: Image.Image, box, radius: int = 0):
    x0, y0, x1, y1 = fit_box(img.size[0], img.size[1], box)
    img = img.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    if img.mode == "RGBA":
        alpha = img.getchannel("A")
        img = img.convert("RGB")
        canvas.paste(img, (x0, y0), alpha)
    else:
        canvas.paste(img, (x0, y0))


def compose(scene_no: int, use_b: bool = False) -> Image.Image:
    name = f"scene_{scene_no:03d}b.png" if use_b else f"scene_{scene_no:03d}.png"
    canvas = Image.open(GEN / name).convert("RGB")
    for box, kind, asset, param in COMPOSITES.get(scene_no, []):
        if kind == "icon":
            img = Image.open(asset).convert("RGBA")
            paste_contain(canvas, img, box)
        elif kind == "image":
            img = Image.open(asset).convert("RGB")
            paste_contain(canvas, img, box)
        elif kind == "crop":
            img = Image.open(asset).convert("RGB").crop(param)
            paste_contain(canvas, img, box)
        elif kind == "quote":
            draw_quote(canvas, box, asset, param)
    draw_band(canvas)
    return canvas


def draw_band(canvas: Image.Image):
    d = ImageDraw.Draw(canvas)
    d.rectangle((0, BAND_Y, 1920, 1080), fill=BAND)
    d.line((0, BAND_Y, 1920, BAND_Y), fill=BAND_EDGE, width=3)


def draw_quote(canvas: Image.Image, box, lines, source):
    d = ImageDraw.Draw(canvas)
    x0, y0, x1, y1 = box
    pad = 24
    inner_w = x1 - x0 - pad * 2
    fs = 38
    fnt = font(fs)
    while True:
        wmax = max([d.textlength(ln, font=fnt) for ln in lines] + [0])
        if wmax <= inner_w or fs <= 30:
            break
        fs -= 2
        fnt = font(fs)
    lh = int(fs * 1.5)
    src_f = font(24)
    total_h = len(lines) * lh + 16 + 30
    y = y0 + (y1 - y0 - total_h) // 2
    for ln in lines:
        d.text(((x0 + x1) // 2, y), ln, font=fnt, fill=NAVY, anchor="ma")
        y += lh
    y += 16
    d.text(((x0 + x1) // 2, y), source, font=src_f, fill=GRAY, anchor="ma")


def clip_durations() -> list[tuple[str, float]]:
    """[(clip_name, dur)] ordered. 33A and 33B split SCENE-033."""
    order = [f"SCENE-{n:03d}" for n in range(1, 36)]
    starts = [SCENES[s][0] for s in order]
    ends = [SCENES[s][1] for s in order]
    switch = SWITCH_033
    out: list[tuple[str, float]] = []
    boundaries = starts + [ends[34]]
    for i, n in enumerate(range(1, 36)):
        if n == 33:
            out.append(("scene_033.png", switch - starts[i] + TRANS[len(out)]))
            out.append(("scene_033b.png", boundaries[i + 1] - switch + TRANS[len(out)]))
        else:
            out.append((f"scene_{n:03d}.png", boundaries[i + 1] - starts[i] + TRANS[len(out)]))
    return out


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--compose-only", action="store_true")
    ap.add_argument("--output", type=Path, default=OUT / "draft_v2.mp4",
                    help="最終動画の出力先（既定: output/draft_v2.mp4）")
    args = ap.parse_args()

    if subprocess.run(["ffmpeg", "-version"], capture_output=True).returncode != 0:
        raise SystemExit("ffmpeg not found")
    COMPOSED.mkdir(parents=True, exist_ok=True)
    CLIPS.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    # 1. compose
    for n in range(1, 36):
        for use_b in (True, False) if n == 33 else (False,):
            canvas = compose(n, use_b)
            cname = f"scene_{n:03d}b.png" if use_b else f"scene_{n:03d}.png"
            canvas.save(COMPOSED / cname)
            print("composed", cname, flush=True)
    if args.compose_only:
        return 0

    # 2. clips
    clips = clip_durations()
    total_core = sum(d - TRANS[i] for i, (_, d) in enumerate(clips))
    print(f"clips={len(clips)} projected_total={total_core:.3f} (target 475.142)")
    for i, (cname, dur) in enumerate(clips):
        seg = CLIPS / f"clip_{i:03d}.mp4"
        if seg.exists():
            continue
        src = COMPOSED / cname
        scene_no = int(cname[6:9])
        anim = ANIM.get(scene_no, "none")
        frames = max(int(round(dur * 30)), 30)
        if anim == "slow_zoom":
            step = 0.05 / frames
            vf = (f"zoompan=z='min(zoom+{step:.6f},1.05)':"
                  f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30")
        elif anim == "slow_pan":
            vf = ("zoompan=z='1.03':"
                  f"x='(iw-iw/zoom)*on/{frames}':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30")
        else:
            vf = "scale=1920:1080,format=yuv420p"
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", "30",
             "-t", f"{dur:.3f}", "-i", str(src),
             "-vf", vf, "-frames:v", str(frames),
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
             "-pix_fmt", "yuv420p", "-r", "30", str(seg)],
            check=True,
        )
        print(f"clip {i:03d} {cname} dur={dur:.3f} anim={anim}", flush=True)

    # 3. xfade chain
    inputs = []
    for i in range(len(clips)):
        inputs += ["-i", str(CLIPS / f"clip_{i:03d}.mp4")]
    fc = []
    prev = "[0:v]"
    cum_d = clips[0][1]
    cum_t = 0.0
    for i in range(1, len(clips)):
        d = TRANS[i - 1]
        out_l = f"[v{i}]"
        if d <= 0:
            # cut: plain concat inside chain
            fc.append(f"{prev}[{i}:v]concat=n=2:v=1:a=0{out_l}")
        else:
            offset = cum_d - cum_t - d
            fc.append(f"{prev}[{i}:v]xfade=transition=fade:duration={d:.2f}:offset={offset:.3f}{out_l}")
        cum_d += clips[i][1]
        if d > 0:
            cum_t += d
        prev = out_l
    fc.append(f"{prev}format=yuv420p[vout]")
    video_xfade = WORK / "v2_xfade.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", *inputs,
         "-filter_complex", ";".join(fc), "-map", "[vout]",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
         "-pix_fmt", "yuv420p", "-r", "30", str(video_xfade)],
        check=True,
    )
    print("xfade done:", video_xfade)

    # 4. final mux with captions
    ass_file = EP / "captions_v2.ass"
    make_captions_v2(ass_file)
    draft = args.output if args.output.is_absolute() else ROOT / args.output
    draft.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error",
         "-i", str(video_xfade), "-i", str(NARRATION),
         "-vf", f"ass={ass_file.relative_to(ROOT).as_posix()}",
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
         "-shortest", str(draft)],
        check=True,
    )
    print(f"draft_v2: {draft} ({draft.stat().st_size} bytes)")
    return 0


def make_captions_v2(ass_path: Path) -> None:
    """subtitle_plan.md の97cueをASS化（72px・下部帯・実測segment時刻ベース）。"""
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Yu Gothic,72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,3,0,5,60,60,45,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with MANIFEST.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    seg = {int(r["segment_id"]): r for r in rows}
    # SUB plan: (segment_id, [cue texts])  — split units get 2-3 cues with
    # timing split proportional to display text width.
    plan = build_sub_plan(seg)
    out = [header]
    for sub in plan:
        start = float(seg[sub["seg"]]["start_sec"])
        end = float(seg[sub["seg"]]["end_sec"])
        dur = end - start
        lines = sub["cues"]
        widths = [est_w(c) for c in lines]
        total_w = sum(widths)
        acc = 0.0
        for c, wd in zip(lines, widths):
            st = start + dur * (acc / total_w)
            acc += wd
            en = start + dur * (acc / total_w)
            t = c.replace("\n", "\\N")
            out.append(f"Dialogue: 0,{ts(st)},{ts(en)},Default,,0,0,45,,{{\\an5\\pos(960,980)}}{t}")
            assert est_w(c) <= SUBTITLE_MAX_W, f"overflow: {c}"
    ass_path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"captions_v2.ass: {sum(len(s['cues']) for s in plan)} cues")


def build_sub_plan(seg: dict) -> list[dict]:
    """subtitle_plan.md の表（SUB-ID→segment→表示行）を組み込む。"""
    # (segment_id, [cue表示（'\n'は2行目）])
    plan = [
        (1, ["アプリの名前やアイコンが、\n急に変わって驚いた方はいませんか。"]),
        (2, ["マイナポータルアプリは、8月25日から\n「マイナアプリ」になりました。"]),
        (3, ["お伝えしますが、マイナポータルという\nサービス自体は、なくなりません。"]),
        (4, ["アプリを消して、入れ直す\n必要もありません。"]),
        (5, ["今日は、何が変わったのか、今すべきことを\n5つに分けて確認します。"]),
        (6, ["マイナアプリは、これまで使われてきた\nマイナポータルアプリの、新しい名前です。"]),
        (7, ["同じアプリのアップデート版で、\nいわば「名前を変えた」ものです。"]),
        (8, ["そこに、「デジタル認証アプリ」の\n機能も統合されました。"]),
        (9, ["デジタル認証アプリは、マイナンバーカードで\n「本人であることを確認する」ためのアプリでした。"]),
        (10, ["「認証」は「本人確認」という意味です。"]),
        (11, ["これまで、行政の手続きには\nマイナポータルアプリ、", "民間のサービスにはデジタル認証アプリと、\n場面によって使い分ける必要がありました。"]),
        (12, ["それが、マイナアプリひとつで\nできるようになります。"]),
        (13, ["ひとつのアプリにまとめたのが、\n今回の変更の中心です。"]),
        (14, ["変わったのは、主に3つです。"]),
        (15, ["1つ目は、スマホアプリの名前です。"]),
        (16, ["「マイナポータルアプリ」が\n「マイナアプリ」になりました。"]),
        (17, ["2つ目は、アプリアイコンです。"]),
        (18, ["ピンクのグラデーションに「マイナ」の文字と、\n桜のマークのデザインになりました。"]),
        (19, ["しばらくの間は、左下に「マイナちゃん」が\nついた、期間限定のアイコンです。"]),
        (20, ["デジタル庁は、年内をめどに、\n最終的なデザインに統一すると案内しています。"]),
        (21, ["3つ目は、ログインや認証に使うアプリが、\nひとつに統合されたことです。"]),
        (22, ["デジタル認証アプリは、2026年8月25日をもって、\n単体での提供が終了しました。"]),
        (23, ["開くと、マイナアプリの利用を\n案内する画面が表示される、", "と公式のよくある質問にあります。"]),
        (24, ["使っていた人も、同じ機能を\nマイナアプリで引き続き使えます。"]),
        (25, ["ここで、いちばん大事なことをお伝えします。"]),
        (26, ["マイナポータルというサービス自体が、\nなくなったわけではありません。"]),
        (27, ["マイナポータルは、行政サービスの\nオンライン窓口です。"]),
        (28, ["ウェブサイトは、引き続き使えます。"]),
        (29, ["医療費などの自己情報の確認や、\n引越しやパスポートの申請も、今までどおりです。"]),
        (30, ["変わったのは、スマホアプリの\n名前とアイコン、", "そしてログインや認証に使うアプリが\n統合されたことです。"]),
        (31, ["ログインのときの本人確認の役割が、\nマイナポータルアプリから、", "マイナアプリにバトンタッチされた、\nと考えると分かりやすいです。"]),
        (32, ["では、ずっとマイナポータルアプリを\n使っていた人は、何をすればいいのでしょうか。"]),
        (33, ["まず、今お使いのアプリの\n名前とアイコン、", "そして、ストアで公開されている\n情報を確認してください。"]),
        (34, ["マイナポータルアプリなら、アップデートするだけで、\nそのままマイナアプリとして使えます。"]),
        (35, ["削除して、入れ直す\n必要はありません。"]),
        (36, ["スマホの「自動更新」の設定がオンになっていれば、\nそのまま自動で更新されている場合があります。"]),
        (37, ["オンになっていなければ、\nApp StoreやGoogle Playで", "「マイナアプリ（旧マイナポータルアプリ）」を\n探して、ご自分で更新してください。"]),
        (38, ["アップデート後も、スマホの中に入れた\nマイナンバーカードの設定や、", "これまでの機能・データは\n引き継がれます。"]),
        (39, ["再登録は不要です。"]),
        (40, ["アップデートしなくても、\nマイナポータルアプリは当面使えます。"]),
        (41, ["ただ、一部の手続きでは、マイナアプリが\n必要になる、と公式に案内されています。"]),
        (42, ["ここで注意です。"]),
        (43, ["分からなくなったからといって、アプリを\n削除して入れ直すのは、まず待ってください。"]),
        (44, ["公式のよくある質問には、アプリを入れ直したあと、\nマイナアプリが開かなくなった、", "という質問への案内があります。"]),
        (45, ["スマホには「後からインストールしたアプリが\n優先して開く」という仕組みがあり、", "デジタル認証アプリを後から入れ直すと、\nマイナアプリの代わりに開くことがあります。"]),
        (46, ["困ったときは、まず削除ではなく、", "公式のよくある質問や、概要欄の\n公式ページを確認するのが安心です。"]),
        (47, ["次に、新しく使う人や、アップデート後に\n開けない人向けの確認です。"]),
        (48, ["まず、動作環境です。"]),
        (49, ["iPhoneはiOS 16.4以上、Androidは\nAndroid 11以降で、NFC機能が必要です。"]),
        (50, ["NFCは、カードをかざして\n読み取るための機能です。"]),
        (51, ["新しく使う人は、初回だけ\n「利用登録」という手続きが必要です。"]),
        (52, ["お手元に、マイナンバーカードと、数字4桁の\n「利用者証明用暗証番号」を用意してください。"]),
        (53, ["実物のカードをかざすか、スマホの中に\nカードを入れている人は、", "顔や指紋で認証します。"]),
        (54, ["また、端末のロック設定が必須です。"]),
        (55, ["PIN、顔認証、指紋認証など、スマホ本体の\nロックが設定されていないと、", "マイナアプリは使えません、\nと公式に案内されています。"]),
        (56, ["もし、マイナポータルにログインできない場合は、\nよくある原因があります。"]),
        (57, ["ブラウザの「プライベートブラウズ」や\n「シークレットモード」を使っていると、", "ストアへの移動を繰り返すことが\nあるそうです。"]),
        (58, ["通常モードに戻して、スマホを再起動してから、\nもう一度試してください。"]),
        (59, ["なお、この動画では、カードの読み取りや\n暗証番号の入力は実演しません。"]),
        (60, ["個人情報にかかわる手続きは、ご自身のスマホで、\n画面の案内に沿って進めてください。"]),
        (61, ["最後に、偽物のアプリや、フィッシングに\nだまされないための、本物の確認ポイントです。"]),
        (62, ["公式のマイナアプリは、App StoreとGoogle Playの、\nふたつの場所からだけ、ダウンロードできます。"]),
        (63, ["アプリの名前は「マイナアプリ\n（旧マイナポータルアプリ）」、", "提供元の表示は、App Storeでは\n「Digital Agency of Japan」、", "Google Playでは「デジタル庁」です。"]),
        (64, ["どちらの場合も、デジタル庁が\n提供元であることを確認してください。"]),
        (65, ["アイコンのデザインは、ピンクのグラデーションに\n「マイナ」の文字と、桜のマークです。"]),
        (66, ["デジタル庁は、マイナポータルをかたる\n偽サイトや偽アプリへの注意喚起を出しています。"]),
        (67, ["メールや電話で、アプリのダウンロードや、\n暗証番号の入力を求められたら、まず疑ってください。"]),
        (68, ["暗証番号などをメールや電話で聞かれても、\n入力・回答しないよう、デジタル庁は案内しています。"]),
        (69, ["公式の相談窓口は、マイナンバー総合フリーダイヤル、\n0120-95-0178です。"]),
        (70, ["心配なことがあれば、一人で判断せず、\n確認するのもひとつの方法です。"]),
        (71, ["今日の内容をまとめます。"]),
        (72, ["今やっていただきたいことは、\n3つです。"]),
        (73, ["1つ目、まず、お使いのアプリが本物かどうか、", "名前と提供元とアイコンを確認する。"]),
        (74, ["2つ目、マイナポータルアプリなら、\n削除せずに、アップデートする。"]),
        (75, ["3つ目、利用登録の案内が出たら、\nマイナンバーカードと数字4桁の暗証番号を用意して、", "端末のロックが設定されているか\n確認する。"]),
        (76, ["慌てて消す前に、\nまず確認する。"]),
        (77, ["それが一番の近道です。"]),
        (78, ["役に立ったら、チャンネル登録して、\n次回も一緒に確認しましょう。"]),
        (79, ["概要欄に、今回確認したデジタル庁の\n公式ページを載せておきます。"]),
        (80, ["分からないことがあれば、\nコメントで教えてください。"]),
    ]
    assert len(plan) == 80
    return [{"seg": s, "cues": c} for s, c in plan]


def est_w(t: str) -> float:
    w = 0.0
    for line_t in t.split("\n"):
        w = max(w, sum(72 if ord(c) > 0x2E7F or c in "（）「」・!?―" else 36 for c in line_t))
    return w


def ts(sec: float) -> str:
    ms = int(round(sec * 100))
    return f"{ms // 360000}:{(ms % 360000) // 6000:02d}:{(ms % 6000) // 100:02d}.{ms % 100:02d}"


if __name__ == "__main__":
    raise SystemExit(main())
