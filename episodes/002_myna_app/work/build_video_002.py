# -*- coding: utf-8 -*-
"""Episode 002 draft_v1 video builder.

1. Render one 1920x1080 panel per narration unit (PIL)
2. Encode each panel as a silent H.264 segment (duration = unit + pad)
3. Concat segments (stream copy)
4. Final mux: concat video + narration (loudnorm) + burned ASS captions

Templates: icon / full / crop / two / card / listcard / header / endcard.
Subtitle band (navy, y885..1080) is drawn into every panel; ASS text sits
inside the band at pos(960,980).
"""
from __future__ import annotations

import csv
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[3]
EP = ROOT / "episodes" / "002_myna_app"
ASSETS = EP / "assets" / "official"
WORK = EP / "work"
PANELS = WORK / "panels_v1"
SEGS = WORK / "segs_v1"
OUT = EP / "output"
MANIFEST = EP / "audio" / "voicevox_kenzaki" / "segments_manifest.csv"
NARRATION = EP / "audio" / "voicevox_kenzaki" / "narration_kenzaki.wav"
ASS_FILE = EP / "captions_v1.ass"

W, H = 1920, 1080
CONTENT = (60, 40, 1860, 860)          # x0,y0,x1,y1 (band starts y=885)
BAND_Y = 885
NAVY = (26, 42, 74)
PINK = (224, 90, 115)
GRAY = (96, 112, 136)
BG = (255, 251, 248)
BAND = (22, 38, 63)
BAND_EDGE = (60, 86, 128)
WHITE = (255, 255, 255)

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\yugothb.ttc",
    str(ROOT / "episodes" / "001_google_security" / "work" / "font.ttc"),
]


def font(size: int) -> ImageFont.FreeTypeFont:
    for p in FONT_CANDIDATES:
        if Path(p).exists():
            return ImageFont.truetype(p, size, index=0)
    raise SystemExit("no font found")


def draw_band(d: ImageDraw.ImageDraw) -> None:
    d.rectangle((0, BAND_Y, W, H), fill=BAND)
    d.line((0, BAND_Y, W, BAND_Y), fill=BAND_EDGE, width=3)


def fit_box(src_w: int, src_h: int, box) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    scale = min(bw / src_w, bh / src_h)
    dw, dh = int(src_w * scale), int(src_h * scale)
    x = x0 + (bw - dw) // 2
    y = y0 + (bh - dh) // 2
    return x, y, x + dw, y + dh


def paste_rounded(canvas: Image.Image, img: Image.Image, box, radius: int = 24, border: tuple = (222, 226, 234)):
    x0, y0, x1, y1 = fit_box(*img.size, box)
    img = img.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    if img.mode == "RGBA":
        alpha = img.getchannel("A")
        img = img.convert("RGB")
    else:
        alpha = Image.new("L", img.size, 255)
    rounded = Image.new("L", img.size, 0)
    ImageDraw.Draw(rounded).rounded_rectangle((0, 0, img.size[0], img.size[1]), radius=radius, fill=255)
    mask = ImageChops.multiply(alpha, rounded)
    canvas.paste(img, (x0, y0), mask)
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((x0, y0, x1 - 1, y1 - 1), radius=radius, outline=border, width=3)


def open_img(path: Path | str) -> Image.Image:
    img = Image.open(str(path)).convert("RGB")
    return img


def text_center(d: ImageDraw.ImageDraw, cx: int, y: int, text: str, fnt, fill, spacing: int = 8):
    d.text((cx, y), text, font=fnt, fill=fill, anchor="ma")


# ---------- templates ----------

def tpl_icon(canvas, p: dict):
    img = open_img(ASSETS / p["img"])
    box = (760, 150, 1160, 550)
    paste_rounded(canvas, img, box, radius=56)
    d = ImageDraw.Draw(canvas)
    label = p.get("label") or []
    y = 640
    for ln in label:
        text_center(d, 960, y, ln, font(54), NAVY)
        y += 78
    if p.get("sub"):
        text_center(d, 960, y + 6, p["sub"], font(40), GRAY)


def tpl_full(canvas, p: dict):
    img = open_img(ASSETS / p["img"])
    paste_rounded(canvas, img, CONTENT)


