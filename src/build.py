# Bygger profilens SVG-grafik till ../assets. Kör: python src/build.py
# Stil: zine/risograf – kopieringsbrus, rivna papperslappar, tejp, röd tusch och stämpel.
import base64, math, pathlib, random

SRC = pathlib.Path(__file__).parent
OUT = SRC.parent / "assets"
OUT.mkdir(exist_ok=True)

def b64(name): return base64.b64encode((SRC / name).read_bytes()).decode()

FONTS = "".join(f"@font-face{{font-family:R;font-weight:{w};src:url(data:font/woff2;base64,{b64(f)})}}"
                for w, f in ((700, "roboto-700.woff2"), (900, "roboto-900.woff2")))
RED, PAPER, INK, BG = "#ff2a4a", "#f1ece0", "#111111", "#141414"
STYLE = f"""{FONTS}text{{font-family:R,Roboto,Arial,sans-serif}}
.draw{{stroke-dasharray:var(--l);stroke-dashoffset:var(--l);animation:dr .9s cubic-bezier(.6,0,.3,1) var(--d,.3s) forwards}}
@keyframes dr{{to{{stroke-dashoffset:0}}}}
.drop{{opacity:0;animation:dp .5s cubic-bezier(.2,1.4,.4,1) var(--d,0s) forwards}}
@keyframes dp{{from{{opacity:0;transform:translateY(-24px)}}to{{opacity:1;transform:none}}}}"""
# rough = ojämna tryckkanter, grain = kopieringsbrus
DEFS = """<filter id="rough"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="3"/></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="3" seed="7" stitchTiles="stitch"/>
<feColorMatrix values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .09 0"/></filter>"""

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace("'", "&#8217;")

