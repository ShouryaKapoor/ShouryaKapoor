"""Generate the static SVGs (hero banner + project cards) in light and dark.

Run:  python scripts/build_assets.py
Edit the CONTENT section below, re-run, commit. No dependencies.
"""

import json
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
        "slug": "vanepoint",
        "year": "2026",
        "title": "Vanepoint",
        "tag": "v0.1 preview",
        "wide": True,
        "desc": [
            "Turns your phone into a low-latency air mouse, presenter remote, inertia trackball and",
            "precision dial for your laptop. Encrypted end to end, paired devices only, no cloud.",
        ],
        "chips": ["Rust", "Tauri", "TypeScript", "Expo", "Noise Protocol"],
    },
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
        "slug": "vitalis",
        "year": "2025",
        "title": "Vitalis",
        "desc": [
            "AI symptom checker: describe how you feel, get",
            "structured, plain-language guidance back.",
        ],
        "chips": ["React", "FastAPI", "Python", "LLMs"],
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

CH = 210


def card(p: dict, idx: int, t: dict) -> str:
    CW = 1200 if p.get("wide") else 590
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
    num = f"{idx + 1:02d}"
    tag = ""
    if p.get("tag"):
        tw = len(p["tag"]) * 12 * CHAR + 22
        tag = (f'<rect x="56" y="24" width="{tw:.0f}" height="22" rx="11" fill="{t['a1']}" fill-opacity=".14"/>'
               f'<text x="{56 + tw / 2:.0f}" y="39" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t['a1']}">{esc(p['tag'])}</text>')
    art = ""
    if p.get("wide"):
        art = f"""
  <g opacity=".95">
    <rect x="860" y="58" width="62" height="112" rx="12" fill="none" stroke="{t['muted']}" stroke-width="2"/>
    <rect x="880" y="64" width="22" height="4" rx="2" fill="{t['dim']}"/>
    <circle cx="891" cy="122" r="18" fill="none" stroke="{t['a1']}" stroke-width="2" stroke-dasharray="3 4">
      <animateTransform attributeName="transform" type="rotate" from="0 891 122" to="360 891 122" dur="8s" repeatCount="indefinite"/>
    </circle>
    <circle cx="891" cy="122" r="5" fill="{t['a1']}"/>
    <path id="arc" d="M932 104 C 990 40, 1050 40, 1088 92" fill="none" stroke="{t['line']}" stroke-width="2" stroke-dasharray="2 7"/>
    <circle r="5" fill="{t['a2']}">
      <animateMotion dur="2.4s" repeatCount="indefinite" keyPoints="0;1" keyTimes="0;1" calcMode="spline" keySplines=".5 0 .5 1"><mpath href="#arc"/></animateMotion>
      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.15;.8;1" dur="2.4s" repeatCount="indefinite"/>
    </circle>
    <rect x="1030" y="100" width="128" height="80" rx="8" fill="none" stroke="{t['muted']}" stroke-width="2"/>
    <path d="M1016 186 h156" stroke="{t['muted']}" stroke-width="2" stroke-linecap="round"/>
    <path d="M1088 120 l0 26 l7 -6 l5 11 l5 -2 l-5 -11 l9 0 z" fill="{t['fg']}">
      <animateTransform attributeName="transform" type="translate" values="0 0;10 6;-6 10;0 0" dur="2.4s" repeatCount="indefinite"/>
    </path>
  </g>"""
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
  <text x="28" y="40" font-family="{MONO}" font-size="13" fill="{t['a1']}">{num}</text>{tag}
  <text x="{CW - 52}" y="40" text-anchor="end" font-family="{MONO}" font-size="13" fill="{t['dim']}">{p['year']}</text>
  <text x="{CW - 28}" y="42" text-anchor="end" font-family="{SANS}" font-size="20" fill="{t['muted']}">↗</text>
  <text x="28" y="76" font-family="{SANS}" font-size="26" font-weight="700" letter-spacing="-.5" fill="{t['fg']}">{esc(p['title'])}</text>
  {desc}
  {''.join(chips)}{art}
</svg>
"""


# ───────────────────────────── TOOLKIT ─────────────────────────────
# Icon paths come from Simple Icons (CC0), vendored in scripts/icons.json so
# nothing is fetched at render time. Edit that file to add/remove tools.

ICONS = json.loads((Path(__file__).parent / "icons.json").read_text(encoding="utf-8"))


def _lum(hex_: str) -> float:
    r, g, b = (int(hex_[i : i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _icon_color(hex_: str, mode: str, t: dict) -> str:
    """Keep brand colours, but rescue ones that vanish on the background."""
    lum = _lum(hex_)
    if mode == "dark" and lum < 0.22:
        return t["fg"]  # black logos (Next.js, GitHub) → near-white
    if mode == "light" and lum > 0.62:
        r, g, b = (int(int(hex_[i : i + 2], 16) * 0.62) for i in (0, 2, 4))
        return f"#{r:02x}{g:02x}{b:02x}"  # yellow/lime → darker shade
    return f"#{hex_}"


def toolkit(mode: str, t: dict) -> str:
    tile, step, x0, row_h, top = 56, 128, 196, 108, 34
    h = top + row_h * len(ICONS) + 6
    body, n = [], 0
    for r, (group, items) in enumerate(ICONS.items()):
        y = top + r * row_h
        body.append(f'<text x="28" y="{y + 34}" font-family="{MONO}" font-size="13" fill="{t["muted"]}">{esc(group)}</text>')
        if r:
            body.append(f'<line x1="28" y1="{y - 14}" x2="1172" y2="{y - 14}" stroke="{t["line"]}" stroke-dasharray="2 6"/>')
        for i, it in enumerate(items):
            x = x0 + i * step
            delay = 0.04 * n
            n += 1
            dur = delay + 0.45
            body.append(f"""<g opacity="1">
      <animate attributeName="opacity" values="0;0;1" keyTimes="0;{delay / dur:.3f};1" dur="{dur:.2f}s" fill="freeze"/>
      <rect x="{x}" y="{y}" width="{tile}" height="{tile}" rx="14" fill="{t['panel']}" stroke="{t['line']}"/>
      <path transform="translate({x + 14} {y + 14}) scale(1.1667)" d="{it['path']}" fill="{_icon_color(it['hex'], mode, t)}"/>
      <text x="{x + tile / 2}" y="{y + tile + 22}" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{t['fg']}">{esc(it['name'])}</text>
    </g>""")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{h}" viewBox="0 0 1200 {h}" role="img" aria-label="Toolkit: {esc(', '.join(i['name'] for v in ICONS.values() for i in v))}">
  {''.join(body)}
</svg>
"""


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("card-*.svg"):
        old.unlink()  # drop cards for projects no longer listed
    for mode, t in THEMES.items():
        (OUT / f"hero-{mode}.svg").write_text(hero(t), encoding="utf-8")
        (OUT / f"toolkit-{mode}.svg").write_text(toolkit(mode, t), encoding="utf-8")
        for i, p in enumerate(PROJECTS):
            (OUT / f"card-{p['slug']}-{mode}.svg").write_text(card(p, i, t), encoding="utf-8")
    print("wrote", sorted(x.name for x in OUT.glob("*.svg")))


if __name__ == "__main__":
    main()
