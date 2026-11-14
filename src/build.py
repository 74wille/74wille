# Bygger profilens SVG-grafik till ../assets. Kör: python src/build.py
import base64, pathlib, random

SRC = pathlib.Path(__file__).parent
OUT = SRC.parent / "assets"
OUT.mkdir(exist_ok=True)

def b64(name): return base64.b64encode((SRC / name).read_bytes()).decode()

FONTS = "".join(
    f"@font-face{{font-family:{f};font-weight:{w};src:url(data:font/woff2;base64,{b64(file)})}}"
    for f, w, file in (("R", 700, "roboto-700.woff2"), ("R", 900, "roboto-900.woff2"),
                       ("M", 500, "mono-500.woff2"), ("M", 700, "mono-700.woff2")))

BG, LINE, RED, TXT, MUTED = "#060708", "#1c1f24", "#ff2a4a", "#f2f2f2", "#6b7280"
BASE = f"{FONTS}.r{{font-family:R,Roboto,Arial,sans-serif}}.m{{font-family:M,'Roboto Mono',Consolas,monospace}}"
SCAN = ('<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">'
        '<rect width="4" height="1" fill="#fff" fill-opacity=".035"/></pattern>')

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;")

def glitch_text(x, y, size, text, cls="r", weight=900, ls=-4):
    """Text med RGB-split och ryckiga glitch-skivor."""
    t = f'x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" letter-spacing="{ls}"'
    return f'''<g class="gl">
<text {t} fill="#00e5ff" class="{cls} ca" opacity=".75">{text}</text>
<text {t} fill="{RED}" class="{cls} cb" opacity=".85">{text}</text>
<text {t} fill="{TXT}" class="{cls}">{text}</text>
<text {t} fill="{TXT}" class="{cls} s1">{text}</text>
<text {t} fill="{RED}" class="{cls} s2">{text}</text></g>'''

GLITCH_CSS = """
.ca{animation:ca 3s steps(1) infinite}.cb{animation:cb 3s steps(1) infinite}
@keyframes ca{0%,100%{transform:translate(-3px,0)}20%{transform:translate(-6px,1px)}22%{transform:translate(2px,-1px)}24%{transform:translate(-3px,0)}70%{transform:translate(-9px,0)}71%{transform:translate(-3px,0)}}
@keyframes cb{0%,100%{transform:translate(3px,0)}20%{transform:translate(6px,-1px)}22%{transform:translate(-2px,1px)}24%{transform:translate(3px,0)}70%{transform:translate(9px,0)}71%{transform:translate(3px,0)}}
.s1,.s2{opacity:0}
.s1{animation:s1 3s steps(1) infinite}.s2{animation:s2 3s steps(1) infinite}
@keyframes s1{20%{opacity:1;clip-path:inset(30% 0 52% 0);transform:translateX(-14px)}22%{opacity:1;clip-path:inset(62% 0 20% 0);transform:translateX(10px)}24%{opacity:0}70%{opacity:1;clip-path:inset(10% 0 75% 0);transform:translateX(18px)}72%{opacity:0}}
@keyframes s2{21%{opacity:.9;clip-path:inset(45% 0 40% 0);transform:translateX(12px)}23%{opacity:0}71%{opacity:.9;clip-path:inset(70% 0 12% 0);transform:translateX(-16px)}72%{opacity:0}}
.flick{animation:fl 4s steps(1) infinite}@keyframes fl{0%,100%{opacity:1}43%{opacity:.2}44%{opacity:1}46%{opacity:.4}47%{opacity:1}}
.blink{animation:bl 1s steps(1) infinite}@keyframes bl{50%{opacity:0}}
.sweep{animation:sw 4.5s linear infinite}@keyframes sw{from{transform:translateY(-60px)}to{transform:translateY(420px)}}
"""

