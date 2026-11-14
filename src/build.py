# Bygger profilens SVG-grafik till ../assets. Kör: python src/build.py
import base64, pathlib, random

SRC = pathlib.Path(__file__).parent
OUT = SRC.parent / "assets"
OUT.mkdir(exist_ok=True)

def b64(name): return base64.b64encode((SRC / name).read_bytes()).decode()

FONTS = "".join(
    f"@font-face{{font-family:R;font-weight:{w};src:url(data:font/woff2;base64,{b64(f'roboto-{w}.woff2')})}}"
    for w in (400, 700, 900))

BG, LINE, ACC, ACC2, TXT, MUTED = "#0b0f14", "#1f2933", "#5b9bd5", "#a8d1f5", "#e6edf3", "#8b98a5"

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;")

# ---------- banner ----------
def header():
    random.seed(7)
    W, H = 1280, 360
    pixels = []
    for _ in range(46):
        x, y, s = random.randrange(20, W - 20), random.randrange(20, H - 20), random.choice((4, 6, 8))
        d, dur = random.random() * 4, 2.5 + random.random() * 3
        pixels.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{random.choice((ACC, ACC2, "#ffffff"))}" '
                      f'class="px" style="animation-delay:{d:.2f}s;animation-duration:{dur:.2f}s"/>')
    icons = [("WillesJournal-160.png", 930, 70, 0), ("PromptForge-160.png", 1090, 120, .8),
             ("WillesDesktop-160.png", 950, 200, 1.6), ("GasEgg-160.png", 1100, 260, 2.4)]
    ic = "".join(
        f'<g class="bob" style="animation-delay:{d}s"><rect x="{x-6}" y="{y-6}" width="{112 if i<3 else 92}" height="{112 if i<3 else 92}" rx="24" fill="#111821" stroke="{LINE}"/>'
        f'<image href="data:image/png;base64,{b64(n)}" x="{x+4}" y="{y+4}" width="{92 if i<3 else 72}" height="{92 if i<3 else 72}" clip-path="url(#c{i})"/></g>'
        f'<clipPath id="c{i}"><rect x="{x+4}" y="{y+4}" width="{92 if i<3 else 72}" height="{92 if i<3 else 72}" rx="18"/></clipPath>'
        for i, (n, x, y, d) in enumerate(icons))
    sub = "I build desktop apps, web apps and Roblox games."
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>{FONTS}
text{{font-family:R,Roboto,Helvetica,Arial,sans-serif}}
.px{{opacity:0;animation:tw ease-in-out infinite}}@keyframes tw{{50%{{opacity:.8}}}}
.bob{{animation:bob 6s ease-in-out infinite}}@keyframes bob{{50%{{transform:translateY(-10px)}}}}
.glow{{animation:drift 14s ease-in-out infinite alternate}}@keyframes drift{{to{{transform:translate(420px,60px)}}}}
.type{{clip-path:inset(0 100% 0 0);animation:type 3.2s steps({len(sub)}) .6s forwards}}@keyframes type{{to{{clip-path:inset(0 0 0 0)}}}}
.cur{{animation:blink 1s step-end infinite}}@keyframes blink{{50%{{opacity:0}}}}
.cur{{transform:translateX(0);animation:blink 1s step-end infinite,mv 3.2s steps({len(sub)}) .6s forwards}}@keyframes mv{{to{{transform:translateX(var(--w))}}}}
.in{{opacity:0;animation:in .9s ease-out forwards}}@keyframes in{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
</style>
<defs>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#ffffff" stroke-opacity=".045"/></pattern>
<radialGradient id="g1"><stop offset="0" stop-color="{ACC}" stop-opacity=".35"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/></radialGradient>
<linearGradient id="name" x1="0" x2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="{ACC2}"/><stop offset="1" stop-color="{ACC}"/></linearGradient>
<linearGradient id="fade" x1="0" x2="1"><stop offset=".55" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}" stop-opacity=".0"/></linearGradient>
<clipPath id="card"><rect width="{W}" height="{H}" rx="22"/></clipPath>
</defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect width="{W}" height="{H}" fill="url(#grid)"/>
<circle class="glow" cx="220" cy="120" r="380" fill="url(#g1)"/>
{''.join(pixels)}
<text class="in" x="72" y="96" font-size="17" font-weight="700" letter-spacing="5" fill="{ACC}">STOCKHOLM · SWEDEN</text>
<text class="in" x="64" y="222" font-size="150" font-weight="900" letter-spacing="-4" fill="url(#name)" style="animation-delay:.15s">WILLE</text>
<g style="--w:{len(sub)*12.35:.0f}px">
<text class="type" x="72" y="282" font-size="22" font-weight="400" fill="{TXT}">{sub}</text>
<rect class="cur" x="74" y="264" width="11" height="24" fill="{ACC}"/>
</g>
<text class="in" x="72" y="322" font-size="15" font-weight="700" letter-spacing="3" fill="{MUTED}" style="animation-delay:.4s">ELECTRON  ·  NEXT.JS  ·  SUPABASE  ·  LUAU</text>
{ic}
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="22" fill="none" stroke="{LINE}"/>
</g>
</svg>'''

# ---------- appkort ----------
def card(icon, name, lines, chips, cta, accent):
    W, H = 600, 250
    chip_svg, x = "", 196
    for c in chips:
        w = len(c) * 8.4 + 26
        chip_svg += f'<rect x="{x}" y="176" width="{w:.0f}" height="30" rx="15" fill="{accent}" fill-opacity=".14" stroke="{accent}" stroke-opacity=".5"/><text x="{x+w/2:.0f}" y="196" font-size="13" font-weight="700" fill="{accent}" text-anchor="middle" letter-spacing="1">{c}</text>'
        x += w + 10
    body = "".join(f'<text x="196" y="{112+i*24}" font-size="17" fill="{MUTED}">{esc(l)}</text>' for i, l in enumerate(lines))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>{FONTS}text{{font-family:R,Roboto,Helvetica,Arial,sans-serif}}
.sh{{animation:sh 5s ease-in-out infinite}}@keyframes sh{{0%,60%{{transform:translateX(-700px)}}100%{{transform:translateX(700px)}}}}
.bob{{animation:bob 5s ease-in-out infinite}}@keyframes bob{{50%{{transform:translateY(-5px)}}}}</style>
<defs><clipPath id="r"><rect width="{W}" height="{H}" rx="20"/></clipPath><clipPath id="i"><rect x="40" y="48" width="124" height="124" rx="28"/></clipPath>
<linearGradient id="s" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<radialGradient id="g" cx="0.15" cy="0.3" r=".7"><stop offset="0" stop-color="{accent}" stop-opacity=".22"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient></defs>
<g clip-path="url(#r)">
<rect width="{W}" height="{H}" fill="{BG}"/><rect width="{W}" height="{H}" fill="url(#g)"/>
<rect class="sh" x="0" y="0" width="300" height="{H}" fill="url(#s)" transform="skewX(-20)"/>
<g class="bob"><image href="data:image/png;base64,{b64(icon)}" x="40" y="48" width="124" height="124" clip-path="url(#i)"/></g>
<text x="196" y="80" font-size="30" font-weight="900" fill="{TXT}" letter-spacing="-.5">{esc(name)}</text>
{body}{chip_svg}
<text x="{W-36}" y="{H-26}" font-size="15" font-weight="700" fill="{accent}" text-anchor="end" letter-spacing="1">{cta} →</text>
<rect x="0" y="{H-3}" width="{W}" height="3" fill="{accent}"/>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="20" fill="none" stroke="{LINE}"/></g></svg>'''

