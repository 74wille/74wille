# Bygger profilens SVG-grafik till ../assets. Kör: python src/build.py
# Stil: mörk grafit, ett enda typsnitt (Familjen Grotesk, ritat i Stockholm), inga ramar eller etiketter.
# Det enda som sticker ut är det jättestora namnet som skärs av i bannerns nederkant.
import base64, pathlib

SRC = pathlib.Path(__file__).parent
OUT = SRC.parent / "assets"
OUT.mkdir(exist_ok=True)

def b64(name): return base64.b64encode((SRC / name).read_bytes()).decode()

FONTS = "".join(f"@font-face{{font-family:F;font-weight:{w};src:url(data:font/woff2;base64,{b64(f'familjen-{w}.woff2')})}}"
                for w in (400, 700))
GRAPHITE, PAPER, STONE, MOSS = "#1b1f1d", "#d8d5cc", "#8c918a", "#6b736d"
STYLE = f"{FONTS}text{{font-family:F,Arial,sans-serif}}"

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace("'", "&#8217;")

def svg(W, H, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<style>{STYLE}</style>{body}</svg>')

def T(x, y, s, txt, fill=PAPER, w=400, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{s}" font-weight="{w}" fill="{fill}" {extra}>{txt}</text>'

# ---------- banner ----------
def header():
    W, H = 1280, 360
    return svg(W, H, f'''<clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath>
<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{GRAPHITE}"/>
{T(64, 92, 26, "I make apps, mostly for myself, sometimes for you.", STONE)}
{T(44, 440, 400, "wille", PAPER, 700, 'letter-spacing="-18"')}</g>''')

# ---------- appar (tre i bredd, en bild per länk) ----------
def card(name, desc, plat):
    W, H = 420, 190
    return svg(W, H, f'''<rect width="{W}" height="{H}" rx="8" fill="{GRAPHITE}"/>
{T(32, 66, 30, esc(name), PAPER, 700, 'letter-spacing="-.5"')}
{T(32, 104, 19, esc(desc), STONE)}
{T(32, 158, 16, plat, MOSS)}''')

# ---------- rubriker ----------
def title(text):
    return svg(1280, 72, T(4, 48, 26, text, STONE, 700, 'letter-spacing="-.3"'))

def footer():
    W = 1280
    return svg(W, 70, T(W / 2, 40, 17, "Stockholm", MOSS, 400, 'text-anchor="middle"'))

APPS = (("Wille's Journal", "Log your trades and see what works.", "Windows and Mac"),
        ("Wille's Desktop", "Widgets and taskbar tweaks.", "Windows"),
        ("PromptForge", "A terminal you set up with checkboxes.", "Windows"))
files = {"banner.svg": header(), "footer.svg": footer(),
         "title-work.svg": title("Things I've made"),
         "title-stack.svg": title("What I use"),
         "title-activity.svg": title("Lately")}
for key, app in zip(("journal", "desktop", "promptforge"), APPS):
    files[f"card-{key}.svg"] = card(*app)
for n, s in files.items():
    (OUT / n).write_text(s, encoding="utf-8")
    print(n, len(s) // 1024, "KB")
