# -*- coding: utf-8 -*-
"""Episode 007 公式引用カード v4: 「読めない情報は、ないのと同じ」基準。

- 画面下部の小文字（URL全文・確認日・※注記・細かいsource）を全削除。
  provenance は sources.md / media_manifest.csv / publish description / local/web_check に保持。
- 出典は短形「出典：○○公式」のみ44px以上で表示。
- 文字サイズ基準: L1 66〜96px / L2 52px以上 / pill 44px / source 44px。
- 文節改行（wrap_jp）・overflow機械検査・2カラム分離（008/009）は v3 継承。
"""
from __future__ import annotations
import pathlib, sys
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = pathlib.Path(r"C:\Codex\260829_youtube-anshin\episodes\007_myna_app_login")
OUT = BASE / "assets" / "official"
ICONS = pathlib.Path(r"C:\Codex\260829_youtube-anshin\assets\icons\material_symbols")
W, H = 1920, 1080
INK, SOFT = "#173a68", "#587187"
CIRCLE = {"navy": "#e9edf5", "blue": "#eaf4ff", "green": "#eaf7ee", "amber": "#fdf3e0"}
PROTECTED = ["マイナアプリ", "マイナポータル", "マイナンバーカード", "利用者証明用電子証明書",
             "電子証明書", "スマートフォン", "iPhone", "Android", "0120-95-0178", "iOS", "NFC"]

def font(size, bold=True):
    try:
        return ImageFont.truetype(r"C:\Windows\Fonts\meiryob.ttc" if bold else r"C:\Windows\Fonts\meiryo.ttc", size)
    except Exception:
        return ImageFont.load_default()

def split_chunks(text):
    tokens = []
    buf = ""
    i = 0
    while i < len(text):
        matched = None
        for term in PROTECTED:
            if text.startswith(term, i):
                matched = term
                break
        if matched:
            buf += matched
            i += len(matched)
            continue
        ch = text[i]
        buf += ch
        if ch in "、。」？！ " or ch in "　":
            tokens.append(buf)
            buf = ""
        i += 1
    if buf:
        tokens.append(buf)
    return tokens

def wrap_jp(draw, text, f, maxw):
    chunks = split_chunks(text)
    lines: list[str] = []
    cur = ""
    for chk in chunks:
        if not chk:
            continue
        if cur and draw.textlength(cur + chk, font=f) > maxw:
            lines.append(cur)
            cur = chk
        elif not cur and draw.textlength(chk, font=f) > maxw:
            sub = ""
            for c in chk:
                if sub and draw.textlength(sub + c, font=f) > maxw and not (c.isascii() and sub[-1].isascii()):
                    lines.append(sub)
                    sub = c
                else:
                    sub += c
            if sub:
                cur = sub
        else:
            cur += chk
    if cur:
        lines.append(cur)
    return lines

def base_canvas():
    canvas = Image.new("RGBA", (W, H), "#ffffff")
    d = ImageDraw.Draw(canvas)
    d.rectangle((0, 0, W, 14), fill="#2f74bb")
    d.rectangle((0, H - 180, W, H), fill="#f7fbfe")
    return canvas

def draw_pill(d, pill, x=110, y=60):
    f = font(44)
    w = int(d.textlength(pill, font=f)) + 40
    d.rectangle((x, y, x + w, y + 74), fill="#eaf4ff")
    d.text((x + 20, y + 8), pill, font=f, fill="#2f74bb")

