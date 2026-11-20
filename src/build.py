# Bygger profilens SVG-grafik till ../assets. Kör: python src/build.py
# Stil: mörk, minimalistisk och nonchalant – monospace, gemener, grå toner och en blinkande markör.
import base64, pathlib

SRC = pathlib.Path(__file__).parent
OUT = SRC.parent / "assets"
OUT.mkdir(exist_ok=True)

def b64(name): return base64.b64encode((SRC / name).read_bytes()).decode()

FONTS = "".join(f"@font-face{{font-family:M;font-weight:{w};src:url(data:font/woff2;base64,{b64(f)})}}"
                for w, f in ((500, "mono-500.woff2"), (700, "mono-700.woff2")))
BG, LINE, FG, DIM, FAINT = "#0d1117", "#21262d", "#e6edf3", "#7d8590", "#484f58"
STYLE = f"""{FONTS}text{{font-family:M,ui-monospace,Menlo,Consolas,monospace}}
.blink{{animation:bl 1.1s steps(1) infinite}}@keyframes bl{{50%{{opacity:0}}}}"""

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace("'", "&#8217;")

def svg(W, H, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<style>{STYLE}</style>{body}</svg>')

def T(x, y, s, txt, fill=FG, w=500, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{s}" font-weight="{w}" fill="{fill}" {extra}>{txt}</text>'

# ---------- banner ----------
def header():
    W, H = 1280, 300
    return svg(W, H, f'''<rect width="{W}" height="{H}" rx="12" fill="{BG}" stroke="{LINE}"/>
{T(64, 74, 18, "~/wille", FAINT)}
{T(1216, 74, 18, "stockholm, se", FAINT, 500, 'text-anchor="end"')}
{T(60, 176, 84, "wille", FG, 700)}
<rect class="blink" x="330" y="112" width="40" height="72" fill="{FG}"/>
{T(64, 236, 24, "full-stack dev. makes apps, ships some of them.", DIM)}''')

# ---------- projektkort (tre i bredd) ----------
def card(i, name, desc, plat):
    W, H = 420, 210
    return svg(W, H, f'''<g>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="{BG}" stroke="{LINE}"/>
{T(30, 62, 26, esc(name).lower(), FG, 700)}
{T(30, 104, 17, esc(desc).lower(), DIM)}
{T(30, 176, 14, plat.lower(), FAINT)}
{T(390, 176, 16, "get →", DIM, 500, 'text-anchor="end"')}</g>''')

# ---------- rubriker ----------
def title(text, note):
    W, H = 1280, 80
    return svg(W, H, f'''{T(4, 50, 22, f"// {text}", DIM, 700)}
{T(24 + len(text) * 13.5 + 40, 50, 18, note, FAINT)}''')

def footer():
    W = 1280
    return svg(W, 80, T(W / 2, 46, 18, "that's about it.", FAINT, 500, 'text-anchor="middle"'))

APPS = (("Wille's Journal", "Log every trade. See what works.", "windows · mac"),
        ("Wille's Desktop", "Widgets and taskbar tweaks.", "windows"),
        ("PromptForge", "A terminal set up with checkboxes.", "windows"))
files = {"banner.svg": header(), "footer.svg": footer(),
         "title-work.svg": title("shipped", "live, download if you want"),
         "title-stack.svg": title("tools", "what i use"),
         "title-activity.svg": title("activity", "commits")}
for i, (key, app) in enumerate(zip(("journal", "desktop", "promptforge"), APPS)):
    files[f"card-{key}.svg"] = card(i, *app)
for n, s in files.items():
    (OUT / n).write_text(s, encoding="utf-8")
    print(n, len(s) // 1024, "KB")
