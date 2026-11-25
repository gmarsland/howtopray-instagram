# Podcast covers and episode list (version 2)

For the podcast of the book *How to Pray for the Sick and Expect a Miracle* by Graham Marsland.
Branch `podcast` only; `main` is not touched, so the Instagram daily run is not affected.

**Version 2, 26 November 2026, 9 am.** At Graham's word ("I don't want it to follow exactly the chapters
of the book ... Let's just follow the lenses of people that would be interested in this subject"), the
episodes follow the people who listen. Eight lenses, three episodes each in the first 24, rotating so
that no two neighbouring episodes speak to the same person. Version 1 (one episode per chapter) is in
this branch's history.

## The eight lenses

| Lens | Who is listening | Episodes |
|---|---|---|
| A | When you are the one who is sick | 1, 9, 17 |
| B | When your child is sick | 2, 10, 18 |
| C | When you are caring for someone | 3, 11, 19 |
| D | When you have never prayed for anyone | 4, 12, 20 |
| E | When you are still waiting | 5, 13, 21 |
| F | When you are not sure God still heals | 6, 14, 22 |
| G | When you lead others | 7, 15, 23 |
| H | When you are getting to know Jesus | 8, 16, 24 |

## What is here

| Path | What it is |
|---|---|
| `covers/3000/show.png`, `episode-01.png` to `episode-24.png` | 3000 x 3000 PNG, for podcast hosts |
| `covers/1000/show.jpg`, `episode-01.jpg` to `episode-24.jpg` | 1000 x 1000 JPG, for web pages |
| `covers/contact-sheet.png` | all 25 on one sheet |
| `episodes.json` | the show, the lenses and the 24 episodes: number, slug, title, lens, lensTitle, fromTheBook, scripture, description, picture, cover, coverLarge, length, pilot, audioFile, audioUrl, approved |
| `lens_episodes.json` | the full plan for each episode, including the exact text for the notebook's customise box |
| `lens_plan.py` | writes `lens_episodes.json` |
| `make_covers.py` | draws every cover and writes `episodes.json` from `lens_episodes.json` |

To fetch: `git clone --depth 1 --branch podcast https://github.com/gmarsland/howtopray-instagram`

## The covers

The book's own style: navy `#13233f`, gold `#d6b668`, cream `#f5f0e4`, Gelasio and Carlito, the double gold frame.
At the top, the book's name and "THE PODCAST". In the middle, a gold line picture, different for every
episode (`picture` in `episodes.json`). Under it, in small gold capitals, the lens ("WHEN YOUR CHILD IS SICK"),
then the title, which is the question that person is asking, and at the foot the Scripture the episode stands on.

To redraw: `python3 make_covers.py .` in this folder (Python with Playwright and Pillow, Google Chrome,
and the Gelasio and Carlito typefaces).

## Rules

1. An episode is shown to the public only when `approved` is true. Graham sets that after he has listened to it.
2. The two voices are made with artificial intelligence. Every page and listing says so plainly.
3. No promise of healing. Nobody who is still sick is blamed. "Keep seeing your doctor."
4. Do not link to these GitHub addresses from the live website. Copy the pictures into the website.

The brief for the website is in the Claude project, `claude/podcast-website-kit.md`.
