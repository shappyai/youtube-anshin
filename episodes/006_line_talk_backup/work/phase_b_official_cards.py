from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(r"C:\Codex\260829_youtube-anshin")
EPISODE_DIR = ROOT / "episodes" / "006_line_talk_backup"
OUT_DIR = EPISODE_DIR / "assets" / "official"
sys.path.insert(0, str(ROOT / "scripts"))
from scene_renderer import pil_font  # noqa: E402


CARDS = [
    {
        "filename": "line_backup_transfer_menu_fallback.png",
        "title": "標準バックアップの手順",
        "quote": [
            "ホーム ＞ 設定 ＞ バックアップ・引き継ぎ",
            "＞ トークのバックアップ",
            "「今すぐバックアップ」をタップ",
        ],
        "source": "LINE公式「トーク履歴を標準バックアップするには？」",
        "url": "https://guide.line.me/ja/account-and-settings/account-and-profile/talk-backup.html",
    },
    {
        "filename": "line_talk_backup_datetime_fallback.png",
        "title": "バックアップ完了の確認",
        "quote": [
            "LINE公式の手順：",
            "「今すぐバックアップ」をタップ",
            "表示はアプリのバージョンで異なる場合があります",
        ],
        "source": "LINE公式「トーク履歴を標準バックアップするには？」",
        "url": "https://guide.line.me/ja/account-and-settings/account-and-profile/talk-backup.html",
    },
    {
        "filename": "line_auto_backup_fallback.png",
        "title": "自動バックアップの設定",
        "quote": [
            "バックアップ頻度 ＞ 自動バックアップをオンにする",
            "公式手順に沿って、頻度を選びます",
        ],
        "source": "LINE公式「トーク履歴を標準バックアップするには？」",
        "url": "https://guide.line.me/ja/account-and-settings/account-and-profile/talk-backup.html",
    },
    {
        "filename": "line_icloud_drive_crop.png",
        "title": "iCloud Driveを確認",
        "quote": [
            "トークを復元するには、",
            "LINEアカウントの引き継ぎ前に",
            "iCloud Driveをオンにしてください",
        ],
        "source": "LINE公式「トーク履歴を復元するには？」",
        "url": "https://guide.line.me/ja/account-and-settings/account-and-profile/restore-talk-history.html",
    },
    {
        "filename": "line_backup_pin_fallback.png",
        "title": "バックアップ用のPINコード",
        "quote": [
            "バックアップ用のPINコードを作成",
            "6桁の数字を登録します",
            "実際の番号は画面に表示しません",
        ],
        "source": "LINE公式「[バックアップ用のPINコード]とは？」",
        "url": "https://guide.line.me/ja/account-and-settings/account-and-profile/talk-backup-pin.html",
    },
    {
        "filename": "line_standard_backup_same_os_crop.png",
        "title": "標準バックアップの対応範囲",
        "quote": [
            "同じOSへの引き継ぎで利用できます",
            "iPhone → iPhone ／ Android → Android",
            "公式案内より",
        ],
        "source": "LINE公式「トーク履歴を標準バックアップするには？」",
        "url": "https://guide.line.me/ja/account-and-settings/account-and-profile/talk-backup.html",
    },
    {
        "filename": "line_backup_trouble_media_crop.png",
        "title": "画像・動画のバックアップ",
        "quote": [
            "標準バックアップでは、",
            "画像・動画はバックアップ・復元されません",
            "必要なものは端末に保存します",
        ],
        "source": "LINE公式「トーク履歴のバックアップ⋅復元で困ったとき」",
        "url": "https://guide.line.me/ja/account-and-settings/account-and-profile/talk-backup-trouble.html",
    },
]


def draw_centered(draw: ImageDraw.ImageDraw, text: str, box: tuple[int, int, int, int], font, fill):
    left, top, right, bottom = box
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    draw.text(((left + right - width) // 2, (top + bottom - height) // 2), text, font=font, fill=fill)


def make_card(card: dict) -> None:
    # The official-scene renderer has a 1680x515 asset slot.  Build the
    # excerpt at that size so the quoted source text stays large and legible.
    image = Image.new("RGB", (1680, 515), "#f3f8fc")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1680, 62), fill="#2d6fae")
    draw.text((46, 15), "LINE公式手順｜保存HTML由来の引用カード", font=pil_font(25, bold=True), fill="#ffffff")
    draw.rounded_rectangle((38, 80, 1642, 450), radius=16, fill="#ffffff", outline="#b8cee1", width=3)
    draw.text((76, 99), card["title"], font=pil_font(31, bold=True), fill="#17324d")
    draw.text((76, 150), "公式文言の要点", font=pil_font(20, bold=True), fill="#2d6fae")
    y = 186
    for index, line in enumerate(card["quote"]):
        color = "#17324d" if index < len(card["quote"]) - 1 else "#47708e"
        size = 34 if index < len(card["quote"]) - 1 else 23
        draw.text((205, y), line, font=pil_font(size, bold=index == 0), fill=color)
        y += 48 if size >= 30 else 35
    draw.text((76, 332), "※ 実際のLINE画面ではありません。画面表示はバージョンにより異なります。", font=pil_font(18), fill="#a04c36")
    draw.text((76, 365), card["source"], font=pil_font(18, bold=True), fill="#385d76")
    draw.rectangle((0, 450, 1680, 515), fill="#e9f0f6")
    draw.text((48, 469), "一次情報確認用｜確認日：2026-09-02", font=pil_font(18, bold=True), fill="#17324d")
    image.save(OUT_DIR / card["filename"], format="PNG", optimize=True)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for card in CARDS:
        make_card(card)
        print(card["filename"])


if __name__ == "__main__":
    main()
