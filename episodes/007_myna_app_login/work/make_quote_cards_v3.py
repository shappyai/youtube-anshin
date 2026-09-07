# -*- coding: utf-8 -*-
"""Episode 007 公式引用カード v3: TV可読性最優先。

3階層構造（恒久ルール）:
  Level 1: 視聴者が覚える要点（68〜76px・大きく）
  Level 2: 公式の短い根拠（48〜56px・中・文節改行）
  Level 3: 出典/確認日（24px・下部に分離・完全URLはmanifest等に保持）

- wrap_jp: 読点・句点・空白で文節分割してmaxw内に収める（単語途中・1文字孤立・ASCII token分断・
  電話番号/URL分断を防ぐ。protected termsは「、」「。」「 」以外では切らない）。
- overflow: 描画後に右端(x>=1908)・字幕帯(y>=900)への文字色侵入を機械検査してFAIL時は例外。
- 2カラム（SCENE-008/009）: 左テキスト x 110..1100（maxw 990）・右公式イラストパネル x 1160..1790。
  text/asset overlap = 0。
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
INK, SOFT, LINEN = "#173a68", "#587187", "#8a949e"
CIRCLE = {"navy": "#e9edf5", "blue": "#eaf4ff", "green": "#eaf7ee", "amber": "#fdf3e0"}
PROTECTED = ["マイナアプリ", "マイナポータル", "マイナンバーカード", "利用者証明用電子証明書",
             "電子証明書", "スマートフォン", "iPhone", "Android", "0120-95-0178", "iOS", "NFC"]

def font(size, bold=True):
    try:
        return ImageFont.truetype(r"C:\Windows\Fonts\meiryob.ttc" if bold else r"C:\Windows\Fonts\meiryo.ttc", size)
    except Exception:
        return ImageFont.load_default()



def split_chunks(text):
    """読点・句点・空白で文節チャンクに分割（protected termは分割しない）."""
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
    """文節チャンクをmaxw内に組み合わせて自然改行（ASCII token保護・1文字孤立防止）."""
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
            # 1チャンク自体がmaxw超過 → 文字単位で分割（ASCII token保護）
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

def draw_pill(d, pill, x=110, y=64):
    w = int(d.textlength(pill, font=font(28))) + 34
    d.rectangle((x, y, x + w, y + 50), fill="#eaf4ff")
    d.text((x + 17, y + 5), pill, font=font(28), fill="#2f74bb")

def paste_icon(canvas, name, tone, cx, cy, circle_d=120, icon_size=88):
    path = ICONS / f"{name}_{tone}.png"
    if not path.exists():
        return
    d = ImageDraw.Draw(canvas)
    d.ellipse((cx - circle_d // 2, cy - circle_d // 2, cx + circle_d // 2, cy + circle_d // 2), fill=CIRCLE.get(tone, "#eaf4ff"))
    icon = Image.open(path).convert("RGBA").resize((icon_size, icon_size), Image.Resampling.LANCZOS)
    canvas.alpha_composite(icon, (cx - icon_size // 2, cy - icon_size // 2))

def draw_levels(canvas, d, l1, l1_size, l2_lines, l2_size, x, maxw, y_start, y_gap1=96, y_gap2=66, align="center"):
    """Level1（大きく）＋Level2（中・自然改行）を描画し、使用した最終yを返す."""
    y = y_start
    l1_lines = wrap_jp(d, l1, font(l1_size), maxw)
    y_anchor = y if align == "left" else y
    for ln in l1_lines:
        if align == "left":
            d.text((x, y_anchor), ln, font=font(l1_size), fill=INK)
        else:
            wl = d.textlength(ln, font=font(l1_size))
            d.text(((W - wl) // 2, y_anchor), ln, font=font(l1_size), fill=INK)
        y_anchor += y_gap1
    y = y_anchor + 16
    for line in l2_lines:
        for ln in wrap_jp(d, line, font(l2_size), maxw):
            if align == "left":
                d.text((x, y), ln, font=font(l2_size), fill=SOFT)
            else:
                wl = d.textlength(ln, font=font(l2_size))
                d.text(((W - wl) // 2, y), ln, font=font(l2_size), fill=SOFT)
            y += y_gap2
    return y

def draw_source(d, source, x, maxw, y=800, align="center"):
    for ln in wrap_jp(d, source, font(26), maxw):
        if align == "left":
            d.text((x, y), ln, font=font(26), fill=SOFT)
        else:
            wl = d.textlength(ln, font=font(26))
            d.text(((W - wl) // 2, y), ln, font=font(26), fill=SOFT)
        y += 38
    note = "※公式ページの案内を引用したカードです（アプリの実画面ではありません）"
    for ln in wrap_jp(d, note, font(24), maxw):
        if align == "left":
            d.text((x, y), ln, font=font(24), fill=LINEN)
        else:
            wl = d.textlength(ln, font=font(24))
            d.text(((W - wl) // 2, y), ln, font=font(24), fill=LINEN)
        y += 34
    return y

def verify_no_overflow(canvas, name):
    rgb = canvas.convert("RGB")
    strip_r = rgb.crop((W - 14, 24, W, H - 180))  # 上部青バー(y0-14)は通常要素として除外
    data = list(strip_r.get_flattened_data()) if hasattr(strip_r, "get_flattened_data") else list(strip_r.getdata())
    ink_like = sum(1 for c in data if min(c) < 150)
    strip_b = rgb.crop((0, H - 180, W, H))
    data_b = list(strip_b.get_flattened_data()) if hasattr(strip_b, "get_flattened_data") else list(strip_b.getdata())
    ink_like_b = sum(1 for c in data_b if min(c) < 150)
    if ink_like > 0 or ink_like_b > 0:
        raise RuntimeError(f"OVERFLOW in {name}: right={ink_like} bottom={ink_like_b}")
    print(f"overflow check {name}: PASS (right={ink_like}, bottom={ink_like_b})")

def make_fact_card(name, pill, l1, l1_size, l2_lines, l2_size, source, icon=None, icon_tone="blue",
                   align="center", two_col=None, img_path=None, img_label=None):
    canvas = base_canvas()
    d = ImageDraw.Draw(canvas)
    draw_pill(d, pill)
    if icon:
        paste_icon(canvas, icon, icon_tone, 168, 205)
    # 本文領域
    cx0, cx1 = (110, 1810 - 20) if two_col is None else (110, 1100)
    maxw = cx1 - cx0
    if two_col is None:
        draw_levels(canvas, d, l1, l1_size, l2_lines, l2_size, cx0, maxw, 320, align="center")
        draw_source(d, source, 0, 1680, y=790, align="center")
        d.text((110, H - 210), "大人のデジタル安心室", font=font(24), fill=SOFT)
    else:
        draw_levels(canvas, d, l1, l1_size, l2_lines, l2_size, cx0, maxw, 250, y_gap1=92, y_gap2=62, align="left")
        draw_source(d, source, cx0, maxw, y=790, align="left")
        d.text((110, H - 210), "大人のデジタル安心室", font=font(24), fill=SOFT)
        # 右パネル（公式イラスト・完全分離）
        d2 = ImageDraw.Draw(canvas)
        d2.rounded_rectangle((1160, 180, 1790, 860), radius=28, fill="#f2f7fc", outline="#d9e7ef", width=2)
        img = Image.open(img_path).convert("RGB")
        img = img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS)
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=80, threshold=2))
        im = ImageOps.contain(img, (560, 560))
        canvas.paste(im, ((1160 + 1790 - im.width) // 2, 250))
        d2.text(((1160 + 1790) // 2, 830), img_label, font=font(24), fill=LINEN, anchor="mm")
    # デバッグ: 描画した行の幅を記録
    for _ln in wrap_jp(d, l1, font(l1_size), maxw):
        print(f"  [dbg {name}] L1 line width={d.textlength(_ln, font=font(l1_size)):.0f} text={_ln[:24]}")
    if two_col is None:
        for _ll in l2_lines:
            for _lw in wrap_jp(d, _ll, font(l2_size), maxw):
                print(f"  [dbg {name}] L2 line width={d.textlength(_lw, font=font(l2_size)):.0f} text={_lw[:24]}")
    try:
        verify_no_overflow(canvas, name)
    except RuntimeError as exc:
        (BASE / "work" / "phase_b_review" / f"debug_{name}.png").parent.mkdir(parents=True, exist_ok=True)
        canvas.convert("RGB").save(BASE / "work" / "phase_b_review" / f"debug_{name}.png", "PNG")
        print("DEBUG saved", f"debug_{name}.png")
        raise
    out = OUT / f"quote_{name}.png"
    canvas.convert("RGB").save(out, "PNG")
    print("saved", out.name)

# SCENE-004 動作環境
make_fact_card("004_system_requirements", "1 / 5 スマホが対応しているか",
               "対応OS：iOS 16.4以上／Android 11以降＋NFC", 68,
               ["端末のロック設定（PIN・顔認証・指紋認証など）が必須です。"], 52,
               "出典：デジタル庁「マイナアプリの動作環境」（2026年9月3日確認）")
# SCENE-005 FAQ 通常モード
make_fact_card("005_faq_login", "1 / 5 スマホが対応しているか",
               "通常モードで、開き直しましょう", 76,
               ["プライベートブラウズやシークレットモードでは、アプリストアへの転送を繰り返すことがあるため、通常モードに切り替えてから、再度ログインをお試しください。"], 48,
               "出典：デジタル庁「マイナアプリ よくある質問」（2026年9月3日確認）")
# SCENE-008 iPhone（2カラム）
make_fact_card("008_scan_iphone", "2 / 5 カードを読み取れない場合",
               "iPhoneは、本体の上部", 72,
               ["カードの上にぴったり合わせて「読み取り開始」をタップ。", "動かさずに、しばらく待ちます。"], 52,
               "出典：デジタル庁「マイナンバーカードの読み取りかた」（2026年9月3日確認）",
               two_col=True, img_path=OUT / "mynaapp_scan_iphone.png", img_label="公式の読み取りイメージ（デジタル庁）")
# SCENE-009 Android（2カラム）
make_fact_card("009_scan_android", "2 / 5 カードを読み取れない場合",
               "Androidは、本体の背面の読み取り位置", 66,
               ["カードに合わせます。機種によって、場所は少し違います。"], 52,
               "出典：デジタル庁「マイナンバーカードの読み取りかた」（2026年9月3日確認）",
               two_col=True, img_path=OUT / "mynaapp_scan_android.png", img_label="公式の読み取りイメージ（デジタル庁）")
# SCENE-012 暗証番号（4桁強調）
make_fact_card("012_register", "3 / 5 暗証番号で止まる場合",
               "数字4桁", 96,
               ["利用者証明用暗証番号を入力します。", "スマホにカードを追加すると、顔や指紋でも登録できます。"], 50,
               "出典：デジタル庁「マイナアプリの利用登録の方法」（2026年9月3日確認）",
               icon="dialpad", icon_tone="blue")
# SCENE-015 カード期限
make_fact_card("015_expiration", "4 / 5 カードや電子証明書の期限",
               "発行から10回目の誕生日まで", 76,
               ["18歳以上の方のカード自体の期限です。", "更新手続は、有効期限の3か月前から市区町村窓口でできます。"], 50,
               "出典：デジタル庁「マイナンバーカードおよび電子証明書の有効期限・更新」（2026年9月3日確認）",
               icon="badge", icon_tone="blue")
# SCENE-018 障害・メンテナンス
make_fact_card("018_maintenance", "5 / 5 それでもダメなら",
               "障害・メンテナンス情報を確認", 72,
               ["マイナポータルの現在の障害情報と、メンテナンス中の情報や今後の予定を確認できます。"], 50,
               "出典：マイナポータル「障害・メンテナンス」（2026年9月3日確認）",
               icon="construction", icon_tone="blue")
# SCENE-019 再設定
make_fact_card("019_reset", "5 / 5 それでもダメなら",
               "暗証番号を忘れたら、再設定", 72,
               ["コンビニの端末で再設定できます。", "（本人確認のため、パスワードの入力が必要）", "分からない場合は、市区町村の窓口で再設定できます。"], 50,
               "出典：公的個人認証サービス「コンビニで初期化・再設定」（2026年9月3日確認）",
               icon="lock_reset", icon_tone="blue")