def tpl_phone(canvas, p: dict):
    """Small phone screenshots: max 2.6x upscale, centered, with a label."""
    img = open_img(ASSETS / p["img"])
    x0, y0, x1, y1 = 140, 50, 1780, 830
    bw, bh = x1 - x0, y1 - y0
    scale = min(bw / img.size[0], bh / img.size[1], 2.6)
    dw, dh = int(img.size[0] * scale), int(img.size[1] * scale)
    x = x0 + (bw - dw) // 2
    y = y0 + (bh - dh) // 2
    paste_rounded(canvas, img, (x, y, x + dw, y + dh), radius=28)
    d = ImageDraw.Draw(canvas)
    if p.get("label"):
        text_center(d, 960, 855, p["label"], font(42), GRAY)


def tpl_crop(canvas, p: dict):
    img = open_img(ASSETS / p["img"])
    box = p["crop"]
    img = img.crop(box)
    paste_rounded(canvas, img, CONTENT)


def tpl_two(canvas, p: dict):
    left = open_img(ASSETS / p["img1"])
    right = open_img(ASSETS / p["img2"])
    if p.get("crop1"):
        left = left.crop(p["crop1"])
    if p.get("crop2"):
        right = right.crop(p["crop2"])
    lbox = (60, 90, 930, 790)
    rbox = (990, 90, 1860, 790)
    paste_rounded(canvas, left, lbox)
    paste_rounded(canvas, right, rbox)
    d = ImageDraw.Draw(canvas)
    text_center(d, 495, 830, p.get("label1", "App Store"), font(42), NAVY)
    text_center(d, 1425, 830, p.get("label2", "Google Play"), font(42), NAVY)


def tpl_card(canvas, p: dict):
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((180, 220, 1740, 760), radius=40, fill=(255, 255, 255),
                        outline=(235, 226, 220), width=3)
    lines = p["lines"]
    n = len(lines)
    total_h = n * 104 + (n - 1) * 12
    y = (720 + 220 - total_h) // 2
    for ln in lines:
        text_center(d, 960, y, ln, font(72 if n <= 2 else 64), NAVY)
        y += 104
    if p.get("sub"):
        text_center(d, 960, y + 34, p["sub"], font(42), GRAY)
    d.rounded_rectangle((860, 200, 1060, 212), radius=6, fill=PINK)


def tpl_listcard(canvas, p: dict):
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((120, 90, 1800, 820), radius=40, fill=(255, 255, 255),
                        outline=(235, 226, 220), width=3)
    text_center(d, 960, 150, p["title"], font(64), NAVY)
    y = 250
    hl = p.get("hl", 0)
    for i, item in enumerate(p["items"], 1):
        col = PINK if i == hl else GRAY
        d.ellipse((260, y, 360, y + 100), fill=(255, 240, 244) if i == hl else (247, 249, 252))
        text_center(d, 310, y + 50, str(i), font(66), col)
        text_center(d, 970, y + 54, item, font(58), NAVY if i == hl else (64, 80, 108))
        if i < len(p["items"]):
            d.line((260, y + 128, 1660, y + 128), fill=(238, 240, 246), width=3)
        y += 168


def tpl_header(canvas, p: dict):
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((140, 180, 1780, 780), radius=40, fill=(255, 255, 255),
                        outline=(235, 226, 220), width=3)
    num = p["num"]
    text_center(d, 960, 330, num, font(120), PINK)
    text_center(d, 960, 500, p["title"], font(86), NAVY)
    if p.get("sub"):
        text_center(d, 960, 630, p["sub"], font(44), GRAY)


def tpl_endcard(canvas, p: dict):
    img = open_img(ASSETS / "presskit_keyvisual_01.png")
    paste_rounded(canvas, img, (0, 0, 1920, 880), radius=0)
    ov = Image.new("RGBA", (W, 880), (18, 30, 52, 120))
    canvas.paste(Image.new("RGB", (W, 880), (20, 32, 56)), (0, 0))
    d = ImageDraw.Draw(canvas)
    text_center(d, 960, 300, p.get("channel", "大人のデジタル安心室"), font(76), WHITE)
    y = 430
    for ln in p["lines"]:
        text_center(d, 960, y, ln, font(52), (240, 244, 252))
        y += 84
    if p.get("sub"):
        text_center(d, 960, y + 20, p["sub"], font(40), (200, 210, 228))


