"""Generate the static SVGs (hero banner + project cards) in light and dark.

Run:  python scripts/build_assets.py
Edit the CONTENT section below, re-run, commit. No dependencies.
"""

from pathlib import Path

from theme import MONO, SANS, THEMES, esc

OUT = Path(__file__).resolve().parent.parent / "assets"

# ───────────────────────────── CONTENT ─────────────────────────────

TAGLINES = [
    "building AI agents that actually ship",
    "MSc Intelligent Systems @ Trinity College Dublin",
    "full-stack · GenAI · RAG · multi-agent systems",
]

STATUS = [
    ("based in", "Dublin, Ireland"),
    ("studying", "MSc CS · Intelligent Systems"),
    ("at", "Trinity College Dublin"),
    ("previously", "Project Lead · Kusum Healthcare"),
]

PROJECTS = [
    {
        "slug": "comic",
        "year": "2025",
        "title": "One-Shot Comic Maker",
        "desc": [
            "Prompt → finished comic strip. Gemini writes the script",
            "as structured JSON, Imagen 3 paints every panel.",
        ],
        "chips": ["React 19", "TypeScript", "Gemini", "Imagen 3"],
    },
    {
        "slug": "likho",
        "year": "2025",
        "title": "Likho · लिखो",
        "desc": [
            "A writing & storytelling platform with a flashlight-",
            "cursor intro, live story analytics and AI visuals.",
        ],
        "chips": ["Next.js 14", "Neon", "Drizzle", "Gemini"],
    },
    {
        "slug": "vitalis",
        "year": "2025",
        "title": "Vitalis",
        "desc": [
            "AI symptom checker: describe how you feel, get",
            "structured, plain-language guidance back.",
        ],
        "chips": ["React", "FastAPI", "Python", "LLMs"],
    },
    {
        "slug": "more",
        "year": "",
        "title": "More on GitHub",
        "desc": [
            "Vanepoint · Distill-it · Flex · Scriptify ·",
            "NavSwift, plus a lot of experiments.",
        ],
        "chips": ["browse all repos"],
    },
]

# ───────────────────────────── HERO ─────────────────────────────

W, H = 1200, 340
CHAR = 0.6  # monospace advance ≈ 0.6em


def hero(t: dict) -> str:
    cycle = 4 * len(TAGLINES)  # seconds per full loop
    fs = 22
    tx = 64 + 30  # text start after the "> " prompt

    typed = []
    for i, line in enumerate(TAGLINES):
        w = len(line) * fs * CHAR + 2
        # one slot = 4s of a 12s loop: type 1.2s, hold, erase 0.5s
        kt = "0;0.1;0.27;0.31;1"
        vals = f"0;{w:.0f};{w:.0f};0;0"
        xs = f"{tx};{tx + w:.0f};{tx + w:.0f};{tx};{tx}"
        typed.append(f"""
    <clipPath id="c{i}"><rect x="{tx}" y="222" height="34" width="0">
      <animate attributeName="width" values="{vals}" keyTimes="{kt}" dur="{cycle}s" begin="{i * 4}s" repeatCount="indefinite" calcMode="spline" keySplines=".4 0 .6 1;0 0 1 1;.4 0 .6 1;0 0 1 1"/>
    </rect></clipPath>
    <text x="{tx}" y="246" clip-path="url(#c{i})" font-family="{MONO}" font-size="{fs}" fill="{t['fg']}">{esc(line)}</text>
    <rect x="{tx}" y="226" width="11" height="26" rx="1.5" fill="{t['a2']}" opacity="0">
      <animate attributeName="x" values="{xs}" keyTimes="{kt}" dur="{cycle}s" begin="{i * 4}s" repeatCount="indefinite" calcMode="spline" keySplines=".4 0 .6 1;0 0 1 1;.4 0 .6 1;0 0 1 1"/>
      <animate attributeName="opacity" values="1;0" keyTimes="0;0.333" dur="{cycle}s" begin="{i * 4}s" repeatCount="indefinite" calcMode="discrete"/>
    </rect>""")

    rows = []
    py = 128
    for k, v in STATUS:
        rows.append(
            f'<text x="814" y="{py}" font-family="{MONO}" font-size="13" fill="{t["dim"]}">{esc(k)}</text>'
            f'<text x="906" y="{py}" font-family="{MONO}" font-size="13" fill="{t["fg"]}">{esc(v)}</text>'
        )
        py += 30

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Shourya Kapoor — software engineer, MSc Intelligent Systems at Trinity College Dublin">
  <defs>
    <linearGradient id="g" x1="0" x2="1">
      <stop offset="0" stop-color="{t['a1']}"/><stop offset=".5" stop-color="{t['a2']}"/><stop offset="1" stop-color="{t['a3']}"/>
    </linearGradient>
    <linearGradient id="gs" x1="0" x2="1">
      <stop offset="0" stop-color="{t['a1']}"/><stop offset=".5" stop-color="{t['a2']}"/><stop offset="1" stop-color="{t['a3']}"/><stop offset="1.5" stop-color="{t['a1']}"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="6s" repeatCount="indefinite"/>
    </linearGradient>
    <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="1" fill="{t['line']}"/>
    </pattern>
    <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="70"/></filter>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="22"/></clipPath>
  </defs>

  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="{t['bg']}"/>
    <rect width="{W}" height="{H}" fill="url(#dots)"/>
    <g filter="url(#blur)" opacity=".55">
      <circle cx="980" cy="60" r="150" fill="{t['a1']}">
        <animate attributeName="cx" values="980;880;980" dur="14s" repeatCount="indefinite"/>
        <animate attributeName="cy" values="60;120;60" dur="11s" repeatCount="indefinite"/>
      </circle>
      <circle cx="1120" cy="300" r="120" fill="{t['a2']}">
        <animate attributeName="cx" values="1120;1040;1120" dur="12s" repeatCount="indefinite"/>
      </circle>
      <circle cx="640" cy="380" r="110" fill="{t['a3']}" opacity=".7">
        <animate attributeName="cx" values="640;720;640" dur="16s" repeatCount="indefinite"/>
      </circle>
    </g>
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="21.5" fill="none" stroke="{t['line']}"/>

  <!-- window chrome -->
  <circle cx="34" cy="32" r="6" fill="#ff5f57"/><circle cx="54" cy="32" r="6" fill="#febc2e"/><circle cx="74" cy="32" r="6" fill="#28c840"/>
  <text x="{W / 2}" y="37" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{t['dim']}">~/shourya-kapoor — zsh</text>
  <line x1="0" y1="58" x2="{W}" y2="58" stroke="{t['line']}"/>

  <!-- intro -->
  <text x="64" y="118" font-family="{MONO}" font-size="16" fill="{t['muted']}">hello, world — I'm</text>
  <text x="60" y="190" font-family="{SANS}" font-size="74" font-weight="800" letter-spacing="-2.5" fill="{t['fg']}">Shourya Kapoor<tspan fill="{t['a2']}">.</tspan></text>

  <text x="64" y="246" font-family="{MONO}" font-size="22" font-weight="700" fill="{t['a1']}">&gt;</text>{''.join(typed)}

  <rect x="64" y="284" width="300" height="4" rx="2" fill="url(#gs)"/>

  <!-- status panel -->
  <rect x="790" y="86" width="368" height="202" rx="14" fill="{t['panel']}" fill-opacity=".82" stroke="{t['line']}"/>
  <circle cx="818" cy="254" r="5" fill="#28c840">
    <animate attributeName="r" values="5;8;5" dur="2s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="1;.35;1" dur="2s" repeatCount="indefinite"/>
  </circle>
  <circle cx="818" cy="254" r="4" fill="#28c840"/>
  <text x="834" y="259" font-family="{MONO}" font-size="13" fill="{t['fg']}">open to internships &amp; grad roles</text>
  <line x1="814" y1="232" x2="1134" y2="232" stroke="{t['line']}"/>
  {''.join(rows)}
