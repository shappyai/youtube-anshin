#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""capture_android.py — 001_google_security の YouTube 素材を安全に撮影する最小実装。

対象環境（固定）: Pixel 9a Emulator / Android 16 / 1080x2424 / 420dpi / 日本語 /
撮影専用 Google アカウント。同一 AVD である限り SHOT 専用の座標記録を許容する。

方式:
  1. am start で目的 URL を直接開く（アドレスバー入力はしない）
  2. ページロードを 15〜20 秒待つ
  3. 録画前のドライランで uiautomator dump を 1 回取得し、期待日本語テキストと
     タップ座標を確認・記録（capture_coords.json へ保存）
  4. 本番録画では uiautomator dump を繰り返さず、記録済み座標 + sleep で操作
  5. 録画終了後に uiautomator dump を 1 回取得し、到達画面（日本語）を確認

安全ルール:
  - Google アカウント設定の変更をしない
  - ON/OFF 変更・削除・ログアウト・接続解除・作成・追加・許可・続行などの
    確定操作をしない（タップ対象の文言チェックで防御）
  - 期待テキストが見つからない場合は録画せず安全に停止する
  - 一時ファイル・素材は削除しない（既存動画の置き換え時はバックアップのみ）

使い方:
  python scripts/capture_android.py --dry-run --shot 01
  python scripts/capture_android.py --shot 01      # ドライラン確認後に録画
  python scripts/capture_android.py --shot all

外部依存なし。ffprobe があれば動画検証に使用し、なければ内蔵 MP4 パーサで検証する。
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
EPISODE = ROOT / "episodes" / "001_google_security"
RAW = EPISODE / "raw"
LOG_DIR = ROOT / "logs"
COORDS_JSON = EPISODE / "capture_coords.json"
MOSAIC_JSON = EPISODE / "privacy_mosaic_targets.json"
MANIFEST = EPISODE / "media_manifest.csv"
DEVICE_PATH = "/sdcard/cap_shot.mp4"

ADB = shutil.which("adb") or "adb"


def _find_ffprobe() -> str | None:
    p = shutil.which("ffprobe")
    if p:
        return p
    for cand in (Path.home() / "AppData/Local/Microsoft/WinGet/Packages").glob(
        "Gyan.FFmpeg*/*/bin/ffprobe.exe"
    ):
        return str(cand)
    return None


FFPROBE = _find_ffprobe()
SECURITY_URL = "https://myaccount.google.com/security?hl=ja"

# タップしてはいけない操作系の文言（確定操作の防止）
DANGEROUS_TAP = re.compile(
    r"削除|ログアウト|サインアウト|接続を解除|オフにする|オンにする|無効にする|"
    r"有効にする|作成|追加|許可する|^許可|続行|変更する|更新する|"
    r"パスワードを変更|ブロック|報告|停止"
)

