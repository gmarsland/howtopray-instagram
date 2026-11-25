"""Cover art for the podcast "How to Pray for the Sick and Expect a Miracle".

Version 2 (26 November 2026): the episodes follow the people who listen (eight lenses), not the
chapters of the book. The episode list is lens_episodes.json, made by lens_plan.py.

One square cover for the show and one for each of the first 24 episodes, in the book's own style:
navy, gold and cream, Gelasio and Carlito, the double gold frame and the sun-cross emblem used for
the Instagram posts and the "Stand on this" videos. Each episode has its own gold line picture,
taken from its Bible story or Scripture, and the lens it speaks to.

Usage:  python3 make_covers.py OUTDIR            all covers, a contact sheet and episodes.json
        python3 make_covers.py OUTDIR motifs     only a sheet of the pictures, for checking

Writes  OUTDIR/covers/3000/episode-NN.png and show.png   (3000 x 3000, for podcast hosts)
        OUTDIR/covers/1000/episode-NN.jpg and show.jpg   (1000 x 1000, for web pages)
        OUTDIR/covers/contact-sheet.png
        OUTDIR/episodes.json
"""
import json, pathlib, sys
from playwright.sync_api import sync_playwright
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
NAVY, GOLD, CREAM = "#13233f", "#d6b668", "#f5f0e4"
ADDRESS = "https://howtoprayforthesickandexpectamiracle.com"
EMBLEM = ('<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round">'
          '<circle cx="32" cy="32" r="13"/><path d="M32 24v16M27 29h10"/><g stroke-width="1.4">'
          '<path d="M32 6v7M32 51v7M6 32h7M51 32h7M13.6 13.6l5 5M45.4 45.4l5 5M13.6 50.4l5-5M45.4 18.6l5-5"/></g></svg>')
FONTS = """
@font-face{font-family:Gelasio;src:url(file:///usr/share/fonts/truetype/google-fonts/ofl/gelasio/Gelasio[wght].ttf);font-weight:400 700;font-style:normal}
@font-face{font-family:Gelasio;src:url(file:///usr/share/fonts/truetype/google-fonts/ofl/gelasio/Gelasio-Italic[wght].ttf);font-weight:400 700;font-style:italic}
@font-face{font-family:Carlito;src:url(file:///usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf);font-weight:400}
@font-face{font-family:Carlito;src:url(file:///usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf);font-weight:700}
"""