def brackets(W, H, m=14, l=26, c=RED):
    p = lambda d: f'<path d="{d}" fill="none" stroke="{c}" stroke-width="3"/>'
    return (p(f"M{m} {m+l}V{m}H{m+l}") + p(f"M{W-m-l} {m}H{W-m}V{m+l}") +
            p(f"M{m} {H-m-l}V{H-m}H{m+l}") + p(f"M{W-m-l} {H-m}H{W-m}V{H-m-l}"))

# ---------- banner ----------
def header():
    random.seed(11)
    W, H = 1280, 380
    noise = "".join(f'<rect x="{random.randrange(W)}" y="{random.randrange(H)}" width="{random.choice((2,3,40,90,160))}" height="2" fill="{random.choice((RED, "#fff"))}" '
                    f'opacity="0" style="animation:nz {2+random.random()*3:.2f}s steps(1) {random.random()*3:.2f}s infinite"/>'
                    for _ in range(26))
    sub = "> building desktop apps, web apps & tools_"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>{BASE}{GLITCH_CSS}
@keyframes nz{{0%{{opacity:0}}5%{{opacity:.7}}8%{{opacity:0}}}}
.type{{clip-path:inset(0 100% 0 0);animation:ty 2.6s steps({len(sub)}) .5s forwards}}@keyframes ty{{to{{clip-path:inset(0 0 0 0)}}}}
</style>
<defs>{SCAN}
<pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse"><path d="M48 0H0V48" fill="none" stroke="#fff" stroke-opacity=".04"/></pattern>
<linearGradient id="sw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{RED}" stop-opacity="0"/><stop offset="1" stop-color="{RED}" stop-opacity=".12"/></linearGradient>
<clipPath id="cut"><path d="M0 0H{W-60}L{W} 60V{H}H60L0 {H-60}Z"/></clipPath>
</defs>
<g clip-path="url(#cut)">
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect width="{W}" height="{H}" fill="url(#grid)"/>
<path d="M{W-520} 0H{W}V{H}H{W-820}Z" fill="{RED}" fill-opacity=".06"/>
<path d="M{W-470} 0H{W-455}L{W-755} {H}H{W-770}Z" fill="{RED}" fill-opacity=".5"/>
<rect class="sweep" x="0" y="0" width="{W}" height="60" fill="url(#sw)"/>
{noise}
<text x="72" y="92" font-size="16" font-weight="700" letter-spacing="4" fill="{RED}" class="m flick">// STOCKHOLM, SE · EST. 2026</text>
{glitch_text(62, 250, 176, "WILLE")}
<text x="72" y="306" font-size="22" font-weight="500" fill="{TXT}" class="m type">{esc(sub)}</text>
<text x="72" y="344" font-size="14" font-weight="700" letter-spacing="3" fill="{MUTED}" class="m">ELECTRON / NEXT.JS / SUPABASE / NODE</text>
<g class="m" font-size="13" font-weight="700" fill="{MUTED}" letter-spacing="2" text-anchor="end">
<text x="{W-70}" y="290">SYS.STATUS <tspan fill="{RED}" class="blink">■ ONLINE</tspan></text>
<text x="{W-70}" y="314">BUILDS.SHIPPED <tspan fill="{TXT}">03</tspan></text>
<text x="{W-70}" y="338">SLEEP <tspan fill="{TXT}">OPTIONAL</tspan></text></g>
<rect width="{W}" height="{H}" fill="url(#scan)"/>
{brackets(W, H)}
</g></svg>'''

# ---------- projektkort ----------
def card(num, name, lines, chips, cta, tag):
    W, H = 600, 260
    chip_svg, x = "", 40
    for c in chips:
        w = len(c) * 9 + 24
        chip_svg += (f'<rect x="{x}" y="188" width="{w:.0f}" height="28" fill="none" stroke="{MUTED}"/>'
                     f'<text x="{x+w/2:.0f}" y="207" font-size="12" font-weight="700" fill="{TXT}" text-anchor="middle" letter-spacing="1" class="m">{c}</text>')
        x += w + 8
    body = "".join(f'<text x="40" y="{140+i*22}" font-size="15" font-weight="500" fill="{MUTED}" class="m">{esc(l)}</text>' for i, l in enumerate(lines))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>{BASE}{GLITCH_CSS}</style>
<defs>{SCAN}<clipPath id="cut"><path d="M0 0H{W-34}L{W} 34V{H}H34L0 {H-34}Z"/></clipPath></defs>
<g clip-path="url(#cut)">
<rect width="{W}" height="{H}" fill="{BG}"/>
<text x="{W-24}" y="{H-20}" font-size="190" font-weight="900" fill="#fff" fill-opacity=".04" text-anchor="end" class="r" letter-spacing="-8">{num}</text>
<text x="40" y="52" font-size="13" font-weight="700" letter-spacing="3" fill="{RED}" class="m">{num} // {tag}</text>
{glitch_text(36, 104, 44, esc(name), ls=-1)}
{body}{chip_svg}
<text x="{W-40}" y="{H-36}" font-size="15" font-weight="700" fill="{RED}" text-anchor="end" letter-spacing="2" class="m">[ {cta} ]<tspan class="blink">_</tspan></text>
<rect width="{W}" height="{H}" fill="url(#scan)"/>
<path d="M.5 .5H{W-34}L{W-.5} 34V{H-.5}H34L.5 {H-34}Z" fill="none" stroke="{LINE}" stroke-width="2"/>
<path d="M0 0H140" stroke="{RED}" stroke-width="6"/>
</g></svg>'''

