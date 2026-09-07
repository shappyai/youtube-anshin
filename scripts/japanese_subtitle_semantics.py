"""Permanent semantic line-break policy for Japanese subtitles.

The channel's subtitles are written for viewers in their 50s–70s.  A line
break is therefore selected in this order: sentence/clause meaning, bunsetsu
integrity, modifier relation, and only then visual balance.  Character-count
splitting is deliberately not used as a primary rule.

This module is intentionally dependency-light.  The production runtime does
not guarantee a Japanese morphological analyser, so the boundary recogniser
uses a maintained set of protected terms plus conservative Japanese grammar
patterns.  It is shared by the generator and the preflight checker so that a
cue cannot pass a different definition of a natural boundary than the one
used to generate it.
"""
from __future__ import annotations

import re
import unicodedata
from typing import Any, Iterable

MAX_LINES = 2
MAX_WIDTH = 1800
TARGET_CHARS = 34

FORBIDDEN_START = set("、。，．・：；！？％）」』】〕〉｝＞ー…ゃゅょぁぃぅぇぉっャュョァィゥェォッ")
FORBIDDEN_END = set("（「『【〔〈｛＜")
STRONG_PUNCTUATION = set("。！？!?")
SOFT_PUNCTUATION = set("、，；：;:」』）)]】〉》…")

# Existing protected names and the short compounds used by Episode 012.  A
# protected term may contain a line break only at its outer edge.
PROTECTED_TERMS: tuple[str, ...] = (
    "マイナアプリ",
    "マイナポータルアプリ",
    "デジタル認証アプリ",
    "マイナンバーカード",
    "利用者証明用暗証番号",
    "Digital Agency of Japan",
    "App Store",
    "Google",
    "Googleフォト",
    "Googleアカウント",
    "Google ドライブ",
    "バックアップ",
    "バックアップ済み",
    "未バックアップ",
    "標準バックアップ",
    "自動バックアップ",
    "プレミアムバックアップ",
    "バックアップ・引き継ぎ",
    "バックアップ用の暗証番号",
    "バックアップ用のPINコード",
    "PINコード",
    "トーク履歴",
    "トークのバックアップ",
    "今すぐバックアップ",
    "メイン端末",
    "引き継ぎガイド",
    "iCloud Drive",
    "LYPプレミアム",
    "セーフティネット",
    "空き容量を増やす",
    "デバイスから削除",
    "最近削除した項目",
    "Google Play",
    "iPhone",
    "iPhoneなどでは",
    "Android",
    "YouTube",
    "LINE",
    "NFC",
    "0120-95-0178",
    # Episode 012 compounds.  These are display terms, not official UI
    # reconstructions; keeping them whole makes the subtitle meaning stable.
    "公式アプリ",
    "公式サイト",
    "公式窓口",
    "公式情報",
    "支払い情報",
    "支払い情報を更新してください",
    "カード会社",
    "カード番号",
    "カード明細",
    "利用確認",
    "再配達",
    "不在票",
    "不正アプリ",
    "個人情報",
    "カード情報",
    "利用停止",
    "登録情報",
    "相談先",
    "相談例",
    "IDとパスワード",
    "不正利用の可能性があります",
    "約20万円の利用を知らせる",
    "届け物を待っている気持ち",
    "安全と決めない",
    "公式サイトにある案内",
    "正規サイトで真偽を確認",
    "公的なお知らせ",
    "お知らせ",
    "検索を経由して正規サイト",
    "会社によって",
    "画面にIDやパスワード",
    "確認ページ",
    "誘導される手口",
    "入力した場合",
    "同じ内容があるか",
    "国民生活センター",
    "フィッシング対策協議会",
    "消費者庁",
    "国税庁",
    "宅配便",
    "ネットショッピング",
    "普段使っている",
    "普段利用している",
    "届け物",
    "本物かどうか",
    "本物らしく",
    "本物そっくり",
    "見分けなくて",
    "今日中に",
    "e-Tax",
    "SMS",
    "メール",
    "アカウント",
    "パスワード",
    "ファイル",
    "確認手順",
    "チャンネル登録",
)

PARTICLES = (
    "から", "まで", "だけ", "ほど", "しか", "ので", "のに", "にも", "では",
    "とは", "には", "へは", "では", "は", "が", "を", "に", "へ", "で",
    "と", "も", "や", "ね", "よ", "よって",
)

