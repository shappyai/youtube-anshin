import re, sys
from pathlib import Path
sys.path.insert(0, 'episodes/001_google_security/work')
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
EP = Path('episodes/001_google_security')
HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Yu Gothic,72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,3,0,5,60,60,45,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
MAXW = 1780
W_JP, W_AS = 72.0, 36.0
FORBID_START = "、。，．」』）】〕〉》！？：；ぁぃぅぇぉゃゅょっー"
FORBID_END = "（「『〔【"
PARTICLE = "はがをにでとものからよりまで、。"
SUFFIXES = ["されています","されます","できます","あります","なります","います","ください","しましょう","します","ました","ません","ます","です","ないか","こと","もの","ので","から","ため","よう","場合"]

def est_w(t):
    return sum(W_JP if ord(c) > 0x2E7F or c in "（）「」・!?―" else W_AS for c in t)

def cands(text):
    out = []
    n = len(text)
    for p in range(1, n):
        if text[p] in FORBID_START: continue
        if text[p-1] in FORBID_END: continue
        if n - p < 2: continue
        ok = text[p-1] in PARTICLE
        if not ok:
            ok = any(text[:p].endswith(s) for s in SUFFIXES)
        if ok: out.append(p)
    return out

def wrap(text):
    if est_w(text) <= MAXW: return [text]
    best = None
    for p in cands(text):
        l1, l2 = text[:p], text[p:]
        w1, w2 = est_w(l1), est_w(l2)
        if w1 > MAXW or w2 > MAXW: continue
        sc = abs(w1 - w2)
        if best is None or sc < best[0]: best = (sc, l1, l2)
    if best: return [best[1], best[2]]
    return None

def split_point(text):
    half = est_w(text) / 2.0
    best = None
    for p in cands(text):
        if p < 4 or len(text) - p < 4: continue
        sc = abs(est_w(text[:p]) - half)
        if best is None or sc < best[0]: best = (sc, p)
    if best: return best[1]
    acc, cut = 0.0, max(1, len(text)//2)
    for i, ch in enumerate(text):
        if acc >= half:
            while cut < len(text) and text[cut] in FORBID_START: cut += 1
            break
        acc += W_JP if ord(ch) > 0x2E7F else W_AS
        cut = i
    return max(cut, 1)

def ts(sec):
    ms = int(round(sec * 100))
    return f"{ms // 360000}:{(ms % 360000) // 6000:02d}:{(ms % 6000) // 100:02d}.{ms % 100:02d}"

srt = (EP / "captions_v8.srt").read_text(encoding="utf-8")
blocks = re.split(r"\n\s*\n", srt.strip())
out = [HEADER]
n_split = 0
for b in blocks:
    lines = [l for l in b.splitlines() if l.strip()]
    if len(lines) < 3 or not lines[0].strip().isdigit(): continue
    m = re.match(r"(\d+):(\d+):(\d+),(\d+)\s*-->\s*(\d+):(\d+):(\d+),(\d+)", lines[1])
    if not m: continue
    def to_sec(g):
        h, mi, s, ms = map(int, g)
        return h * 3600 + mi * 60 + s + ms / 1000.0
    start, end = to_sec(m.groups()[:4]), to_sec(m.groups()[4:])
    text = "".join(lines[2:]).strip()
    dur = end - start
    w = wrap(text)
    if w:
        events = [(start, end, "\\N".join(w))]
    else:
        pos = split_point(text)
        if pos <= 0 or pos >= len(text):
            events = [(start, end, text)]
        else:
            l1 = text[:pos].rstrip("、。"); l2 = text[pos:].lstrip()
            w1 = est_w(l1)
            mid = start + dur * (w1 / (w1 + est_w(l2)))
            e1 = wrap(l1) or [l1]; e2 = wrap(l2) or [l2]
            events = [(start, mid, "\\N".join(e1)), (mid, end, "\\N".join(e2))]
            n_split += 1
    for st, en, t in events:
        if en <= st or not t: continue
        out.append(f"Dialogue: 0,{ts(st)},{ts(en)},Default,,0,0,45,,{{\\an5\\pos(960,980)}}{t}")
(EP / "captions_v8.ass").write_text("\n".join(out) + "\n", encoding="utf-8")
dlg = sum(1 for l in out if l.startswith("Dialogue:"))
print(f"captions_v8.ass: {dlg} cues / split={n_split} (62px, pos 960,990)")

