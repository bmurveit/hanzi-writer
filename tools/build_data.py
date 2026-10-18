"""
Build the offline data files for the Hanzi writing app.

Run it like this (from the hz-writer folder):
    python3 tools/build_data.py path/to/node_modules/hanzi-writer-data

Inputs:
  tools/hsk_vocab.json  HSK 3.0 word list (levels, pinyin, meanings, word types,
                        frequency), from github.com/drkameleon/complete-hsk-vocabulary
                        (MIT license).
  data/mywords.js       Your own extra words (edit that file to change them).

Outputs:
  data/words.js    HSK 1-3 words + My words, with everything the app needs.
  data/strokes.js  Stroke data for every character in those words (for offline use).
  data/dict.js     Pinyin + meaning for all ~11,000 HSK words, so the app's
                   "Add a word" form can fill them in for you.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
MAX_LEVEL = 3          # include HSK 1 up to this level
HANZI = re.compile(r"[一-鿿]")

# The HSK data tags each word with grammar codes. These are grouped into
# plain-English word types for the app's "Word types" sections.
TYPE_NAMES = {
    "v": "Verbs", "vn": "Verbs", "vd": "Verbs",
    "n": "Nouns", "nr": "Nouns", "ns": "Nouns", "nt": "Nouns", "nz": "Nouns", "s": "Nouns",
    "a": "Adjectives", "an": "Adjectives", "ad": "Adjectives", "b": "Adjectives", "z": "Adjectives",
    "d": "Adverbs",
    "q": "Measure words & numbers", "m": "Measure words & numbers",
    "r": "Pronouns",
    "t": "Time words",
    "f": "Position words",
    "p": "Grammar words", "c": "Grammar words", "u": "Grammar words",
    "y": "Grammar words", "e": "Grammar words", "o": "Grammar words",
    "i": "Phrases & idioms", "l": "Phrases & idioms",
}


def word_types(codes):
    names = []
    for c in codes:
        name = TYPE_NAMES.get(c)
        if name and name not in names:
            names.append(name)
    return names


def read_js_array(path, var):
    """Read a 'window.X = [...];' file. Strips // comments, then parses the JSON."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    text = "\n".join(line for line in text.splitlines() if not line.strip().startswith("//"))
    body = text[text.index("[", text.index(var)): text.rindex("]") + 1]
    body = re.sub(r",\s*]", "]", body)   # allow a trailing comma after the last line
    return json.loads(body)


def write_js(path, var, value, indent=None):
    # Written as JavaScript (not .json) so a plain <script> tag can load it,
    # which keeps the app working offline and when opened straight from disk.
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"window.{var} = ")
        json.dump(value, f, ensure_ascii=False, indent=indent,
                  separators=(",", ":") if indent is None else None)
        f.write(";\n")


def main():
    data_dir = sys.argv[1]
    with open(os.path.join(HERE, "hsk_vocab.json"), encoding="utf-8") as f:
        vocab = json.load(f)

    words = []
    # 1. HSK 1..MAX_LEVEL words.
    for w, v in vocab.items():
        if v["l"] and v["l"] <= MAX_LEVEL:
            words.append({"word": w, "pinyin": v["p"], "meaning": v["m"],
                          "hsk": v["l"], "freq": v["f"], "types": word_types(v["t"])})
    have = {w["word"] for w in words}

    # 2. My words (skipping any that are already in HSK 1-3).
    mine = 0
    for hanzi, pinyin, meaning in read_js_array(os.path.join(ROOT, "data", "mywords.js"), "HZ_MYWORDS"):
        if hanzi in have:
            continue
        v = vocab.get(hanzi)
        words.append({"word": hanzi, "pinyin": pinyin, "meaning": meaning, "mine": True,
                      "hsk": v["l"] if v else None, "freq": v["f"] if v else None,
                      "types": word_types(v["t"]) if v else []})
        have.add(hanzi)
        mine += 1

    # 3. Stroke data for every character used.
    chars = sorted({c for w in words for c in w["word"] if HANZI.match(c)})
    strokes, missing = {}, []
    for c in chars:
        path = os.path.join(data_dir, c + ".json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                strokes[c] = json.load(f)
        else:
            missing.append(c)

    # 4. Dictionary for the "Add a word" form: [pinyin, meaning, hsk level].
    dictionary = {w: [v["p"], v["m"], v["l"]] for w, v in vocab.items()}

    out = os.path.join(ROOT, "data")
    write_js(os.path.join(out, "words.js"), "HZ_WORDS", words, indent=0)
    write_js(os.path.join(out, "strokes.js"), "HZ_STROKES", strokes)
    write_js(os.path.join(out, "dict.js"), "HZ_DICT", dictionary)

    print(f"{len(words) - mine} HSK 1-{MAX_LEVEL} words + {mine} of My words")
    print(f"{len(chars)} characters bundled")
    if missing:
        print("No stroke data for:", "".join(missing))


if __name__ == "__main__":
    main()