# A discourse marker or topic-only prefix is not a useful visual line by
# itself.  These boundaries remain semantically valid in prose, but are
# deliberately excluded from subtitle wrapping so ``ただし、`` or
# ``日本郵便は、`` cannot become a stranded first line.
SHORT_PREFIX_BOUNDARIES = (
    "ただし、", "1つ目、", "2つ目、", "3つ目、", "日本郵便は、", "迷う場合は",
)

# These are phrase endings that can close a bunsetsu.  The list intentionally
# excludes bare stems such as "しま" or "なり"; they are handled as blocked
# in known inflection units below, never as safe boundaries.
AUXILIARY_ENDINGS = (
    "してください", "しておいてください", "していません", "しています", "している",
    "されます", "される", "されて", "ありました", "ありません", "あります",
    "なりました", "なります", "できます", "できる", "ください", "しました",
    "します", "でした", "でしょう", "ません", "ます", "ない", "なくて",
    "ました", "です", "いる", "ある", "なる", "した", "する", "したら",
    "すれば", "して", "しても", "された", "されている", "開いて", "使って", "よう",
)

# A boundary inside any of these spans is a word/conjugation split.  The
# longest items are checked first, so e.g. あり|ます is caught by あります.
INFLECTION_UNITS = (
    "しておいてください", "していません", "しています", "されている", "されます",
    "される", "ありました", "ありません", "あります", "なりました", "なります",
    "できます", "できる", "ください", "しました", "します", "でした", "です", "でしょう",
    "ません", "ました", "ます", "ない", "なくて", "いる", "ある", "なる",
    "したら", "すれば", "しても", "された", "されて", "して", "した", "する",
    "開いて", "使って", "見分ける", "決めない", "届いた", "届く", "届ける",
    "届けられませんでした", "届きませんでした", "届かない", "確認してください",
    "つながる", "よう", "盗む", "違う", "入力した場合",
    "勧め", "勧める", "勧めています",
)

# A line beginning with one of these is almost always showing an orphaned
# particle or auxiliary.  Long forms must be listed before their prefixes.
ORPHAN_STARTS = (
    "ありません", "あります", "なりません", "なります", "できます", "できる",
    "ありませんでした", "ません", "ました", "ます", "でした", "です", "でしょう", "ください",
    "しています", "している", "してください", "して", "した", "する", "され", "いる", "ある", "なる", "ない",
    "なく", "られる", "れる", "れば", "たら", "か", "から", "まで", "だけ", "ほど",
    "しか", "ので", "のに", "には", "にも", "では", "とは", "の", "は", "が", "を",
    "に", "へ", "で", "と", "も", "や", "ね", "よ", "て",
    "あれば",
)

STEM_ENDINGS = (
    "確認しま", "案内しま", "急がされ", "なりま", "されま", "できま", "してい",
    "使え", "開き", "届い", "書かれ", "決め", "進め", "見分け", "思い", "あり",
    "い", "し",
)

_PROTECTED_SORTED = tuple(sorted(PROTECTED_TERMS, key=len, reverse=True))
_PARTICLES_SORTED = tuple(sorted(PARTICLES, key=len, reverse=True))
_AUXILIARY_SORTED = tuple(sorted(AUXILIARY_ENDINGS, key=len, reverse=True))
_INFLECTION_SORTED = tuple(sorted(INFLECTION_UNITS, key=len, reverse=True))
_ORPHAN_SORTED = tuple(sorted(ORPHAN_STARTS, key=len, reverse=True))


def clean(text: str) -> str:
    """Remove layout whitespace for semantic comparisons."""
    return re.sub(r"\s+", "", str(text or ""))


def _is_kanji(char: str) -> bool:
    return bool(char) and ("\u3400" <= char <= "\u9fff" or "\uf900" <= char <= "\ufaff")


def _is_hiragana(char: str) -> bool:
    return bool(char) and "\u3040" <= char <= "\u309f"


def _is_katakana(char: str) -> bool:
    return bool(char) and ("\u30a0" <= char <= "\u30ff" or "\u31f0" <= char <= "\u31ff")


def _is_ascii_word(char: str) -> bool:
    return bool(char) and (char.isascii() and (char.isalnum() or char in "-_./#%"))


def _matches_at(text: str, index: int, terms: Iterable[str]) -> list[str]:
    return [term for term in terms if text.startswith(term, index)]


