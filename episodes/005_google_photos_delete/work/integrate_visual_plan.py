"""Episode 005: Visual Agent plan (work/subagents/...) を episode.json の scenes へ統合する。

canonical single-writer に従い、実行は親Codexのみ。本スクリプトは:
- render_mode: official_placeholder -> official（placeholder asset を official_asset に設定）
- gpt_image scene: fit_mode=full_bleed / text_render_mode=codex
- animation: very_slow_zoom 等を phase2_video が解釈できる名前に正規化
- CTA scene（narrationなし）は episode.json の scenes へ入れず、postroll(channel_common_cta) に委ねる
- narration_segments の scene_id を各sceneの range から逆参照で設定
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(r"C:\Codex\260829_youtube-anshin")
EP = ROOT / "episodes" / "005_google_photos_delete"
EPISODE = EP / "episode.json"
VISUAL = Path(r"C:\Codex\260829_youtube-anshin\work\subagents\005_google_photos_delete\visual_plan.json")

ANIM_MAP = {
    "very_slow_zoom": "very_slow_zoom",
    "section_fade": "section_fade",
    "summary_stagger": "summary_stagger",
    "static": "static",
}


def main() -> None:
    ep = json.loads(EPISODE.read_text(encoding="utf-8"))
    plan = json.loads(VISUAL.read_text(encoding="utf-8"))

    scenes: list[dict] = []
    for v in plan["scenes"]:
        if v.get("narration_range", {}).get("start") is None:
            continue  # CTA scene -> postroll
        start = int(v["narration_range"]["start"])
        end = int(v["narration_range"]["end"])
        scene: dict = {
            "id": int(v["scene_id"]),
            "section_label": v["section_label"],
            "layout": v["layout"],
            "render_mode": "official" if v["render_mode"] == "official_placeholder" else v["render_mode"],
            "text_render_mode": "codex",
            "main_message": v.get("purpose", ""),
            "headline": v["codex_overlay_text"]["headline"] or "確認",
            "support_text": v["codex_overlay_text"]["support_text"],
            "official_asset": [],
            "official_asset_crop": [],
            "animation": ANIM_MAP.get(v["animation_recommendation"], "static"),
            "start_segment": start,
            "end_segment": end,
            "subtitle_ids": [f"SUB-{i:03d}" for i in range(start, end + 1)],
        }
        if v.get("codex_overlay_text", {}).get("items"):
            scene["items"] = v["codex_overlay_text"]["items"]
        if scene["render_mode"] == "gpt_image":
            scene["fit_mode"] = "full_bleed"
            scene["image_prompt"] = v["image_prompt"]
        if scene["render_mode"] == "official":
            scene["official_asset"] = [
                {
                    "kind": "placeholder",
                    "path": v.get("asset_placeholder_path", "assets/emulator/phase_b_capture.png"),
                    "label": v["main_visual"],
                }
            ]
        scenes.append(scene)

    # segment -> scene_id を逆引きで設定
    seg_cover: dict[int, int] = {}
    for s in scenes:
        for i in range(s["start_segment"], s["end_segment"] + 1):
            assert i not in seg_cover, f"segment {i} が複数sceneに割当"
            seg_cover[i] = s["id"]
    for seg in ep["narration_segments"]:
        sid = int(seg["id"])
        assert sid in seg_cover, f"segment {sid} がどのsceneにも属さない"
        seg["scene_id"] = seg_cover[sid]

    ep["scenes"] = scenes
    # 親CodexがPowerShellのCopy-Itemでepisode.jsonへ反映する（write-throughはここでは行わない）
    out = EP / "work" / "episode.scenes.json"
    out.write_text(json.dumps(ep, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"scenes={len(scenes)} segments_cov={len(seg_cover)} "
          f"template={sum(1 for s in scenes if s['render_mode']=='template')} "
          f"gpt_image={sum(1 for s in scenes if s['render_mode']=='gpt_image')} "
          f"official={sum(1 for s in scenes if s['render_mode']=='official')}")


if __name__ == "__main__":
    main()