# The pictures, by subject. Each is drawn in a 200 x 200 box with gold lines.
# class t = thin line, class f = filled.
M = {
 'key': '<g transform="rotate(-35 100 100)"><circle cx="60" cy="100" r="27"/><circle cx="60" cy="100" r="9"/>'
    '<path d="M87 100H170M150 100v22M165 100v15"/></g>',                                   # the key to prayer
 'hand': '<path d="M78 174V130L62 112Q54 102 61 95Q68 89 75 97L88 113V66A8 8 0 0 1 104 66V54A8 8 0 0 1 120 54V62'
    'A8 8 0 0 1 136 62V78A7 7 0 0 1 150 78V132Q150 158 134 174"/>'
    '<path class="t" d="M104 68V104M120 64V104M136 80V106M70 174H142"/>'
    '<path class="t" d="M100 22v12M70 30l6 10M130 30l-6 10"/>',                             # Jesus reached out His hand
 'marah': '<path d="M26 128q12.3-13 24.6 0t24.6 0 24.6 0 24.6 0 24.6 0 24.6 0"/>'
    '<path class="t" d="M38 150q11-11 22 0t22 0 22 0 22 0 22 0M58 170q10.5-10 21 0t21 0 21 0 21 0"/>'
    '<path d="M146 30L92 116"/><path d="M128 59l-22-6M114 81l22 8M135 47l17 10"/>'
    '<path class="t" d="M76 108q16-12 32 0"/>',                                            # the wood and the water at Marah
 'cross': '<path d="M100 40V150M70 76H130"/><path d="M28 172Q100 122 172 172"/>'
    '<path class="t" d="M100 14v12M58 34l8 9M142 34l-8 9M38 66l11 5M162 66l-11 5"/>',     # the cross
 'people': '<circle cx="60" cy="76" r="13"/><path d="M34 140Q34 102 60 102Q72 102 80 110"/>'
    '<circle cx="140" cy="76" r="13"/><path d="M166 140Q166 102 140 102Q128 102 120 110"/>'
    '<circle cx="100" cy="84" r="17"/><path d="M64 164Q64 116 100 116Q136 116 136 164"/>', # every believer
 'bible': '<path d="M100 84Q68 66 32 78V156Q68 144 100 162Q132 144 168 156V78Q132 66 100 84ZM100 84V162"/>'
    '<path class="t" d="M48 96Q70 88 88 98M48 114Q70 106 88 116M48 132Q70 124 88 134M112 98Q130 88 152 96'
    'M112 116Q130 106 152 114M112 134Q130 124 152 132"/>'
    '<path class="t" d="M100 30v24M66 38l8 20M134 38l-8 20"/>',                            # He sent His word
 'eye': '<path d="M26 108Q100 42 174 108Q100 174 26 108Z"/><circle cx="100" cy="108" r="27"/>'
    '<circle class="f" cx="100" cy="108" r="10"/>'
    '<path class="t" d="M100 28v18M62 38l7 16M138 38l-7 16M30 62l12 12M170 62l-12 12"/>', # "let me see again"
 'bread': '<path d="M58 80Q58 46 100 46Q142 46 142 80Q142 92 130 92H70Q58 92 58 80Z"/>'
    '<path class="t" d="M82 56l-7 20M101 54l-7 22M120 56l-7 20"/>'
    '<path d="M168 156L140 136Q88 96 36 136Q88 176 140 136L168 116"/><circle class="f" cx="60" cy="132" r="3.5"/>',  # bread and a fish: a father's good gifts
 'gate': '<path d="M46 170V86Q46 34 100 34Q154 34 154 86V170"/><path d="M68 170V92Q68 58 100 58Q132 58 132 92V170"/>'
    '<path d="M30 170H170"/><path class="t" d="M20 184H180M100 58V170M46 92H68M132 92H154"/>'
    '<circle class="f" cx="92" cy="122" r="2.6"/><circle class="f" cx="108" cy="122" r="2.6"/>',  # the gate called Beautiful
 'cloak': '<path d="M84 38L42 64L34 104L62 100L66 160H134L138 100L166 104L158 64L116 38"/><path d="M84 38Q100 54 116 38"/>'
     '<path class="t" d="M88 72Q83 118 86 158M112 72Q117 118 114 158"/>'
     '<path d="M70 160v16M83 160v16M96 160v16M109 160v16M122 160v16"/><path class="t" d="M132 160v14"/>',  # the cloak she touched
 'flame': '<path d="M82 100H118V168H82Z"/><path d="M60 170H140"/><path class="t" d="M100 100V88M92 100v16"/>'
     '<path d="M100 40Q120 68 100 88Q80 68 100 40Z"/>'
     '<path class="t" d="M100 16v10M68 34l8 8M132 34l-8 8M56 64h12M132 64h12"/>',          # a small flame: "I do believe; help my unbelief!"
 'rock': '<path d="M60 138L74 86L100 58L130 80L144 138"/><path class="t" d="M100 58L106 102L130 80M106 102L94 138"/>'
     '<path d="M18 140q10.5-11 21 0t21 0M144 140q9.5-11 19 0t19 0"/>'
     '<path class="t" d="M30 160q11.7-11 23.4 0t23.4 0 23.4 0 23.4 0 23.4 0 23.4 0M54 178q11.5-10 23 0t23 0 23 0 23 0"/>',  # a wave or a rock
 'fire': '<path d="M46 172H154V150H46ZM82 150V172M118 150V172M58 150V128H142V150M100 128V150"/>'
     '<path d="M100 36C126 68 134 90 119 110C110 121 90 121 81 110C66 90 84 76 100 36Z"/>'
     '<path class="t" d="M100 78C110 92 110 104 100 111C90 104 90 92 100 78ZM64 100Q56 112 64 124M136 100Q144 112 136 124"/>',  # fire on Carmel
 'tomb': '<path d="M14 168H186"/><path d="M26 168Q30 52 104 48Q178 52 182 168"/>'
     '<path d="M62 168V122Q62 92 90 92Q118 92 118 122V168"/><circle cx="148" cy="138" r="28"/>'
     '<path class="t" d="M90 106v14M76 112l5 12M104 112l-5 12M104 22v12M64 30l6 10M144 30l-6 10"/>',  # the stone rolled away
 'crown': '<path d="M36 74L72 106L100 56L128 106L164 74L156 152H44Z"/><path class="t" d="M46 132H154"/>'
     '<circle class="f" cx="36" cy="68" r="5.5"/><circle class="f" cx="100" cy="50" r="5.5"/><circle class="f" cx="164" cy="68" r="5.5"/>'
     '<circle class="f" cx="76" cy="142" r="3"/><circle class="f" cx="100" cy="142" r="3"/><circle class="f" cx="124" cy="142" r="3"/>',  # the name above every name
 'needle': '<path d="M136 60L58 154"/><ellipse cx="142" cy="52" rx="5" ry="11" transform="rotate(40 142 52)"/>'
     '<path class="t" d="M142 52C178 68 172 106 140 110C108 114 96 138 126 148"/>'
     '<circle cx="150" cy="152" r="17"/><circle class="f" cx="144" cy="146" r="2.4"/><circle class="f" cx="156" cy="146" r="2.4"/>'
     '<circle class="f" cx="144" cy="158" r="2.4"/><circle class="f" cx="156" cy="158" r="2.4"/>',  # Tabitha's needle and thread
 'heart': '<path d="M100 166C38 120 30 88 43 67C58 43 90 50 100 78C110 50 142 43 157 67C170 88 162 120 100 166Z"/>'
     '<path class="t" d="M100 142C60 112 56 94 62 82C71 68 90 72 100 92C110 72 129 68 138 82C144 94 140 112 100 142Z"/>',  # moved with compassion
 'hand-in-hand': '<circle cx="126" cy="54" r="11"/><path d="M126 66V118M126 118L113 166M126 118L140 166M126 80L148 102M126 80L101 100"/>'
     '<circle cx="76" cy="62" r="11"/><path d="M76 74V122M76 122L64 166M76 122L88 166M76 86L101 100M76 86L60 110"/>'
     '<path class="t" d="M36 174H164"/>',                                                 # led by the hand
 'oil': '<path d="M78 84Q50 104 50 132Q50 170 100 170Q150 170 150 132Q150 104 122 84"/><path d="M78 84V60H122V84M70 60H130"/>'
     '<path d="M90 60V46H110V60"/><path class="f" d="M100 106Q117 130 100 146Q83 130 100 106Z"/>',  # oil
 'ten': ''.join(f'<circle cx="{x}" cy="{y}" r="10.5"/>' for y in (40, 72, 104) for x in (64, 100, 136))
     + '<circle class="f" cx="100" cy="158" r="13"/><path class="t" d="M152 120Q170 150 128 158M128 158l12-9M128 158l13 5"/>',  # ten, and the one who came back
 'sunrise': '<path d="M22 140H178"/><path d="M56 140A44 44 0 0 1 144 140"/>'
     '<path d="M100 84V62M128 91.5L138.5 73.3M72 91.5L61.5 73.3M148.5 112L166.6 101.5M51.5 112L33.4 101.5"/>'
     '<path class="t" d="M46 156H154M68 172H132"/>',                                       # a new day
 'kneel': '<circle cx="98" cy="54" r="12"/><path d="M96 68L88 126L120 158M120 160H60M95 82L114 100L130 78"/>'
     '<path class="t" d="M36 168H164M140 44l10-14M152 60l16-8M124 34l2-16"/>',             # pray, and do not lose heart
 'cloud': '<path d="M22 138H178"/><path d="M80 112Q62 112 64 97Q66 84 81 86Q85 68 103 70Q119 70 123 86Q139 84 141 98Q141 112 127 112Z"/>'
     '<path class="t" d="M34 156q11-11 22 0t22 0 22 0 22 0 22 0 22 0M56 174q11-10 22 0t22 0 22 0 22 0"/>'
     + ''.join(f'<circle class="f" cx="{x}" cy="{y}" r="2.8"/>' for x, y in ((46, 62), (62, 44), (82, 34), (103, 30), (124, 34), (144, 44), (160, 62))),  # the seventh time: a small cloud from the sea
 'road': '<path d="M20 66H93M107 66H180"/><path d="M38 184L93 66M162 184L107 66"/>'
     '<path class="t" d="M100 84v10M100 102v8"/><path class="t" d="M100 40v12M72 46l6 10M128 46l-6 10"/>'
     '<circle cx="87" cy="124" r="7"/><path d="M87 131V154L80 172M87 154L94 172M87 138L78 149"/>'
     '<circle cx="113" cy="124" r="7"/><path d="M113 131V154L106 172M113 154L120 172M113 138L122 149"/>',  # sent out two by two
 'crowd': ''.join(f'<path class="t" d="M{x+9} {y-9}L{x} {y}L{x+9} {y+9}"/>' for y in (58, 142) for x in (34, 64, 94, 124, 154))
     + ''.join(f'<path class="t" d="M{x+7} {y-7}L{x} {y}L{x+7} {y+7}"/>' for y in (30, 170) for x in (64, 94, 124))
     + '<path d="M28 100H164M146 82l18 18-18 18"/><circle class="f" cx="40" cy="100" r="8"/>',  # one person walking against the crowd
}