# プライバシー検出（公開動画に映してはいけない情報）
PRIVACY_PATTERNS = [
    ("email", re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")),
    ("phone", re.compile(r"0\d{9,10}(?!\d)|0\d{1,4}[-－\s]\d{1,4}[-－\s]\d{3,4}(?!\d)|\+81[-－\s]?\d{1,4}[-－\s]?\d{1,4}[-－\s]?\d{3,4}")),
    ("auth_code", re.compile(r"確認コード|認証コード|verification code|one[- ]?time code|OTP", re.I)),
    ("location", re.compile(r"日本、|都道府県|東京都|大阪府|北海道|福岡県|愛知県|神奈川県|埼玉県|千葉県|位置情報")),
    ("device", re.compile(r"Google emulator|デバイス名|device name|Windows(?!\s*$)", re.I)),
]


class CaptureError(RuntimeError):
    """安全に中断するための例外。"""


class Logger:
    def __init__(self, path: Path):
        LOG_DIR.mkdir(exist_ok=True)
        self.fh = path.open("a", encoding="utf-8")
        self.ts0 = time.time()
        self._closed = False
        self._info(f"=== capture_android.py 開始 {dt.datetime.now().isoformat(timespec='seconds')} ===")

    def _info(self, msg: str):
        line = f"[{time.time() - self.ts0:7.1f}s] {msg}"
        print(line, flush=True)
        self.fh.write(line + "\n")
        self.fh.flush()

    def info(self, msg: str):
        self._info(msg)

    def warn(self, msg: str):
        self._info("警告: " + msg)

    def close(self):
        if self._closed:
            return
        self._closed = True
        self.fh.write(f"=== 終了 {dt.datetime.now().isoformat(timespec='seconds')} ===\n")
        self.fh.close()


def adb(serial: str, *args: str, timeout: int = 120) -> str:
    cmd = [ADB, "-s", serial, *args]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return ""
    if r.returncode != 0:
        return ""
    return r.stdout.decode("utf-8", errors="replace").strip()


def shell_out(*args: str, timeout: int = 120) -> str:
    try:
        r = subprocess.run([ADB, *args], capture_output=True, timeout=timeout)
        return r.stdout.decode("utf-8", errors="replace")
    except Exception:
        return ""


def choose_device(serial: str | None) -> str:
    out = shell_out("devices", "-l")
    devs = [ln.split()[0] for ln in out.splitlines()[1:] if ln.strip() and "device" in ln.split()]
    if not devs:
        raise CaptureError("adb devices で接続中のデバイスが見つかりません")
    if serial:
        if serial not in devs:
            raise CaptureError(f"指定のシリアル {serial} が接続されていません")
        return serial
    emus = [d for d in devs if d.startswith("emulator-")]
    if len(emus) != 1:
        raise CaptureError(f"エミュレータを1台特定できません: {emus or 'なし'}. --serial で指定してください")
    return emus[0]


def log_device_info(logger: Logger, serial: str):
    info = {
        "Android": adb(serial, "shell", "getprop", "ro.build.version.release"),
        "SDK": adb(serial, "shell", "getprop", "ro.build.version.sdk"),
        "model": adb(serial, "shell", "getprop", "ro.product.model"),
        "locale": adb(serial, "shell", "getprop", "persist.sys.locale"),
    }
    wm = adb(serial, "shell", "wm", "size")
    density = adb(serial, "shell", "wm", "density")
    stay = adb(serial, "shell", "settings", "get", "global", "stay_on_while_plugged_in")
    logger.info(f"デバイス情報: {info} / 解像度: {wm} / density: {density} / stay_on: {stay}")
    if "1080x2424" not in wm:
        logger.warn(f"想定外の解像度です（想定: 1080x2424）: {wm}")
    return wm


def ui_dump(serial: str) -> str:
    """uiautomator dump を 1 回取得し XML 文字列を返す。失敗時は "". """
    if not adb(serial, "shell", "uiautomator", "dump", "/sdcard/ui_dump.xml"):
        return ""
    return adb(serial, "shell", "cat", "/sdcard/ui_dump.xml")


def parse_nodes(xml: str) -> list[dict]:
    nodes = []
    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        return nodes

    def walk(el):
        nodes.append({
            "text": (el.attrib.get("text") or "").strip(),
            "desc": (el.attrib.get("content-desc") or "").strip(),
            "clickable": el.attrib.get("clickable") == "true",
            "bounds": el.attrib.get("bounds") or "",
        })
        for c in el:
            walk(c)

    walk(root)
    return nodes


def bounds_xy(bounds: str) -> tuple[int, int, int, int] | None:
    m = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds)
    return tuple(map(int, m.groups())) if m else None


def find_node(xml: str, patterns: list[str]) -> dict | None:
    """patterns に一致する最大面積のノードを返す。"""
    best, best_area = None, -1
    for n in parse_nodes(xml):
        hay = f"{n['text']} {n['desc']}".strip()
        if any(re.search(p, hay) for p in patterns):
            bb = bounds_xy(n["bounds"])
            if bb:
                area = (bb[2] - bb[0]) * (bb[3] - bb[1])
                if area > best_area:
                    best, best_area = n, area
    return best


