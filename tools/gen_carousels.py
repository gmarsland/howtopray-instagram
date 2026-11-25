"""Builds the four carousels (five slides each, 1080 x 1350) in the book's style.
Words come from the website preview's cards page (cards.html, 24 November 2026);
every verse was checked against the Berean Standard Bible on 25 November 2026."""
import os, pathlib
from playwright.sync_api import sync_playwright

OUT = pathlib.Path("/home/claude/instagram/posts")
FONTS = """
@font-face{font-family:Gelasio;src:url(file:///usr/share/fonts/truetype/google-fonts/ofl/gelasio/Gelasio[wght].ttf);font-weight:400 700;font-style:normal}
@font-face{font-family:Gelasio;src:url(file:///usr/share/fonts/truetype/google-fonts/ofl/gelasio/Gelasio-Italic[wght].ttf);font-weight:400 700;font-style:italic}
@font-face{font-family:Carlito;src:url(file:///usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf);font-weight:400}
@font-face{font-family:Carlito;src:url(file:///usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf);font-weight:700}
@font-face{font-family:Carlito;src:url(file:///usr/share/fonts/truetype/crosextra/Carlito-Italic.ttf);font-style:italic}
"""
NAVY, GOLD, GOLD_D, GOLD_LINE, CREAM, PAPER = "#13233f", "#d6b668", "#7d5f1c", "#c5a352", "#f5f0e4", "#faf7f0"
EMBLEM = ('<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round">'
          '<circle cx="32" cy="32" r="13"/><path d="M32 24v16M27 29h10"/><g stroke-width="1.4">'
          '<path d="M32 6v7M32 51v7M6 32h7M51 32h7M13.6 13.6l5 5M45.4 45.4l5 5M13.6 50.4l5-5M45.4 18.6l5-5"/></g></svg>')
DIAMOND = '<div class="orn"><span></span><i></i><span></span></div>'
ADDRESS = "HowToPrayForTheSickAndExpectAMiracle.com"