def tpl_quotecard(canvas, p: dict):
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((180, 130, 1740, 830), radius=40, fill=(255, 255, 255),
                        outline=(235, 226, 220), width=3)
    d.rounded_rectangle((180, 130, 196, 830), radius=12, fill=PINK)
    text_center(d, 960, 180, p.get("src", "マイナアプリ よくある質問｜デジタル庁"), font(36), GRAY)
    if p.get("q"):
        text_center(d, 960, 240, p["q"], font(44), (60, 76, 106))
    y = 330
    for ln in p["lines"]:
        text_center(d, 960, y, ln, font(58), NAVY)
        y += 92


TEMPLATES = {
    "icon": tpl_icon,
    "full": tpl_full,
    "phone": tpl_phone,
    "crop": tpl_crop,
    "two": tpl_two,
    "card": tpl_card,
    "listcard": tpl_listcard,
    "header": tpl_header,
    "endcard": tpl_endcard,
    "quotecard": tpl_quotecard,
}


# ---------- unit -> visual mapping ----------

V = {}

def _v(uid, tpl, **kw):
    V[uid] = {"tpl": tpl, **kw}

# intro
_v(1, "icon", img="official_icon_rounded_3x.png", label=["新しい マイナアプリ"])
_v(2, "card", lines=["マイナポータルアプリ  →  マイナアプリ", "8月25日から名前が変わりました"])
_v(3, "card", lines=["マイナポータルというサービスは、", "なくなりません。"])
_v(4, "card", lines=["アプリを消して、入れ直す", "必要はありません。"])
_v(5, "listcard", title="今日確認すること", items=["マイナアプリとは何か", "何が変わったのか", "すでに使っていた人は？", "新しく使う人・開けない人", "本物の確認ポイント"])
# 1/5
_v(6, "header", num="1 / 5", title="マイナアプリとは何か", sub="そもそも、何をするアプリ？")
_v(7, "crop", img="browser/br_02_svc_top_faq.png", crop=(0, 950, 1440, 2100))
_v(8, "crop", img="browser/br_03_news_20260825.png", crop=(0, 260, 1440, 820))
_v(9, "phone", img="official_screen_card.png", label="マイナンバーカードの機能（公式画面）")
_v(10, "card", lines=["「認証」は「本人確認」", "という意味です。"])
_v(11, "full", img="official_services_grid.png")
_v(12, "phone", img="official_screen_home.png", label="マイナアプリのホーム画面（公式画面）")
_v(13, "card", lines=["ひとつのアプリにまとめたのが、", "今回の変更の中心です。"])
# 2/5
_v(14, "header", num="2 / 5", title="何が変わったのか", sub="主に3つ")
_v(15, "card", lines=["1つ目は、スマホアプリの名前。"])
_v(16, "card", lines=["「マイナポータルアプリ」", "→「マイナアプリ」"])
_v(17, "card", lines=["2つ目は、アプリアイコン。"])
_v(18, "icon", img="official_icon_rounded_3x.png", label=["新アイコン"])
_v(19, "icon", img="official_icon_limited_3x.png", label=["期間限定アイコン", "（しばらくの間）"])
_v(20, "card", lines=["デジタル庁は、年内をめどに", "最終的なデザインに統一すると案内"])
_v(21, "card", lines=["3つ目は、ログイン・認証に", "使うアプリが統合されたこと。"])
_v(22, "crop", img="browser/br_03_news_20260825.png", crop=(0, 300, 1440, 900))
_v(23, "card", lines=["開くと、マイナアプリの利用を", "案内する画面が表示されます"])
_v(24, "card", lines=["使っていた人も、同じ機能を", "マイナアプリで引き続き使えます"])
_v(25, "card", lines=["ここからが、いちばん大事なことです。"])
_v(26, "crop", img="browser/br_02_svc_top_faq.png", crop=(0, 5300, 1440, 6050))
_v(27, "crop", img="browser/br_02_svc_top_faq.png", crop=(0, 5680, 1440, 6550))
_v(28, "card", lines=["ウェブサイトは、引き続き使えます。"])
_v(29, "card", lines=["医療費などの自己情報の確認も、", "引越し・パスポートの申請も、今までどおり"])
_v(30, "card", lines=["変わるのは、ログインの方法だけ。"])
_v(31, "card", lines=["本人確認の役割が、", "マイナアプリにバトンタッチ"])
# 3/5
_v(32, "header", num="3 / 5", title="すでに使っていた人は？", sub="まず確認、次に更新")
_v(33, "card", lines=["まず、今お使いのアプリの", "名前とアイコンを確認"])
_v(34, "card", lines=["マイナポータルアプリなら、", "アップデートするだけでOK"])
_v(35, "card", lines=["削除して、入れ直す", "必要はありません。"])
_v(36, "quotecard",
   q="Q. マイナポータルアプリは自動的にアップデートされますか？",
   lines=["A. App StoreやGoogle Playの自動更新設定を", "ご利用の場合は、自動的に更新される", "場合があります。"],
   src="マイナアプリ よくある質問｜デジタル庁")