def node_center(node: dict) -> tuple[int, int]:
    bb = bounds_xy(node["bounds"])
    return (bb[0] + bb[2]) // 2, (bb[1] + bb[3]) // 2


def screen_texts(xml: str) -> list[str]:
    return [n["text"] for n in parse_nodes(xml) if n["text"]]


def find_with_retry(logger, serial: str, patterns: list[str], label: str,
                    wait_between: float = 2.5, max_wait: float = 40.0) -> tuple[str, dict]:
    """ドライラン用: 短間隔で dump を繰り返し（a11y ツリー生存を維持）、
    期待要素が見つかった時点の XML とノードを返す。見つからなければ安全停止。
    録画中は呼ばないこと（録画中は記録済み座標 + sleep のみ）。"""
    t0 = time.time()
    n_dumps = 0
    while time.time() - t0 < max_wait:
        xml = ui_dump(serial)
        n_dumps += 1
        if xml:
            node = find_node(xml, patterns)
            if node:
                logger.info(f"[{label}] 検出（{n_dumps} 回目の dump・{time.time() - t0:.0f}秒）: bounds={node['bounds']}")
                return xml, node
        time.sleep(wait_between)
    raise CaptureError(
        f"[{label}] 期待要素が見つかりません（{n_dumps} 回 dump）。"
        f"画面構成が変わった可能性があります。パターン={patterns}"
    )


def tap_xy(logger: Logger, serial: str, x: int, y: int, label: str, pause: float = 0.8):
    time.sleep(pause)  # タップ前 0.5〜1 秒静止
    r = subprocess.run([ADB, "-s", serial, "shell", "input", "tap", str(x), str(y)],
                       capture_output=True, timeout=60)
    if r.returncode != 0:
        raise CaptureError(f"タップ実行に失敗しました ({x},{y}) rc={r.returncode}")
    logger.info(f"[{label}] タップ ({x},{y})（{pause:.1f}秒静止後）")


def swipe_up(serial: str, wm: str, frac: float = 0.25):
    m = re.search(r"(\d+)x(\d+)", wm)
    if not m:
        return
    w, h = int(m.group(1)), int(m.group(2))
    x = w // 2
    y0, y1 = int(h * 0.75), int(h * (0.75 - frac))
    adb(serial, "shell", "input", "swipe", str(x), str(y0), str(x), str(y1), "300")


def scan_privacy(logger: Logger, xml: str, screen_name: str, shot_id: str,
                 attention: list[str], mosaic_db: dict):
    """プライバシー情報を検出してモザイク対象 DB に記録する（検出のみ・停止しない）。"""
    hits = []
    seen = set()
    for n in parse_nodes(xml):
        hay = f"{n['text']} {n['desc']}".strip()
        if not hay:
            continue
        for kind, pat in PRIVACY_PATTERNS:
            for m in pat.finditer(hay):
                key = (kind, n["bounds"], m.start())
                if key in seen:
                    continue
                seen.add(key)
                hits.append({"shot": shot_id, "screen": screen_name, "kind": kind,
                             "text": hay[max(0, m.start() - 20): m.end() + 20], "bounds": n["bounds"]})
        for ap in attention:
            for m in re.finditer(ap, hay):
                key = ("att", n["bounds"], m.start(), ap)
                if key in seen:
                    continue
                seen.add(key)
                hits.append({"shot": shot_id, "screen": screen_name, "kind": "attention",
                             "text": hay[max(0, m.start() - 20): m.end() + 20], "bounds": n["bounds"]})
    if hits:
        db = mosaic_db.get("shots", {}).setdefault(shot_id, [])
        for h in hits:
            if not any((x["screen"], x["kind"], x["bounds"]) == (h["screen"], h["kind"], h["bounds"]) for x in db):
                db.append(h)
        kinds = {}
        for h in hits:
            kinds[h["kind"]] = kinds.get(h["kind"], 0) + 1
        logger.warn(f"[{screen_name}] プライバシー検出 {len(hits)} 件（{kinds}）→ モザイク対象に記録")
    return hits


def load_json(path: Path, default):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return default