PICTURE = {"key": "A key (the key to prayer)", "hand": "An outstretched hand (\u201cI am willing\u201d)",
           "marah": "A piece of wood and the water at Marah", "cross": "The cross", "people": "Three people (every believer)",
           "bible": "An open Bible (He sent His word)", "eye": "An eye (\u201clet me see again\u201d)",
           "bread": "Bread and a fish (a father\u2019s good gifts)", "gate": "The gate called Beautiful",
           "cloak": "The cloak she touched", "flame": "A small flame (\u201cI do believe; help my unbelief!\u201d)",
           "rock": "A rock in the waves (Peter on the water)", "fire": "The altar and the fire on Carmel",
           "tomb": "The stone rolled away", "crown": "A crown (the name above every name)", "needle": "A needle and thread (Tabitha)",
           "heart": "A heart (moved with compassion)", "hand-in-hand": "One person leading another by the hand",
           "oil": "A flask of oil (James 5:14)", "ten": "Ten, and the one who came back",
           "sunrise": "A sunrise (when you do not see it yet)", "kneel": "A person kneeling in prayer",
           "cloud": "A small cloud rising from the sea, and seven marks", "road": "A road, and two people setting out",
           "crowd": "One person walking against the crowd"}
LENGTH = {}        # filled in as each episode is made, for example {1: "18:40"}
PILOTS = {1, 2, 5}  # made first, for Graham to hear
# where a title should break, when the automatic break reads badly
BREAKS = {16: "Why Do Christians Pray<br>\u201cin Jesus\u2019 Name\u201d?"}