def protected_boundary(text: str, end: int) -> bool:
    """Return True when ``end`` falls inside a protected display term."""
    for term in _PROTECTED_SORTED:
        start = text.find(term)
        while start >= 0:
            if start < end < start + len(term):
                return True
            start = text.find(term, start + 1)
    return False


def _inflection_boundary(text: str, end: int) -> bool:
    for term in _INFLECTION_SORTED:
        start = text.find(term)
        while start >= 0:
            if start < end < start + len(term):
                return True
            start = text.find(term, start + 1)
    return False


def _particle_end(text: str, end: int) -> str | None:
    """Return the particle ending at ``end`` when it is a plausible edge."""
    if end <= 0:
        return None
    for particle in _PARTICLES_SORTED:
        start = end - len(particle)
        if start < 1 or text[start:end] != particle:
            continue
        if particle == "や":
            # や is a list connector.  Breaking immediately after it leaves
            # the following item visually unattached (画面や／通知).
            continue
        # Keep the recogniser broad.  Lexical false positives are rejected by
        # the orphan and modifier checks below; broad recognition is needed
        # for edges such as だけで／安全.
        previous = text[start - 1]
        if _is_kanji(previous) or _is_katakana(previous) or _is_ascii_word(previous) or _is_hiragana(previous):
            return particle
        if len(particle) >= 2:
            return particle
    return None


def _starts_predicate(text: str, end: int) -> bool:
    """Conservative verb/predicate starts for the maintained cue lexicon."""
    starts = (
        "更新", "知らせ", "届く", "届き", "届け", "連絡", "確認", "開き", "開く", "進み", "進む",
        "つなが", "誘導", "電話", "説明", "見分け", "違う",
        "装う", "決め", "思い", "行い", "受け", "探し", "応じ", "入力", "変更", "削除",
        "避け", "求め", "当て", "選び", "変え", "相談", "利用", "盗む", "伝え", "あれば",
        "あります", "ありません", "なります", "できます", "します",
    )
    return any(text.startswith(start, end) for start in starts)


def _auxiliary_end(text: str, end: int) -> str | None:
    if end <= 0:
        return None
    for ending in _AUXILIARY_SORTED:
        start = end - len(ending)
        if start < 1 or text[start:end] != ending:
            continue
        if _inflection_boundary(text, end - 1):
            # This is only a guard for an overlapping unit; the full ending
            # remains a valid edge.
            pass
        return ending
    return None


def _script_transition(previous: str, following: str) -> bool:
    if not previous or not following:
        return False
    if _is_ascii_word(previous) != _is_ascii_word(following):
        return True
    if _is_kanji(previous) != _is_kanji(following):
        return True
    if _is_katakana(previous) != _is_katakana(following):
        return True
    return False