def save_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ---- SHOT 定義（固定環境向け・座標はドライランで記録）----
SHOTS = {
    "01": {
        "id": "SHOT-01",
        "filename": "shot_01_security_checkup.mp4",
        "screen": "セキュリティ診断",
        "start_tab": "about:blank",
        "steps": [
            {"kind": "open_url", "url": SECURITY_URL, "wait": 18},
            {"kind": "verify", "name": "セキュリティとログイン", "patterns": [r"セキュリティとログイン", r"おすすめのセキュリティ対策があります"], "capture_as": "checkup_card", "hold": 2.5},
            {"kind": "tap", "key": "checkup_card"},
            {"kind": "verify", "name": "セキュリティ診断(最終)", "patterns": [r"推奨される対応があります"], "wait": 18, "hold": 3.0},
        ],
        "final_ja": [r"推奨される対応があります"],
        "attention": [r"日本、", r"東京都", r"Google emulator", r"Windows"],
        "required_taps": ["checkup_card"],
    },
    "02": {
        "id": "SHOT-02",
        "filename": "shot_02_recovery.mp4",
        "screen": "再設定用の電話番号",
        "start_tab": "about:blank",
        "steps": [
            # 方針変更: スクロール経路は使わず、確認済みの直接URLで開く
            {"kind": "open_url", "url": "https://myaccount.google.com/phone?hl=ja", "wait": 18},
            {"kind": "verify", "name": "電話番号(最終)", "patterns": [r"電話番号"], "wait": 18, "hold": 3.0},
        ],
        "final_ja": [r"電話番号"],
        "attention": [r"\+81", r"0\d{9,10}", r"@"],
        "required_taps": [],
    },
    "03": {
        "id": "SHOT-03",
        "filename": "shot_03_2step.mp4",
        "screen": "2段階認証・パスキー",
        "start_tab": "about:blank",
        "steps": [
            {"kind": "open_url", "url": SECURITY_URL, "wait": 18},
            {"kind": "verify", "name": "セキュリティとログイン", "patterns": [r"セキュリティとログイン"], "hold": 1.5},
            {"kind": "scroll", "key": "2fa_card", "patterns": [r"2\s*段階認証プロセス"], "max_swipes": 4},
            {"kind": "tap", "key": "2fa_card", "patterns": [r"2\s*段階認証プロセス"]},
            {"kind": "verify", "name": "2段階認証・パスキー(最終)", "patterns": [r"2\s*段階認証", r"パスキー"], "wait": 18, "hold": 3.0},
        ],
        "final_ja": [r"2\s*段階認証", r"パスキー"],
        "attention": [r"確認コード", r"@", r"電話番号"],
        "required_taps": ["2fa_card"],
    },
    "04": {
        "id": "SHOT-04",
        "filename": "shot_04_devices.mp4",
        "screen": "お使いのデバイス",
        "start_tab": "about:blank",
        "steps": [
            {"kind": "open_url", "url": SECURITY_URL, "wait": 18},
            {"kind": "verify", "name": "セキュリティとログイン", "patterns": [r"セキュリティとログイン"], "hold": 1.5},
            {"kind": "scroll", "key": "devices_card", "patterns": [r"お使いのデバイス"], "max_swipes": 5},
            {"kind": "tap", "key": "devices_card", "patterns": [r"お使いのデバイス"]},
            {"kind": "verify", "name": "デバイス一覧(最終)", "patterns": [r"アカウントにアクセスしたデバイス", r"デバイスを管理"], "wait": 18, "hold": 3.0},
        ],
        "final_ja": [r"デバイスを管理"],
        "attention": [r"日本、", r"東京都", r"Google emulator", r"Windows"],
        "required_taps": ["devices_card"],
    },
    "05": {
        "id": "SHOT-05",
        "filename": "shot_05_connections.mp4",
        "screen": "リンク済みアプリ（サードパーティ接続）",
        "start_tab": "about:blank",
        "steps": [
            # 方針変更: スクロール経路は使わず、確認済みの直接URLで開く
            {"kind": "open_url", "url": "https://myaccount.google.com/connections?hl=ja", "wait": 18},
            {"kind": "verify", "name": "リンク済みアプリ(最終)", "patterns": [r"リンク済みアプリ"], "wait": 18, "hold": 3.0},
        ],
        "final_ja": [r"リンク済みアプリ"],
        "attention": [r"@", r"日本、", r"東京都"],
        "required_taps": [],
    },
}


