"""Convert the accepted Episode 002 planning files into episode.json.

This is a one-time, repeatable migration aid.  It reads the existing
script-adjacent CSV/Markdown files and never touches audio, video, source
images, or any of the existing episode outputs.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EPISODE_DIR = ROOT / "episodes" / "002_myna_app"


SOURCES = [
    {
        "source_id": "SRC-001",
        "url": "https://digital-gov.note.jp/n/n64bc51024681",
        "title": "マイナポータルアプリが「マイナアプリ」になりました（利用登録のご案内）",
        "organization": "デジタル庁",
        "claim": "2026年8月25日から提供開始。マイナポータルアプリにデジタル認証アプリの仕組みを統合し、既存利用者はアップデートだけで利用できる。",
    },
    {
        "source_id": "SRC-002",
        "url": "https://www.digital.go.jp/policies/mynumber/local-government/mynaportal-app",
        "title": "マイナアプリ（自治体向け活用情報）",
        "organization": "デジタル庁",
        "claim": "ログイン認証、電子署名、券面情報入力支援、スマホ用電子証明書搭載の4機能と、行政・民間での利用を確認。",
    },
    {
        "source_id": "SRC-003",
        "url": "https://www.digital.go.jp/speech/minister-260825-01",
        "title": "松本大臣記者会見（令和8年8月25日）",
        "organization": "デジタル庁",
        "claim": "2026年8月25日のリリース、両アプリの統合、自動更新、初回登録、端末ロック、暫定アイコンについて確認。",
    },
    {
        "source_id": "SRC-004",
        "url": "https://services.digital.go.jp/mynaapp/",
        "title": "マイナアプリ（サービスサイト・トップ）",
        "organization": "デジタル庁",
        "claim": "呼称変更、期間限定アイコン、既存アプリのアップデート、マイナポータルWebの継続利用、公式ストアへの導線を確認。",
    },
    {
        "source_id": "SRC-005",
        "url": "https://services.digital.go.jp/mynaapp/news/20260825-01/",
        "title": "マイナアプリの提供を開始しました（お知らせ）",
        "organization": "デジタル庁",
        "claim": "マイナポータルアプリへのデジタル認証アプリ機能統合と、マイナポータルWebの継続利用を確認。",
    },
    {
        "source_id": "SRC-006",
        "url": "https://services.digital.go.jp/mynaapp/system-requirements/",
        "title": "マイナアプリの動作環境",
        "organization": "デジタル庁",
        "claim": "iOS 16.4以上、Android 11以降かつNFC、端末ロック設定が必要であることを確認。",
    },
    {
        "source_id": "SRC-007",
        "url": "https://services.digital.go.jp/mynaapp/register/",
        "title": "マイナアプリの利用登録の方法",
        "organization": "デジタル庁",
        "claim": "初回登録の流れ、実物カードと数字4桁の暗証番号、スマホ内カードの顔・指紋認証を確認。",
    },
    {
        "source_id": "SRC-008",
        "url": "https://services.digital.go.jp/mynaapp/communication-guidelines/",
        "title": "マイナアプリ 広報素材およびガイドライン",
        "organization": "デジタル庁",
        "claim": "正しい呼称、公式アイコンの仕様、公式素材、移行期間の新旧呼称併記を確認。",
    },
    {
        "source_id": "SRC-009",
        "url": "https://developers.digital.go.jp/documents/auth-and-sign/implement-guideline/",
        "title": "行政機関等・民間事業者向け実装ガイドライン",
        "organization": "デジタル庁",
        "claim": "デジタル認証アプリがマイナアプリに統合され、単体利用が終了したことを確認。",
    },
    {
        "source_id": "SRC-010",
        "url": "https://apps.apple.com/jp/app/マイナアプリ-旧マイナポータルアプリ/id1476359069",
        "title": "App Store「マイナアプリ（旧マイナポータルアプリ）」",
        "organization": "Apple",
        "claim": "アプリ名、販売元 Digital Agency of Japan、同じアプリID・バンドルIDの掲載情報を確認。",
    },
    {
        "source_id": "SRC-011",
        "url": "https://play.google.com/store/apps/details?id=jp.go.cas.mpa",
        "title": "Google Play「マイナアプリ（旧マイナポータルアプリ）」",
        "organization": "Google",
        "claim": "アプリ名、提供者デジタル庁、マイナポータルアプリをアップデートして統合した説明を確認。",
    },
    {
        "source_id": "SRC-012",
        "url": "https://support.mynaapp.digital.go.jp/hc/ja",
        "title": "マイナアプリ よくある質問",
        "organization": "デジタル庁",
        "claim": "自動更新、名前・アイコン変更、未更新時、データ引き継ぎ、入れ直し、ログイン不調の公式案内を確認。",
    },
    {
        "source_id": "SRC-013",
        "url": "https://www.digital.go.jp/news/b32e5c16-8272-4cc3-9171-b4c583325feb",
        "title": "年金事務所を騙る偽サイト・偽アプリへの注意喚起",
        "organization": "デジタル庁",
        "claim": "公式アプリはApp Store・Google Playからのみ入手すること、偽サイト・偽アプリ事案、相談窓口を確認。",
    },
    {
        "source_id": "SRC-014",
        "url": "https://www.digital.go.jp/news/4750a8f5-1061-4ae6-903b-cfb327a50465",
        "title": "マイナポータルを騙った詐欺メール・偽サイトへの注意喚起",
        "organization": "デジタル庁",
        "claim": "不審なメールでは暗証番号などの個人情報を入力しないよう案内していることを確認。",
    },
    {
        "source_id": "SRC-015",
        "url": "https://services.digital.go.jp/mynaapp/",
        "title": "マイナポータル（Web）の継続利用に関する相互参照",
        "organization": "デジタル庁",
        "claim": "公式サービスサイト等で、マイナポータルWebは変わらず利用できることを確認。",
        "verification_note": "myna.go.jp本体はWAFで自動取得できなかったため、関連する公式ページの記述を相互参照。",
    },
]


SECTION_LABELS = {
    1: "はじめに", 2: "はじめに", 3: "はじめに",
    4: "1 / 5 マイナアプリとは何か", 5: "1 / 5 マイナアプリとは何か", 6: "1 / 5 マイナアプリとは何か",
    7: "2 / 5 何が変わったのか", 8: "2 / 5 何が変わったのか", 9: "2 / 5 何が変わったのか",
    10: "2 / 5 何が変わったのか", 11: "2 / 5 何が変わったのか", 12: "2 / 5 何が変わったのか",
    13: "3 / 5 すでに使っていた人は？", 14: "3 / 5 すでに使っていた人は？", 15: "3 / 5 すでに使っていた人は？",
    16: "3 / 5 すでに使っていた人は？", 17: "3 / 5 すでに使っていた人は？", 18: "3 / 5 すでに使っていた人は？",
    19: "3 / 5 すでに使っていた人は？",
    20: "4 / 5 新しく使う人・開けない人", 21: "4 / 5 新しく使う人・開けない人", 22: "4 / 5 新しく使う人・開けない人",
    23: "4 / 5 新しく使う人・開けない人", 24: "4 / 5 新しく使う人・開けない人", 25: "4 / 5 新しく使う人・開けない人",
    26: "5 / 5 本物の確認ポイント", 27: "5 / 5 本物の確認ポイント", 28: "5 / 5 本物の確認ポイント",
    29: "5 / 5 本物の確認ポイント", 30: "5 / 5 本物の確認ポイント", 31: "5 / 5 本物の確認ポイント",
    32: "まとめ", 33: "まとめ", 34: "まとめ", 35: "まとめ",
}


SCENE_COPY: dict[int, dict[str, Any]] = {
    1: {"layout": "layout_03_visual_text", "headline": "8月25日から「マイナアプリ」", "support_text": "名前とアイコンが変わります", "main_message": "マイナポータルアプリは、マイナアプリになりました。"},
    2: {"layout": "layout_06_caution", "headline": "マイナポータルは、なくなりません", "support_text": "アプリを消して、入れ直す必要はありません", "main_message": "サービスそのものは、引き続き使えます。"},
    3: {"layout": "layout_02_list", "headline": "今日は5つのことを確認", "support_text": "変更点と、今やることを順番に見ていきます", "main_message": "5項目の一覧", "items": ["マイナアプリとは何か", "何が変わったのか", "すでに使っていた人は？", "新しく使う人・開けない人", "本物の確認ポイント"]},
    4: {"layout": "layout_03_visual_text", "headline": "同じアプリの、新しい名前", "support_text": "マイナポータルアプリのアップデート版です", "main_message": "名前を変えたアプリです。"},
    5: {"layout": "layout_04_text_official", "headline": "認証は、本人確認", "support_text": "デジタル認証アプリの機能も統合されました", "main_message": "マイナンバーカードで本人であることを確認する機能です。"},
    6: {"layout": "layout_05_compare", "headline": "2つのアプリを、1つに", "support_text": "行政と民間の本人確認をまとめます", "main_message": "マイナアプリひとつで使えるようになります。"},
    7: {"layout": "layout_08_section", "headline": "何が変わったのか", "support_text": "名前・アイコン・ログインや認証のアプリが変わります", "main_message": "2 / 5の確認ポイント"},
    8: {"layout": "layout_05_compare", "headline": "アイコンも変わりました", "support_text": "期間限定のデザインもあります", "main_message": "公式素材の新旧アイコンを比較します。"},
    9: {"layout": "layout_04_text_official", "headline": "ログインや認証も、1つに", "support_text": "デジタル認証アプリは単体提供が終了しました", "main_message": "機能はマイナアプリで引き続き使えます。"},
    10: {"layout": "layout_05_compare", "headline": "マイナポータルは、なくなりません", "support_text": "変わるのは、スマホアプリの名前とログイン方法", "main_message": "サービスとアプリを分けて考えると安心です。"},
    11: {"layout": "layout_01_hero", "headline": "マイナポータルは、行政の窓口", "support_text": "ウェブサイトは、今までどおり使えます", "main_message": "医療費の確認や各種申請も対象です。"},
    12: {"layout": "layout_03_visual_text", "headline": "ログインの役割が、バトンタッチ", "support_text": "マイナポータルアプリから、マイナアプリへ", "main_message": "概念図で、役割の移り変わりを確認します。"},
    13: {"layout": "layout_04_text_official", "headline": "まず、今のアプリを確認", "support_text": "名前・アイコン・ストアの情報", "main_message": "すでに使っている人は、最初に表示を確認します。"},
    14: {"layout": "layout_04_text_official", "headline": "アップデートするだけでOK", "support_text": "自動更新の設定によっては、そのまま更新されます", "main_message": "削除して入れ直す必要はありません。"},
    15: {"layout": "layout_04_text_official", "headline": "自分で更新する場合", "support_text": "App StoreやGoogle Playで公式の掲載情報を確認", "main_message": "アプリ名と提供元を見てから更新します。"},
    16: {"layout": "layout_02_list", "headline": "設定とデータは、引き継がれます", "support_text": "再登録は不要。ただし一部の手続きはマイナアプリが必要です", "main_message": "アップデート後の確認", "items": ["スマホのマイナンバーカード設定", "これまでの機能・データ", "再登録は不要", "一部の手続きではマイナアプリが必要"]},
    17: {"layout": "layout_06_caution", "headline": "削除・入れ直しは、まず待って", "support_text": "分からないときは、公式FAQを確認", "main_message": "慌ててアプリを消す前に、案内を確認します。"},
    18: {"layout": "layout_05_compare", "headline": "後から入れたアプリが、優先されます", "support_text": "入れ直しの前に、仕組みを確認", "main_message": "インストールの順番で、開くアプリが決まる場合があります。"},
    19: {"layout": "layout_06_caution", "headline": "困ったら、まず確認", "support_text": "公式FAQと概要欄の公式ページ", "main_message": "削除ではなく、公式の案内を見ます。"},
    20: {"layout": "layout_08_section", "headline": "まず、動作環境を確認", "support_text": "4 / 5 新しく使う人・開けない人", "main_message": "端末の条件から確認します。"},
    21: {"layout": "layout_04_text_official", "headline": "対応OSとNFCを確認", "support_text": "iPhoneはiOS 16.4以上／Androidは11以降＋NFC", "main_message": "NFCはカードをかざして読み取る機能です。"},
    22: {"layout": "layout_04_text_official", "headline": "初回だけ「利用登録」", "support_text": "カードと数字4桁の暗証番号を用意", "main_message": "スマホ内のカードなら顔・指紋で認証できます。"},
    23: {"layout": "layout_06_caution", "headline": "端末のロック設定が必須", "support_text": "PIN・顔認証・指紋認証", "main_message": "ロック未設定ではマイナアプリを使えません。"},
    24: {"layout": "layout_02_list", "headline": "ログインできないとき", "support_text": "まず通常モードに戻して、再起動して再確認", "main_message": "公式FAQにある確認手順", "items": ["プライベートブラウズをやめる", "シークレットモードをやめる", "通常モードで端末を再起動", "もう一度試す"]},
    25: {"layout": "layout_06_caution", "headline": "個人情報の操作は、ご自身のスマホで", "support_text": "カード読み取り・暗証番号入力は実演しません", "main_message": "画面の案内に沿って、落ち着いて進めてください。"},
    26: {"layout": "layout_08_section", "headline": "本物は、2つのストアから", "support_text": "App StoreまたはGoogle Play", "main_message": "5 / 5 本物の確認ポイント"},
    27: {"layout": "layout_05_compare", "headline": "提供元を確認", "support_text": "Digital Agency of Japan ／ デジタル庁", "main_message": "ストアの掲載情報を公式画面で確認します。"},
    28: {"layout": "layout_03_visual_text", "headline": "アイコンのデザインを確認", "support_text": "ピンクのグラデーション・「マイナ」・桜", "main_message": "実際の公式素材を表示します。"},
    29: {"layout": "layout_06_caution", "headline": "偽サイト・偽アプリに注意", "support_text": "メールや電話の案内は、まず疑う", "main_message": "公式ストア以外からインストールしないようにします。"},
    30: {"layout": "layout_06_caution", "headline": "暗証番号を入力・回答しない", "support_text": "不審な連絡から操作しない", "main_message": "デジタル庁の注意喚起を確認します。"},
    31: {"layout": "layout_06_caution", "headline": "心配なときの相談窓口", "support_text": "マイナンバー総合フリーダイヤル 0120-95-0178", "main_message": "一人で判断せず、確認する方法もあります。"},
    32: {"layout": "layout_07_summary", "headline": "今やることは、3つ", "support_text": "まずは名前・提供元・アイコン", "main_message": "まとめの1つ目", "items": ["本物かどうかを確認する", "名前・提供元・アイコンを見る", "公式ストアの掲載情報を確認"]},
    33: {"layout": "layout_07_summary", "headline": "アップデートと利用登録を確認", "support_text": "削除せず更新／カード・暗証番号・端末ロック", "main_message": "まとめの2つ目と3つ目", "items": ["マイナポータルアプリなら削除せずアップデート", "利用登録ならカードと数字4桁を用意", "端末のロック設定を確認"]},
    34: {"layout": "layout_01_hero", "headline": "慌てて消す前に、まず確認", "support_text": "役に立ったらチャンネル登録を", "main_message": "怖がらせる前に、確認する。"},
    35: {"layout": "layout_01_hero", "headline": "概要欄の公式ページを確認", "support_text": "分からないことはコメントで教えてください", "main_message": "今回確認した公式情報を概要欄に載せています。"},
}


def image_asset(filename: str, label: str) -> dict[str, Any]:
    folder = "browser/" if filename.startswith("br_") else ""
    return {"kind": "image", "path": f"assets/official/{folder}{filename}", "label": label}


def quote_asset(text: str, source: str, label: str = "公式FAQ") -> dict[str, Any]:
    return {"kind": "quote", "text": text, "source": source, "label": label}


def crop(asset_index: int, box: list[int] | None = None, slot: str = "right", fit: str = "contain", note: str = "") -> dict[str, Any]:
    value: dict[str, Any] = {"asset_index": asset_index, "slot": slot, "fit": fit}
    if box is not None:
        value["box"] = box
    if note:
        value["note"] = note
    return value


def official_assets(scene_id: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    faq = "https://support.mynaapp.digital.go.jp/hc/ja"
    if scene_id == 1:
        return [image_asset("official_icon_rounded_3x.png", "公式アイコン")], []
    if scene_id == 5:
        return [image_asset("official_screen_card.png", "公式カード読み取り画面")], []
    if scene_id == 8:
        return [
            image_asset("official_icon_rounded_3x.png", "新アイコン"),
            image_asset("official_icon_limited_3x.png", "期間限定アイコン"),
        ], []
    if scene_id == 9:
        return [image_asset("br_03_news_20260825.png", "デジタル庁のお知らせ")], [crop(0, [143, 240, 1297, 760])]
    if scene_id == 10:
        return [image_asset("br_02_svc_top_faq.png", "公式サービスサイトFAQ")], [
            crop(0, [0, 5300, 1440, 5680], "left"),
            crop(0, [0, 5680, 1440, 6080], "right"),
        ]
    if scene_id == 13:
        return [image_asset("br_09_gplay.png", "Google Play公式掲載")], [crop(0, [80, 100, 1240, 560])]
    if scene_id == 14:
        return [quote_asset("App StoreやGoogle Playの自動更新設定をご利用の場合は、自動的に更新される場合があります。自動更新を利用していない場合は、ご自身でアップデートをお願いします。", faq, "公式FAQ・自動更新")], []
    if scene_id == 15:
        return [image_asset("br_09_gplay.png", "Google Play公式掲載")], [crop(0, [80, 100, 1240, 560])]
    if scene_id == 17:
        return [quote_asset("Q. アプリを入れ直したら、マイナアプリが開かなくなりました。", faq, "公式FAQ・質問")], []
    if scene_id == 18:
        return [quote_asset("A. 後からインストールしたアプリが優先して開く仕組みになっています。マイナアプリを優先したい場合は、マイナアプリをデジタル認証アプリより後にインストールし直すか、デジタル認証アプリをアンインストールします。", faq, "公式FAQ・回答")], []
    if scene_id == 21:
        return [image_asset("br_06_sysreq.png", "公式・動作環境")], [crop(0, [0, 300, 1440, 1150])]
    if scene_id == 22:
        return [
            image_asset("official_screen_register_card_auth.png", "公式・カード認証"),
            image_asset("official_screen_register_biometric.png", "公式・顔・指紋認証"),
        ], []
    if scene_id == 23:
        return [
            image_asset("official_screen_register_device_lock.png", "公式・端末ロック"),
            image_asset("br_06_sysreq.png", "公式・端末ロック案内"),
        ], [crop(1, [0, 1500, 1440, 2350], "right", "contain")]
    if scene_id == 27:
        return [
            image_asset("br_08_appstore.png", "App Store公式掲載"),
            image_asset("br_09_gplay.png", "Google Play公式掲載"),
        ], [crop(0, [250, 60, 1440, 620], "left"), crop(1, [80, 100, 1240, 560], "right")]
    if scene_id == 28:
        return [image_asset("official_icon_rounded_3x.png", "公式アイコン")], []
    if scene_id == 29:
        return [image_asset("br_10_notice_fakeapp.png", "デジタル庁・偽アプリ注意")], [crop(0, [0, 380, 1440, 1000])]
    if scene_id == 30:
        return [image_asset("br_11_notice_phishing.png", "デジタル庁・フィッシング注意")], [crop(0, [0, 400, 1440, 1150])]
    if scene_id == 31:
        return [image_asset("br_10_notice_fakeapp.png", "公式・相談窓口")], [crop(0, [0, 1000, 1440, 1600])]
    return [], []


def parse_subtitles(path: Path) -> list[dict[str, Any]]:
    subtitles: list[dict[str, Any]] = []
    pattern = re.compile(r"^\|\s*(SUB-\d+)\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*\d+\s*\|")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if not match:
            continue
        subtitle_id, segment_id, display = match.groups()
        display = display.replace(chr(96), "").replace(r"\N", "\n")
        lines = [part.strip() for part in display.splitlines() if part.strip()]
        subtitles.append({"id": subtitle_id, "text_lines": lines, "segment_id": int(segment_id)})
    return subtitles


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def make_episode(output: Path) -> dict[str, Any]:
    timeline_rows = parse_csv(EPISODE_DIR / "timeline_plan.csv")
    segment_rows = parse_csv(EPISODE_DIR / "audio" / "voicevox_kenzaki" / "segments_manifest.csv")
    subtitles = parse_subtitles(EPISODE_DIR / "subtitle_plan.md")
    subtitles_by_segment: dict[int, list[str]] = {}
    for subtitle in subtitles:
        subtitles_by_segment.setdefault(subtitle["segment_id"], []).append(subtitle["id"])

    scenes: list[dict[str, Any]] = []
    scene_by_segment: dict[int, int] = {}
    for row in timeline_rows:
        scene_id = int(row["scene_id"].split("-")[-1])
        start_segment = int(row["narration_segment_start"])
        end_segment = int(row["narration_segment_end"])
        for segment_id in range(start_segment, end_segment + 1):
            scene_by_segment[segment_id] = scene_id
        copy = SCENE_COPY[scene_id]
        assets, crops = official_assets(scene_id)
        scene = {
            "id": scene_id,
            "legacy_id": row["scene_id"],
            "layout": copy["layout"],
            "section_label": SECTION_LABELS[scene_id],
            "main_message": copy["main_message"],
            "headline": copy["headline"],
            "support_text": copy["support_text"],
            "official_asset": assets,
            "official_asset_crop": crops,
            "animation": row["transition"],
            "start_segment": start_segment,
            "end_segment": end_segment,
            "subtitle_ids": [value for value in row["subtitle_ids"].split(";") if value],
            "image_filename": row["image_filename"],
            "visual_type": row["visual_type"],
            "legacy_official_asset": row["official_asset"],
            "legacy_notes": row["notes"],
            "timing": {
                "start_sec": float(row["start"]),
                "end_sec": float(row["end"]),
                "duration_sec": round(float(row["end"]) - float(row["start"]), 3),
            },
        }
        if "items" in copy:
            scene["items"] = copy["items"]
        scenes.append(scene)

    reading_overrides = {
        1: {"方": "かた"},
        45: {"後から": "あとから"},
        47: {"開けない": "ひらけない"},
    }
    segments: list[dict[str, Any]] = []
    for row in segment_rows:
        segment_id = int(row["segment_id"])
        pad = float(row["pad_after_sec"]) if row.get("pad_after_sec") else 0.0
        segments.append(
            {
                "id": segment_id,
                "section": row["section"],
                "narration": row["text"],
                "reading_overrides": reading_overrides.get(segment_id, {}),
                "pause_after": pad,
                "scene_id": scene_by_segment.get(segment_id),
                "subtitle_ids": subtitles_by_segment.get(segment_id, []),
                "shot_id": row.get("shot") or None,
                "section_start": row.get("section_start") == "yes",
                "audio_path": f"audio/voicevox_kenzaki/{row['wav_path']}",
                "duration_sec": float(row["duration_sec"]),
                "start_sec": float(row["start_sec"]),
                "end_sec": float(row["end_sec"]),
                "audio_status": row.get("status", ""),
                "audio_notes": row.get("notes", ""),
            }
        )

    publish = json.loads((EPISODE_DIR / "publish.json").read_text(encoding="utf-8"))
    title = publish["selected_title"]
    target_duration = max(float(row["end_sec"]) for row in segment_rows)
    episode = {
        "schema_version": "1.0.0",
        "episode": {
            "episode_id": "002",
            "slug": "myna_app",
            "title": title,
            "target_duration": round(target_duration, 3),
            "status": "publish_ready",
            "topic": "マイナポータルアプリからマイナアプリへの変更",
            "target_audience": "スマホのアプリ名・アイコン変更に戸惑う50〜70代とその家族",
        },
        "sources": [{**source, "verified_at": "2026-08-30"} for source in SOURCES],
        "narration_segments": segments,
        "subtitles": subtitles,
        "scenes": scenes,
        "publish": {
            "title": title,
            "description": publish["description"],
            "chapters": publish["chapters"],
            "voice_credit": publish["credit"],
            "title_candidates": publish.get("title_candidates", []),
            "tags": publish.get("tags", []),
            "source_urls": publish.get("source_urls", []),
            "visibility": publish.get("visibility", "private"),
        },
        "timeline": {
            "fps": 30,
            "total_duration_sec": round(target_duration, 3),
            "source_file": "timeline_plan.csv",
            "audio_manifest": "audio/voicevox_kenzaki/segments_manifest.csv",
            "scene_count": len(scenes),
            "narration_segment_count": len(segments),
            "subtitle_count": len(subtitles),
        },
        "migration": {
            "source_files": [
                "script.md",
                "scene_plan.md",
                "subtitle_plan.md",
                "timeline_plan.csv",
                "audio/voicevox_kenzaki/segments_manifest.csv",
                "publish.json",
            ],
            "note": "Episode 002の既存動画・音声・完成画像は再生成していない。",
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(episode, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return episode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", type=Path, default=EPISODE_DIR / "episode.json")
    args = parser.parse_args()
    data = make_episode(args.output.resolve())
    print(f"wrote {args.output.resolve()}")
    print(
        f"segments={len(data['narration_segments'])} subtitles={len(data['subtitles'])} "
        f"scenes={len(data['scenes'])} duration={data['episode']['target_duration']:.3f}s"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
