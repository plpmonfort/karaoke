# 🎤 Karaoke Night

A song picker for karaoke, organised by **where you are in the evening**.

Open it, and it deals you 3 or 5 suggestions from the right phase — warm-up songs
to start, bangers for peak hour, big emotional closers for last call. Everything
is driven by a spreadsheet you own and edit.

**Live app:** _(add your GitHub Pages URL here once published)_

---

## The three phases

| Phase | When | What it's for |
|---|---|---|
| 🌅 **Warm-Up** | Start of the evening | Easy, warm, everybody-knows-it. Loosen up the room. |
| 🔥 **Hype** | Middle of the evening | Peak hour. Bangers, anthems, nobody sitting down. |
| 🌙 **Closer** | End of the evening | Last call. Big feelings, arms around shoulders. |

The app checks the clock and pre-selects the phase you're probably in, but you can
override it any time.

Starting database: **187 songs** — 45 warm-up, 75 hype, 67 closers.

---

## Files

```
Karaoke/
├── index.html                    ← the web app (open this)
├── songs.js                      ← generated data — do not edit by hand
├── Karaoke_Song_Database.xlsx    ← YOUR song list. This is the source of truth.
├── build.py                      ← xlsx → songs.js
├── seed_database.py              ← recreates the xlsx from scratch
├── songs_seed.py                 ← the original 187-song compilation
├── manifest.webmanifest          ← makes it installable on a phone
├── sw.js                         ← service worker, for offline use
├── make_icons.py                 ← regenerates the app icons
├── icons/                        ← home-screen icons
└── requirements.txt
```

---

## Adding your own songs

1. Open **`Karaoke_Song_Database.xlsx`** and go to the **Songs** sheet.
2. Type a new row under the last one. Category, Difficulty, Format, Vocal Range,
   Energy, Crowd and Active are all dropdowns — just pick from the list.
3. Save the file.
4. Run the build:

```bash
python3 build.py
```

5. Commit `songs.js` and push. The live site updates.

To hide a song without deleting it, set its **Active** column to `N`.

### What the columns mean

| Column | Meaning |
|---|---|
| **Category** | `Warm-Up`, `Hype`, or `Closer` |
| **Energy** | 1–5. How much the song lifts the room. |
| **Difficulty** | `Easy`, `Medium`, `Hard`, `Legend`. Legend = bring your whole chest. |
| **Format** | `Solo`, `Duet`, `Group` |
| **Vocal Range** | Roughly where it sits: `Low` → `Wide` |
| **Crowd** | 1–5. How likely the room sings along with you. |
| **Notes** | Free text. Shows on the card in the app. |
| **Active** | `Y` / `N`. Set `N` to park a song. |

`build.py` is forgiving — it clamps out-of-range numbers, falls back on
unrecognised values, skips blank rows, and prints a warning for anything it had
to fix. It won't crash on a messy spreadsheet.

---

## Publishing to GitHub Pages

```bash
git init
git add .
git commit -m "Karaoke Night song picker"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git push -u origin main
```

Then on GitHub: **Settings → Pages → Source: `main` branch, `/ (root)`**.

Your app will be live at `https://YOUR-USERNAME.github.io/YOUR-REPO/` in a minute
or two.

> If you put these files in a **subfolder** of a bigger repo, point Pages at the
> root and the app lives at `.../YOUR-REPO/Karaoke/`.

No build step, no dependencies, no server. `index.html` loads `songs.js` as a
plain `<script>`, so it works when opened straight off your hard drive too —
just double-click `index.html`.

---

## 📱 Installing it on your phone

Once it's live on GitHub Pages, you can save it to your home screen and it
behaves like a normal app: its own mic icon, fullscreen (no browser bars), and
**it works with no signal** — handy, because karaoke rooms are usually a dead
zone.

**iPhone / iPad** — open the Pages URL in **Safari** (this doesn't work in
Chrome on iOS), tap the **Share** button, scroll down, tap **Add to Home
Screen**. The app itself will remind you.

**Android** — open it in Chrome and you'll get an **Install app** button right
in the page. Or use the ⋮ menu → **Install app**.

Once installed it stops nagging you about installing.

### Keeping the phone version up to date

The service worker is deliberately **network-first**: whenever your phone has a
connection it fetches the latest `songs.js` and only falls back to its cached
copy when offline. So after you push new songs, just open the app while online
and they're there. No cache-clearing, no reinstalling.

> ⚠️ Offline mode needs **HTTPS**, which GitHub Pages gives you for free. It's
> switched off when you open `index.html` straight off your disk — the app still
> works, it just won't cache.

### Restyling the icon

```bash
python3 make_icons.py
```

---

## Setup (only needed to run the Python scripts)

```bash
pip3 install -r requirements.txt
```

Regenerating the workbook from the original compilation — **this erases your
Excel edits**, so it refuses to run unless you force it:

```bash
python3 seed_database.py --force
```

---

## Things the app does

- **Auto-detects the phase** from the time of day
- **3 or 5 picks** per roll, with a slot-machine spin, confetti and fireworks
- **Swipe a card left or right** to throw it away and get another one — or use
  the **Swap** button. Either way the other cards stay put.
- **"Sang it"** marks a song done — it drops to the back of the queue and is
  remembered between visits (stored locally in your browser, nothing leaves it)
- **Find karaoke** opens a YouTube search for that track
- **Full songbook** with search and filters by phase, difficulty and format
- Colour theme shifts with the phase — gold, hot pink, then violet
- Works on a phone, respects `prefers-reduced-motion`, and has a mute button

Keyboard: <kbd>Space</kbd> rerolls.