def load_coords() -> dict:
    return load_json(COORDS_JSON, {"shots": {}})


def save_coords(coords: dict):
    save_json(COORDS_JSON, coords)


def verify_dump(logger, serial, shot: dict, step: dict, mosaic_db: dict, wm: str, coords: dict):
    """短間隔 dump で（ページ上部のまま）期待日本語テキストを確認する。
    スクロールしないのは、Chrome のツリーが現 viewport のみを含むため。
    見つからなければ画面構成変化とみなして安全に停止する（ドライランのみ）。"""
    xml, node = find_with_retry(logger, serial, step["patterns"], step["name"])
    if step.get("capture_as"):
        x, y = node_center(node)
        coords_key = step["capture_as"]
        hay = f"{node['text']} {node['desc']}".strip()
        dm = DANGEROUS_TAP.search(hay)
        if dm:
            raise CaptureError(f"確定操作と判断される要素はタップしません: '{dm.group()}'")
        coords.setdefault("shots", {}).setdefault(shot["id"], {})[coords_key] = {
            "x": x, "y": y, "bounds": node["bounds"], "pattern": step["patterns"]
        }
        logger.info(f"[タップ対象 {coords_key}] 座標を記録: ({x},{y}) bounds={node['bounds']}")
    logger.info(f"[{step['name']}] 日本語表示を確認 OK: {step['patterns']}")
    scan_privacy(logger, xml, step["name"], shot["id"], shot.get("attention", []), mosaic_db)
    time.sleep(step.get("hold", 0.0))


def execute_steps(logger, serial, shot: dict, mode: str, coords: dict, wm: str, mosaic_db: dict):
    """ドライラン(dry)は dump 1 回・座標記録つき。録画(record)は記録済み座標 + sleep。"""
    for step in shot["steps"]:
        kind = step["kind"]
        if kind == "open_url":
            time.sleep(step.get("pause", 1.0))
            adb(serial, "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", step["url"])
            logger.info(f"URLを開く: {step['url']}")
            time.sleep(step.get("wait", 18))
        elif kind == "verify":
            if mode == "dry":
                if step.get("wait"):
                    time.sleep(step["wait"])
                verify_dump(logger, serial, shot, step, mosaic_db, wm, coords)
            else:
                # 録画中は dump を繰り返さない（待機 + 静止のみ）
                time.sleep(step.get("wait", 0) + step.get("hold", 0.0))
                logger.info(f"[{step['name']}] 録画中: 待機 {step.get('wait', 0) + step.get('hold', 0.0):.0f}秒")
        elif kind == "tap":
            key = step["key"]
            # ドライラン・録画とも記録済み座標をタップ（スクロールしない）
            c = coords.get("shots", {}).get(shot["id"], {}).get(key)
            if not c:
                raise CaptureError(f"{key} の座標記録がありません（ドライランで記録されるまで録画不可）")
            tap_xy(logger, serial, c["x"], c["y"], f"タップ対象 {key}", step.get("pause", 1.0))
        elif kind == "scroll":
            key = step["key"]
            if mode == "dry":
                # カードが「画面内に見える位置」で見つかるまで次を繰り返す:
                #   1) 2.5秒間隔の連続 dump（a11y ツリー生存を維持）で検索
                #   2) 見つからない or 画面外なら 1 スワイプして再検索
                # 見つかった位置（座標）とスクロール回数を記録する
                target = None
                swipes = 0
                while swipes <= step.get("max_swipes", 4):
                    t0 = time.time()
                    while time.time() - t0 < 30:
                        xml = ui_dump(serial)
                        node = find_node(xml, step["patterns"])
                        if node:
                            bb = bounds_xy(node["bounds"])
                            cy = (bb[1] + bb[3]) // 2 if bb else -1
                            if 350 <= cy <= 2300:  # 画面上部バー／下部ジェスチャー領域を除く
                                target = node
                                break
                            break  # 見つかったが画面外 -> スワイプへ
                        time.sleep(2.5)
                    if target:
                        break
                    if swipes >= step.get("max_swipes", 4):
                        break
                    swipe_up(serial, wm)
                    swipes += 1
                    time.sleep(3)
                if not target:
                    raise CaptureError(f"[スクロール {key}] 要素が見つかりません（画面構成変化の可能性）")
                x, y = node_center(target)
                coords.setdefault("shots", {}).setdefault(shot["id"], {})[key] = {
                    "x": x, "y": y, "bounds": target["bounds"], "swipes": swipes
                }
                logger.info(f"[スクロール {key}] {swipes} 回のスワイプで発見・座標を記録: ({x},{y}) bounds={target['bounds']}")
                time.sleep(1.0)
            else:
                sw = coords.get("shots", {}).get(shot["id"], {}).get(key, {}).get("swipes", 0)
                for _ in range(sw):
                    swipe_up(serial, wm)
                    time.sleep(4)
                logger.info(f"[スクロール {key}] 録画中: {sw} 回スワイプ")