def paste_icon(canvas, name, tone, cx, cy, circle_d=128, icon_size=94):
    path = ICONS / f"{name}_{tone}.png"
    if not path.exists():
        return
    d = ImageDraw.Draw(canvas)
    d.ellipse((cx - circle_d // 2, cy - circle_d // 2, cx + circle_d // 2, cy + circle_d // 2), fill=CIRCLE.get(tone, "#eaf4ff"))
    icon = Image.open(path).convert("RGBA").resize((icon_size, icon_size), Image.Resampling.LANCZOS)
    canvas.alpha_composite(icon, (cx - icon_size // 2, cy - icon_size // 2))

def draw_l1(d, l1, size, maxw, y, align="center", gap=100):
    y0 = y
    for ln in wrap_jp(d, l1, font(size), maxw):
        if align == "left":
            d.text((110, y0), ln, font=font(size), fill=INK)
        else:
            wl = d.textlength(ln, font=font(size))
            d.text(((W - wl) // 2, y0), ln, font=font(size), fill=INK)
        y0 += gap
    return y0 + 14

def draw_l2(d, l2_lines, size, maxw, y, align="center", gap=70):
    for line in l2_lines:
        for ln in wrap_jp(d, line, font(size), maxw):
            if align == "left":
                d.text((110, y), ln, font=font(size), fill=SOFT)
            else:
                wl = d.textlength(ln, font=font(size))
                d.text(((W - wl) // 2, y), ln, font=font(size), fill=SOFT)
            y += gap
    return y

def draw_source_short(d, source, y, align="center", size=44):
    f = font(size)
    if align == "left":
        d.text((110, y), source, font=f, fill=SOFT)
    else:
        wl = d.textlength(source, font=f)
        d.text(((W - wl) // 2, y), source, font=f, fill=SOFT)
    return y

def verify_no_overflow(canvas, name):
    rgb = canvas.convert("RGB")
    strip_r = rgb.crop((W - 14, 24, W, H - 180))
    data = list(strip_r.get_flattened_data()) if hasattr(strip_r, "get_flattened_data") else list(strip_r.getdata())
    ink_r = sum(1 for c in data if min(c) < 150)
    strip_b = rgb.crop((0, H - 180, W, H))
    data_b = list(strip_b.get_flattened_data()) if hasattr(strip_b, "get_flattened_data") else list(strip_b.getdata())
    ink_b = sum(1 for c in data_b if min(c) < 150)
    if ink_r > 0 or ink_b > 0:
        raise RuntimeError(f"OVERFLOW in {name}: right={ink_r} bottom={ink_b}")
    print(f"overflow check {name}: PASS")

def make_card(name, pill, l1, l1_size, l2_lines, l2_size, source, icon=None, icon_tone="blue",
              two_col=False, img_path=None, align="left"):
    canvas = base_canvas()
    d = ImageDraw.Draw(canvas)
    draw_pill(d, pill)
    if icon:
        paste_icon(canvas, icon, icon_tone, 168, 218)
    maxw = 1680 if not two_col else 990
    if two_col:
        y = draw_l1(d, l1, l1_size, maxw, 250, align="left")
        y = draw_l2(d, l2_lines, l2_size, maxw, y, align="left")
        draw_source_short(d, source, 800, align="left")
        d.text((110, H - 230), "大人のデジタル安心室", font=font(30), fill=SOFT)
        # 右パネル（公式イラスト・完全分離 x>=1160）
        d2 = ImageDraw.Draw(canvas)
        d2.rounded_rectangle((1160, 180, 1790, 860), radius=28, fill="#f2f7fc", outline="#d9e7ef", width=2)
        img = Image.open(img_path).convert("RGB")
        img = img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS)
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=80, threshold=2))
        im = ImageOps.contain(img, (540, 540))
        canvas.paste(im, ((1160 + 1790 - im.width) // 2, 240))
        wl = d2.textlength(source, font=font(44))
        d2.text(((1160 + 1790 - wl) // 2, 806), source, font=font(44), fill=SOFT)
    else:
        y = draw_l1(d, l1, l1_size, maxw, 320, align="center")
        draw_l2(d, l2_lines, l2_size, maxw, y, align="center")
        draw_source_short(d, source, 800, align="center")
        d.text((110, H - 230), "大人のデジタル安心室", font=font(30), fill=SOFT)
    verify_no_overflow(canvas, name)
    out = OUT / f"quote_{name}.png"
    canvas.convert("RGB").save(out, "PNG")
    print("saved", out.name)

SRC_MYNA = "出典：マイナアプリ公式"
SRC_DGT = "出典：デジタル庁"
SRC_MYP = "出典：マイナポータル公式"
SRC_JPKI = "出典：公的個人認証サービス"

make_card("004_system_requirements", "1/5 スマホが対応しているか",
          "対応OS：iOS 16.4以上／Android 11以降＋NFC", 68,
          ["端末のロック設定（PIN・顔認証・指紋認証など）が必須です。"], 52,
          SRC_MYNA)
make_card("005_faq_login", "1/5 スマホが対応しているか",
          "通常モードで、開き直しましょう", 76,
          ["プライベートブラウズやシークレットモードでは、アプリストアへの転送を繰り返すことがあるため、",
           "通常モードに切り替えてから、再度ログインをお試しください。"], 52,
          SRC_MYNA)
make_card("008_scan_iphone", "2/5 カードを読み取れない場合",
          "iPhoneは、本体の上部", 76,
          ["カードの上にぴったり合わせて「読み取り開始」をタップ。", "動かさずに、しばらく待ちます。"], 52,
          SRC_MYNA, two_col=True, img_path=OUT / "mynaapp_scan_iphone.png")
make_card("009_scan_android", "2/5 カードを読み取れない場合",
          "Androidは、本体の背面の読み取り位置", 66,
          ["カードに合わせます。機種によって、場所は少し違います。"], 52,
          SRC_MYNA, two_col=True, img_path=OUT / "mynaapp_scan_android.png")
make_card("012_register", "3/5 暗証番号で止まる場合",
          "数字4桁", 96,
          ["利用者証明用暗証番号を入力します。", "スマホにカードを追加すると、顔や指紋でも登録できます。"], 52,
          SRC_MYNA, icon="dialpad", icon_tone="blue")
make_card("015_expiration", "4/5 カードや電子証明書の期限",
          "発行から10回目の誕生日まで", 76,
          ["18歳以上の方のカード自体の期限です。", "更新手続は、有効期限の3か月前から市区町村窓口でできます。"], 52,
          SRC_DGT, icon="badge", icon_tone="blue")
make_card("018_maintenance", "5/5 それでもダメなら",
          "障害・メンテナンス情報を確認", 72,
          ["マイナポータルの現在の障害情報と、メンテナンス中の情報や今後の予定を確認できます。"], 52,
          SRC_MYP, icon="construction", icon_tone="blue")
make_card("019_reset", "5/5 それでもダメなら",
          "暗証番号を忘れたら、再設定", 72,
          ["コンビニの端末で再設定できます。", "（本人確認のため、パスワードの入力が必要）", "分からない場合は、市区町村の窓口で再設定できます。"], 52,
          SRC_JPKI, icon="lock_reset", icon_tone="blue")
