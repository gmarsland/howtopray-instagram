"""Instagram Stories (1080 x 1920): one verse card each, in the same design as the Reel's last frame.
Words stay between y 250 and y 1450, clear of Instagram's top bar, the reply bar and a link sticker.
Verses checked word for word against the Berean Standard Bible on 25 November 2026."""
import json, pathlib, sys, re
from playwright.sync_api import sync_playwright
from gen_carousels import NAVY, GOLD, CREAM, EMBLEM

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/home/claude/instagram/posts/stories")
NW = "<span style='white-space:nowrap'>{}</span>"

STORIES = [
    ("story-mark-1-41", "When you wonder<br>if He is willing",
     f"Moved with compassion, Jesus reached out His hand and touched the man. {NW.format('“I am willing,”')} {NW.format('He said.')} {NW.format('“Be clean!”')}", "MARK 1:41"),
    ("story-1-peter-2-24", "When you need<br>something to stand on",
     f"He Himself bore our sins in His body on the tree, so that we might die to sin and live to righteousness. {NW.format('“By His stripes')} you are healed.”", "1 PETER 2:24"),
    ("story-mark-10-51", "When you do not<br>know what to pray",
     f"“What do you want Me to do for you?” Jesus asked. “Rabboni,” said the blind man, {NW.format('“let me see again.”')}", "MARK 10:51"),
    ("story-hebrews-10-23", "When you do not<br>see it yet",
     "Let us hold resolutely to the hope we profess, for He who promised is faithful.", "HEBREWS 10:23"),
    ("story-hebrews-4-16", "If you are<br>still sick",
     "Let us then approach the throne of grace with confidence, so that we may receive mercy and find grace to help us in our time of need.", "HEBREWS 4:16"),
]

def html(title, verse, ref):
    return f"""<!doctype html><html><head><meta charset=utf-8><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:{NAVY}}}
body{{font-family:Carlito,sans-serif;-webkit-font-smoothing:antialiased}}
.f1,.f2{{position:absolute;border:2px solid {GOLD}}} .f1{{inset:46px}} .f2{{inset:58px;border-width:1px;opacity:.75}}
.c{{position:absolute;left:120px;right:120px;top:250px;bottom:470px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}}
.c *{{text-wrap:balance}}
.em{{width:118px;height:118px;color:{GOLD}}}
.label{{font-weight:700;font-size:30px;letter-spacing:.34em;color:{GOLD};margin-top:30px}}
.title{{font-family:Gelasio;font-style:italic;font-weight:500;font-size:72px;line-height:1.15;color:{GOLD};margin-top:24px}}
.bar{{width:120px;height:3px;background:{GOLD};margin:34px auto 38px}}
.verse{{font-family:Gelasio;font-size:{52 if len(re.sub('<[^>]+>', '', verse)) > 150 else 60}px;line-height:1.42;color:{CREAM};max-width:830px}}
.orn{{display:flex;align-items:center;gap:18px;margin:32px auto 24px}}
.orn span{{display:block;width:70px;height:1.5px;background:{GOLD}}} .orn i{{display:block;width:14px;height:14px;background:{GOLD};transform:rotate(45deg)}}
.ref{{font-weight:700;font-size:34px;letter-spacing:.2em;color:{GOLD}}}
.healer{{font-family:Gelasio;font-style:italic;font-weight:500;font-size:56px;color:{GOLD};margin-top:36px}}
</style></head><body><div class="f1"></div><div class="f2"></div><div class="c">
<div class="em">{EMBLEM}</div><div class="label">STAND ON THIS</div><div class="title">{title}</div><div class="bar"></div>
<div class="verse">{verse}</div><div class="orn"><span></span><i></i><span></span></div><div class="ref">{ref}</div>
<div class="healer">Jesus is the healer.</div></div></body></html>"""

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    report = {}
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        for slug, title, verse, ref in STORIES:
            pg.set_content(html(title, verse, ref), wait_until="load"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(150)
            top, low, right = pg.evaluate("""() => { let t=1e9,m=0,r=0; for (const e of document.querySelectorAll('.c *')) { const b=e.getBoundingClientRect(); if (b.height) { t=Math.min(t,b.top); m=Math.max(m,b.bottom); r=Math.max(r,b.right);} } return [Math.round(t),Math.round(m),Math.round(r)]; }""")
            f = OUT / f"{slug}_1080x1920.png"; pg.screenshot(path=str(f))
            report[slug] = {"top": top, "lowest": low, "right": right}
        b.close()
    print(json.dumps(report))