# ---------- rubriker ----------
def title(text, sub):
    W = 1280
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 70" width="{W}" height="70">
<style>{FONTS}text{{font-family:R,Roboto,Helvetica,Arial,sans-serif}}
.bar{{transform-origin:0 0;transform:scaleX(0);animation:g 1.2s .2s cubic-bezier(.2,.8,.2,1) forwards}}@keyframes g{{to{{transform:scaleX(1)}}}}</style>
<rect x="0" y="16" width="8" height="34" rx="2" fill="{ACC}"/>
<text x="26" y="44" font-size="30" font-weight="900" fill="{ACC2}" letter-spacing="2">{text}</text>
<text x="{26+len(text)*22+24}" y="44" font-size="17" fill="{MUTED}">{esc(sub)}</text>
<rect class="bar" x="0" y="66" width="{W}" height="2" fill="{LINE}"/></svg>'''

def footer():
    random.seed(3)
    W = 1280
    bars = "".join(f'<rect x="{i*16}" y="{40-h}" width="12" height="{h}" fill="{ACC}" opacity="{.15+h/60:.2f}" class="b" style="animation-delay:{i*.04:.2f}s"/>'
                   for i, h in enumerate(random.randint(4, 36) for _ in range(80)))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 110" width="{W}" height="110">
<style>{FONTS}text{{font-family:R,Roboto,Helvetica,Arial,sans-serif}}
.b{{transform-box:fill-box;transform-origin:bottom;animation:eq 1.8s ease-in-out infinite alternate}}@keyframes eq{{from{{transform:scaleY(.25)}}}}</style>
{bars}<text x="{W/2}" y="92" font-size="16" font-weight="700" letter-spacing="6" fill="{MUTED}" text-anchor="middle">THANKS FOR STOPPING BY</text></svg>'''

files = {
    "header.svg": header(),
    "card-journal.svg": card("WillesJournal-160.png", "Wille's Journal",
        ["The complete trading journal. Log every trade,", "track your stats and grow with your mentor."],
        ["WINDOWS", "MAC"], "DOWNLOAD", "#4fbf6b"),
    "card-desktop.svg": card("WillesDesktop-160.png", "Wille's Desktop",
        ["Premium desktop widgets and taskbar", "customization for Windows."],
        ["WINDOWS"], "DOWNLOAD", ACC),
    "card-promptforge.svg": card("PromptForge-160.png", "PromptForge",
        ["A Windows terminal you shape with checkboxes.", "Every session starts with the PATH you chose."],
        ["WINDOWS", "ELECTRON"], "DOWNLOAD", "#e07a4f"),
    "card-gasegg.svg": card("GasEgg-160.png", "Steal a Gas Egg",
        ["Roblox game with my own pixel-style models,", "UI, animations and sound."],
        ["ROBLOX", "LUAU"], "PLAY", "#a77bf3"),
    "title-work.svg": title("SHIPPED", "apps and games you can use right now"),
    "title-stack.svg": title("STACK", "what I build with"),
    "title-activity.svg": title("ACTIVITY", "my contributions, eaten live"),
    "footer.svg": footer(),
}
for n, s in files.items():
    (OUT / n).write_text(s, encoding="utf-8")
    print(n, len(s) // 1024, "KB")