def load():
    data = json.loads((HERE / "lens_episodes.json").read_text())
    return data["lenses"], data["episodes"]


def slug(t):
    s = "".join(c.lower() if c.isalnum() else "-" for c in t.replace("\u2019", "").replace("\u201c", "").replace("\u201d", ""))
    while "--" in s:
        s = s.replace("--", "-")
    return s.strip("-")


def svg(key, px):
    return (f'<svg width="{px}" height="{px}" viewBox="0 0 200 200" fill="none" stroke="currentColor" stroke-width="3.4" '
            f'stroke-linecap="round" stroke-linejoin="round">{M[key]}</svg>')


BASE = f"""{FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1500px;height:1500px;overflow:hidden;background:{NAVY}}}
body{{font-family:Carlito,sans-serif;-webkit-font-smoothing:antialiased;text-rendering:geometricPrecision;text-align:center;color:{CREAM}}}
.f1,.f2{{position:absolute;border:3px solid {GOLD}}} .f1{{inset:54px}} .f2{{inset:70px;border-width:1.5px;opacity:.75}}
svg .t{{stroke-width:2.2;opacity:.85}} svg .f{{fill:currentColor;stroke:none}}
.top{{position:absolute;left:0;right:0;top:116px}}
.bt1{{font-weight:700;font-size:40px;letter-spacing:.2em;padding-left:.2em}}
.bt2{{font-family:Gelasio;font-style:italic;font-weight:500;font-size:50px;color:{GOLD};margin-top:2px}}
.pod{{display:flex;align-items:center;justify-content:center;gap:22px;margin-top:20px;font-weight:700;font-size:27px;letter-spacing:.42em;color:{GOLD}}}
.pod b{{padding-left:.42em}} .pod i{{display:block;width:76px;height:1.5px;background:{GOLD}}}
.ring{{position:absolute;left:50%;top:322px;width:552px;height:552px;margin-left:-276px;border:3px solid {GOLD};border-radius:50%;
 display:flex;align-items:center;justify-content:center;color:{GOLD}}}
.ring:before{{content:"";position:absolute;inset:15px;border:1.5px solid {GOLD};border-radius:50%;opacity:.6}}
.lens{{position:absolute;left:150px;right:150px;top:910px;font-weight:700;font-size:29px;letter-spacing:.24em;padding-left:.24em;color:{GOLD};text-transform:uppercase}}
.title{{position:absolute;left:150px;right:150px;top:962px;height:252px;display:flex;align-items:center;justify-content:center}}
.title span{{font-family:Gelasio;font-weight:500;line-height:1.13;text-wrap:balance;display:block}}
.foot{{position:absolute;left:0;right:0;top:1240px}}
.orn{{display:flex;align-items:center;justify-content:center;gap:20px}}
.orn span{{display:block;width:84px;height:2px;background:{GOLD}}} .orn i{{display:block;width:16px;height:16px;background:{GOLD};transform:rotate(45deg)}}
.ref{{font-weight:700;font-size:44px;letter-spacing:.22em;color:{GOLD};padding-left:.22em;margin-top:34px}}
"""
HEAD = ('<div class="f1"></div><div class="f2"></div><div class="top"><div class="bt1">HOW TO PRAY FOR THE SICK</div>'
        '<div class="bt2">and Expect a Miracle</div><div class="pod"><i></i><b>THE PODCAST</b><i></i></div></div>')