def verify_mp4(logger: Logger, path: Path, shot_id: str) -> dict:
    """ffprobe 優先、なければ内蔵 MP4 パーサで検証。"""
    size = path.stat().st_size
    logger.info(f"動画検証: {path.name} ({size} bytes)")
    if FFPROBE:
        try:
            r = subprocess.run(
                [FFPROBE, "-v", "error", "-select_streams", "v:0",
                 "-show_entries", "stream=codec_name,width,height",
                 "-show_entries", "format=duration,size", "-of", "json", str(path)],
                capture_output=True, timeout=120)
            info = json.loads(r.stdout.decode("utf-8", errors="replace"))
            s = info["streams"][0]
            dur = float(info["format"]["duration"])
            res = {"tool": "ffprobe", "codec": s.get("codec_name"), "width": s.get("width"),
                   "height": s.get("height"), "duration_s": round(dur, 1)}
            logger.info(f"ffprobe: {res}")
            return res
        except Exception as e:
            logger.warn(f"ffprobe 失敗 -> 内蔵パーサで検証: {e}")
    data = path.read_bytes()
    res = {"tool": "builtin", "size": len(data), "ftyp": data[4:8] == b"ftyp", "h264": b"avc1" in data}

    def be32(b, o):
        return int.from_bytes(b[o:o + 4], "big")

    total, scale = 0, 0
    pos = 0
    while pos + 8 <= len(data) and total == 0:
        size = be32(data, pos)
        if size < 8 or pos + size > len(data):
            break
        if data[pos + 4:pos + 8] == b"moov":
            end = pos + size
            q = pos + 8
            while q + 8 <= end:
                s2 = be32(data, q)
                if s2 < 8 or q + s2 > end:
                    break
                if data[q + 4:q + 8] == b"trak":
                    e2 = q + s2
                    r2 = q + 8
                    while r2 + 8 <= e2:
                        s3 = be32(data, r2)
                        if s3 < 8 or r2 + s3 > e2:
                            break
                        if data[r2 + 4:r2 + 8] == b"mdia":
                            e3 = r2 + s3
                            u = r2 + 8
                            while u + 8 <= e3:
                                s4 = be32(data, u)
                                if s4 < 8 or u + s4 > e3:
                                    break
                                t4 = data[u + 4:u + 8]
                                if t4 == b"mdhd":
                                    scale = be32(data, u + (20 if data[u + 8] == 0 else 28))
                                if t4 == b"minf":
                                    e4 = u + s4
                                    v = u + 8
                                    while v + 8 <= e4:
                                        s5 = be32(data, v)
                                        if s5 < 8:
                                            break
                                        if data[v + 4:v + 8] == b"stbl":
                                            e5 = v + s5
                                            w = v + 8
                                            while w + 8 <= e5:
                                                s6 = be32(data, w)
                                                if s6 < 8:
                                                    break
                                                if data[w + 4:w + 8] == b"stts":
                                                    cnt = be32(data, w + 12)
                                                    x = w + 16
                                                    for _ in range(cnt):
                                                        total += be32(data, x) * be32(data, x + 4)
                                                        x += 8
                                                w += s6
                                        v += s5
                                u += s4
                        r2 += s3
                q += s2
        pos += size
    res["duration_s"] = round(total / scale, 1) if scale else -1
    logger.info(f"内蔵パーサ: {res}")
    return res


