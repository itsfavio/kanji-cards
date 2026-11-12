# Kanji Cards 漢字カード

Japanese flashcards for studying a class's vocab chapter by chapter. Each card has three sides: the word, its reading, and the meaning. You can hear each word, see its pitch accent, and watch (or trace) the stroke order of every kanji and kana.

It's a plain static site with no build step, no backend, and no accounts. Open it and start studying. It's the Japanese sibling of [Hanzi Cards](https://github.com/itsfavio/hanzi-cards).

**Live site:** `https://itsfavio.github.io/kanji-cards/`

## Features

- **Chapters.** Make one per lesson. They stay saved, so you don't have to re-enter words.
- **3-sided cards.** Word → reading → meaning. Tap the card to turn it. Use **Focus on** to pick which side each card starts on, for example to drill meaning → word.
- **Pitch accent.** Every reading shows its pitch: a line over the high beats and a tick where the pitch drops, colored by pattern (heiban, atamadaka, nakadaka, odaka), so you start remembering words by their accent.
- **Rōmaji or kana only.** Chosen on first visit, switchable any time with the **Readings** toggle: kana only, or kana with rōmaji underneath while you're still learning kana.
- **Pronunciation.** Plays the word in a Japanese voice (from its kana, so it never picks the wrong reading of the kanji). **Slow** says it again one beat (mora) at a time, so you can hear long vowels, small っ and ん.
- **Stroke order.** Animated stroke order in Japanese stroke order for about 7,500 kanji plus all hiragana and katakana, on a practice grid, and a Practice mode where you trace each stroke and get a hint after two misses. Each kanji shows its on'yomi, kun'yomi and meaning.
- **Built-in dictionary.** Type kanji, kana, rōmaji or English and the reading, pitch accent and meaning fill in automatically from JMdict (about 219k words). Polite and conjugated forms (食べます, 行きました, 勉強しました, 高くない) are looked up in their dictionary form.
- **Which word did you mean?** Words that could be more than one word (はし: 橋 bridge, 端 edge, 箸 chopsticks) get a red note, and you confirm the one you mean before they're added.
- **Add from a photo.** Snap or upload a picture of a vocab list or textbook page and the app reads the kanji and kana off it, right in your browser, and drops them in the box, ready to look up.
- **Paste an image.** Copy a screenshot or picture of Japanese text and paste it with Ctrl/⌘ + V (or long-press → Paste on a phone) on the Add words tab or Quick search. It's read the same way as a photo.
- **Quick search.** Look up any word in kanji, kana, rōmaji or English to see its readings, pitch accent, meanings, word type (る-verb, う-verb, な-adjective…) and each kanji's readings, without adding it to a chapter.
- **Quick write.** Type kanji, kana, rōmaji or English to watch the stroke order and practice tracing it, without adding it to a chapter. Japanese is drawn exactly as typed, so あいうえお draws the kana.
- **Instructor mode.** Teach a chapter's new words to a class: the word, then its reading with furigana and pitch accent, then the stroke order of every character (looping until you move on), then the meaning. Click or press → / Space to advance, and use **Full screen** for a projector.
- **Spaced repetition.** Grade each card **Don't know it**, **Still learning** or **I know it**. Missed cards come back later in the same session, and each "I know it" spaces the next review further out (1, 3, 7, then 14 days). A card is only Known, and stops showing, after you recall it at every step.
- **Active recall.** Stroke order stays hidden while you study. Tick **Show stroke order** to keep it open, or press **Peek strokes** on a card you're stuck on.

## How to use it

1. **Pick how readings are shown.** On first visit, choose kana only or kana + rōmaji. Change it later with the **Readings** toggle above the chapter list.
2. **Make a chapter.** Type a name, like `Lesson 3` or `第3課`, in the box under the chapter list and press **+**.
3. **Add words.** On the **Add words** tab, enter one entry per line and press **Look up** (or Ctrl/⌘ + Enter):

   ```
   食べる                    a word in kanji or kana
   先生 学生 友達             several words on one line
   上手 じょうず good at      word + reading + your own meaning
   食べます                   polite forms find the dictionary form (食べる)
   taberu                    rōmaji search, then pick the word
   eat                       English search, then pick the word
   ```

   Or press **From a photo** and pick (or snap) a picture of your vocab list. The app reads the words off it and puts them in the box for you to check and look up. You can also copy an image and paste it straight in: Ctrl/⌘ + V on a computer, or long-press the box and tap **Paste** on a phone.

   Everything shows up for review first. You can switch readings for words with more than one (今日 きょう / こんにち), edit readings and meanings, tick **Kana only** to write a card in kana, or remove entries. Then press **Add**. Words already in the chapter are skipped.
4. **Study.** On the **Study** tab you get today's reviews plus any new cards (**Due**). Switch to **All** for extra practice; reviewing a card early doesn't move its schedule. Tap the card to turn it and **Hear it** for pronunciation, then grade yourself:

   | Button | What happens |
   | --- | --- |
   | **Don't know it** | Starts the card's reviews over. It comes back after about 3 cards and needs "I know it" twice before it leaves the session. |
   | **Still learning** | Moves the card one step back. It comes back after about 5 cards. |
   | **I know it** | Schedules the next review: tomorrow, then 3, 7 and 14 days later. Recalling it once more after the 14-day gap makes it **Known**, and it stops showing. |

   Stroke order is hidden so you practice recalling the word first. Tick **Show stroke order** to keep it open, or press **Peek strokes** for just the current card.
5. **Manage.** The **Words** tab lists the whole chapter. Fix a reading or meaning inline, change a card's status, or delete cards.

### Keyboard shortcuts (Study tab)

| Key | Action |
| --- | --- |
| `Space` | Turn the card |
| `←` `→` | Previous / next card |
| `S` | Speak the word |
| `1` `2` `3` | Jump to word / reading / meaning |

### Pitch accent colors

The number is the beat (mora) after which the pitch drops, as in the NHK accent dictionary.

| Pattern | Number | Color | Example |
| --- | --- | --- | --- |
| Heiban (flat) | 0 | blue | がくせい: low, then high to the end, and a following particle stays high |
| Atamadaka | 1 | red | はし (箸): high, then drops after the first beat |
| Nakadaka | 2 … n−1 | orange | たべる: rises, then drops inside the word |
| Odaka | n | green | はし (橋): rises, then drops after the word, on the particle |

## Notes

- **Where your cards are saved:** in your browser (localStorage). They stay put between visits on the same device and browser. Clearing site data, or switching to another device or browser, starts you fresh. Kanji Cards keeps its data separate from Hanzi Cards, even on the same site.
- **No sound?** Pronunciation uses your device's built-in text-to-speech, so a Japanese voice needs to be installed.
  - iPhone / Mac: Settings → Accessibility → Spoken Content → Voices → Japanese
  - Windows: Settings → Time & Language → Speech → Add voices → Japanese
  - Android: usually included. Otherwise check Settings → Text-to-speech.
- **First dictionary load:** the dictionary is about 17 MB (about 7 MB to download, compressed) and only loads the first time you open **Add words**, Quick search or Quick write. Studying doesn't need it.
- **Pitch accent** comes from Kanjium's list of about 124k words. Words it doesn't have show their reading without pitch marks. Accent can vary by region and speaker; this is standard Tokyo Japanese.
- **Reading photos:** the first time you read an image (**From a photo** or paste), the app downloads a text-recognition model ([PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) PP-OCRv6, about 55 MB) from this site and runs it on your device in a background worker. After that the browser keeps it. The image never leaves your device, and there's no server or AI service involved. It reads kanji, hiragana and katakana, and copes with screenshots, photos of printed pages and neat handwriting, but always check what it read before looking up.

## Hosting it yourself

### GitHub Pages
1. Fork or copy this repo. It must be public on a free GitHub plan.
2. Go to **Settings → Pages → Build and deployment**, choose **Deploy from a branch**, then branch `main`, folder `/ (root)`, and **Save**.
3. After about a minute it's live at `https://<username>.github.io/<repo>/`.

### Locally
```sh
python -m http.server 8000
# open http://localhost:8000
```
Opening `index.html` directly as a file won't work, because browsers block the dictionary fetch from `file://`.

## Project structure

```
index.html              the whole app (HTML, CSS, JS in one file)
data/dict.tsv           JMdict, trimmed: spellings, readings with pitch accent and frequency, meaning, word type
data/kanji.tsv          KANJIDIC2: each kanji's on'yomi, kun'yomi, meanings, stroke count, grade
data/strokes/sNN.json   stroke data for ~7,500 kanji and all kana, split by code point and loaded on demand
data/ocr/*.tar          PP-OCRv6 small text detection + recognition models (ONNX)
vendor/ocr/             on-device OCR worker: PaddleOCR.js + OpenCV.js + ONNX Runtime Web, bundled
scripts/build_data.py   regenerates data/dict.tsv, data/kanji.tsv and data/strokes/
scripts/build_ocr.sh    rebuilds vendor/ocr/ and fetches data/ocr/ (sources and pinned versions in scripts/ocr/)
```

The Hanzi Writer library (which draws the stroke animations) loads from the jsDelivr CDN. Everything else is served from this repo.

### Rebuilding the data
To pull a newer JMdict and KANJIDIC2, or update the other sources:
```sh
python scripts/build_data.py
```
It needs only Python 3. The first run downloads its sources into `.sources/` (kept out of git): JMdict and KANJIDIC2 are the latest EDRDG releases, while Kanjium, wordfreq and animCJK are pinned to a commit in the script. Delete `.sources/` to download fresh copies. The script rewrites `data/` and updates the stroke-chunk index inside `index.html`.

### Rebuilding the OCR
To update PaddleOCR.js or change the worker (`scripts/ocr/worker.js`):
```sh
sh scripts/build_ocr.sh
```
It installs the versions pinned in `scripts/ocr/package.json`, bundles the worker into `vendor/ocr/`, and downloads the models into `data/ocr/` if they're missing. The models are kept in this repo because the official download host doesn't allow cross-site requests.

## Credits

- **[JMdict](https://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project) and [KANJIDIC2](https://www.edrdg.org/wiki/index.php/KANJIDIC_Project):** dictionary and kanji data, © the [Electronic Dictionary Research and Development Group](https://www.edrdg.org/), used in conformance with the Group's [licence](https://www.edrdg.org/edrdg/licence.html) (CC BY-SA 4.0). `data/dict.tsv` and `data/kanji.tsv` are trimmed derivatives and are shared under the same license.
- **[Kanjium](https://github.com/mifunetoshiro/kanjium):** pitch accent data (CC BY-SA 4.0). "The pitch accent notation, verb particle data, phonetics, homonyms and other additions or modifications to EDICT, KANJIDIC or KRADFILE were provided by Uros O. through his free database."
- **[wordfreq](https://github.com/rspeer/wordfreq)** by Robyn Speer: Japanese word frequencies used to rank search results (data CC BY-SA 4.0; sources include Wikipedia, OpenSubtitles, ParaCrawl and the Leeds Internet Corpus).
- **[animCJK](https://github.com/parsimonhi/animCJK):** Japanese stroke-order data for kanji and kana. Kanji data derives from Arphic fonts and [Make Me a Hanzi](https://github.com/skishore/makemeahanzi) under the [Arphic Public License](data/strokes/ARPHICPL.TXT); kana data is also available under the [LGPL](data/strokes/LGPL.txt) (see [COPYING.txt](data/strokes/COPYING.txt)).
- **[Hanzi Writer](https://hanziwriter.org/):** stroke animation and tracing (MIT).
- **[PaddleOCR / PaddleOCR.js](https://github.com/PaddlePaddle/PaddleOCR):** on-device text recognition and the PP-OCRv6 models (Apache-2.0), with [ONNX Runtime Web](https://onnxruntime.ai/) (MIT), [OpenCV.js](https://github.com/TechStark/opencv-js) (Apache-2.0) and [Clipper](https://www.npmjs.com/package/clipper-lib) (Boost).
- Fonts: [Klee One](https://fonts.google.com/specimen/Klee+One) (a textbook-style Japanese font, so characters look the way they're written by hand), Noto Serif JP and IBM Plex, via Google Fonts (SIL Open Font License).