def svg(W, H, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<style>{STYLE}</style><defs>{DEFS}</defs>{body}</svg>')

def T(x, y, s, txt, fill=INK, w=900, ls=0, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{s}" font-weight="{w}" letter-spacing="{ls}" fill="{fill}" {extra}>{txt}</text>'

def torn(x, y, w, h, seed, fill=PAPER, edges="tb"):
    """Papperslapp med rivna kanter (t=topp, b=botten)."""
    r = random.Random(seed)
    def edge(y0, a, b):
        pts, xx = [], a
        while (xx < b) if a < b else (xx > b):
            pts.append(f"{xx:.0f} {y0 + r.uniform(-4, 4):.1f}"); xx += r.uniform(8, 22) * (1 if a < b else -1)
        return pts + [f"{b:.0f} {y0:.0f}"]
    top = edge(y, x, x + w) if "t" in edges else [f"{x} {y}", f"{x+w} {y}"]
    bot = edge(y + h, x + w, x) if "b" in edges else [f"{x+w} {y+h}", f"{x} {y+h}"]
    return f'<path d="M{" L".join(top + bot)}Z" fill="{fill}"/>'

def tape(cx, cy, w, rot, txt=""):
    t = T(cx, cy + 8, 20, txt, INK, 900, 2, 'text-anchor="middle"') if txt else ""
    return (f'<g transform="rotate({rot} {cx} {cy})"><rect x="{cx-w/2}" y="{cy-17}" width="{w}" height="34" '
            f'fill="#e9e1c8" fill-opacity=".82"/>{t}</g>')

def marker(x1, y, x2, seed, w=12, d=".3s", amp=4):
    r = random.Random(seed); pts, x = [(x1, y)], x1
    while x < x2:
        x = min(x + r.randint(40, 90), x2); pts.append((x, y + r.uniform(-amp, amp)))
    L = sum(math.dist(a, b) for a, b in zip(pts, pts[1:])) + 10
    d_ = "M" + " L".join(f"{a:.0f} {b:.1f}" for a, b in pts)
    return (f'<path class="draw" style="--l:{L:.0f};--d:{d}" d="{d_}" stroke="{RED}" stroke-width="{w}" '
            f'fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>')

def halftone(x0, y0, W, H, cx, cy, step=14, maxr=6.5):
    dots = []
    for x in range(x0, x0 + W, step):
        for y in range(y0, y0 + H, step):
            k = 1 - math.dist((x, y), (cx, cy)) / 420
            if k > .05: dots.append(f'<circle cx="{x}" cy="{y}" r="{maxr*k:.1f}"/>')
    return f'<g fill="{RED}" opacity=".85">{"".join(dots)}</g>'

# ---------- banner ----------
def header():
    W, H = 1280, 400
    return svg(W, H, f'''<rect width="{W}" height="{H}" fill="{BG}"/>
{halftone(820, 0, 460, 400, 1280, 0)}
<g filter="url(#rough)">
{T(54, 242, 236, "wille", RED, 900, -10, 'opacity=".9"')}
{T(46, 236, 236, "wille", PAPER, 900, -10)}
</g>
{marker(52, 272, 640, 3, 16)}
<g class="drop" style="--d:.9s" transform="rotate(-2 400 330)">{torn(40, 300, 640, 66, 5)}
{T(66, 346, 30, "makes apps. ships them. repeats.", INK, 900, -.5)}</g>
<g class="drop" style="--d:.6s">{tape(1040, 74, 290, 6, "STOCKHOLM, SWEDEN")}</g>
<rect width="{W}" height="{H}" filter="url(#grain)"/>''')

# ---------- projektlappar (tre i bredd) ----------
def card(i, name, desc, plat):
    W, H = 420, 250
    rot = (-2.2, 1.6, -1.2)[i]
    return svg(W, H, f'''<g class="drop" style="--d:{.15*i:.2f}s"><g transform="rotate({rot} 210 130)">
<rect x="22" y="34" width="376" height="190" fill="#000" opacity=".35" transform="translate(6 7)"/>
{torn(22, 34, 376, 190, 20 + i, PAPER, "b")}
{T(46, 102, 36, esc(name), INK, 900, -1)}
{marker(46, 118, 46 + len(name) * 17, 9 + i, 6, f"{.5 + .15*i:.2f}s", 2)}
{T(46, 156, 19, esc(desc), "#555", 700)}
{T(46, 200, 15, plat, RED, 900, 3)}
{T(374, 200, 18, "get it ↓", INK, 900, 0, 'text-anchor="end"')}
<rect x="22" y="34" width="376" height="190" filter="url(#grain)"/>
</g>{tape(210, 34, 120, (-4, 3, -2)[i])}</g>''')

# ---------- rubriker ----------
def title(text, note, seed):
    W, H = 1280, 96
    w = len(text) * 27 + 60
    return svg(W, H, f'''<g transform="rotate(-1.5 {w/2} 50)">{torn(0, 20, w, 58, seed)}
{T(28, 64, 38, text, INK, 900, 1)}</g>
{T(w + 34, 60, 22, note, "#8b949e", 700)}
{marker(w + 30, 72, w + 34 + len(note) * 11, seed, 4, ".4s", 2)}''')

def footer():
    W = 1280
    return svg(W, 100, f'''{marker(440, 30, 840, 2, 6, ".2s", 6)}
{T(W/2, 80, 22, "thanks for scrolling. now go ship something.", "#8b949e", 700, 0, 'text-anchor="middle"')}''')

APPS = (("Wille's Journal", "Log every trade. See what works.", "WINDOWS · MAC"),
        ("Wille's Desktop", "Widgets and taskbar tweaks.", "WINDOWS"),
        ("PromptForge", "A terminal set up with checkboxes.", "WINDOWS"))
files = {"header.svg": header(), "footer.svg": footer(),
         "title-work.svg": title("SHIPPED", "live, go download", 31),
         "title-stack.svg": title("TOOLS", "what i build with", 32),
         "title-activity.svg": title("ACTIVITY", "commits, eaten alive", 33)}
for i, (key, app) in enumerate(zip(("journal", "desktop", "promptforge"), APPS)):
    files[f"card-{key}.svg"] = card(i, *app)
for n, s in files.items():
    (OUT / n).write_text(s, encoding="utf-8")
    print(n, len(s) // 1024, "KB")
