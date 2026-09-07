from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

ROOT = Path(r"C:\Codex\260829_youtube-anshin")
EPISODE_DIR = ROOT / "episodes" / "006_line_talk_backup"
EPISODE_JSON = EPISODE_DIR / "episode.json"
OFFICIAL_DIR = EPISODE_DIR / "assets" / "official"
OUT_DIR = EPISODE_DIR / "work" / "phase_b_review" / "readability_fix"
sys.path.insert(0, str(ROOT / "scripts"))

from scene_renderer import HEIGHT, SAFE_HEIGHT, WIDTH, pil_font  # noqa: E402

# scene_id -> (card filename, crop x0, crop x1, crop y0, crop y1)
# quote block: first quote at y=186 (34px, pitch 48), last line 23px,
# disclaimer at y=332 (18px).  x is measured per card below.
CARD_FILES = {
    6: "line_backup_transfer_menu_fallback.png",
    7: "line_talk_backup_datetime_fallback.png",
    11: "line_auto_backup_fallback.png",
    14: "line_icloud_drive_crop.png",
    16: "line_backup_pin_fallback.png",
    20: "line_standard_backup_same_os_crop.png",
    22: "line_backup_trouble_media_crop.png",
}


def measure_crop_box(card: dict) -> tuple[int, int, int, int]:
    draw = ImageDraw.Draw(Image.new("RGB", (1680, 515)))
    quotes = card["quote"]
    max_width = 0
    y = 186
    for index, line in enumerate(quotes):
        size = 34 if index < len(quotes) - 1 else 23
        width = int(draw.textlength(line, font=pil_font(size, bold=index == 0)))
        max_width = max(max_width, width)
        y += 48 if size >= 30 else 35
    disclaimer_width = int(
        draw.textlength(
            "※ 実際のLINE画面ではありません。画面表示はバージョンにより異なります。",
            font=pil_font(18),
        )
    )
    max_width = max(max_width, disclaimer_width)
    right = min(1660, 205 + max_width + 40)
    left = 40
    # quotes start at y=186; crop a little headroom and include the disclaimer
    top = 174
    bottom = 364
    if max_width + 150 < 880:
        right = left + 880
    return (left, top, right, bottom)


def compose_fix(scene: dict, card_path: Path, box: tuple[int, int, int, int]) -> dict:
    headline = str(scene.get("headline") or "").replace("\n", "")
    card = Image.open(card_path).convert("RGB")
    crop = card.crop(box)
    scale = min(1780 / crop.width, 2.45)
    display_width = int(crop.width * scale)
    display_height = int(crop.height * scale)
    if display_height > 540:
        scale = 540 / crop.height
        display_width = int(crop.width * scale)
        display_height = 540

    canvas = Image.new("RGB", (WIDTH, HEIGHT), "#f7fbfe")
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, WIDTH, 14), fill="#2f74bb")
    draw.rectangle((0, HEIGHT - SAFE_HEIGHT, WIDTH, HEIGHT), fill="#f7fbfe")
    draw.line((0, HEIGHT - SAFE_HEIGHT, WIDTH, HEIGHT - SAFE_HEIGHT), fill="#c8deed", width=3)

    draw_fitted = ImageDraw.Draw(canvas)
    from scene_renderer import draw_fitted as fit

    fit(draw_fitted, (90, 55, 1830, 235), headline, 92, 68, "#173a68", 2, "left", 0.12)
    fit(draw_fitted, (95, 250, 1830, 300), "LINE公式手順引用カードを拡大表示（実在UIではありません）", 30, 26, "#587187", 1, "left")

    resized = crop.resize((display_width, display_height), Image.Resampling.LANCZOS)
    x = (WIDTH - display_width) // 2
    y = 330 + max(0, (540 - display_height) // 2)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((x + 10, y + 12, x + display_width + 10, y + display_height + 12), fill="#c8deed")
    canvas.paste(resized, (x, y))
    draw.rectangle((x, y, x + display_width, y + display_height), outline="#b8cee1", width=3)

    fit(ImageDraw.Draw(canvas), (95, 890, 1300, 945), "大人のデジタル安心室", 26, 24, "#587187", 1, "left")
    output = OUT_DIR / f"scene_{int(scene['id']):03d}_readability.png"
    canvas.save(output, "PNG", optimize=True)
    return {
        "scene_id": int(scene["id"]),
        "card": card_path.name,
        "crop_box": list(box),
        "crop_pixels": list(crop.size),
        "scale": round(scale, 2),
        "display_pixels": [display_width, display_height],
        "output": str(output.relative_to(EPISODE_DIR)).replace("\\", "/"),
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    data = json.loads(EPISODE_JSON.read_text(encoding="utf-8"))
    scenes = {int(scene["id"]): scene for scene in data["scenes"]}
    # The generator module is imported instead of parsing its source.
    sys.path.insert(0, str(EPISODE_DIR / "work"))
    import importlib.util

    spec = importlib.util.spec_from_file_location("official_cards", EPISODE_DIR / "work" / "phase_b_official_cards.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    results = []
    for scene_id, filename in CARD_FILES.items():
        card = next(item for item in module.CARDS if item["filename"] == filename)
        box = measure_crop_box(card)
        results.append(compose_fix(scenes[scene_id], OFFICIAL_DIR / filename, box))
    manifest = {
        "purpose": "Phase B後半: 公式fallback引用カードの可読性確認用・拡大表示（単一構図・ズーム演出なし）",
        "policy": "実UIを作り直していない。AIでUIを生成していない。元の公式カード素材をクロップしただけ。",
        "review_only": True,
        "canonical": "episode.json の official_asset は変更していない。差し替え判断は人間の承認後に親Codexのみが行う。",
        "scenes": results,
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
