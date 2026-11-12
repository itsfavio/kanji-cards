"""Rebuild data/ for Kanji Cards.

Usage (from the repo root):
    python scripts/build_data.py

The first run downloads its sources into .sources/ (kept out of git):
    JMdict_e.gz, kanjidic2.xml.gz     EDRDG, latest release (updated daily)
    accents.txt                       Kanjium, pinned commit (pitch accent)
    large_ja.msgpack.gz               wordfreq v3.2 (how often each word is used)
    graphicsJa*.txt, licenses         animCJK, pinned commit (Japanese stroke order)
Delete .sources/ (or one file in it) to download a newer copy.

Writes:
    data/dict.tsv          one line per JMdict entry (see the format note below)
    data/kanji.tsv         KANJIDIC2: readings and meanings of each kanji
    data/strokes/sNN.json  stroke data split by code point, and the chunk index (STARTS) in index.html
"""
import os, re, io, json, gzip, glob, shutil, struct, urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, ".sources")
DATA = os.path.join(ROOT, "data")
KANJIUM = "https://raw.githubusercontent.com/mifunetoshiro/kanjium/9ebca4589565c696e7c39e089e2e928ad65f678c/data/source_files/raw/"
ANIMCJK = "https://raw.githubusercontent.com/parsimonhi/animCJK/c63765b150cbd567c71d05cf4a4f8d00b57045c9/"
SOURCES = {
    "JMdict_e.gz": "http://ftp.edrdg.org/pub/Nihongo/JMdict_e.gz",
    "kanjidic2.xml.gz": "http://www.edrdg.org/kanjidic/kanjidic2.xml.gz",
    "accents.txt": KANJIUM + "accents.txt",
    "large_ja.msgpack.gz": "https://raw.githubusercontent.com/rspeer/wordfreq/42233e6c36ce792031bcccfa17cdd0cec9af5fa7/wordfreq/data/large_ja.msgpack.gz",
    "graphicsJa.txt": ANIMCJK + "graphicsJa.txt",
    "graphicsJaKana.txt": ANIMCJK + "graphicsJaKana.txt",
    "animcjk-APL.txt": ANIMCJK + "licenses/APL/english/ARPHICPL.TXT",
    "animcjk-LGPL.txt": ANIMCJK + "licenses/LGPL.txt",
    "animcjk-COPYING.txt": ANIMCJK + "licenses/COPYING.txt",
}

def src(name):
    path = os.path.join(SRC, name)
    if not os.path.exists(path):
        os.makedirs(SRC, exist_ok=True)
        print("downloading", SOURCES[name])
        req = urllib.request.Request(SOURCES[name], headers={"User-Agent": "kanji-cards-build"})
        with urllib.request.urlopen(req) as r, open(path + ".part", "wb") as fh:
            shutil.copyfileobj(r, fh)
        os.replace(path + ".part", path)
    return path

def read_text(name):
    path = src(name)
    if name.endswith(".gz"):
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            return fh.read()
    with open(path, encoding="utf-8") as fh:
        return fh.read()

def xml_root_iter(text, tag):
    # The EDRDG files declare their tags (&n; &v1; ...) as DTD entities. Keep the short codes instead of
    # expanding them, and drop the DTD so the standard parser doesn't need it.
    text = re.sub(r"<!DOCTYPE.*?\]>", "", text, count=1, flags=re.S)
    text = re.sub(r"&(?!(?:amp|lt|gt|quot|apos);)([\w-]+);", r"\1", text)
    for _, el in ET.iterparse(io.BytesIO(text.encode("utf-8")), events=("end",)):
        if el.tag == tag:
            yield el
            el.clear()