def cover(e):
    t = e["title"]; size = 100 if len(t) <= 24 else 92 if len(t) <= 34 else 84
    return (f'<!doctype html><html><head><meta charset=utf-8><style>{BASE}</style></head><body>{HEAD}'
            f'<div class="ring">{svg(e["picture"], 400)}</div>'
            f'<div class="lens">{e["lensTitle"]}</div>'
            f'<div class="title"><span style="font-size:{size}px">{BREAKS.get(e["number"], t)}</span></div>'
            f'<div class="foot"><div class="orn"><span></span><i></i><span></span></div><div class="ref">{e["scripture"].upper()}</div></div>'
            f'</body></html>')


def show_cover():
    return (f'<!doctype html><html><head><meta charset=utf-8><style>{BASE}'
            f'.em{{position:absolute;left:50%;top:150px;width:330px;height:330px;margin-left:-165px;color:{GOLD}}}'
            f'.s1{{position:absolute;left:0;right:0;top:520px;font-weight:700;font-size:92px;letter-spacing:.1em;padding-left:.1em;line-height:1.16}}'
            f'.s2{{position:absolute;left:0;right:0;top:752px;font-family:Gelasio;font-style:italic;font-weight:500;font-size:124px;color:{GOLD}}}'
            f'.s3{{position:absolute;left:0;right:0;top:948px}} .s3 .pod{{font-size:44px;margin:0}} .s3 .pod i{{width:130px;height:2px}}'
            f'.s4{{position:absolute;left:0;right:0;top:1090px;font-family:Gelasio;font-style:italic;font-weight:500;font-size:74px;color:{CREAM}}}'
            f'.s5{{position:absolute;left:0;right:0;top:1262px;font-weight:700;font-size:40px;letter-spacing:.32em;padding-left:.32em;color:{GOLD}}}'
            f'</style></head><body><div class="f1"></div><div class="f2"></div><div class="em">{EMBLEM}</div>'
            f'<div class="s1">HOW TO PRAY<br>FOR THE SICK</div><div class="s2">and Expect a Miracle</div>'
            f'<div class="s3"><div class="pod"><i></i><b>THE PODCAST</b><i></i></div></div>'
            f'<div class="s4">Jesus is the healer.</div><div class="s5">GRAHAM MARSLAND</div></body></html>')


def motif_sheet():
    cells = "".join(f'<div style="width:250px;height:290px;color:{GOLD};text-align:center">{svg(k, 230)}'
                    f'<div style="font:700 20px Carlito;color:{CREAM}">{k}</div></div>' for k in sorted(M))
    return (f'<!doctype html><html><head><meta charset=utf-8><style>{FONTS}svg .t{{stroke-width:2.2;opacity:.85}} svg .f{{fill:currentColor;stroke:none}}'
            f'body{{margin:0;background:{NAVY};width:1500px;display:flex;flex-wrap:wrap}}</style></head><body>{cells}</body></html>')


