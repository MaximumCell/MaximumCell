"""v2 design: "Ask Ali's Agent" — the profile as an animated AI chat.

    python3 scripts/build_assets_v2.py

Writes assets/v2/chat-{dark,light}.svg, assets/v2/artifact-*.svg and assets/v2/prompts-{dark,light}.svg.
All animation is SMIL so it plays inside GitHub's image proxy.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "v2"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

T = {
    "dark": dict(bg="#0e1117", win="#141922", line="#262d3a", text="#e6edf3", dim="#8b949e",
                 user="#2f6feb", userText="#ffffff", bot="#1b2230", tool="#0f1a14", toolLine="#2a4a36",
                 ok="#3fb950", accent="#d97757", chip="#1f2733"),
    "light": dict(bg="#f6f8fa", win="#ffffff", line="#d8dee4", text="#1f2328", dim="#656d76",
                  user="#0969da", userText="#ffffff", bot="#f1f3f6", tool="#f0f9f2", toolLine="#b7dfc1",
                  ok="#1a7f37", accent="#c2410c", chip="#eef1f5"),
}

W = 1000


def fade(begin, dur=0.35):
    return f'<animate attributeName="opacity" from="0" to="1" begin="{begin}s" dur="{dur}s" fill="freeze"/>'


def rise(begin):
    return (f'<animateTransform attributeName="transform" type="translate" from="0 8" to="0 0" '
            f'begin="{begin}s" dur="0.35s" fill="freeze" additive="sum"/>')


def typing_dots(x, y, begin, end, t):
    """Three bouncing dots shown between begin and end."""
    g = [f'<g opacity="0"><set attributeName="opacity" to="1" begin="{begin}s"/><set attributeName="opacity" to="0" begin="{end}s"/>',
         f'<rect x="{x}" y="{y}" width="64" height="34" rx="17" fill="{t["bot"]}"/>']
    for i in range(3):
        cx = x + 18 + i * 14
        g.append(f'<circle cx="{cx}" cy="{y+17}" r="4" fill="{t["dim"]}"><animate attributeName="cy" values="{y+17};{y+11};{y+17}" dur="0.9s" begin="{i*0.15}s" repeatCount="indefinite"/></circle>')
    g.append("</g>")
    return "".join(g)


def user_msg(text, y, begin, t):
    w = len(text) * 7.6 + 32
    x = W - 40 - w
    return (f'<g opacity="0">{fade(begin)}{rise(begin)}'
            f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="38" rx="19" fill="{t["user"]}"/>'
            f'<text x="{x+16:.0f}" y="{y+24}" font-family="{SANS}" font-size="14" fill="{t["userText"]}">{escape(text)}</text></g>')


def bot_msg(lines, y, begin, t, width=640):
    h = 22 * len(lines) + 20
    out = [f'<g opacity="0">{fade(begin)}{rise(begin)}',
           f'<circle cx="58" cy="{y+18}" r="16" fill="{t["accent"]}"/>',
           f'<text x="58" y="{y+23}" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="700" fill="#fff">AI</text>',
           f'<rect x="86" y="{y}" width="{width}" height="{h}" rx="14" fill="{t["bot"]}"/>']
    for i, (seg) in enumerate(lines):
        out.append(f'<text x="104" y="{y+28+i*22}" font-family="{SANS}" font-size="14" fill="{t["text"]}">{seg}</text>')
    out.append("</g>")
    return "".join(out), h


def chat(theme):
    t = T[theme]
    H = 640
    p = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Ask Ali's agent — an animated AI chat introducing Rao Ali Hassan">
<rect width="{W}" height="{H}" rx="20" fill="{t['bg']}"/>
<rect x="16" y="16" width="{W-32}" height="{H-32}" rx="16" fill="{t['win']}" stroke="{t['line']}"/>
<!-- header -->
<circle cx="52" cy="52" r="18" fill="{t['accent']}"/><text x="52" y="58" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="700" fill="#fff">A</text>
<text x="80" y="48" font-family="{SANS}" font-size="16" font-weight="700" fill="{t['text']}">Ask Ali's Agent</text>
<circle cx="84" cy="64" r="4" fill="{t['ok']}"><animate attributeName="opacity" values="1;0.3;1" dur="1.6s" repeatCount="indefinite"/></circle>
<text x="94" y="68" font-family="{SANS}" font-size="12" fill="{t['dim']}">online · knows everything about Rao Ali Hassan</text>
<rect x="{W-196}" y="38" width="156" height="28" rx="14" fill="{t['chip']}" stroke="{t['line']}"/>
<text x="{W-118}" y="57" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t['dim']}">model: ali-v2026</text>
<line x1="16" y1="88" x2="{W-16}" y2="88" stroke="{t['line']}"/>
''']
    # 1. user asks
    p.append(user_msg("Who is Ali and what does he build?", 106, 0.4, t))
    p.append(typing_dots(86, 158, 1.0, 2.2, t))
    m, h = bot_msg([
        "Hey! 👋 <tspan font-weight='700'>Rao Ali Hassan</tspan> is an AI Engineer &amp; Full-Stack Developer in Lahore.",
        "He's Technical Lead at <tspan font-weight='700'>Aaghaz AI</tspan> and builds LLM agents, RAG pipelines,",
        "MCP tools and Next.js + Supabase apps. Let me pull up what he's shipped…",
    ], 158, 2.2, t, width=660)
    p.append(m)
    # 2. tool call
    ty = 158 + h + 14
    p.append(f'''<g opacity="0">{fade(3.0)}
<rect x="86" y="{ty}" width="660" height="92" rx="12" fill="{t['tool']}" stroke="{t['toolLine']}"/>
<text x="104" y="{ty+26}" font-family="{MONO}" font-size="13" fill="{t['dim']}">⚙ tool_use</text>
<text x="190" y="{ty+26}" font-family="{MONO}" font-size="13" fill="{t['text']}">list_projects(owner="MaximumCell")</text>
<g><circle cx="720" cy="{ty+21}" r="7" fill="none" stroke="{t['dim']}" stroke-width="2" stroke-dasharray="11 33"><animateTransform attributeName="transform" type="rotate" from="0 720 {ty+21}" to="360 720 {ty+21}" dur="0.8s" repeatCount="indefinite"/></circle>
<set attributeName="opacity" to="0" begin="4.0s"/></g>
<text x="712" y="{ty+26}" font-family="{SANS}" font-size="14" fill="{t['ok']}" opacity="0">✓<set attributeName="opacity" to="1" begin="4.0s"/></text>
''')
    chips = ["thunder", "claude-video-editor", "sherlock", "physicslab", "creatorsuit", "pdf-ai"]
    x = 104
    for i, c in enumerate(chips):
        w = len(c) * 7.6 + 22
        b = 4.0 + i * 0.18
        p.append(f'<g opacity="0">{fade(b, 0.25)}<rect x="{x:.0f}" y="{ty+44}" width="{w:.0f}" height="28" rx="14" fill="{t["chip"]}" stroke="{t["line"]}"/>'
                 f'<text x="{x+11:.0f}" y="{ty+63}" font-family="{MONO}" font-size="12.5" fill="{t["text"]}">{c}</text></g>')
        x += w + 8
    p.append("</g>")
    # 3. second question
    y2 = ty + 92 + 18
    p.append(user_msg("Is he open to work?", y2, 5.6, t))
    p.append(typing_dots(86, y2 + 52, 6.1, 7.0, t))
    m, h2 = bot_msg([
        "<tspan fill='" + t['ok'] + "' font-weight='700'>✓ Yes!</tspan> AI Engineer · Full-Stack · AI Automation — Lahore or remote.",
        "Reach him on LinkedIn or at alihassanwinner@gmail.com 🚀",
    ], y2 + 52, 7.0, t, width=600)
    p.append(m)
    # input bar
    iy = H - 74
    p.append(f'''<line x1="16" y1="{iy-14}" x2="{W-16}" y2="{iy-14}" stroke="{t['line']}"/>
<rect x="40" y="{iy}" width="{W-80}" height="40" rx="20" fill="{t['chip']}" stroke="{t['line']}"/>
<text x="62" y="{iy+25}" font-family="{SANS}" font-size="14" fill="{t['dim']}">Ask anything about Ali…</text>
<rect x="232" y="{iy+11}" width="2" height="18" fill="{t['text']}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" repeatCount="indefinite"/></rect>
<circle cx="{W-62}" cy="{iy+20}" r="14" fill="{t['accent']}"/>
<path d="M{W-67},{iy+20} l10,0 m-4,-5 l5,5 l-5,5" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
''')
    return "".join(p)


ARTIFACTS = [
    ("thunder", "⚡", "Thunder", "AI video &amp; image studio · Gemma 4 agent", "Live app", "#7aa2f7"),
    ("claude-video", "🎬", "Claude Code Video Editor", "Plugin that auto-edits YouTube videos", "Claude Code plugin", "#d97757"),
    ("sherlock", "🔍", "Sherlock", "OSINT tool · scored correlations + review", "FastAPI · Next.js", "#3fb950"),
    ("physicslab", "🧪", "PhysicsLab", "Gemini tutor · 3D sims · ML lab (FYP)", "Live app", "#7dcfff"),
    ("creatorsuit", "🗂", "CreatorSuit", "Internal tool used by the Aaghaz AI team", "Live app", "#e0af68"),
    ("pdf-ai", "📄", "PDF AI", "Chat with PDFs · RAG + vector search", "LangChain · Gemini", "#bb9af7"),
]


def artifact(a, theme):
    slug, icon, title, sub, kind, col = a
    t = T[theme]
    Wc, Hc = 480, 96
    live = kind == "Live app"
    dot = (f'<circle cx="{Wc-30}" cy="{Hc/2}" r="5" fill="{t["ok"]}"><animate attributeName="r" values="4;6;4" dur="1.4s" repeatCount="indefinite"/></circle>'
           if live else
           f'<path d="M{Wc-36},{Hc/2-6} l8,6 l-8,6" stroke="{t["dim"]}" stroke-width="2" fill="none" stroke-linecap="round"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{Wc}" height="{Hc}" viewBox="0 0 {Wc} {Hc}" role="img" aria-label="{escape(title)}">
<rect x="1" y="1" width="{Wc-2}" height="{Hc-2}" rx="14" fill="{t['win']}" stroke="{t['line']}"/>
<rect x="16" y="16" width="64" height="64" rx="12" fill="{col}" fill-opacity="0.16" stroke="{col}" stroke-opacity="0.5"/>
<text x="48" y="58" text-anchor="middle" font-family="{SANS}" font-size="28">{icon}</text>
<text x="96" y="40" font-family="{SANS}" font-size="16" font-weight="700" fill="{t['text']}">{escape(title)}</text>
<text x="96" y="62" font-family="{SANS}" font-size="13" fill="{t['dim']}">{sub}</text>
<text x="96" y="82" font-family="{MONO}" font-size="11" fill="{col}">ARTIFACT · {kind.upper()}</text>
{dot}
</svg>
'''


PROMPTS = ["What's his strongest project?", "Can he build AI agents?", "Does he teach?", "What's his stack?"]


def prompts(theme):
    t = T[theme]
    x, parts = 0, []
    for i, q in enumerate(PROMPTS):
        w = len(q) * 7.4 + 30
        parts.append(f'<g opacity="0">{fade(0.3+i*0.2)}<rect x="{x+1:.0f}" y="1" width="{w:.0f}" height="34" rx="17" fill="{t["win"]}" stroke="{t["line"]}"/>'
                     f'<text x="{x+15:.0f}" y="23" font-family="{SANS}" font-size="13" fill="{t["text"]}">{escape(q)}</text></g>')
        x += w + 10
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{x:.0f}" height="36" viewBox="0 0 {x:.0f} 36">{"".join(parts)}</svg>\n'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for th in T:
        (OUT / f"chat-{th}.svg").write_text(chat(th), encoding="utf-8")
        (OUT / f"prompts-{th}.svg").write_text(prompts(th), encoding="utf-8")
        for a in ARTIFACTS:
            (OUT / f"artifact-{a[0]}-{th}.svg").write_text(artifact(a, th), encoding="utf-8")
    print("wrote", len(list(OUT.iterdir())), "files")


if __name__ == "__main__":
    main()
