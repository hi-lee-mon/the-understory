# docs/44 §6 五十音順総索引の再生成（独立検証 findings 2/9/10/11/15 対応）
import re, unicodedata
from janome.tokenizer import Tokenizer

PATH = "docs/44_glossary.md"
doc = open(PATH).read()
lines = doc.splitlines(keepends=True)

tok = Tokenizer()

def kata2hira(s):
    return "".join(chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" else c for c in s)

def est_reading(term):
    """表層からの推定読み（ひらがな）。括弧・記号は除去。"""
    base = re.sub(r"[（(][^）)]*[）)]", "", term)
    base = re.sub(r"[`*\[\]【】〈〉《》「」『』〜〜-]", "", base).strip()
    out = []
    for t in tok.tokenize(base):
        r = t.reading
        if r == "*":
            r = t.surface
        out.append(kata2hira(r))
    return "".join(out)

# 推定読みの正典既知上書き（検証指摘＋正典ふりがな由来）
OVR = {
    "名づけられたごみ処理場": "なづけられたごみしょりば",  # ごみ処理場＝ごみしょりば（docs/23 §8.3）
    "端到端": "えんたんえん",
    "正本": "しょうほん",
    "正本節": "しょうほんせつ",
    "楽堂（きき手のいないホール）": "がくどう",
}

SMALL = "ぁぃぅぇぉっゃゅょゎ"
BIG = "あいうえおつやゆよわ"
SMALL2BIG = str.maketrans(SMALL, BIG)
VOWEL = {}
GYO_BASE = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん"
for ch in GYO_BASE:
    col = "あいうえお"[GYO_BASE.index(ch) % 5] if ch != "ん" else "ん"
    VOWEL[ch] = col

def seion(ch):
    """濁音・半濁音を清音化（NFDで゛゜を除去）"""
    return "".join(c for c in unicodedata.normalize("NFD", ch) if c not in "゙゚")

def sort_key(reading):
    """正規化読みのソートキー：清音化＋小書き→大書き＋長音は前字の母音に展開"""
    k = []
    for c in kata2hira(reading):
        c = seion(c)
        if c in SMALL:
            c = BIG[SMALL.index(c)]
        if c == "ー":
            k.append(VOWEL.get(k[-1], "") if k else "")
        elif c in "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん":
            k.append(c)
        else:
            k.append(c)  # 非仮名はそのまま（先頭のみ影響）
    return "".join(k)

GOJU_ORDER = ["あ", "い", "う", "え", "お", "か", "き", "く", "け", "こ",
              "さ", "し", "す", "せ", "そ", "た", "ち", "つ", "て", "と",
              "な", "に", "ぬ", "ね", "の", "は", "ひ", "ふ", "へ", "ほ",
              "ま", "み", "む", "め", "も", "や", "ゆ", "よ",
              "ら", "り", "る", "れ", "ろ", "わ", "を", "ん"]

def gyo_of(key):
    """ソートキーの行（清音行に併合）。非仮名は None"""
    if not key:
        return None
    c = key[0]
    return c if c in GOJU_ORDER else None

# --- 本文 §1〜§4 の行収集 ---
sec = None
mode = None  # "term" | "sys" | None
rows = []  # (term, reading_cell, note, own_sec, canon_sec, is_ref)
sec_re = re.compile(r"^#{2,4}\s*([\d]+(?:\.[\d]+)*(?:-[a-z])?)\s")

def is_sep_row(line):
    return line.startswith("|") and all(
        set(c.strip()) <= set("-") for c in line.strip().strip("|").split("|") if c.strip() != ""
    ) and "---" in line

for i, l in enumerate(lines[:1128]):
    m = sec_re.match(l)
    if m:
        sec = m.group(1)
        mode = None
        continue
    if not l.startswith("|"):
        continue
    if is_sep_row(l):
        continue
    cells = [c.strip() for c in l.strip().strip("|").split("|")]
    if not cells or cells[0] == "":
        continue
    # 次行が区切り行なら本行はヘッダ——認識したヘッダのみ mode を立て、他は None に戻す
    nxt = lines[i + 1] if i + 1 < len(lines) else ""
    if is_sep_row(nxt):
        mode = {"用語": "term", "体系": "sys"}.get(cells[0])
        continue
    if mode is None or sec is None:
        continue
    term = cells[0]
    if term.startswith("**") or not term:
        continue
    note = cells[-1]
    is_ref = "参照行——" in note
    canon_sec = sec
    if is_ref:
        mm = re.search(r"§(\d+(?:\.\d+)*(?:-[a-z])?)", note)
        if mm:
            canon_sec = mm.group(1)
    if mode == "term":
        reading = cells[1] if len(cells) > 1 else "—"
    else:
        reading = "—"
    rows.append((term, reading, note, sec, canon_sec, is_ref))

# --- 読み決定・行割当・ソート ---
# 参照行の解決後、同一用語×同一所在節では実体行を優先して重複を落とす
seen = {}
for term, reading, note, own, canon, is_ref in rows:
    loc = canon if is_ref else own
    rcell = reading
    if rcell in ("—", "（正典未記）", "", "（推定）"):
        est = OVR.get(term) or est_reading(term)
        disp = f"（推定：{est}）"
        key = sort_key(est)
    else:
        disp = rcell
        key = sort_key(rcell)
    k = (term, loc)
    if k in seen:
        # 実体行（非参照行）を優先、同格なら正典読みを持つ方を優先
        old = seen[k]
        if old[5] and not is_ref:
            seen[k] = (key, term, disp, canon, own, is_ref)
        elif old[5] == is_ref and "推定" in old[2] and "推定" not in disp:
            seen[k] = (key, term, disp, canon, own, is_ref)
    else:
        seen[k] = (key, term, disp, canon, own, is_ref)
items = list(seen.values())

buckets = {}
extra = []
for it in items:
    g = gyo_of(it[0])
    if g:
        buckets.setdefault(g, []).append(it)
    else:
        extra.append(it)

for g in buckets:
    buckets[g].sort(key=lambda x: (x[0], x[1]))
extra.sort(key=lambda x: (x[0], x[1]))

# --- §6 ブロック生成 ---
out = ["## 6. 五十音順総索引\n", "\n",
       "> 全収録語を五十音順に（P-GL-02）。主語行のみ収録——異表記・別称は各行の「異表記・備考」列で本文側へ誘導する。\n",
       "> 読み列が「（推定：…）」の行は表層からの推定読みで配列（暫定）。濁音・半濁音始まりの語は清音行へ併合して配列。参照行の所在節は語彙正本の実体節を指す。仮名以外で始まる語は末尾の「記号・英数」に集約。\n", "\n"]

total = 0
for g in GOJU_ORDER:
    if g not in buckets:
        continue
    out.append(f"### {g}行\n\n| 用語 | 読み | 所在節 |\n|---|---|---|\n")
    for key, term, disp, canon, own, is_ref in buckets[g]:
        loc = canon if is_ref else own
        out.append(f"| {term} | {disp} | §{loc} |\n")
        total += 1
    out.append("\n")
if extra:
    out.append("### 記号・英数\n\n| 用語 | 読み | 所在節 |\n|---|---|---|\n")
    for key, term, disp, canon, own, is_ref in extra:
        loc = canon if is_ref else own
        out.append(f"| {term} | {disp} | §{loc} |\n")
        total += 1
    out.append("\n")

new_sec6 = "".join(out).rstrip("\n") + "\n"

# --- splice ---
start = next(i for i, l in enumerate(lines) if l.startswith("## 6."))
end = next(i for i, l in enumerate(lines) if l.startswith("## 7."))
lines[start:end] = [new_sec6 + "\n"]
open(PATH, "w").write("".join(lines))
print(f"rows={len(rows)} indexed={total} extra={len(extra)}")
for g in GOJU_ORDER:
    if g in buckets:
        print(f"  {g}行: {len(buckets[g])}")