def to_hira(s):
    return "".join(chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" else c for c in s)

SMALL = set("ぁぃぅぇぉゃゅょゎゕゖァィゥェォャュョヮ")
def mora_count(kana):
    return sum(1 for c in kana if c not in SMALL)

# ---------------------------------------------------------------- pitch accent (Kanjium)
ACC = {}
for line in read_text("accents.txt").splitlines():
    p = line.split("\t")
    if len(p) < 3:
        continue
    word, reading, acc = p[0], p[1] or p[0], p[2]
    nums = []
    for n in re.findall(r"\d+", re.sub(r"\([^)]*\)", "", acc)):
        if n not in nums:
            nums.append(n)
    if nums:
        ACC.setdefault((word, to_hira(reading)), ",".join(nums))

def accent_for(forms, reading):
    m = mora_count(reading)
    for f in forms:
        a = ACC.get((f, to_hira(reading)))
        if a:
            ok = [n for n in a.split(",") if int(n) <= m]
            return ",".join(ok)
    return ""

# ---------------------------------------------------------------- word frequency
# wordfreq's list is msgpack: [header, bucket0, bucket1, ...], where bucket i holds the words whose frequency is
# 10^(-i/100); Zipf frequency = 9 - i/100 (about 7 for the most common words, 1 for very rare ones).
def msgpack_load(b):
    pos = 0
    def take(n):
        nonlocal pos
        pos += n
        return b[pos - n:pos]
    def obj():
        t = take(1)[0]
        if t <= 0x7f: return t
        if 0x80 <= t <= 0x8f: return {obj(): obj() for _ in range(t & 0x0f)}
        if 0x90 <= t <= 0x9f: return [obj() for _ in range(t & 0x0f)]
        if 0xa0 <= t <= 0xbf: return take(t & 0x1f).decode("utf-8")
        if t >= 0xe0: return t - 0x100
        if t == 0xc0: return None
        if t in (0xc2, 0xc3): return t == 0xc3
        if t in (0xd9, 0xda, 0xdb): return take(struct.unpack(">" + "BHI"[t - 0xd9], take(1 << (t - 0xd9)))[0]).decode("utf-8")
        if t in (0xdc, 0xdd): return [obj() for _ in range(struct.unpack(">" + "HI"[t - 0xdc], take(2 << (t - 0xdc)))[0])]
        if t in (0xde, 0xdf):
            n = struct.unpack(">" + "HI"[t - 0xde], take(2 << (t - 0xde)))[0]
            return {obj(): obj() for _ in range(n)}
        if t in (0xcc, 0xcd, 0xce, 0xcf): return struct.unpack(">" + "BHIQ"[t - 0xcc], take(1 << (t - 0xcc)))[0]
        if t in (0xd0, 0xd1, 0xd2, 0xd3): return struct.unpack(">" + "bhiq"[t - 0xd0], take(1 << (t - 0xd0)))[0]
        raise ValueError("unsupported msgpack type %x" % t)
    return obj()

ZIPF = {}
with gzip.open(src("large_ja.msgpack.gz"), "rb") as fh:
    buckets = msgpack_load(fh.read())[1:]
for i, words in enumerate(buckets):
    for w in words:
        ZIPF.setdefault(w, 9 - i / 100)

COMMON = {"news1", "ichi1", "spec1", "spec2", "gai1"}  # JMdict's own definition of a common word
def score(tags, text):
    """How common a spelling is: 100 if JMdict marks it common, plus 10 x its Zipf frequency from wordfreq
    (0-80). So common words always rank above uncommon ones, and by everyday frequency among themselves.
    (JMdict's newspaper bands alone rank 詠む above 書く, and 喫する above 食べる.)"""
    return (100 if COMMON & set(tags) else 0) + int(round(max(0.0, ZIPF.get(text, 0.0)) * 10))

# ---------------------------------------------------------------- JMdict
# dict.tsv, one line per entry (an entry whose senses differ by spelling is split over several lines):
#   K  kanji spellings, "|"-separated
#   R  readings, "|"-separated
#   D  meaning: senses "; "-separated, glosses within a sense ", "-separated, cut near 140 characters
#   P  part-of-speech codes of the first sense ("v5k,vt")
#   U  "u" when the word is usually written in kana alone
#   C  "+" when the line continues the previous line's entry (same word, other spellings)
# Each spelling is  [~]text[#accent][@restriction][*score]:
#   ~           irregular, outdated or rare: found when searched, but not shown by default
#   #accent     pitch accent: mora after which the pitch drops (0 = flat), "," between alternatives
#   @0,2 / @-   (readings) only for those kanji spellings / only in kana
#   *score      how common it is: 100+ = a common word (JMdict), plus 10 x Zipf frequency (see score())
def gloss_text(sense):
    out = ", ".join(g.replace(";", ",").strip() for g in sense["gloss"])
    return out

dict_lines = []
n_entries = 0
for e in xml_root_iter(read_text("JMdict_e.gz"), "entry"):
    kanji = []
    for k in e.findall("k_ele"):
        inf = [x.text for x in k.findall("ke_inf")]
        if "sK" in inf:
            continue
        text = k.findtext("keb")
        kanji.append({"t": text, "rare": any(x in inf for x in ("iK", "oK", "rK")),
                      "s": score([x.text for x in k.findall("ke_pri")], text)})
    kset = {k["t"] for k in kanji}
    readings = []
    for r in e.findall("r_ele"):
        inf = [x.text for x in r.findall("re_inf")]
        if "sk" in inf or "ok" in inf:
            continue
        text = r.findtext("reb")
        restr = [x.text for x in r.findall("re_restr")]
        if r.find("re_nokanji") is not None or not kanji:
            pairs_with = [None]
        elif restr:
            pairs_with = [k for k in restr if k in kset]
            if not pairs_with:
                continue
        else:
            pairs_with = [k["t"] for k in kanji]
        readings.append({"t": text, "rare": any(x in inf for x in ("ik", "rk")), "with": pairs_with,
                         "s": score([x.text for x in r.findall("re_pri")], text)})
    senses, last_pos = [], []
    for s in e.findall("sense"):
        pos = [x.text for x in s.findall("pos")] or last_pos  # a sense's pos carries over to the next ones
        last_pos = pos
        misc = [x.text for x in s.findall("misc")]
        gl = [g.text for g in s.findall("gloss") if g.text]
        if "X" in misc or not gl:
            continue
        senses.append({"pos": pos, "misc": misc, "gloss": gl,
                       "stagk": [x.text for x in s.findall("stagk")], "stagr": [x.text for x in s.findall("stagr")]})
    if not readings or not senses:
        continue
    # Group spellings by the senses they have (usually one group per entry).
    groups = {}
    for r in readings:
        for k in r["with"]:
            ss = tuple(i for i, s in enumerate(senses)
                       if (not s["stagk"] or (k is not None and k in s["stagk"])) and (not s["stagr"] or r["t"] in s["stagr"]))
            if not ss:
                continue
            groups.setdefault(ss, []).append((k, r))
    if not groups:
        continue
    n_entries += 1
    for gi, (ss, pairs) in enumerate(groups.items()):
        ks = [k for k in kanji if any(p[0] == k["t"] for p in pairs)]
        kidx = {k["t"]: i for i, k in enumerate(ks)}
        rs = []
        for k, r in pairs:
            if r not in rs:
                rs.append(r)
        kparts = [("~" if k["rare"] else "") + k["t"] + ("*%d" % k["s"] if k["s"] else "") for k in ks]
        rparts = []
        for r in rs:
            withs = [p[0] for p in pairs if p[1] is r]
            if withs == [None]:
                restr = "@-" if ks else ""
            else:
                idx = sorted(kidx[w] for w in withs)
                restr = "" if len(idx) == len(ks) else "@" + ",".join(map(str, idx))
            forms = [w for w in withs if w] or [r["t"]]
            acc = accent_for(forms + [k["t"] for k in ks], r["t"])
            rparts.append(("~" if r["rare"] else "") + r["t"] + ("#" + acc if acc else "") + restr + ("*%d" % r["s"] if r["s"] else ""))
        out, n = [], 0
        for i in ss:
            g = gloss_text(senses[i])
            if out and n + len(g) > 140:
                break
            out.append(g)
            n += len(g) + 2
        first = senses[ss[0]]
        dict_lines.append("\t".join([
            "|".join(kparts), "|".join(rparts), "; ".join(out).replace("\t", " "),
            ",".join(first["pos"]), "u" if "uk" in first["misc"] else "", "+" if gi else ""]).rstrip("\t"))

os.makedirs(DATA, exist_ok=True)
with open(os.path.join(DATA, "dict.tsv"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(dict_lines))
print("dict entries", n_entries, "lines", len(dict_lines), round(os.path.getsize(os.path.join(DATA, "dict.tsv")) / 1e6, 1), "MB")

# ---------------------------------------------------------------- KANJIDIC2
# kanji.tsv: kanji, on'yomi (katakana, ","), kun'yomi (hiragana, "." before okurigana, ","), meanings ("; "),
#            stroke count, school grade, old JLPT level (4 = easiest), newspaper frequency rank
kanji_lines = []
for c in xml_root_iter(read_text("kanjidic2.xml.gz"), "character"):
    lit = c.findtext("literal")
    rm = c.find("reading_meaning")
    on, kun, mean = [], [], []
    if rm is not None:
        for g in rm.findall("rmgroup"):
            for r in g.findall("reading"):
                if r.get("r_type") == "ja_on":
                    on.append(r.text)
                elif r.get("r_type") == "ja_kun":
                    kun.append(r.text)
            for m in g.findall("meaning"):
                if m.get("m_lang") in (None, "en"):
                    mean.append(m.text)
    if not (on or kun or mean):
        continue
    misc = c.find("misc")
    kanji_lines.append("\t".join([lit, ",".join(on), ",".join(kun), "; ".join(mean[:6]),
                                  misc.findtext("stroke_count") or "", misc.findtext("grade") or "",
                                  misc.findtext("jlpt") or "", misc.findtext("freq") or ""]))
with open(os.path.join(DATA, "kanji.tsv"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(kanji_lines))
print("kanji", len(kanji_lines), round(os.path.getsize(os.path.join(DATA, "kanji.tsv")) / 1e6, 1), "MB")

# ---------------------------------------------------------------- stroke data (animCJK), chunked by code point
out_dir = os.path.join(DATA, "strokes")
for f in glob.glob(os.path.join(out_dir, "s*.json")):
    os.remove(f)
os.makedirs(out_dir, exist_ok=True)
items = []
for name in ("graphicsJa.txt", "graphicsJaKana.txt"):
    for line in read_text(name).splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        ch = d["character"]
        if len(ch) != 1:
            continue
        items.append((ord(ch), ch, {"strokes": d["strokes"], "medians": d["medians"]}))
items.sort()
chunks, cur, size, starts = [], {}, 0, []
for cp, ch, d in items:
    s = json.dumps(d, separators=(",", ":"), ensure_ascii=False)
    if size + len(s) > 300_000 and cur:
        chunks.append(cur)
        cur, size = {}, 0
    if not cur:
        starts.append(cp)
    cur[ch] = d
    size += len(s)
if cur:
    chunks.append(cur)
for i, c in enumerate(chunks):
    with open(os.path.join(out_dir, "s%02d.json" % i), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(c, fh, separators=(",", ":"), ensure_ascii=False)
for name, dest in (("animcjk-APL.txt", "ARPHICPL.TXT"), ("animcjk-LGPL.txt", "LGPL.txt"), ("animcjk-COPYING.txt", "COPYING.txt")):
    shutil.copy(src(name), os.path.join(out_dir, dest))
# point the page at the new chunk boundaries
page = os.path.join(ROOT, "index.html")
if os.path.exists(page):
    html = open(page, encoding="utf-8").read()
    html, n = re.subn(r"const STARTS = \[[0-9,]*\];", "const STARTS = " + json.dumps(starts, separators=(",", ":")) + ";", html)
    assert n == 1, "couldn't find STARTS in index.html"
    open(page, "w", encoding="utf-8", newline="\n").write(html)
print("stroke chunks", len(chunks), "chars", len(items))