CSS = FONTS + f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;overflow:hidden}}
body{{font-family:Carlito,sans-serif;-webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}}
.s *{{text-wrap:balance}}
.s{{position:relative;width:1080px;height:1350px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:150px 130px}}
.navy{{background:{NAVY};color:{CREAM}}}
.white{{background:#fff;color:{NAVY}}}
.paper{{background:{PAPER};color:{NAVY}}}
.navy:before,.navy:after{{content:"";position:absolute;border:2px solid {GOLD};pointer-events:none}}
.navy:before{{inset:46px}} .navy:after{{inset:58px;border-width:1px;opacity:.75}}
.white:before,.paper:before{{content:"";position:absolute;inset:52px;border:1.5px solid {GOLD_LINE}}}
.em{{width:118px;height:118px;color:{GOLD};margin-bottom:46px}}
.white .em,.paper .em{{color:{GOLD_LINE};width:84px;height:84px;margin-bottom:38px}}
.label{{font-family:Carlito;font-weight:700;font-size:28px;letter-spacing:.34em;text-transform:uppercase;color:{GOLD};margin-bottom:44px}}
.white .label,.paper .label{{color:{GOLD_D}}}
.title{{font-family:Gelasio;font-style:italic;font-weight:500;font-size:86px;line-height:1.14;color:{GOLD};max-width:820px}}
.bar{{width:120px;height:3px;background:{GOLD};margin:50px auto 46px}}
.sub{{font-size:38px;line-height:1.4;color:{CREAM};max-width:740px}}
.swipe{{position:absolute;bottom:96px;right:110px;font-family:Carlito;font-size:27px;letter-spacing:.22em;text-transform:uppercase;color:{GOLD};opacity:.9}}
.verse{{font-family:Gelasio;font-size:58px;line-height:1.46;color:{CREAM};max-width:820px}}
.orn{{display:flex;align-items:center;gap:18px;margin:52px auto 40px}}
.orn span{{display:block;width:70px;height:1.5px;background:{GOLD}}}
.orn i{{display:block;width:14px;height:14px;background:{GOLD};transform:rotate(45deg)}}
.white .orn span,.paper .orn span{{background:{GOLD_LINE}}} .white .orn i,.paper .orn i{{background:{GOLD_LINE}}}
.ref{{font-family:Carlito;font-weight:700;font-size:34px;letter-spacing:.2em;color:{GOLD}}}
.prayer{{font-family:Carlito;font-size:50px;line-height:1.55;color:{NAVY};max-width:820px}}
.gap{{display:inline-block;width:230px;border-bottom:3px solid {GOLD_LINE};transform:translateY(-10px)}}
.hint{{font-family:Carlito;font-style:italic;font-size:30px;color:#5b6577;margin-top:34px}}
.healer{{font-family:Gelasio;font-style:italic;font-size:44px;color:{GOLD_D}}}
.steps{{list-style:none;text-align:left;max-width:800px;margin-top:6px}}
.steps li{{display:flex;gap:34px;align-items:baseline;margin:0 0 46px}}
.steps .n{{font-family:Gelasio;font-style:italic;font-size:76px;line-height:1;color:{GOLD_LINE};min-width:52px}}
.steps b{{display:block;font-family:Gelasio;font-weight:600;font-size:48px;line-height:1.25;color:{NAVY}}}
.steps span{{display:block;font-size:36px;line-height:1.4;color:#3b4658;margin-top:8px}}
.note{{font-size:31px;line-height:1.45;color:#3b4658;max-width:760px;margin-top:4px}}
.big{{font-family:Gelasio;font-weight:500;font-size:74px;line-height:1.25;color:{NAVY};max-width:820px}}
.lines p{{font-family:Gelasio;font-size:52px;line-height:1.35;color:{NAVY};margin:0 0 44px;max-width:820px}}
.lines p.small{{font-family:Carlito;font-size:38px;line-height:1.45;color:#3b4658}}
.close .healer2{{font-family:Gelasio;font-style:italic;font-weight:500;font-size:84px;color:{GOLD};line-height:1.1}}
.ask{{font-size:44px;line-height:1.4;color:{CREAM};margin-top:58px;max-width:760px}}
.doc{{font-size:34px;color:{CREAM};opacity:.92;margin-top:48px;letter-spacing:.02em}}
.addr{{font-family:Carlito;font-size:29px;color:{GOLD};margin-top:70px;letter-spacing:.03em}}
.bsb{{position:absolute;bottom:92px;left:0;right:0;font-size:22px;letter-spacing:.12em;color:{CREAM};opacity:.55;text-transform:uppercase}}
"""

def page(cls, inner):
    return f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body><div class='s {cls}'>{inner}</div></body></html>"

def cover(title, sub):
    return page("navy", f"<div class='em'>{EMBLEM}</div><div class='label'>A prayer for the sick</div>"
                        f"<div class='title'>{title}</div><div class='bar'></div><div class='sub'>{sub}</div>"
                        "<div class='swipe'>Swipe &nbsp;&rarr;</div>")

def verse(text, ref):
    return page("navy", f"<div class='label'>Stand on this</div><div class='verse'>{text}</div>{DIAMOND}<div class='ref'>{ref}</div>")

def prayer(text, hint):
    return page("white", f"<div class='em'>{EMBLEM}</div><div class='label'>Pray this</div><div class='prayer'>{text}</div>"
                         f"<div class='hint'>{hint}</div>{DIAMOND}<div class='healer'>Jesus is the healer.</div>")

def how():
    return page("paper", "<div class='label'>When someone is sick</div><ol class='steps'>"
                "<li><span class='n'>1</span><div><b>Read the verse aloud.</b><span>It is what God has said.</span></div></li>"
                "<li><span class='n'>2</span><div><b>Pray the prayer.</b><span>Say their name where the line is.</span></div></li>"
                "<li><span class='n'>3</span><div><b>Expect Him to do what He said.</b><span>And when a healing comes, have it confirmed by a doctor, and give the glory to Jesus.</span></div></li>"
                "</ol>")

def close(invite):
    ask = "<div class='ask'>Who came to mind? Send this to them.</div>" if invite else ""
    return page("navy close", f"<div class='em'>{EMBLEM}</div><div class='healer2'>Jesus is the healer.</div>{ask}"
                              f"<div class='doc'>Keep seeing your doctor.</div><div class='addr'>{ADDRESS}</div>"
                              "<div class='bsb'>Scripture: Berean Standard Bible</div>")

GAP = "<span class='gap'></span>"
CAROUSELS = {
    "week-1-when-you-wonder-if-he-is-willing": [
        cover("When you wonder if He is willing", "God’s Word to stand on, and a prayer ready to pray."),
        verse("Moved with compassion, Jesus reached out His hand and touched the man. <span style='white-space:nowrap'>“I am willing,”</span> <span style='white-space:nowrap'>He said.</span> <span style='white-space:nowrap'>“Be clean!”</span>", "MARK 1:41"),
        prayer(f"Lord Jesus, You were willing then, and You have not changed. I <span style='white-space:nowrap'>bring {GAP}</span> to You. I ask You to heal them, in the name of Jesus Christ of Nazareth. Amen.",
               "Say their name where the line is."),
        how(),
        close(True),
    ],
    "week-2-when-you-need-something-to-stand-on": [
        cover("When you need something to stand on", "God’s Word to stand on, and a prayer ready to pray."),
        verse("He Himself bore our sins in His body on the tree, so that we might die to sin and live to righteousness. <span style='white-space:nowrap'>“By His stripes you are healed.”</span>", "1 PETER 2:24"),
        prayer(f"Father, thank You for the cross. You have said that by His stripes we are healed, and I stand on what You have said. I ask You to <span style='white-space:nowrap'>heal {GAP},</span> in the name of Jesus Christ of Nazareth. Amen.",
               "Say their name where the line is."),
        how(),
        close(False),
    ],
    "week-3-when-you-do-not-know-what-to-pray": [
        cover("When you do not know what to pray", "God’s Word to stand on, and a prayer ready to pray."),
        verse("“What do you want Me to do for you?” Jesus asked. “Rabboni,” said the blind man, <span style='white-space:nowrap'>“let me see again.”</span>", "MARK 10:51"),
        prayer(f"Lord Jesus, You asked a blind man what he wanted, and he told You plainly. So I tell You plainly what I am asking. I ask You <span style='white-space:nowrap'>to {GAP}.</span> In the name of Jesus Christ of Nazareth. Amen.",
               "Say plainly what you are asking where the line is."),
        how(),
        close(False),
    ],
    "week-4-if-you-are-still-sick": [
        cover("If you are still sick", "A word for you, and God’s Word to stand on."),
        verse("Let us then approach the throne of grace with confidence, so that we may receive mercy and find grace to help us in our time of need.", "HEBREWS 4:16"),
        page("white", f"<div class='em'>{EMBLEM}</div><div class='big'>You are not to blame, and you are not forgotten.</div>{DIAMOND}<div class='healer'>Jesus is the healer.</div>"),
        page("paper", "<div class='label'>For today</div><div class='lines'>"
                      "<p>Come to Him again today.</p><p>Ask others to pray with you.</p>"
                      "<p class='small'>Keep seeing your doctor. Jesus sent the man He healed to be examined (Mark 1:44).</p></div>"),
        close(True),
    ],
}

if __name__ == "__main__":
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for name, slides in CAROUSELS.items():
            d = OUT / name; d.mkdir(parents=True, exist_ok=True)
            for i, html in enumerate(slides, 1):
                f = d / f"{name}_slide-{i}_1080x1350.png"
                pg.set_content(html, wait_until="load"); pg.evaluate("document.fonts.ready")
                pg.wait_for_timeout(120)
                pg.screenshot(path=str(f), full_page=False)
                # overflow check: content must not run past the frame
                over = pg.evaluate("""() => { const s=document.querySelector('.s'); let m=0;
                    for (const e of s.querySelectorAll('*')) { const r=e.getBoundingClientRect(); if(r.height) m=Math.max(m,r.bottom);} return Math.round(m); }""")
                print(f.name, "lowest ink y =", over)
        b.close()