def update_manifest(logger: Logger, shot_id: str, duration_s: float):
    if not MANIFEST.exists():
        raise CaptureError("media_manifest.csv が見つかりません")
    rows = list(csv.reader(MANIFEST.open(encoding="utf-8-sig")))
    today = dt.date.today().isoformat()
    for row in rows:
        if row and row[0] == shot_id:
            row[3] = f"撮影済み {today}（capture_android.py・{duration_s:.0f}秒・テストアカウント）"
    with MANIFEST.open("w", encoding="utf-8-sig", newline="") as f:
        csv.writer(f).writerows(rows)
    logger.info(f"{MANIFEST.name} を更新: {shot_id} -> 撮影済み")


def open_start_tab(logger, serial, shot: dict):
    """Chrome を再起動してから開始タブ（新規タブ）を用意する。
    タブ蓄積によるエミュレータ劣化を避けるため毎回フレッシュなプロセスにする。
    ダイアログは選択せず BACK で閉じる（設定変更しない）。"""
    adb(serial, "shell", "am", "force-stop", "com.android.chrome")
    time.sleep(2.0)
    adb(serial, "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", shot["start_tab"])
    time.sleep(4.0)
    xml = ui_dump(serial)
    if re.search(r"言語を選択|Select.*(your )?language", xml, re.I) and re.search(r"キャンセル|Cancel|OK", xml, re.I):
        logger.warn("Chrome 言語選択ダイアログ -> 選択せず BACK で閉じます")
        adb(serial, "shell", "input", "keyevent", "4")
        time.sleep(1.5)
    if re.search(r"通知|notifications", xml, re.I) and re.search(r"No thanks|続行|許可|Allow", xml, re.I):
        logger.warn("通知許可プロンプト -> 選択せず BACK で閉じます")
        adb(serial, "shell", "input", "keyevent", "4")
        time.sleep(1.5)
    logger.info(f"開始画面: Chrome の新しいタブ ({shot['start_tab']})")


