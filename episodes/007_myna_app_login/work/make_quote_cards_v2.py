# -*- coding: utf-8 -*-
"""Episode 007 公式引用カード v2: 008/009=2カラム分離、012/015/018/019=semantic icon追加、004/005=視覚整理。

公式本文の文言は変更しない（抜粋・改行位置のみ）。テキストと画像の領域を構造的に分離する
（left column x<=1000 / right column x>=1060。text/asset overlap=0）。
"""
from __future__ import annotations
import pathlib
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

BASE = pathlib.Path(r"C:\Codex\260829_youtube-anshin\episodes\007_myna_app_login")
OUT = BASE / "assets" / "official"
ICONS = pathlib.Path(r"C:\Codex\260829_youtube-anshin\assets\icons\material_symbols")
W, H = 1920, 1080
INK, SOFT = "#173a68", "#587187"
LINEN = "#8a949e"

def font(size, bold=True):
    try:
        return ImageFont.truetype(r"C:\Windows\Fonts\meiryob.ttc" if bold else r"C:\Windows\Fonts\meiryo.ttc", size)
    except Exception:
        return ImageFont.load_default()

def wrap_px(draw, text, f, maxw):
    lines, cur = [], ""
    for ch in text:
        if cur and draw.textlength(cur + ch, font=f) > maxw:
            # ASCII token不可分（20:00等）
            if (ch.isascii() and cur[-1].isascii()):
                cur += ch
                continue
            lines.append(cur); cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    return lines

