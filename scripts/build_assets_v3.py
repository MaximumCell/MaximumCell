"""v3 design: "Ali's corkboard" — a warm, handmade, human profile.

    python3 scripts/build_assets_v3.py

Writes assets/v3/hero.svg, assets/v3/story.svg and assets/v3/polaroid-*.svg.
Self-contained SVG (own paper background) so it looks the same in light and dark mode.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "v3"
HAND = "'Bradley Hand', 'Segoe Print', 'Comic Neue', 'Comic Sans MS', 'Chalkboard SE', cursive"
SERIF = "Georgia, 'Iowan Old Style', 'Palatino Linotype', serif"
INK = "#2b2a33"
PAPER = "#fbf7ef"
LINE = "#dfe7f1"


def draw_on(length, begin, dur=1.2):
    """Animate a path so it looks hand-drawn."""
    return (f'stroke-dasharray="{length}" stroke-dashoffset="{length}">'
            f'<animate attributeName="stroke-dashoffset" from="{length}" to="0" begin="{begin}s" dur="{dur}s" fill="freeze"/>')


def paper(w, h, rx=18):
    lines = "".join(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="{LINE}" stroke-width="1"/>' for y in range(56, h, 32))
    return (f'<rect width="{w}" height="{h}" rx="{rx}" fill="{PAPER}"/>'
            f'<g clip-path="url(#pclip)">{lines}<line x1="44" y1="0" x2="44" y2="{h}" stroke="#f3b6b6" stroke-width="1.5"/></g>'
            f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{rx}" fill="none" stroke="#e7dccb"/>')


def sticky(x, y, rot, color, lines, begin):
    w, h = 210, 96
    txt = "".join(f'<text x="18" y="{40+i*26}" font-family="{HAND}" font-size="19" fill="{INK}">{l}</text>' for i, l in enumerate(lines))
    return f'''<g transform="translate({x},{y}) rotate({rot})" opacity="0">
<animate attributeName="opacity" from="0" to="1" begin="{begin}s" dur="0.4s" fill="freeze"/>
<rect x="4" y="6" width="{w}" height="{h}" fill="#000" opacity="0.08"/>
<rect width="{w}" height="{h}" fill="{color}"/>
<path d="M{w-26},{h} L{w},{h-26} L{w},{h} Z" fill="#000" opacity="0.06"/>
<circle cx="{w/2}" cy="10" r="6" fill="#d9534f"/><circle cx="{w/2-2}" cy="8" r="2" fill="#fff" opacity="0.7"/>
{txt}</g>'''


def hero():
    W, H = 1000, 460
    p = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Hi, I'm Ali — I build things with AI and teach people how to build them too.">
<defs><clipPath id="pclip"><rect width="{W}" height="{H}" rx="18"/></clipPath></defs>
{paper(W, H)}
<text x="72" y="118" font-family="{HAND}" font-size="58" fill="{INK}">Hi, I'm Ali <tspan>👋</tspan></text>
<path d="M74,138 C160,128 260,146 360,134" fill="none" stroke="#e8743b" stroke-width="5" stroke-linecap="round" {draw_on(300, 0.3, 0.9)}</path>
<text x="74" y="192" font-family="{SERIF}" font-size="23" fill="{INK}">I build things with AI —</text>
<text x="74" y="224" font-family="{SERIF}" font-size="23" fill="{INK}">and teach people how to build them too.</text>
<text x="74" y="276" font-family="{SERIF}" font-size="17" fill="#5f5a6b">Technical Lead at <tspan font-weight="700">Aaghaz AI</tspan> · Lahore, Pakistan</text>
<text x="74" y="306" font-family="{SERIF}" font-size="17" fill="#5f5a6b">Full-stack developer · AI engineer · teacher</text>
<!-- open to work stamp -->
<g transform="translate(74,350) rotate(-4)" opacity="0"><animate attributeName="opacity" from="0" to="1" begin="2.4s" dur="0.3s" fill="freeze"/>
<rect width="250" height="54" rx="8" fill="none" stroke="#2e8b57" stroke-width="3"/>
<rect x="6" y="6" width="238" height="42" rx="5" fill="none" stroke="#2e8b57" stroke-width="1.2"/>
<text x="125" y="35" text-anchor="middle" font-family="{SERIF}" font-size="17" font-weight="700" letter-spacing="2" fill="#2e8b57">OPEN TO NEW WORK</text></g>
''']
    # doodle: laptop + mug
    p.append(f'''<g transform="translate(560,300)" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
<path d="M10,0 L150,-2 L152,92 L8,94 Z" {draw_on(480, 0.6, 1.0)}</path>
<path d="M-14,98 L176,96 L186,112 L-24,114 Z" {draw_on(420, 1.4, 0.8)}</path>
<path d="M32,30 l14,12 l-14,12 M58,56 l30,0" stroke="#e8743b" {draw_on(90, 2.0, 0.5)}</path>
</g>
<g transform="translate(790,330)" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round">
<path d="M0,0 L4,74 Q6,84 18,84 L56,84 Q68,84 70,74 L74,0 Z" fill="#f6d6c0" {draw_on(260, 0.9, 0.9)}</path>
<path d="M74,16 Q100,18 98,40 Q96,60 72,58" {draw_on(90, 1.6, 0.5)}</path>
<path d="M22,-12 q-8,-14 0,-28 q8,-14 0,-28" stroke="#9a9aa5" stroke-width="2.5" opacity="0.7"><animateTransform attributeName="transform" type="translate" values="0,0;0,-6;0,0" dur="2.4s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.2;0.8;0.2" dur="2.4s" repeatCount="indefinite"/></path>
<path d="M46,-12 q-8,-14 0,-28 q8,-14 0,-28" stroke="#9a9aa5" stroke-width="2.5" opacity="0.7"><animateTransform attributeName="transform" type="translate" values="0,-3;0,-9;0,-3" dur="2.4s" begin="0.8s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.2;0.8;0.2" dur="2.4s" begin="0.8s" repeatCount="indefinite"/></path>
</g>
''')
    p.append(sticky(560, 46, -4, "#fff3a3", ["🎬 I make YouTube", "videos about AI tools"], 1.0))
    p.append(sticky(780, 70, 5, "#ffd1dc", ["🎙 I host a podcast", "with founders"], 1.3))
    p.append(sticky(590, 160, 2, "#cdeafe", ["🎓 BS Physics,", "COMSATS '26"], 1.6))
    p.append("</svg>\n")
    return "".join(p)


STORY = [
    ("2022", ["started BS Physics", "@ COMSATS"]),
    ("2025", ["first full-stack", "apps (MERN)"]),
    ("Aug '25", ["LangChain + Kaggle", "deep learning certs"]),
    ("Oct '25", ["shipped PhysicsLab,", "my final year project"]),
    ("2026", ["graduated · joined", "Aaghaz AI as Tech Lead"]),
    ("Sep '26", ["built Thunder,", "my AI video studio"]),
    ("now", ["looking for my", "next team ✨"]),
]


def story():
    W, H = 1000, 320
    n = len(STORY)
    xs = [140 + i * (W - 230) / (n - 1) for i in range(n)]
    y0 = 170
    # wavy path through points
    d = f"M{xs[0]},{y0}"
    for i in range(1, n):
        mid = (xs[i - 1] + xs[i]) / 2
        dy = -22 if i % 2 else 22
        d += f" Q{mid},{y0+dy} {xs[i]},{y0}"
    p = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="My story so far: a hand-drawn timeline from 2022 to now">
<defs><clipPath id="pclip"><rect width="{W}" height="{H}" rx="18"/></clipPath></defs>
{paper(W, H)}
<text x="64" y="58" font-family="{HAND}" font-size="32" fill="{INK}">my story so far…</text>
<path d="{d}" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" {draw_on(1100, 0.3, 2.6)}</path>
''']
    for i, (when, label) in enumerate(STORY):
        b = 0.3 + 2.6 * i / (n - 1)
        up = i % 2 == 0
        ly = y0 - 46 if up else y0 + 58
        last = i == n - 1
        col = "#e8743b" if last else INK
        lbl = "".join(f'<text x="{xs[i]}" y="{ly + k*22}" text-anchor="middle" font-family="{HAND}" font-size="17" fill="{col}">{escape(t)}</text>' for k, t in enumerate(label))
        when_y = y0 + 34 if up else y0 - 18
        p.append(f'''<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{b:.2f}s" dur="0.35s" fill="freeze"/>
<circle cx="{xs[i]}" cy="{y0}" r="{9 if last else 7}" fill="{'#e8743b' if last else PAPER}" stroke="{col}" stroke-width="3"/>
<text x="{xs[i]}" y="{when_y}" text-anchor="middle" font-family="{SERIF}" font-size="14" font-weight="700" fill="#8a8494">{escape(when)}</text>
{lbl}</g>''')
        if last:
            p.append(f'<circle cx="{xs[i]}" cy="{y0}" r="9" fill="none" stroke="#e8743b" stroke-width="2"><animate attributeName="r" values="9;20;9" dur="2s" begin="3s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.8;0;0.8" dur="2s" begin="3s" repeatCount="indefinite"/></circle>')
    p.append("</svg>\n")
    return "".join(p)


# doodles drawn inside the 240x170 "photo" area
DOODLES = {
    "thunder": ("#ffe8a3", '<path d="M136,22 L92,92 L122,92 L104,150 L158,72 L126,72 L146,22 Z" fill="#ffcc33" stroke="#2b2a33" stroke-width="3.5" stroke-linejoin="round"/>'),
    "claude-video": ("#ffd9c7", '<rect x="62" y="64" width="116" height="78" rx="6" fill="#2b2a33"/><path d="M62,40 L178,40 L178,64 L62,64 Z" fill="#fff" stroke="#2b2a33" stroke-width="3.5"/><path d="M80,40 l14,24 M110,40 l14,24 M140,40 l14,24" stroke="#2b2a33" stroke-width="3.5"/><path d="M110,86 l26,17 l-26,17 Z" fill="#ff8a5c"/>'),
    "sherlock": ("#d7f2dc", '<circle cx="106" cy="80" r="40" fill="#fff" stroke="#2b2a33" stroke-width="4"/><path d="M134,108 L170,144" stroke="#2b2a33" stroke-width="9" stroke-linecap="round"/><path d="M88,70 q18,-18 36,0" fill="none" stroke="#8fd19e" stroke-width="4" stroke-linecap="round"/>'),
    "physicslab": ("#d6ecff", '<circle cx="120" cy="86" r="10" fill="#2b2a33"/><ellipse cx="120" cy="86" rx="62" ry="22" fill="none" stroke="#2b2a33" stroke-width="3.5"/><ellipse cx="120" cy="86" rx="62" ry="22" fill="none" stroke="#2b2a33" stroke-width="3.5" transform="rotate(60 120 86)"/><ellipse cx="120" cy="86" rx="62" ry="22" fill="none" stroke="#2b2a33" stroke-width="3.5" transform="rotate(-60 120 86)"/>'),
    "creatorsuit": ("#fde2c4", '<rect x="74" y="34" width="92" height="116" rx="8" fill="#fff" stroke="#2b2a33" stroke-width="3.5"/><rect x="100" y="26" width="40" height="18" rx="5" fill="#e8743b" stroke="#2b2a33" stroke-width="3"/><path d="M90,72 l8,8 l14,-14 M90,104 l8,8 l14,-14" fill="none" stroke="#2e8b57" stroke-width="3.5" stroke-linecap="round"/><path d="M124,76 h28 M124,108 h28" stroke="#2b2a33" stroke-width="3.5" stroke-linecap="round"/>'),
    "pdf-ai": ("#e8dcff", '<path d="M82,30 L140,30 L162,52 L162,148 L82,148 Z" fill="#fff" stroke="#2b2a33" stroke-width="3.5" stroke-linejoin="round"/><path d="M140,30 L140,52 L162,52" fill="none" stroke="#2b2a33" stroke-width="3.5"/><path d="M96,74 h52 M96,92 h52 M96,110 h34" stroke="#b39ddb" stroke-width="4" stroke-linecap="round"/><circle cx="150" cy="122" r="14" fill="#7e57c2"/><text x="150" y="127" text-anchor="middle" font-family="Georgia" font-size="13" fill="#fff">?</text>'),
}

POLAROIDS = [
    ("thunder", "Thunder", "my AI video studio", "try it live →", -3),
    ("claude-video", "Video Editor", "a Claude Code plugin", "it edits my videos!", 2.5),
    ("sherlock", "Sherlock", "OSINT, done ethically", "FastAPI + Next.js", -1.5),
    ("physicslab", "PhysicsLab", "my final year project", "try it live →", 3),
    ("creatorsuit", "CreatorSuit", "my team uses it daily", "try it live →", -2.5),
    ("pdf-ai", "PDF AI", "chat with your PDFs", "RAG + LangChain", 1.5),
]


def polaroid(slug, title, caption, note, rot):
    W, H = 320, 340
    bg, art = DOODLES[slug]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)} — {escape(caption)}">
<g transform="rotate({rot} 160 170)">
<rect x="46" y="38" width="236" height="276" fill="#000" opacity="0.10" transform="translate(5,7)"/>
<rect x="40" y="32" width="240" height="276" fill="#fffdf8" stroke="#e9e2d6"/>
<g transform="translate(52,44)"><rect width="216" height="170" fill="{bg}"/><g transform="translate(-12,0)">{art}</g></g>
<text x="160" y="250" text-anchor="middle" font-family="{HAND}" font-size="25" fill="{INK}">{escape(title)}</text>
<text x="160" y="278" text-anchor="middle" font-family="{HAND}" font-size="16" fill="#6b6576">{escape(caption)}</text>
<rect x="122" y="18" width="76" height="26" fill="#f3e3a6" opacity="0.85" transform="rotate(-3 160 31)"/>
</g>
<text x="160" y="332" text-anchor="middle" font-family="{HAND}" font-size="15" fill="#e8743b">{escape(note)}</text>
</svg>
'''


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "hero.svg").write_text(hero(), encoding="utf-8")
    (OUT / "story.svg").write_text(story(), encoding="utf-8")
    for p in POLAROIDS:
        (OUT / f"polaroid-{p[0]}.svg").write_text(polaroid(*p), encoding="utf-8")
    print("wrote", len(list(OUT.iterdir())), "files")


if __name__ == "__main__":
    main()
