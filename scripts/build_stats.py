"""Build assets/stats-{dark,light}.svg from live GitHub data.

Runs daily in .github/workflows/profile.yml with the built-in GITHUB_TOKEN,
so the card is a committed file: no third-party service, no rate-limit 503s.

Local test without network:  python scripts/build_stats.py --mock
"""

import json
import os
import sys
import urllib.request
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

from theme import MONO, SANS, THEMES, esc

USER = os.environ.get("GH_USER", "ShouryaKapoor")
OUT = Path(__file__).resolve().parent.parent / "assets"
IGNORE_LANGS = {"Jupyter Notebook", "Procfile", "Dockerfile", "Makefile"}

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 8, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}
"""


def fetch() -> dict:
    token = os.environ["GITHUB_TOKEN"]
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.load(r)
    if "errors" in body:
        raise SystemExit(f"GraphQL error: {body['errors']}")
    return body["data"]["user"]


def mock() -> dict:
    import random

    random.seed(7)
    start = date.today() - timedelta(days=364)
    weeks, d = [], start - timedelta(days=start.weekday() + 1)
    while d <= date.today():
        days = []
        for _ in range(7):
            if d <= date.today():
                days.append({"date": d.isoformat(), "contributionCount": random.choice([0, 0, 1, 2, 3, 5, 8])})
            d += timedelta(days=1)
        weeks.append({"contributionDays": days})
    lang = lambda n, c, s: {"size": s, "node": {"name": n, "color": c}}
    return {
        "followers": {"totalCount": 42},
        "contributionsCollection": {"contributionCalendar": {"totalContributions": 812, "weeks": weeks}},
        "repositories": {
            "totalCount": 24,
            "nodes": [
                {"stargazerCount": 3, "languages": {"edges": [lang("TypeScript", "#3178c6", 900), lang("CSS", "#663399", 120)]}},
                {"stargazerCount": 2, "languages": {"edges": [lang("Python", "#3572A5", 700), lang("JavaScript", "#f1e05a", 400)]}},
                {"stargazerCount": 1, "languages": {"edges": [lang("Java", "#b07219", 300), lang("HTML", "#e34c26", 200)]}},
            ],
        },
    }


# ───────────────────────────── metrics ─────────────────────────────


def streaks(days: list[dict]) -> tuple[int, int]:
    """(current, longest). Today with 0 doesn't break the current streak yet."""
    counts = [d["contributionCount"] for d in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    cur, i = 0, len(counts) - 1
    if i >= 0 and counts[i] == 0:
        i -= 1  # grace for today
    while i >= 0 and counts[i]:
        cur, i = cur + 1, i - 1
    return cur, longest


def top_languages(repos: list[dict], n: int = 5) -> list[tuple[str, str, float]]:
    """Return [(name, color, share)] for the n biggest languages by bytes.

    Bytes are summed across all public, non-fork repos. Notebooks and build
    files are ignored because they inflate totals without saying much.
    """
    size, color = defaultdict(int), {}
    for r in repos:
        for e in r["languages"]["edges"]:
            name = e["node"]["name"]
            if name in IGNORE_LANGS:
                continue
            size[name] += e["size"]
            color[name] = e["node"]["color"] or "#888888"
    total = sum(size.values()) or 1
    ranked = sorted(size.items(), key=lambda kv: kv[1], reverse=True)[:n]
    return [(name, color[name], s / total) for name, s in ranked]


# ───────────────────────────── render ─────────────────────────────

W, H = 1200, 250


def render(u: dict, t: dict) -> str:
    cal = u["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    cur, longest = streaks(days)
    repos = u["repositories"]["nodes"]
    stars = sum(r["stargazerCount"] for r in repos)
    langs = top_languages(repos)

    # stat tiles
    tiles = [
        (f"{cal['totalContributions']:,}", "contributions / year"),
        (str(cur), "day streak (current)"),
        (str(longest), "day streak (longest)"),
        (str(u["repositories"]["totalCount"]), "public repos"),
    ]
    tile_svg = []
    for i, (val, label) in enumerate(tiles):
        x = 40 + (i % 2) * 180
        y = 102 + (i // 2) * 82
        tile_svg.append(
            f'<text x="{x}" y="{y}" font-family="{SANS}" font-size="36" font-weight="800" letter-spacing="-1" fill="{t["fg"]}">{val}</text>'
            f'<text x="{x}" y="{y + 24}" font-family="{MONO}" font-size="12" fill="{t["muted"]}">{esc(label)}</text>'
        )

    # heatmap: last 26 weeks
    weeks = cal["weeks"][-26:]
    peak = max((d["contributionCount"] for w in weeks for d in w["contributionDays"]), default=1) or 1
    cells, cs, gap, hx, hy = [], 11, 3, 436, 74
    for wi, w in enumerate(weeks):
        for d in w["contributionDays"]:
            dow = (date.fromisoformat(d["date"]).weekday() + 1) % 7  # Sun=0
            c = d["contributionCount"]
            lvl = 0 if c == 0 else min(4, 1 + int(3 * c / peak))
            cells.append(
                f'<rect x="{hx + wi * (cs + gap)}" y="{hy + dow * (cs + gap)}" width="{cs}" height="{cs}" rx="3" fill="{t["heat"][lvl]}"/>'
            )
    legend_x = hx + 26 * (cs + gap) - 5 * (cs + gap) - 4
    legend = "".join(
        f'<rect x="{legend_x + i * (cs + gap)}" y="{hy + 7 * (cs + gap) + 8}" width="{cs}" height="{cs}" rx="3" fill="{c}"/>' for i, c in enumerate(t["heat"])
    )

    # language bar
    lx, ly, lw = 866, 92, 294
    bar, legend_l, off = [], [], 0.0
    for i, (name, col, share) in enumerate(langs):
        bar.append(f'<rect x="{lx + off * lw:.1f}" y="{ly}" width="{max(share * lw - 2, 2):.1f}" height="10" fill="{col}"/>')
        off += share
        yy = ly + 36 + i * 22
        legend_l.append(
            f'<circle cx="{lx + 5}" cy="{yy - 4}" r="5" fill="{col}"/>'
            f'<text x="{lx + 18}" y="{yy}" font-family="{SANS}" font-size="14" fill="{t["fg"]}">{esc(name)}</text>'
            f'<text x="{lx + lw}" y="{yy}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{t["muted"]}">{share * 100:.1f}%</text>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="GitHub stats for {USER}">
  <defs>
    <linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{t['a1']}"/><stop offset=".5" stop-color="{t['a2']}"/><stop offset="1" stop-color="{t['a3']}"/></linearGradient>
    <clipPath id="f"><rect width="{W}" height="{H}" rx="18"/></clipPath>
    <clipPath id="bar"><rect x="{lx}" y="{ly}" width="{lw}" height="10" rx="5"/></clipPath>
  </defs>
  <g clip-path="url(#f)"><rect width="{W}" height="{H}" fill="{t['panel']}"/><rect width="{W}" height="3" fill="url(#g)"/></g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="17.5" fill="none" stroke="{t['line']}"/>

  <text x="40" y="46" font-family="{MONO}" font-size="13" fill="{t['a1']}">$ gh stats --user {esc(USER.lower())}</text>
  <text x="{W - 40}" y="46" text-anchor="end" font-family="{MONO}" font-size="12" fill="{t['dim']}">updated {date.today().isoformat()} · ★ {stars}</text>
  {''.join(tile_svg)}

  <line x1="404" y1="70" x2="404" y2="210" stroke="{t['line']}"/>
  <text x="{hx}" y="60" font-family="{MONO}" font-size="12" fill="{t['muted']}">last 26 weeks</text>
  {''.join(cells)}
  <text x="{legend_x - 8}" y="{hy + 7 * (cs + gap) + 18}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{t['dim']}">less</text>
  {legend}
  <text x="{legend_x + 5 * (cs + gap) + 4}" y="{hy + 7 * (cs + gap) + 18}" font-family="{MONO}" font-size="11" fill="{t['dim']}">more</text>

  <line x1="836" y1="70" x2="836" y2="210" stroke="{t['line']}"/>
  <text x="{lx}" y="78" font-family="{MONO}" font-size="12" fill="{t['muted']}">top languages</text>
  <g clip-path="url(#bar)"><rect x="{lx}" y="{ly}" width="{lw}" height="10" fill="{t['line']}"/>{''.join(bar)}</g>
  {''.join(legend_l)}
</svg>
"""


def main() -> None:
    u = mock() if "--mock" in sys.argv else fetch()
    OUT.mkdir(exist_ok=True)
    for mode, t in THEMES.items():
        (OUT / f"stats-{mode}.svg").write_text(render(u, t), encoding="utf-8")
    print("stats written")


if __name__ == "__main__":
    main()