def run_shot(args, logger: Logger, serial: str, shot_id: str, wm: str):
    shot = SHOTS[shot_id]
    logger.info(f"===== {shot['id']} 開始（{shot['filename']}）=====")
    mosaic_db = load_json(MOSAIC_JSON, {"generated_at": "", "shots": {}})
    coords = load_coords()
    coords.setdefault("shots", {}).setdefault(shot_id, {})

    # 1) ドライラン（録画なし）: dump は各画面 1 回・タップ座標を記録
    logger.info("--- ドライラン ---")
    open_start_tab(logger, serial, shot)
    execute_steps(logger, serial, shot, "dry", coords, wm, mosaic_db)
    save_coords(coords)
    save_json(MOSAIC_JSON, mosaic_db)
    for need in shot["required_taps"]:
        if need not in coords["shots"].get(shot["id"], {}):
            raise CaptureError(f"ドライランで {need} の座標が記録されていません")
    logger.info(f"ドライラン完了。{shot['id']} の座標: {coords['shots'].get(shot['id'], {})}")

    if args.dry_run:
        logger.info("DRY-RUN モードのため録画は行いません")
        return None

    # 2) 既存ファイルはバックアップ（削除しない）
    target = RAW / shot["filename"]
    RAW.mkdir(exist_ok=True)
    if target.exists():
        bak = RAW / f"_backup_{Path(shot['filename']).stem}_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        shutil.copy2(target, bak)
        logger.info(f"既存ファイルをバックアップ: {bak.name}")

    # 3) 録画時間の見積り（固定値ベース）
    total = 2.5 + 1.0 + 18.0 + 2.5 + 1.0 + 18.0 + 3.0
    limit = int(min(60, max(35, total + 8)))
    logger.info(f"録画プラン: 見積り {total:.0f}s + 余裕 8s -> limit={limit}s")

    # 4) 録画開始（本番は記録済み座標 + sleep のみ・dump を繰り返さない）
    open_start_tab(logger, serial, shot)  # 録画開始画面（新規タブ）を再セット
    proc = subprocess.Popen(
        [ADB, "-s", serial, "shell", "screenrecord",
         "--time-limit", str(limit), "--bit-rate", "12000000", DEVICE_PATH],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding="utf-8", errors="replace")
    time.sleep(2.5)  # 撮影開始前に 2 秒静止
    logger.info(f"screenrecord 開始（--time-limit {limit}）")
    try:
        execute_steps(logger, serial, shot, "record", coords, wm, mosaic_db)
        time.sleep(3.0)  # 最終画面で 3 秒静止
        logger.info("最終画面で 3 秒静止完了")
    except Exception:
        adb(serial, "shell", "kill", "-INT", "$(pidof screenrecord)")
        raise
    finally:
        proc.wait(timeout=90)
        logger.info(f"screenrecord 終了（rc={proc.returncode}）")

    # 5) pull + ffprobe 等で検証
    adb(serial, "pull", DEVICE_PATH, str(target))
    if not target.exists() or target.stat().st_size == 0:
        raise CaptureError("録画ファイルの pull に失敗しました")
    v = verify_mp4(logger, target, shot_id)
    if v.get("duration_s", 0) < 10:
        raise CaptureError(f"録画が短すぎます: {v.get('duration_s')}秒")

    # 6) 録画後に dump で到達画面（日本語）を確認（録画は終了済み）
    time.sleep(15)  # 画面は静止したまま（録画は終了済み）
    try:
        xml, _node = find_with_retry(logger, serial, shot["final_ja"], shot["screen"] + "(録画後確認)")
    except CaptureError:
        raise CaptureError(
            "録画後の最終画面で日本語キーワードが確認できません（ファイルは残します。"
            "manifest は更新しません）"
        )
    logger.info(f"録画後確認: 最終画面の日本語表示 OK")
    scan_privacy(logger, xml, shot["screen"] + "(録画後)", shot["id"], shot.get("attention", []), mosaic_db)
    save_json(MOSAIC_JSON, mosaic_db)
    update_manifest(logger, shot["id"], v.get("duration_s", 0))
    logger.info(f"{shot['id']} 完了: {target}（{v.get('duration_s')}秒）")
    return v


def main():
    ap = argparse.ArgumentParser(description="Pixel 9a Emulator で YouTube 用画面素材を安全に録画する")
    ap.add_argument("--shot", choices=["01", "02", "03", "04", "05", "all"], default="01")
    ap.add_argument("--dry-run", action="store_true", help="録画せずに画面確認・座標記録のみ")
    ap.add_argument("--serial", default=None)
    args = ap.parse_args()

    log_path = LOG_DIR / f"capture_android_001_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logger = Logger(log_path)
    try:
        serial = choose_device(args.serial)
        logger.info(f"使用デバイス: {serial}")
        wm = log_device_info(logger, serial)
        shot_ids = ["01", "02", "03", "04", "05"] if args.shot == "all" else [args.shot]
        results = {sid: run_shot(args, logger, serial, sid, wm) for sid in shot_ids}
        logger.info(f"結果: { {k: (v and v.get('duration_s')) for k, v in results.items()} }")
        print(f"\nログ保存先: {log_path}")
        print(f"座標記録: {COORDS_JSON}")
        print(f"モザイク対象: {MOSAIC_JSON}")
    except CaptureError as e:
        logger.warn(f"中止: {e}")
        print(f"\n中止: {e}", file=sys.stderr)
        raise SystemExit(2)
    finally:
        logger.close()


if __name__ == "__main__":
    main()
