"""Single-verse posts: a feed image (1080 x 1350) and a Story (1080 x 1920) for each verse in a JSON bank.
Usage: python3 verse_posts.py bank.json OUTDIR
Each bank entry: {"slug", "title", "verse", "ref", "checked"}; only entries with checked == true are rendered.
Every verse must be checked word for word against the Berean Standard Bible before it goes in the bank."""
import json, pathlib, sys, html as H
from playwright.sync_api import sync_playwright
from gen_carousels import NAVY, GOLD, CREAM, EMBLEM
import gen_stories

def feed_html(title, verse, ref):
    return f"""<!doctype html><html><head><meta charset=utf-8><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;overflow:hidden;background:{NAVY}}}
body{{font-family:Carlito,sans-serif;-webkit-font-smoothing:antialiased}}
.f1,.f2{{position:absolute;border:2px solid {GOLD}}} .f1{{inset:46px}} .f2{{inset:58px;border-width:1px;opacity:.75}}
.c{{position:absolute;left:120px;right:120px;top:110px;bottom:150px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}}
.c *{{text-wrap:balance}}
.em{{width:96px;height:96px;color:{GOLD}}}
.label{{font-weight:700;font-size:27px;letter-spacing:.34em;color:{GOLD};margin-top:26px}}
.title{{font-family:Gelasio;font-style:italic;font-weight:500;font-size:62px;line-height:1.15;color:{GOLD};margin-top:20px;max-width:820px}}
.bar{{width:110px;height:3px;background:{GOLD};margin:30px auto 32px}}
.verse{{font-family:Gelasio;font-size:{'52' if len(verse) > 150 else '58'}px;line-height:1.42;color:{CREAM};max-width:830px}}
.orn{{display:flex;align-items:center;gap:18px;margin:28px auto 20px}}
.orn span{{display:block;width:70px;height:1.5px;background:{GOLD}}} .orn i{{display:block;width:13px;height:13px;background:{GOLD};transform:rotate(45deg)}}
.ref{{font-weight:700;font-size:32px;letter-spacing:.2em;color:{GOLD}}}
.addr{{position:absolute;bottom:92px;left:0;right:0;text-align:center;font-size:27px;color:{GOLD};letter-spacing:.03em}}
</style></head><body><div class="f1"></div><div class="f2"></div><div class="c">
<div class="em">{EMBLEM}</div><div class="label">STAND ON THIS</div><div class="title">{title}</div><div class="bar"></div>
<div class="verse">{verse}</div><div class="orn"><span></span><i></i><span></span></div><div class="ref">{ref}</div></div>
<div class="addr">Jesus is the healer. &nbsp;·&nbsp; HowToPrayForTheSickAndExpectAMiracle.com</div></body></html>"""

if __name__ == "__main__":
    bank = json.load(open(sys.argv[1])); out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    report = {}
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        feed = b.new_page(viewport={"width": 1080, "height": 1350}); story = b.new_page(viewport={"width": 1080, "height": 1920})
        for e in bank:
            if not e.get("checked"): continue
            v = H.escape(e["verse"], quote=False); t = H.escape(e["title"], quote=False).replace("|", "<br>"); r = H.escape(e["ref"].upper(), quote=False)
            for pg, h, name in ((feed, feed_html(t.replace("<br>", " "), v, r), f"{e['slug']}_feed_1080x1350.png"),
                                (story, gen_stories.html(t, v, r), f"{e['slug']}_story_1080x1920.png")):
                pg.set_content(h, wait_until="load"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(120)
                low = pg.evaluate("() => { let m=0; for (const x of document.querySelectorAll('.c *')) { const r=x.getBoundingClientRect(); if (r.height) m=Math.max(m,r.bottom);} return Math.round(m); }")
                top = pg.evaluate("() => { let m=1e9; for (const x of document.querySelectorAll('.c *')) { const r=x.getBoundingClientRect(); if (r.height) m=Math.min(m,r.top);} return Math.round(m); }")
                pg.screenshot(path=str(out / name)); report[name] = [top, low]
        b.close()
    print(json.dumps(report, indent=0))
