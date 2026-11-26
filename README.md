# howtopray-instagram

Posts for the Instagram account **howtoprayforthesick** (Graham Marsland, *How to Pray for the Sick and Expect a Miracle*), and the log of how each one did. Buffer publishes the posts and fetches each picture from this repository, so **never move, rename or delete a file under `media/`** once it has been scheduled.

## Accounts

| What | Value |
|---|---|
| Buffer organisation | "My organization", `6b071ecb19a2723798376b26` (Free plan: at most 10 scheduled posts at a time) |
| Buffer channel | howtoprayforthesick (Instagram, professional), `6b0720e88541f09ecba09267` |
| Buffer time zone | Australia/Melbourne (the Buffer account's zone). **The posting slots are US Eastern time (America/New_York)**: work out each `dueAt` from the Eastern time with Python `zoneinfo`, so daylight saving in either country is handled; any correct offset is accepted by Buffer |
| Website | howtoprayforthesickandexpectamiracle.com, Vercel team "Infinite Intelligence" `team_j1aE7VP1Hs5M8dmdQ752dnbg` |
| Picture addresses | `https://raw.githubusercontent.com/gmarsland/howtopray-instagram/main/<path>` |

## What Graham decided (25 and 26 November 2026)

1. **Two posts a day for a US audience, both at 08:00 US Eastern time (America/New_York), every day** (Graham, 26 November 2026: "I'd rather they get it at 8 a.m. on their way to work ... just pick one time zone and we'll stick to that ... the biggest"). Eastern time holds about 47% of Americans, the most of any US zone. The Story and the feed post go out together at 08:00 Eastern: 07:00 Central, 05:00 Pacific, and 00:00 (midnight, the next day) in Melbourne while both countries keep their current clocks. More only when the numbers show it helps (see "When to change"), and never more than three a day without Graham's say.
   - Why these numbers (research, 26 November 2026): Buffer's study of 2.1 million posts found reach per post about 12% higher at 3 to 5 feed posts a week than at 1 to 2, 18% higher at 6 to 9 and 24% higher at 10 or more, with follower growth rising the same way; so one feed post every day (7 a week). Stories mostly reach people who already follow, so one a day until the account has followers. The 2026 timing studies disagree (Buffer: Thursday 9 am, Wednesday 12 pm and 6 pm; Metricool: 8 pm Monday and Tuesday; Later: 5 am); Graham has fixed the time at 08:00 Eastern.
   - **A second Story a day** (also 08:00 Eastern: the day's feed picture with the prayer link) once the account passes 200 followers, because Stories are seen by followers.
2. **Nothing posts until the website is live.**
3. **Scripture posts and wording Graham has approved go out by themselves.** The five prayer cards are approved as written. **Any new prayer in Graham's voice is saved only as a Buffer draft, for his OK.** Never schedule one.
4. Remember what works and lean towards it.

## The rules every post keeps

These come from the project's lens (`claude/launch-plan-summary.md`) and Instagram's own rules.

1. **True.** Every verse is checked word for word against the Berean Standard Bible (BSB) before it goes in `bank/verse_bank.json`, from a page that labels the text as BSB: biblestudytools.com/bsb, heartlight.org, or the "Berean Standard Bible" line on biblehub.com. Record the source. If a part of a verse is used, the reference says "From". If the wording cannot be confirmed, the verse is not used.
2. **Checked.** Nothing says anyone was healed. Healing is confirmed only by a doctor, and these posts never describe a person's healing.
3. **Glory to Jesus.** Scripture is the picture. No boasting about followers or numbers.
4. **Freely given.** Each post is whole: the whole verse or passage used, the whole prayer.
5. **Loves the person.** "Keep seeing your doctor." in every caption. No blame for anyone still sick.
6. **No pressure.** No promise of a result or a date. No "Type Amen", "Share if", "Do not scroll", or "follow for part two". At most five hashtags.
7. **Only what is in `plan/queue.json`.** Never post Brian's video, the films, or anything else. Never use `shareNow` or `shareNext`; schedule with `customScheduled` and a `dueAt`. Never edit or delete a post that has already gone out.
8. **Captions in Graham's voice:** no contractions and no abbreviations.

### Caption for a verse post

```
<Title>.

“<verse>” (<reference>)

Read it aloud. It is what God has said.

There is a free prayer for tonight at the link in my profile. Keep seeing your doctor.

<five hashtags: see "Hashtags" below>
```

### Hashtags (set 26 November 2026, at Graham's request: "for maximum impact")
Instagram allows five. They do not widen reach (Mosseri); they tell Instagram what the post is about and help it appear in hashtag search. So every post gets five chosen for that post, never one block pasted on every post:
1. `#HowToPrayForTheSick` first on every post: the account's own tag, so one tap shows everything.
2. Two for the kind of post: prayer cards `#PrayerForHealing #HealingPrayer`; single verses `#HealingScripture #BibleVerse`.
3. Two for that post's topic, words a person would really search, for example `#JesusHeals`, `#GodHeals`, `#ByHisStripes`, `#JehovahRapha`, `#PrayForTheSick`, `#LayingOnOfHands`, `#WordOfGod`, `#Psalms`, `#PraiseGod`, `#TheCross`, `#HolySpirit`, `#HowToPray`, `#ChristianEncouragement`.
Write each tag in capitals at the start of each word (screen readers read them better). No tag that claims a healing (`#Healed`, `#Miracle`, `#Testimony`) unless Graham approves that post. No duplicates. Exactly five.

A Story has no caption. It carries a link sticker to `https://howtoprayforthesickandexpectamiracle.com/pray?utm_source=instagram&utm_medium=story`.

## The daily run (what the scheduled task does, in order)

1. **Get the repository.** Attach `gmarsland/howtopray-instagram` with push access and clone it. Read this file.
2. **Is the website live?** Call Vercel `get_domain_config` for the domain with the team ID. Live means `misconfigured` is false. If it is not live, add a dated line to `log/learning.md`, push, and stop. Schedule nothing.
   Then check the Story link still lands on the prayer: Vercel `list_deployments` (project `how-to-pray-for-the-sick`, target production, state READY, limit 1), then `web_fetch_vercel_url` on that deployment's URL with path `/pray`. The page must answer 200 and contain both `id='pray'` and `data-pick='me'` (the "Pray now" page with the For me and For someone else buttons). If it does not, schedule no Stories, schedule feed posts only, and tell Graham. (26 November 2026: the website was rebuilt at 10.55 am and the free prayer moved to its own page, `/pray`, which opens on "Pray now"; the Story link changed from `/#for-you` to `/pray` that day.)
3. **Reconcile.** `list_posts` for the channel (scheduled, sent, error). Bring `log/scheduled.json` up to date (queue id, Buffer post id, due time, status). If a post failed, note why in `log/learning.md` and do not retry it more than once.
4. **Learn (first run of each day only).** For every sent post at least 48 hours old with no row in `log/results.csv`, call `get_post` with `includeMetrics: true` and add a row. Then rewrite the "Latest" section of `log/learning.md`: posts so far; average reach (or impressions) per post by kind (carousel, verse, Story), by slot, and by topic; the best and weakest three; the trend in reach per feed post (last 14 days against the 14 before).
5. **Change only by these rules, one change at a time, and write each change and its reason in `log/learning.md`:**
   - After 14 sent feed posts: put the stronger kind (carousel or verse) first in the unscheduled queue, two of every three feed posts.
   - Topics: move unscheduled posts whose topic is like the best three earlier in the queue.
   - Times: fixed at 08:00 Eastern by Graham on 26 November 2026. Do not test or change the time. If the numbers suggest another time would do better, say so in the Monday summary and let Graham decide.
   - **Three a day:** propose a second daily feed post to Graham in the Monday summary (he chooses its time) when the last 14 days' average reach per feed post is at least that of the 14 days before, and the unscheduled queue holds at least 10 days of material. Never more than three a day.
6. **Top up Buffer.** Keep no more than 9 posts scheduled. Take the next unscheduled items from `plan/queue.json` in order and schedule each at the next free day at 08:00 US Eastern time (the Story and the feed post of a day both at 08:00), never in the past. The queue is in day order: each day's Story is the verse of that day's feed post, so a Story and its feed post share the same date and time. Use `create_post` with `schedulingType: automatic`, `mode: customScheduled`, the `dueAt`, the caption, every image with its alt text, and `metadata.instagram`: `type` "carousel" items and verse posts as `post` with `shouldShareToFeed: true`; Stories as `story` with `shouldShareToFeed: false` and `link` set. Record each in `log/scheduled.json`.
7. **Keep the queue full.** When fewer than 8 items are unscheduled, add 4 new verse posts:
   - Choose healing verses not yet in the bank (the list below, or others on healing, prayer for the sick, or the faithfulness of God).
   - Check each against the BSB as in rule 1, and write a title "for the moment" (for example "When you are waiting for results"), never a promise.
   - Add them to `bank/verse_bank.json` with `checked: true` and the source; run `python3 tools/verse_posts.py bank/verse_bank.json media/verses` from the repo root (it needs Python Playwright, Google Chrome, and the Gelasio and Carlito fonts, which this environment has); look at the new images; append a feed item and a Story item for each to `plan/queue.json` in the same shape as the others.
   - Commit and push before scheduling any of them. If the push fails, do not schedule them; note it in `log/learning.md`.
8. **Commit and push** the log.
9. **Tell Graham** (one short message) only when: the website is still not live three days after this started; Buffer shows an error or the channel is disconnected; the queue cannot be refilled; or, on Mondays, a short weekly summary (posts out, reach, what is working, any change made).
10. If the project's docs can be written from the run, replace `claude/instagram-results-log.md` with the "Latest" section of `log/learning.md`.

## Healing verses not yet used (check each before use)

Psalm 41:3 · Matthew 4:23 · Matthew 9:35 · Matthew 15:30–31 · Mark 6:56 · Luke 4:40 · Luke 8:50 · Luke 9:11 · John 14:13–14 · Acts 3:16 · Acts 5:16 · Jeremiah 1:12 · Romans 8:11 · 2 Corinthians 1:20 · 1 John 5:14–15

Already in `bank/verse_bank.json` (never post the same verse twice in 60 days): check the bank before choosing.

## Files

- `plan/queue.json`: every post in order, with its pictures, alt text, caption and kind.
- `bank/verse_bank.json`: every verse used, with where its BSB wording was checked.
- `log/scheduled.json`: what has gone into Buffer. `log/results.csv`: the numbers for each post. `log/learning.md`: what has been learned and every change made.
- `media/films/`: the finished films, kept here so they have a lasting address. They are not in the queue and the task never schedules them (rule 7); Graham decides when a film is posted. A copy under 50 MB is kept here (GitHub refuses files over 100 MB); the full-quality masters stay in Runway.
- `media/merchandise/`: the artwork for the merchandise in the Fourthwall shop (added 26 November 2026 at Graham's request, so every chat and the website can reach it). `previews/` holds a picture of each design on the colour of its product; `print-files/` holds the full print files exactly as uploaded to Fourthwall; `index.json` lists each product with its Fourthwall id, price, Scripture and files. These are not posts: they are not in the queue and the task never schedules them (rule 7). The same files are on the page "Merchandise artwork", https://claude.ai/artifact/FLhKcQSARJs5GUgvsCQda7. Every code in them opens https://howtoprayforthesickandexpectamiracle.com/wear.
- `tools/`: the scripts that draw the posts in the book's style (navy `#13233f`, gold `#d6b668`, cream `#f5f0e4`; Gelasio and Carlito).
