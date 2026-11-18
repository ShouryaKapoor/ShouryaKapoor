"""Shared palette + font stacks for every SVG in this profile.

GitHub serves README images through its camo proxy as <img>, so SVGs can't
load web fonts or run JS. We stick to system font stacks and SMIL/CSS
animation, which both survive the proxy.
"""

SANS = "'Inter','Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','SF Mono',ui-monospace,Menlo,Consolas,monospace"

THEMES = {
    "dark": {
        "bg": "#0b0d12",
        "panel": "#11141b",
        "line": "#1f2430",
        "fg": "#eef0f5",
        "muted": "#8b93a7",
        "dim": "#4a5163",
        "a1": "#7c5cff",  # violet
        "a2": "#22d3ee",  # cyan
        "a3": "#f472b6",  # pink
        "heat": ["#161b22", "#2a2357", "#4b3aa8", "#7c5cff", "#b9a6ff"],
    },
    "light": {
        "bg": "#fbfaf7",
        "panel": "#ffffff",
        "line": "#e7e5df",
        "fg": "#101218",
        "muted": "#5b6272",
        "dim": "#a3a8b4",
        "a1": "#6340f5",
        "a2": "#0891b2",
        "a3": "#db2777",
        "heat": ["#efede7", "#d9d0ff", "#ab98ff", "#7c5cff", "#4b2fd1"],
    },
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
