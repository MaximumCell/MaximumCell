"""Generate the animated SVG artwork for the profile README.

    python3 scripts/build_assets.py

Writes assets/hero-{dark,light}.svg and assets/card-*.svg.
Animations use SMIL so they play inside GitHub's image proxy.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"

THEMES = {
    "dark": dict(bg="#0b0f17", panel="#111827", border="#263043", text="#c9d1d9", dim="#7d8590",
                 prompt="#7aa2f7", ok="#3fb950", accent="#bb9af7", warm="#f7768e", node="#161f2e"),
    "light": dict(bg="#f6f8fa", panel="#ffffff", border="#d0d7de", text="#1f2328", dim="#656d76",
                  prompt="#0969da", ok="#1a7f37", accent="#8250df", warm="#cf222e", node="#f0f3f8"),
}

# (command, output, output colour key)
SESSION = [
    ("whoami", "Rao Ali Hassan · AI Engineer &amp; Full-Stack Developer · Lahore", "text"),
    ("cat role.txt", "Technical Lead @ Aaghaz AI — teaching AI tools to founders &amp; creators", "text"),
    ('claude "what do you build?"', "● LLM agents   ● RAG pipelines   ● MCP tools   ● Next.js + Supabase apps", "accent"),
    ("ls ~/shipped", "thunder/  claude-video-editor/  sherlock/  physicslab/  creatorsuit/  pdf-ai/", "prompt"),
    ("echo $STATUS", "✓ open to AI Engineer · Full-Stack · Automation roles", "ok"),
]

CHAR_W = 8.4      # approx width of one monospace char at 14px
TYPE_SPEED = 0.045  # seconds per char


def hero(theme: str) -> str:
    t = THEMES[theme]
    W, H = 1200, 400
    term_w = 780
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Rao Ali Hassan — AI Engineer terminal intro">
<defs>
  <linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="{t['prompt']}"/><stop offset="0.5" stop-color="{t['accent']}"/><stop offset="1" stop-color="{t['warm']}"/></linearGradient>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="{W}" height="{H}" rx="18" fill="{t['bg']}"/>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="17" fill="none" stroke="url(#edge)" stroke-opacity="0.55"/>
<!-- terminal window -->
<rect x="24" y="24" width="{term_w}" height="{H-48}" rx="12" fill="{t['panel']}" stroke="{t['border']}"/>
<circle cx="48" cy="46" r="6" fill="#ff5f57"/><circle cx="68" cy="46" r="6" fill="#febc2e"/><circle cx="88" cy="46" r="6" fill="#28c840"/>
<text x="{24+term_w/2}" y="51" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t['dim']}">ali@lahore: ~ — claude</text>
<line x1="24" y1="66" x2="{24+term_w}" y2="66" stroke="{t['border']}"/>
''']
    y = 100
    t0 = 0.6
    for i, (cmd, out, ck) in enumerate(SESSION):
        cmd_chars = len(cmd) + 2
        type_dur = round(cmd_chars * TYPE_SPEED, 2)
        cw = round(cmd_chars * CHAR_W + 6, 1)
        parts.append(f'''<clipPath id="c{i}"><rect x="44" y="{y-16}" width="0" height="22"><animate attributeName="width" from="0" to="{cw}" begin="{t0}s" dur="{type_dur}s" fill="freeze" calcMode="discrete" keyTimes="{';'.join(f'{k/cmd_chars:.3f}' for k in range(cmd_chars+1))}" values="{';'.join(f'{k*CHAR_W:.1f}' for k in range(cmd_chars))};{cw}"/></rect></clipPath>
<text x="48" y="{y}" font-family="{MONO}" font-size="14" clip-path="url(#c{i})"><tspan fill="{t['prompt']}">❯ </tspan><tspan fill="{t['text']}">{escape(cmd)}</tspan></text>
''')
        t_out = t0 + type_dur + 0.25
        parts.append(f'''<text x="48" y="{y+24}" font-family="{MONO}" font-size="14" fill="{t[ck]}" opacity="0">{out}<animate attributeName="opacity" from="0" to="1" begin="{t_out}s" dur="0.35s" fill="freeze"/></text>
''')
        y += 54
        t0 = t_out + 0.55
    # blinking cursor after the last line
    parts.append(f'''<rect x="66" y="{y-14}" width="9" height="17" fill="{t['prompt']}" opacity="0"><animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.01;0.5;0.51;1" dur="1s" begin="{t0}s" repeatCount="indefinite"/></rect>
<text x="48" y="{y}" font-family="{MONO}" font-size="14" fill="{t['prompt']}" opacity="0">❯<animate attributeName="opacity" to="1" begin="{t0}s" dur="0.01s" fill="freeze"/></text>
''')
    # agent graph panel
    gx = 24 + term_w + 24
    gw = W - gx - 24
    parts.append(f'''<rect x="{gx}" y="24" width="{gw}" height="{H-48}" rx="12" fill="{t['panel']}" stroke="{t['border']}"/>
<text x="{gx+20}" y="54" font-family="{MONO}" font-size="12" fill="{t['dim']}">// how I ship AI products</text>
''')
    nodes = [("brief", "💬", 0), ("agent", "🧠", 1), ("tools", "🛠", 2), ("ship", "🚀", 3)]
    ny = [104, 170, 236, 302]
    cx = gx + gw / 2
    labels = {"brief": "user brief", "agent": "LLM agent", "tools": "RAG · MCP · APIs", "ship": "deployed app"}
    for k in range(3):
        y1, y2 = ny[k] + 22, ny[k + 1] - 22
        parts.append(f'''<line x1="{cx}" y1="{y1}" x2="{cx}" y2="{y2}" stroke="url(#edge)" stroke-width="2" stroke-dasharray="4 5"><animate attributeName="stroke-dashoffset" from="18" to="0" dur="0.9s" repeatCount="indefinite"/></line>
<circle r="4" fill="{t['accent']}" filter="url(#glow)"><animateMotion dur="1.6s" begin="{k*0.5}s" repeatCount="indefinite" path="M{cx},{y1} L{cx},{y2}"/></circle>
''')
    for (key, icon, k), yy in zip(nodes, ny):
        parts.append(f'''<g opacity="0"><animate attributeName="opacity" to="1" begin="{0.4+k*0.35}s" dur="0.4s" fill="freeze"/>
<rect x="{cx-110}" y="{yy-22}" width="220" height="44" rx="22" fill="{t['node']}" stroke="url(#edge)"/>
<text x="{cx-84}" y="{yy+6}" font-family="{SANS}" font-size="18">{icon}</text>
<text x="{cx-56}" y="{yy+5}" font-family="{MONO}" font-size="14" fill="{t['text']}">{labels[key]}</text>
<circle cx="{cx+92}" cy="{yy}" r="4" fill="{t['ok']}"><animate attributeName="opacity" values="1;0.25;1" dur="1.8s" begin="{k*0.3}s" repeatCount="indefinite"/></circle>
</g>
''')
    parts.append("</svg>\n")
    return "".join(parts)


CARDS = [
    dict(slug="thunder", icon="⚡", title="Thunder", live=True,
         lines=["Conversational AI studio for video & images.", "A Gemma 4 agent refines your brief; Seedance /", "Seedream render it on an infinite canvas."],
         chips=["Next.js 16", "Supabase", "Gemma 4", "Seedance"], c1="#7aa2f7", c2="#bb9af7"),
    dict(slug="claude-video", icon="🎬", title="Claude Code Video Editor", live=False,
         lines=["Claude Code plugin that auto-edits YouTube", "recordings: cuts retakes, adds B-roll & motion", "graphics, renders with Remotion."],
         chips=["Claude Code", "Remotion", "Node.js", "ffmpeg"], c1="#f7768e", c2="#ff9e64"),
    dict(slug="sherlock", icon="🔍", title="Sherlock", live=False,
         lines=["OSINT investigation tool: deterministic", "collectors → confidence-scored correlations", "→ human review. Ethics guardrails built in."],
         chips=["FastAPI", "Next.js 16", "Supabase", "Gemma 4"], c1="#9ece6a", c2="#73daca"),
    dict(slug="physicslab", icon="🧪", title="PhysicsLab · FYP", live=True,
         lines=["Physics learning platform: Gemini tutor with", "Qdrant memory, real-time 2D/3D simulations", "and an ML lab with live training."],
         chips=["Next.js", "Flask", "TensorFlow", "Docker"], c1="#7dcfff", c2="#7aa2f7"),
    dict(slug="creatorsuit", icon="🗂", title="CreatorSuit", live=True,
         lines=["Internal productivity tool used every day", "by the Aaghaz AI team — auth, roles and", "attendance on Postgres row-level security."],
         chips=["Next.js 16", "Supabase", "RLS", "Server Actions"], c1="#e0af68", c2="#f7768e"),
    dict(slug="pdf-ai", icon="📄", title="PDF AI", live=False,
         lines=["Chat with your PDFs: chunking, embeddings", "and vector search with streaming answers", "grounded in your documents."],
         chips=["LangChain", "Gemini", "MongoDB Vector", "Next.js"], c1="#bb9af7", c2="#7dcfff"),
]


def card(c: dict) -> str:
    W, H = 420, 210
    chips = []
    x = 22
    for ch in c["chips"]:
        w = len(ch) * 7.2 + 18
        chips.append(f'<rect x="{x}" y="164" width="{w:.0f}" height="24" rx="12" fill="#ffffff" fill-opacity="0.06" stroke="#ffffff" stroke-opacity="0.12"/>'
                     f'<text x="{x+9}" y="180" font-family="{MONO}" font-size="12" fill="#c9d1d9">{escape(ch)}</text>')
        x += w + 8
    live = ""
    if c["live"]:
        live = (f'<g transform="translate({W-78},26)"><rect width="58" height="22" rx="11" fill="#3fb950" fill-opacity="0.15" stroke="#3fb950" stroke-opacity="0.5"/>'
                f'<circle cx="13" cy="11" r="4" fill="#3fb950"><animate attributeName="r" values="3;5;3" dur="1.4s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="1;0.4;1" dur="1.4s" repeatCount="indefinite"/></circle>'
                f'<text x="23" y="15" font-family="{MONO}" font-size="11" font-weight="700" fill="#3fb950">LIVE</text></g>')
    body = "".join(f'<text x="22" y="{92+i*20}" font-family="{SANS}" font-size="13.5" fill="#9aa4b2">{escape(l)}</text>' for i, l in enumerate(c["lines"]))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(c['title'])}">
<defs>
  <linearGradient id="g" x1="0" y1="0" x2="1" y2="1" gradientUnits="objectBoundingBox">
    <stop offset="0" stop-color="{c['c1']}"/><stop offset="1" stop-color="{c['c2']}"/>
    <animateTransform attributeName="gradientTransform" type="rotate" from="0 0.5 0.5" to="360 0.5 0.5" dur="6s" repeatCount="indefinite"/>
  </linearGradient>
  <radialGradient id="glow" cx="0.15" cy="0.1" r="0.9"><stop offset="0" stop-color="{c['c1']}" stop-opacity="0.22"/><stop offset="1" stop-color="{c['c1']}" stop-opacity="0"/></radialGradient>
</defs>
<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="16" fill="#0d1117" stroke="url(#g)" stroke-width="2"/>
<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="16" fill="url(#glow)"/>
<text x="22" y="52" font-family="{SANS}" font-size="24">{c['icon']}</text>
<text x="58" y="50" font-family="{SANS}" font-size="20" font-weight="700" fill="#f0f6fc">{escape(c['title'])}</text>
{live}
{body}
{''.join(chips)}
</svg>
'''


def main():
    OUT.mkdir(exist_ok=True)
    for th in THEMES:
        (OUT / f"hero-{th}.svg").write_text(hero(th), encoding="utf-8")
    for c in CARDS:
        (OUT / f"card-{c['slug']}.svg").write_text(card(c), encoding="utf-8")
    print("wrote", sorted(p.name for p in OUT.iterdir()))


if __name__ == "__main__":
    main()