_v(37, "crop", img="browser/br_09_gplay.png", crop=(120, 340, 1150, 740))
_v(38, "card", lines=["スマホの中のカード設定や", "機能・データは引き継がれます"])
_v(39, "card", lines=["再登録は不要です。"])
_v(40, "card", lines=["アップデートしなくても、", "当面は使えます"])
_v(41, "card", lines=["ただ、一部の手続きでは", "マイナアプリが必要になります"])
_v(42, "card", lines=["ここで注意です。"])
_v(43, "card", lines=["分からないからといって、", "削除して入れ直すのは、まず待って"])
_v(44, "quotecard",
   q="Q. アプリを入れ直したら、マイナアプリが開かなくなりました。",
   lines=["A. 後からインストールしたアプリが", "優先して開く仕組みになっています。"],
   src="マイナアプリ よくある質問｜デジタル庁")
_v(45, "quotecard",
   q="Q. マイナアプリを優先したい場合は？",
   lines=["・マイナアプリを、デジタル認証アプリより", "　後にインストールし直す", "・デジタル認証アプリをアンインストールする"],
   src="マイナアプリ よくある質問｜デジタル庁")
_v(46, "card", lines=["まずは、公式のよくある質問や", "概要欄の公式ページを確認しましょう"])
# 4/5
_v(47, "header", num="4 / 5", title="新しく使う人・開けない人", sub="動作環境と初回登録")
_v(48, "card", lines=["まず、動作環境です。"])
_v(49, "crop", img="browser/br_06_sysreq.png", crop=(0, 300, 1440, 1150))
_v(50, "card", lines=["NFCは、カードをかざして", "読み取るための機能です。"])
_v(51, "phone", img="official_screen_register_start.png", label="利用登録をはじめる（公式画面）")
_v(52, "phone", img="official_screen_register_card_auth.png", label="実物カードで認証（公式画面）")
_v(53, "phone", img="official_screen_register_biometric.png", label="顔・指紋で認証（公式画面）")
_v(54, "crop", img="browser/br_06_sysreq.png", crop=(0, 1500, 1440, 2350))
_v(55, "phone", img="official_screen_register_device_lock.png", label="端末ロックの利用許可（公式画面）")
_v(56, "card", lines=["ログインできない場合は、", "よくある原因があります。"])
_v(57, "card", lines=["「プライベートブラウズ」や", "「シークレットモード」を使うと、"])
_v(58, "card", lines=["通常モードに戻して、", "スマホを再起動してから、もう一度"])
_v(59, "card", lines=["この動画では、カードの読み取りや", "暗証番号の入力は実演しません。"])
_v(60, "card", lines=["個人情報にかかわる手続きは、", "ご自身のスマホで進めてください。"])
# 5/5
_v(61, "header", num="5 / 5", title="本物の確認ポイント", sub="だまされないために")
_v(62, "card", lines=["公式のマイナアプリは、", "App StoreとGoogle Playの", "2つの場所からだけ入手できます。"])
_v(63, "two", img1="browser/br_08_appstore.png", crop1=(250, 60, 1440, 620),
      img2="browser/br_09_gplay.png", crop2=(120, 340, 1150, 740),
      label1="App Store", label2="Google Play")
