# Hanzi Writer Practice

Practice writing HSK 1–3 words (plus your own) stroke by stroke with the mouse.

## Files

| File | What it is | Edit it? |
|---|---|---|
| `index.html` | The app (HTML, styles and JavaScript in one file) | |
| `sw.js` | Service worker: keeps a copy of the app on the device for offline use | Change `VERSION` to force a refresh |
| `data/topics.js` | Real-life topics (Food & drink, Places in town...) | Yes, freely |
| `data/mywords.js` | Your extra words outside HSK 1–3 | Yes, then rebuild |
| `data/words.js` | HSK 1–3 + My words, built by the script | No (generated) |
| `data/strokes.js` | Stroke data for every character in those words (~2.2 MB) | No (generated) |
| `data/dict.js` | All ~11,000 HSK words, used by "Add a word" to fill in pinyin and meaning | No (generated) |
| `tools/build_data.py` | Builds the three generated files | |
| `tools/hsk_vocab.json` | The HSK 3.0 word list the build reads | |
| `lib/hanzi-writer.min.js` | The Hanzi Writer library that checks your strokes | |
| `LICENSES/` | Licenses for the library and data | |

## Putting it online (GitHub Pages)

1. On github.com: **New repository**, name it `hanzi-writer`, Public, **Create repository**.
2. Click **uploading an existing file** and drag in everything *inside* the `hz-writer`
   folder (so `index.html` is at the top level, not inside a folder). **Commit changes**.
3. **Settings → Pages**: Source **Deploy from a branch**, branch **main**, folder **/ (root)**, **Save**.
4. After a minute the app is at `https://YOUR-USERNAME.github.io/hanzi-writer/`.

Open it once while online; after that it also opens offline.

**Updating:** upload the changed files the same way. Changes appear the second time you
open the app (the first visit downloads them in the background). If a device seems stuck
on an old version, change `VERSION` in `sw.js` (e.g. `hz-v2`) and upload it.

## Backup and restore

Progress is saved in the browser, separately on each device and each website address.
**Backup → Download backup** saves a `.json` file; **Restore from file** on another device
(e.g. via Google Drive) replaces that device's progress after a second confirming click.
Only `hz_` keys are saved or restored; other apps' data (like `ix_` keys) is never touched.

## Adding words

- **In the app:** "Add a word". Saved in your browser. New characters outside HSK 1–3
  are downloaded the first time you write them, then kept for offline use.
- **In the files:** add a line to `data/mywords.js`, then rebuild (below) so the stroke
  data is bundled.

## Rebuilding

1. `npm install hanzi-writer-data` (once, in any folder)
2. `python3 tools/build_data.py path/to/node_modules/hanzi-writer-data`

To include more HSK levels, change `MAX_LEVEL = 3` at the top of the script.

## Credits

- [Hanzi Writer](https://hanziwriter.org) by David Chanin (MIT license)
- Stroke data from Make Me a Hanzi, derived from Arphic fonts (Arphic Public License)
- HSK 3.0 vocabulary from [complete-hsk-vocabulary](https://github.com/drkameleon/complete-hsk-vocabulary) by Yanis Zafirópulos (MIT license)