# ---------- rubriker ----------
def title(idx, text, sub):
    W = 1280
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 80" width="{W}" height="80">
<style>{BASE}{GLITCH_CSS}
.bar{{transform-origin:0 0;transform:scaleX(0);animation:g 1s .2s steps(12) forwards}}@keyframes g{{to{{transform:scaleX(1)}}}}</style>
<text x="0" y="50" font-size="16" font-weight="700" fill="{RED}" class="m">{idx}</text>
{glitch_text(44, 54, 40, text, ls=1)}
<text x="{44+len(text)*28+24}" y="50" font-size="15" font-weight="500" fill="{MUTED}" class="m">// {esc(sub)}</text>
<rect class="bar" x="0" y="72" width="{W}" height="2" fill="{RED}"/><rect x="0" y="72" width="{W}" height="2" fill="{LINE}" opacity=".6"/></svg>'''

def footer():
    W = 1280
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 90" width="{W}" height="90">
<style>{BASE}{GLITCH_CSS}</style>
<rect x="0" y="10" width="{W}" height="2" fill="{LINE}"/><rect x="0" y="10" width="160" height="2" fill="{RED}"/>
<text x="{W/2}" y="60" font-size="15" font-weight="700" letter-spacing="6" fill="{MUTED}" text-anchor="middle" class="m flick">END OF TRANSMISSION <tspan fill="{RED}" class="blink">■</tspan></text></svg>'''

files = {
    "header.svg": header(),
    "card-journal.svg": card("01", "Wille's Journal",
        ["The complete trading journal. Log every", "trade, track your stats, get better."],
        ["WINDOWS", "MAC"], "DOWNLOAD", "DESKTOP APP"),
    "card-desktop.svg": card("02", "Wille's Desktop",
        ["Premium desktop widgets and taskbar", "customization for Windows."],
        ["WINDOWS"], "DOWNLOAD", "DESKTOP APP"),
    "card-promptforge.svg": card("03", "PromptForge",
        ["A Windows terminal you shape with", "checkboxes. Your PATH, your rules."],
        ["WINDOWS", "TERMINAL"], "DOWNLOAD", "DEV TOOL"),
    "title-work.svg": title("01", "SHIPPED", "live, download it"),
    "title-stack.svg": title("02", "ARSENAL", "what i build with"),
    "title-activity.svg": title("03", "ACTIVITY", "commits, eaten alive"),
    "footer.svg": footer(),
}
for n, s in files.items():
    (OUT / n).write_text(s, encoding="utf-8")
    print(n, len(s) // 1024, "KB")