def paste_icon(canvas, name, tone, cx, cy, circle_d=128, icon_size=96):
    circle = {"navy": "#e9edf5", "blue": "#eaf4ff", "green": "#eaf7ee", "amber": "#fdf3e0"}
    path = ICONS / f"{name}_{tone}.png"
    if not path.exists():
        return False
    d = ImageDraw.Draw(canvas)
    d.ellipse((cx - circle_d // 2, cy - circle_d // 2, cx + circle_d // 2, cy + circle_d // 2), fill=circle.get(tone, "#eaf4ff"))
    icon = Image.open(path).convert("RGBA").resize((icon_size, icon_size), Image.Resampling.LANCZOS)
    canvas.alpha_composite(icon, (cx - icon_size // 2, cy - icon_size // 2))
    return True

def base_canvas():
    canvas = Image.new("RGBA", (W, H), "#ffffff")
    d = ImageDraw.Draw(canvas)
    d.rectangle((0, 0, W, 14), fill="#2f74bb")
    d.rectangle((0, H - 180, W, H), fill="#f7fbfe")
    return canvas

def draw_pill(d, pill, x=110, y=72):
    w = int(d.textlength(pill, font=font(30))) + 36
    d.rectangle((x, y, x + w, y + 52), fill="#eaf4ff")
    d.text((x + 18, y + 6), pill, font=font(30), fill="#2f74bb")

def draw_source(d, source_lines, x, y, maxw):
    for s in source_lines:
        f = font(28)
        lines = wrap_px(d, s, f, maxw)
        for ln in lines:
            d.text((x, y), ln, font=f, fill=SOFT)
            y += 40
        y += 4
    d.text((x, y), "確認日：2026-09-03", font=font(26), fill=SOFT)
    y += 40
    d.text((x, y), "※公式ページの案内を引用したカードです（アプリの実画面ではありません）", font=font(24), fill=LINEN)
    return y

def draw_visual_panel(canvas, img_path, label, x0=1060, y0=160, x1=1820, y1=860):
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((x0, y0, x1, y1), radius=28, fill="#f2f7fc", outline="#d9e7ef", width=2)
    img = Image.open(img_path).convert("RGB")
    img = img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS)
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=80, threshold=2))
    box_w, box_h = x1 - x0 - 60, y1 - y0 - 110
    im = ImageOps.contain(img, (box_w, box_h))
    cx = (x0 + x1 - im.width) // 2
    cy = y0 + 24
    canvas.paste(im, (cx, cy))
    d.text(((x0 + x1) // 2, y1 - 56), label, font=font(24), fill=LINEN, anchor="mm")

def card_two_col(name, pill, quote_lines, source_lines, img_path, img_label):
    canvas = base_canvas()
    d = ImageDraw.Draw(canvas)
    draw_pill(d, pill)
    # 左カラム（テキスト）: x 110..1010・54px・maxw 930・文節単位の手分割（右カラムとの重なりゼロ）
    y = 170
    for line in quote_lines:
        for ln in wrap_px(d, line, font(54), 930):
            d.text((110, y), ln, font=font(54), fill=INK)
            y += 88
    y += 10
    draw_source(d, source_lines, 110, y, 860)
    d.text((110, H - 210), "大人のデジタル安心室", font=font(24), fill=SOFT)
    draw_visual_panel(canvas, img_path, img_label)
    out = OUT / f"quote_{name}.png"
    canvas.convert("RGB").save(out, "PNG")
    print("saved", out.name)

def card_icon(name, pill, quote_lines, source_lines, icon_name, icon_tone):
    canvas = base_canvas()
    d = ImageDraw.Draw(canvas)
    draw_pill(d, pill)
    paste_icon(canvas, icon_name, icon_tone, 170, 205, circle_d=128, icon_size=96)
    y = 180
    for line in quote_lines:
        d.text((266, y), line, font=font(60), fill=INK)
        y += 90
    y += 8
    draw_source(d, source_lines, 266, y, 1450)
    d.text((110, H - 210), "大人のデジタル安心室", font=font(24), fill=SOFT)
    out = OUT / f"quote_{name}.png"
    canvas.save(out, "PNG")
    print("saved", out.name)

def card_text(name, pill, quote_lines, source_lines):
    canvas = base_canvas()
    d = ImageDraw.Draw(canvas)
    draw_pill(d, pill)
    y = 180
    for line in quote_lines:
        d.text((110, y), line, font=font(60), fill=INK)
        y += 90
    y += 8
    draw_source(d, source_lines, 110, y, 1560)
    d.text((110, H - 210), "大人のデジタル安心室", font=font(24), fill=SOFT)
    out = OUT / f"quote_{name}.png"
    canvas.save(out, "PNG")
    print("saved", out.name)

# 008 / 009: 2カラム（左テキスト・右公式イラスト・完全分離）
card_two_col("008_scan_iphone", "2 / 5 カードを読み取れない場合",
             ["カードの上に、iPhoneの背面上部を", "ぴったり合わせて、「読み取り開始」", "動かさずに、しばらく待ちます。"],
             ["出典：デジタル庁「マイナンバーカードの読み取りかた」",
              "https://services.digital.go.jp/mynaapp/scan-mynumbercard/"],
             OUT / "mynaapp_scan_iphone.png", "公式の読み取りイメージ（デジタル庁）")
card_two_col("009_scan_android", "2 / 5 カードを読み取れない場合",
             ["Androidは、本体の背面の読み取り位置", "カードに合わせます。機種によって、", "場所は少し違います。"],
             ["出典：デジタル庁「マイナンバーカードの読み取りかた」",
              "https://services.digital.go.jp/mynaapp/scan-mynumbercard/"],
             OUT / "mynaapp_scan_android.png", "公式の読み取りイメージ（デジタル庁）")
# 012 / 015 / 018 / 019: semantic icon 補助
card_icon("012_register", "3 / 5 暗証番号で止まる場合",
          ["利用者証明用暗証番号（数字4桁）を入力する",
           "カードの上に背面上部をぴったり合わせて「読み取り開始」",
           "スマホにカードを追加すると、顔や指紋でも登録できます"],
          ["出典：デジタル庁「マイナアプリの利用登録の方法」",
           "https://services.digital.go.jp/mynaapp/register/"],
          "dialpad", "blue")
card_icon("015_expiration", "4 / 5 カードや電子証明書の期限",
          ["カード発行時に18歳以上：発行から10回目の誕生日まで",
           "更新手続は、有効期限の3か月前から市区町村窓口でできます"],
          ["出典：デジタル庁「マイナンバーカードおよび電子証明書の有効期限・更新」",
           "https://www.digital.go.jp/policies/mynumber/expiration-date/"],
          "badge", "blue")
card_icon("018_maintenance", "5 / 5 それでもダメなら",
          ["マイナポータルの現在の障害情報と、",
           "メンテナンス中の情報や今後の予定を確認できます。"],
          ["出典：マイナポータル「障害・メンテナンス」",
           "https://myna.go.jp/html/info/index.html"],
          "construction", "blue")
card_icon("019_reset", "5 / 5 それでもダメなら",
          ["キオスク端末等でパスワードを初期化・再設定する際は、",
           "本人確認のため、パスワードの入力が必要です。"],
          ["出典：公的個人認証サービス（JPKI）「コンビニで初期化・再設定」",
           "https://www.jpki.go.jp/jpkiidreset/howto/kiosk.html"],
          "lock_reset", "blue")
# 004 / 005: 視覚整理（source wrap・見切れ防止。文言は公式のまま）
card_text("004_system_requirements", "1 / 5 スマホが対応しているか",
          ["対応OS：iOS 16.4以上／Android 11以降＋NFC",
           "端末のロック設定（PIN・顔認証・指紋認証など）が必須"],
          ["出典：デジタル庁「マイナアプリの動作環境」",
           "https://services.digital.go.jp/mynaapp/system-requirements/"])
card_text("005_faq_login", "1 / 5 スマホが対応しているか",
          ["通常モードに切り替えてから、再度ログインをお試しください。",
           "（シークレットモードでは、アプリストア転送を繰り返すことがあります）"],
          ["出典：デジタル庁「マイナアプリ よくある質問」ログインできない記事",
           "https://support.mynaapp.digital.go.jp/hc/ja"])