def boundary_issues(text: str, end: int) -> dict[str, bool]:
    """Classify one potential Japanese line/cue boundary.

    The returned keys are the permanent QA counters requested by the channel.
    ``unnatural_japanese_line_break`` is the aggregate semantic failure.
    """
    value = clean(text)
    if end <= 0 or end >= len(value):
        return {
            "unnatural_japanese_line_break": False,
            "word_split": False,
            "conjugation_split": False,
            "particle_or_auxiliary_orphan": False,
        }
    previous = value[end - 1]
    following = value[end]
    word_split = protected_boundary(value, end)
    if _is_ascii_word(previous) and _is_ascii_word(following):
        word_split = True
    if _is_kanji(previous) and _is_kanji(following):
        # A kanji-to-kanji cut is only allowed after a recognised particle or
        # punctuation.  Otherwise it is almost always a compound split such
        # as 更／新 or 公／式.
        if _particle_end(value, end) is None:
            word_split = True
    if _is_katakana(previous) and _is_katakana(following):
        word_split = True

    conjugation_split = _inflection_boundary(value, end)
    right_orphan = any(value.startswith(start, end) for start in _ORPHAN_SORTED)
    if previous in STRONG_PUNCTUATION:
        # A new cue after a complete sentence is a natural reading boundary,
        # even when the next sentence begins with a discourse marker such as
        # 「ですから」.  The marker is only orphaned when the preceding cue
        # did not already close the sentence.
        right_orphan = False
    if previous in "」』）)]】〉》" and value.startswith("と", end):
        # ``「…」というメール`` is a natural quoted-noun construction, not
        # an orphaned particle.  The closing quote already marks the edge.
        right_orphan = False
    # A line ending in an inflection stem and continuing with hiragana is not
    # a meaningful Japanese edge even when the exact unit was not in the
    # maintained list.
    if _is_hiragana(following) and any(value[:end].endswith(stem) for stem in STEM_ENDINGS):
        conjugation_split = True

    punctuation_edge = previous in FORBIDDEN_START or previous in STRONG_PUNCTUATION or previous in SOFT_PUNCTUATION
    particle_edge = _particle_end(value, end) is not None
    auxiliary_edge = _auxiliary_end(value, end) is not None
    # A particle attached to a substantial phrase may close the first visual
    # line when the predicate starts on the next line (for example,
    # ``手口を\n説明しています``).  The particle is not orphaned there: it
    # remains attached to the phrase on its left.  Actual orphan particles
    # are caught by ``right_orphan`` when the next line starts with the
    # particle itself, and modifier/compound checks still reject edges such
    # as ``公式サイトの\n案内`` or ``支払い情報を更\n新``.
    if particle_edge and _starts_predicate(value, end) and _particle_end(value, end) in {"へ", "て"}:
        right_orphan = True
    modifier_relation = value[:end].endswith(("の", "な")) and (
        _is_kanji(following) or _is_katakana(following) or _is_ascii_word(following)
    )
    if (_is_kanji(following) or _is_katakana(following)) and any(
        value[:end].endswith(ending)
        for ending in ("いる", "ある", "なる", "できる", "使って", "待っている", "見ている", "して", "知らせる", "届いた", "ない", "される", "装う", "盗む")
    ):
        # Keep a relative clause with the noun it modifies where possible.
        modifier_relation = True
    if _is_hiragana(previous) and _is_hiragana(following) and not (particle_edge or auxiliary_edge or punctuation_edge):
        word_split = True
    approved = punctuation_edge or particle_edge or auxiliary_edge or _script_transition(previous, following)
    short_prefix = clean(value[:end]) in SHORT_PREFIX_BOUNDARIES
    if previous == "や":
        # A list connector must stay with the item on its right.
        word_split = True
    unnatural = bool(word_split or conjugation_split or right_orphan or modifier_relation or short_prefix or not approved)
    return {
        "unnatural_japanese_line_break": unnatural,
        "word_split": word_split,
        "conjugation_split": conjugation_split,
        "particle_or_auxiliary_orphan": right_orphan,
    }


def boundary_kind(text: str, end: int) -> tuple[str, int] | None:
    """Return a semantic boundary kind and priority, or None if unsafe."""
    value = clean(text)
    if end <= 0 or end >= len(value):
        return ("end", 0) if end == len(value) else None
    previous = value[end - 1]
    following = value[end]
    if following in FORBIDDEN_START or previous in FORBIDDEN_END:
        return None
    issues = boundary_issues(value, end)
    if any(issues.values()):
        return None
    if previous in STRONG_PUNCTUATION:
        return ("sentence", 1000)
    if previous in SOFT_PUNCTUATION:
        return ("clause", 900)
    if _particle_end(value, end) is not None:
        return ("bunsetsu", 760)
    if _auxiliary_end(value, end) is not None:
        return ("predicate", 740)
    if _script_transition(previous, following):
        return ("token_edge", 420)
    return None


def semantic_boundaries(text: str, max_end: int | None = None) -> list[tuple[int, str, int]]:
    value = clean(text)
    limit = len(value) if max_end is None else min(len(value), max_end)
    result: list[tuple[int, str, int]] = []
    for end in range(1, limit + 1):
        kind = boundary_kind(value, end)
        if kind is not None:
            result.append((end, kind[0], kind[1]))
    return result


def _line_width(text: str, estimated_width: Any, font_px: float = 72.0) -> float:
    return float(estimated_width(text)) * font_px / 72.0


def wrap_lines(text: str, estimated_width: Any, max_width: int = MAX_WIDTH, font_px: float = 72.0) -> list[str]:
    """Wrap a single temporal cue only at approved semantic boundaries."""
    value = clean(text)
    if not value:
        return [""]
    if _line_width(value, estimated_width, font_px) <= max_width:
        return [value]
    candidates = [
        (end, kind, score)
        for end, kind, score in semantic_boundaries(value)
        if _line_width(value[:end], estimated_width, font_px) <= max_width
        and _line_width(value[end:], estimated_width, font_px) <= max_width
        and len(value[:end]) >= 4
        and len(value[end:]) >= 2
    ]
    if not candidates:
        return [value]
    remaining_width = _line_width(value, estimated_width, font_px)
    target_width = remaining_width / 2.0
    end, _kind, _score = max(
        candidates,
        key=lambda item: (
            item[2],
            -abs(_line_width(value[:item[0]], estimated_width, font_px) - target_width),
        ),
    )
    return [value[:end], value[end:]]