_v(64, "crop", img="browser/br_09_gplay.png", crop=(260, 380, 1080, 660))
_v(65, "icon", img="official_icon_rounded_3x.png", label=["ピンクのグラデーション・「マイナ」・桜"])
_v(66, "crop", img="browser/br_10_notice_fakeapp.png", crop=(0, 380, 1440, 1000))
_v(67, "card", lines=["メールや電話で、ダウンロードや", "暗証番号入力を求められたら、疑って"])
_v(68, "crop", img="browser/br_11_notice_phishing.png", crop=(0, 400, 1440, 1150))
_v(69, "crop", img="browser/br_10_notice_fakeapp.png", crop=(0, 1000, 1440, 1600))
_v(70, "card", lines=["一人で判断せず、確認するのも", "ひとつの方法です。"])
# まとめ
_v(71, "header", num="まとめ", title="今やること3つ", sub="今日のおさらい")
_v(72, "card", lines=["今やっていただきたいことは、", "3つです。"])
_v(73, "listcard", title="今やること", items=["アプリ名とアイコンを確認", "必要ならストアで更新", "提供元がデジタル庁か確認"], hl=1)
_v(74, "listcard", title="今やること", items=["アプリ名とアイコンを確認", "必要ならストアで更新", "提供元がデジタル庁か確認"], hl=2)
_v(75, "listcard", title="今やること", items=["アプリ名とアイコンを確認", "必要ならストアで更新", "提供元がデジタル庁か確認"], hl=3)
_v(76, "card", lines=["慌てて消す前に、", "まず確認する。"])
_v(77, "card", lines=["それが一番の近道です。"])
_v(78, "endcard", lines=["役に立ったら、チャンネル登録して、", "次回も一緒に確認しましょう。"], sub="大人のデジタル安心室")
_v(79, "card", lines=["概要欄に、確認したデジタル庁の", "公式ページを載せておきます。"])
_v(80, "endcard", lines=["分からないことがあれば、", "コメントで教えてください。"], sub="大人のデジタル安心室")


# ---------- run ----------

def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--panels-only", action="store_true", help="render panels and stop")
    args = ap.parse_args()

    PANELS.mkdir(parents=True, exist_ok=True)
    SEGS.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg not found")

    with MANIFEST.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 80, f"expected 80 units, got {len(rows)}"

    # render panels + measure durations
    durations: list[float] = []
    for r in rows:
        uid = int(r["segment_id"])
        dur = float(r["duration_sec"]) + float(r["pad_after_sec"] or 0)
        durations.append(dur)
        canvas = Image.new("RGB", (W, H), BG)
        tpl = V[uid]["tpl"]
        TEMPLATES[tpl](canvas, V[uid])
        draw_band(ImageDraw.Draw(canvas))
        panel = PANELS / f"panel_{uid:03d}.png"
        canvas.save(panel)
        print(f"{uid:03d} {tpl:8s} {dur:6.2f}s -> {panel.name}", flush=True)

    concat = SEGS / "concat.txt"
    with concat.open("w", encoding="utf-8") as f:
        for uid in range(1, 81):
            f.write(f"file 'seg_{uid:03d}.mp4'\n")

    for uid, dur in enumerate(durations, 1):
        if args.panels_only:
            break
        seg = SEGS / f"seg_{uid:03d}.mp4"
        if seg.exists():
            continue
        panel = PANELS / f"panel_{uid:03d}.png"
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", "30",
             "-i", str(panel), "-t", f"{dur:.3f}",
             "-c:v", "libx264", "-preset", "ultrafast", "-crf", "20",
             "-pix_fmt", "yuv420p", "-r", "30", str(seg)],
            check=True,
        )
        print(f"seg {uid:03d} done", flush=True)

    video_concat = WORK / "video_concat_v1.mp4"
    if args.panels_only:
        print("panels-only: stopped before encoding")
        return 0
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
         "-i", str(concat), "-c", "copy", str(video_concat)],
        check=True,
    )
    draft = OUT / "draft_v1.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error",
         "-i", str(video_concat), "-i", str(NARRATION),
         "-vf", f"ass={ASS_FILE.relative_to(ROOT).as_posix()}",
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
         "-shortest", str(draft)],
        check=True,
    )
    print(f"draft_v1: {draft} ({draft.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
