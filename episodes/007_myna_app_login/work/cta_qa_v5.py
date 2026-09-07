# -*- coding: utf-8 -*-
"""CTA v5 機械QA: チャンネル名削除・ロゴ/疑似subscribe 0・全文2行60px・reserved・水玉位置."""
from PIL import Image

BASE = r"episodes/007_myna_app_login/work"
IMG = BASE + "/channel_cta.png"
im = Image.open(IMG).convert("RGB")
W, H = im.size
px = im.load()

INK = (63, 140, 88)          # green_text #3f8c58
BAND = (234, 247, 238)       # green_fill #eaf7ee
OUTLINE = (99, 169, 117)     # green_outline #63a975
CHANNEL_INK = (23, 58, 104)  # ink #173a68（チャンネル名・ロゴ濃紺）


def close(c1, c2, tol):
    return all(abs(a - b) <= tol for a, b in zip(c1, c2))


def bbox_of_in(color, tol, box):
    x0, y0, x1, y1 = box
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if close(px[x, y], color, tol):
                xs.append(x); ys.append(y)
    if not xs:
        return None, 0
    return (min(xs), min(ys), max(xs), max(ys)), len(xs)


# 1) チャンネル名・ロゴ（濃紺 ink #173a68）が画面に無いこと
ink_n = 0
for y in range(H):
    for x in range(W):
        if close(px[x, y], CHANNEL_INK, 26):
            ink_n += 1
print(f"CHANNEL_LOGO_AND_NAME_check ink_pixels={ink_n} (expect 0)")

# 2) CTA 帯・本文
band_bb, band_n = bbox_of_in(BAND, 8, (100, 690, 1080, 930))
print(f"GREEN_BAND bbox={band_bb} count={band_n} expect=[138,714,1032,890]")
ink_bb, ink_n2 = bbox_of_in(INK, 18, (100, 700, 1080, 930))
print(f"CTA_INK(in-band) bbox={ink_bb} count={ink_n2} expect y[736,872] x[158,1012]")
if ink_bb:
    rows = {}
    for y in range(ink_bb[1], ink_bb[3] + 1):
        c = 0
        for x in range(ink_bb[0], ink_bb[2] + 1):
            if close(px[x, y], INK, 18):
                c += 1
        rows[y] = c
    bands = []
    cur = None
    for y in sorted(rows):
        if rows[y] > 5:
            if cur is None:
                cur = [y, y]
            else:
                cur[1] = y
        else:
            if cur:
                bands.append(tuple(cur))
                cur = None
    if cur:
        bands.append(tuple(cur))
    print(f"LINE_BANDS(y)= {bands}  => lines={len(bands)}")

# 3) 水玉: 左あり・右なし
DOT_REFS = [(244, 249, 255), (246, 252, 248)]


def dot_hit(c, t=2):
    return any(all(abs(a - b) <= t for a, b in zip(c, r)) for r in DOT_REFS)


left_rows = 0
right_n = 0
for y in range(200, 900):
    cl = sum(1 for x in range(200, 1090) if dot_hit(px[x, y]))
    if cl:
        left_rows += 1
    right_n += sum(1 for x in range(1090, 1800) if dot_hit(px[x, y]))
print(f"BUBBLE_LEFT rows={left_rows} (expect >0) BUBBLE_RIGHT(1090+) n={right_n} (expect 0)")

# 4) 右 reserved クリーン
def foreign_count(box, refs):
    x0, y0, x1, y1 = box
    n = 0
    bb = None
    for y in range(y0, y1):
        for x in range(x0, x1):
            p = px[x, y]
            if not any(close(p, ref, 30) for ref in refs):
                n += 1
                if bb is None:
                    bb = [x, y, x, y]
                else:
                    bb[0] = min(bb[0], x); bb[1] = min(bb[1], y)
                    bb[2] = max(bb[2], x); bb[3] = max(bb[3], y)
    return n, bb


BG_REF = [(247, 251, 254), (240, 246, 253), (239, 245, 252), (255, 255, 255)]
for name, box in [
    ("RESERVED_above_label(1090,20,1800,108)", (1090, 20, 1800, 108)),
    ("RESERVED_below_label(1090,186,1800,880)", (1090, 186, 1800, 880)),
    ("RESERVED_right_of_label(1460,20,1800,880)", (1460, 20, 1800, 880)),
]:
    n, bb = foreign_count(box, BG_REF)
    print(f"{name} foreign={n} bbox={bb}")

label_bb, label_n = bbox_of_in((88, 113, 135), 30, (1090, 100, 1460, 190))
print(f"NEXT_LABEL bbox={label_bb} count={label_n}")

# 5) 疑似subscribe（帯内 outline は周縁のみ）
out_n = 0
if band_bb:
    x0, y0, x1, y1 = band_bb
    for y in range(700, 930):
        for x in range(100, 1080):
            if close(px[x, y], OUTLINE, 16):
                on_edge = (y0 - 8 <= y <= y0 + 8) or (y1 - 8 <= y <= y1 + 8) or +                          (x0 - 8 <= x <= x0 + 8) or (x1 - 8 <= x <= x1 + 8)
                if not on_edge:
                    out_n += 1
print(f"FAKE_SUBSCRIBE_check outline_off_edge={out_n} (expect 0 near band)")

# 6) 説明文（soft #587187）の位置確認（カード中央域 y500-700 に存在）
desc_bb, desc_n = bbox_of_in((88, 113, 135), 26, (150, 400, 1030, 720))
print(f"DESCRIPTION bbox={desc_bb} count={desc_n} (expect y within [555,695] x within [150,1020])")

im.crop((90, 90, 1090, 720)).save(BASE + "/cta_v5_top_crop.png")
im.crop((120, 700, 1090, 910)).save(BASE + "/cta_v5_band_crop.png")
print("DONE")