def main():
    out = pathlib.Path(sys.argv[1]); only_motifs = len(sys.argv) > 2 and sys.argv[2] == "motifs"
    lenses, eps = load()
    assert len({e["picture"] for e in eps}) == len(eps) and all(e["picture"] in M for e in eps)
    big = out / "covers" / "3000"; web = out / "covers" / "1000"
    big.mkdir(parents=True, exist_ok=True); web.mkdir(parents=True, exist_ok=True)
    report = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        if only_motifs:
            pg = b.new_page(viewport={"width": 1500, "height": 1450}, device_scale_factor=1)
            pg.set_content(motif_sheet(), wait_until="load"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(200)
            pg.screenshot(path=str(out / "motifs.png")); b.close(); print("motifs.png"); return
        pg = b.new_page(viewport={"width": 1500, "height": 1500}, device_scale_factor=2)
        jobs = [("show", show_cover())] + [(f"episode-{e['number']:02d}", cover(e)) for e in eps]
        for name, html in jobs:
            pg.set_content(html, wait_until="load"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(150)
            if name != "show":
                box = pg.evaluate("(() => { const s=document.querySelector('.title span').getBoundingClientRect(); const a=document.querySelector('.title').getBoundingClientRect(); const l=document.querySelector('.lens').getBoundingClientRect(); return [Math.round(s.left),Math.round(s.right),Math.round(s.height),Math.round(a.height), Math.round(s.height / parseFloat(getComputedStyle(document.querySelector('.title span')).lineHeight)), Math.round(l.height)]; })()")
                report.append({"file": name, "lines": box[4], "lens_lines": round(box[5] / 33),
                               "fits": box[0] >= 150 and box[1] <= 1350 and box[2] <= box[3] and box[5] <= 40})
            pg.screenshot(path=str(big / f"{name}.png"))
        b.close()
    for name, _ in jobs:
        im = Image.open(big / f"{name}.png").convert("RGB")
        assert im.size == (3000, 3000), im.size
        im.save(big / f"{name}.png", optimize=True)
        im.resize((1000, 1000), Image.LANCZOS).save(web / f"{name}.jpg", quality=90, optimize=True, progressive=True)
    names = [n for n, _ in jobs]; cols, cell, gap = 5, 560, 24
    rows = -(-len(names) // cols)
    sheet = Image.new("RGB", (cols * cell + (cols + 1) * gap, rows * cell + (rows + 1) * gap), "#ffffff")
    for i, name in enumerate(names):
        im = Image.open(web / f"{name}.jpg").resize((cell, cell), Image.LANCZOS)
        sheet.paste(im, (gap + (i % cols) * (cell + gap), gap + (i // cols) * (cell + gap)))
    sheet.save(out / "covers" / "contact-sheet.png", optimize=True)
    episodes = [{"number": e["number"], "slug": slug(e["title"]), "title": e["title"],
                 "lens": e["lens"], "lensTitle": e["lensTitle"], "fromTheBook": e["sources"],
                 "scripture": e["scripture"], "description": e["description"], "picture": PICTURE[e["picture"]],
                 "cover": f"covers/1000/episode-{e['number']:02d}.jpg", "coverLarge": f"covers/3000/episode-{e['number']:02d}.png",
                 "length": LENGTH.get(e["number"]), "pilot": e["number"] in PILOTS,
                 "audioFile": f"episode-{e['number']:02d}.mp3", "audioUrl": None, "approved": False} for e in eps]
    (out / "episodes.json").write_text(json.dumps({
        "show": {"title": "How to Pray for the Sick and Expect a Miracle", "subtitle": "The podcast of the book by Graham Marsland",
                 "cover": "covers/1000/show.jpg", "coverLarge": "covers/3000/show.png", "website": ADDRESS,
                 "voices": "Two voices made with artificial intelligence talk through Graham Marsland\u2019s book and the Bible, one question at a time. Everything they say comes from the book and from the Bible."},
        "lenses": lenses, "episodes": episodes}, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps({"covers": len(jobs), "all_fit": all(r["fits"] for r in report),
                      "not_fitting": [r for r in report if not r["fits"]],
                      "lines": {r["file"][-2:]: r["lines"] for r in report},
                      "lens_lines": sorted({r["lens_lines"] for r in report})}))


if __name__ == "__main__":
    main()