def split_display_text(
    text: str,
    estimated_width: Any,
    max_width: int = MAX_WIDTH,
    max_lines: int = MAX_LINES,
) -> list[str]:
    """Split long display text into temporal cues, preserving semantic edges."""

    def visual_balance_is_bad(lines: list[str]) -> bool:
        if len(lines) != 2:
            return False
        widths = [_line_width(line, estimated_width) for line in lines]
        return min(widths) / max(widths) < 0.35 and len(clean("".join(lines))) >= 10

    def temporal_boundary_for_balance(value: str) -> int | None:
        candidates = []
        for end, kind, score in semantic_boundaries(value):
            if end >= len(value) or len(value[:end]) < 4 or len(value[end:]) < 4:
                continue
            if _line_width(value[:end], estimated_width) > max_width:
                continue
            if _line_width(value[end:], estimated_width) > max_width:
                continue
            candidates.append((end, kind, score))
        if not candidates:
            return None
        total = _line_width(value, estimated_width)
        return max(
            candidates,
            key=lambda item: (
                item[2],
                -abs(_line_width(value[:item[0]], estimated_width) - total / 2.0),
            ),
        )[0]

    remaining = clean(text)
    chunks: list[str] = []
    while remaining:
        lines = wrap_lines(remaining, estimated_width, max_width)
        if len(lines) <= max_lines and all(
            _line_width(line, estimated_width) <= max_width for line in lines
        ):
            if visual_balance_is_bad(lines):
                end = temporal_boundary_for_balance(remaining)
                if end is not None:
                    chunks.append(remaining[:end].strip())
                    remaining = remaining[end:].lstrip()
                    continue
            chunks.append(remaining)
            break
        valid = [
            (end, kind, score)
            for end, kind, score in semantic_boundaries(remaining)
            if end < len(remaining)
            and _line_width(remaining[:end], estimated_width) <= max_width * max_lines
            and len(remaining[:end]) >= 8
        ]
        if not valid:
            raise ValueError(f"cannot find semantic subtitle boundary: {remaining}")
        # Sentence boundaries win.  Otherwise keep a clause/bunsetsu close to
        # the target length and leave enough material for the next cue.
        sentence = [item for item in valid if item[1] == "sentence"]
        if sentence:
            end, _kind, _score = min(sentence, key=lambda item: item[0])
        else:
            target = min(max(8, TARGET_CHARS), max(item[0] for item in valid))
            end, _kind, _score = max(
                valid,
                key=lambda item: (item[2], -abs(item[0] - target)),
            )
        chunk = remaining[:end].strip()
        if not chunk:
            raise ValueError(f"empty semantic subtitle chunk: {remaining}")
        chunks.append(chunk)
        remaining = remaining[end:].lstrip()
    return chunks


def inspect_subtitle_line_breaks(
    text_lines: list[str],
    cue_boundaries: Iterable[tuple[str, str, int]] = (),
) -> dict[str, list[str]]:
    """Inspect visual line breaks and temporal cue boundaries.

    ``cue_boundaries`` contains the full text before each boundary and is
    optional; the preflight passes it to scan both kinds of break.
    """
    issues: dict[str, list[str]] = {
        "unnatural_japanese_line_break": [],
        "word_split": [],
        "conjugation_split": [],
        "particle_or_auxiliary_orphan": [],
    }
    for index in range(len(text_lines) - 1):
        full = clean("".join(text_lines))
        end = len(clean("".join(text_lines[: index + 1])))
        result = boundary_issues(full, end)
        for key, failed in result.items():
            if failed:
                issues[key].append(f"line {index + 1}: {text_lines[index]} / {text_lines[index + 1]}")
    for label, full, end in cue_boundaries:
        result = boundary_issues(full, end)
        for key, failed in result.items():
            if failed:
                issues[key].append(f"{label}: {clean(full[:end])} / {clean(full[end:])}")
    return issues


def is_nfc(text: str) -> bool:
    """Small utility used by reports to keep display strings canonical."""
    return unicodedata.normalize("NFC", str(text)) == str(text)
