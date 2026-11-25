# Podcast covers and episode list

For the podcast of the book *How to Pray for the Sick and Expect a Miracle* by Graham Marsland.
Added on 26 November 2026, at Graham's word ("you can add the files here if needed"), on the branch `podcast`.
The `main` branch is not touched, so the Instagram daily run is not affected.

## What is here

| Path | What it is |
|---|---|
| `covers/3000/show.png`, `covers/3000/episode-01.png` to `episode-24.png` | 3000 x 3000 PNG. For podcast hosts (Apple Podcasts and Spotify ask for a square picture between 1400 and 3000 pixels). |
| `covers/1000/show.jpg`, `covers/1000/episode-01.jpg` to `episode-24.jpg` | 1000 x 1000 JPG. For web pages. |
| `covers/contact-sheet.png` | All 25 on one sheet, to look at. |
| `episodes.json` | The show and the 24 episodes: number, slug, title, part of the book, chapter title, story, Scripture, one line for a web page, what the picture is, cover files, length where known, `audioFile`, `audioUrl`, `approved`. |
| `make_covers.py` | Draws every cover and writes `episodes.json`. The words and the pictures are in this one file. |

Address of any file: `https://raw.githubusercontent.com/gmarsland/howtopray-instagram/podcast/podcast/<path>`

To fetch everything: `git clone --depth 1 --branch podcast https://github.com/gmarsland/howtopray-instagram`

## The covers

The book's own style: navy `#13233f`, gold `#d6b668`, cream `#f5f0e4`, Gelasio and Carlito, the double gold frame.
Each episode has its own gold line picture, taken from that episode's Bible story or its Scripture
(listed as `picture` in `episodes.json`). The title is the question the episode answers, and the line
at the foot is the Scripture the episode stands on. No episode numbers are on the pictures, because
every episode is made to stand alone.

To change a cover, change `make_covers.py` and run `python3 make_covers.py .` in this folder
(needs Python with Playwright and Pillow, Google Chrome, and the Gelasio and Carlito typefaces).

## Rules

1. An episode is shown to the public only when `approved` is true. Graham sets that after he has listened to it.
2. The two voices are made with artificial intelligence. Every page and every listing says so plainly.
3. No promise of healing. Nobody who is still sick is blamed. "Keep seeing your doctor."
4. Do not link to these GitHub addresses from the live website. Copy the pictures into the website.

The full brief for the website is in the Claude project, in `claude/podcast-website-kit.md`.