</svg>
"""


# ───────────────────────────── CARDS ─────────────────────────────

CW, CH = 580, 210


def card(p: dict, idx: int, t: dict) -> str:
    chips, cx = [], 28
    for c in p["chips"]:
        w = len(c) * 12 * CHAR + 22
        chips.append(
            f'<rect x="{cx}" y="160" width="{w:.0f}" height="26" rx="13" fill="none" stroke="{t["line"]}"/>'
            f'<text x="{cx + w / 2:.0f}" y="177" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t["muted"]}">{esc(c)}</text>'
        )
        cx += w + 8
    desc = "".join(
        f'<text x="28" y="{108 + i * 22}" font-family="{SANS}" font-size="15" fill="{t["muted"]}">{esc(d)}</text>'
        for i, d in enumerate(p["desc"])
    )
    num = "··" if p["slug"] == "more" else f"{idx + 1:02d}"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}" role="img" aria-label="{esc(p['title'])}">
  <defs>
    <linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{t['a1']}"/><stop offset=".5" stop-color="{t['a2']}"/><stop offset="1" stop-color="{t['a3']}"/></linearGradient>
    <radialGradient id="glow" cx="1" cy="0" r="1"><stop offset="0" stop-color="{t['a1']}" stop-opacity=".22"/><stop offset="1" stop-color="{t['a1']}" stop-opacity="0"/></radialGradient>
    <clipPath id="f"><rect width="{CW}" height="{CH}" rx="16"/></clipPath>
  </defs>
  <g clip-path="url(#f)">
    <rect width="{CW}" height="{CH}" fill="{t['panel']}"/>
    <rect width="{CW}" height="{CH}" fill="url(#glow)"/>
    <rect width="{CW}" height="3" fill="url(#g)"/>
  </g>
  <rect x=".5" y=".5" width="{CW - 1}" height="{CH - 1}" rx="15.5" fill="none" stroke="{t['line']}"/>
  <text x="28" y="40" font-family="{MONO}" font-size="13" fill="{t['a1']}">{num}</text>
  <text x="{CW - 52}" y="40" text-anchor="end" font-family="{MONO}" font-size="13" fill="{t['dim']}">{p['year']}</text>
  <text x="{CW - 28}" y="42" text-anchor="end" font-family="{SANS}" font-size="20" fill="{t['muted']}">↗</text>
  <text x="28" y="76" font-family="{SANS}" font-size="26" font-weight="700" letter-spacing="-.5" fill="{t['fg']}">{esc(p['title'])}</text>
  {desc}
  {''.join(chips)}
</svg>
"""


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for mode, t in THEMES.items():
        (OUT / f"hero-{mode}.svg").write_text(hero(t), encoding="utf-8")
        for i, p in enumerate(PROJECTS):
            (OUT / f"card-{p['slug']}-{mode}.svg").write_text(card(p, i, t), encoding="utf-8")
    print("wrote", sorted(x.name for x in OUT.glob("*.svg")))


if __name__ == "__main__":
    main()
