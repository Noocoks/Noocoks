#!/usr/bin/env python3
"""Generate a compact, live repository activity panel from the GitHub REST API."""
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.request import Request, urlopen
import json
import os

username = os.environ.get("GITHUB_REPOSITORY_OWNER", "Noocoks")
token = os.environ.get("GH_TOKEN", "")
headers = {"Accept": "application/vnd.github+json", "User-Agent": "Noocoks-profile-telemetry"}
if token:
    headers["Authorization"] = f"Bearer {token}"
request = Request(
    f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated&type=owner",
    headers=headers,
)
with urlopen(request, timeout=30) as response:
    repos = json.load(response)

owned = [repo for repo in repos if not repo.get("fork", False)]
stars = sum(repo.get("stargazers_count", 0) for repo in owned)
forks = sum(repo.get("forks_count", 0) for repo in owned)
recent = sorted(owned, key=lambda repo: repo.get("pushed_at") or "", reverse=True)[:3]

def ago(iso):
    if not iso:
        return "NO PUSH DATA"
    then = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    days = max(0, (datetime.now(timezone.utc) - then).days)
    if days == 0:
        return "UPDATED TODAY"
    if days == 1:
        return "UPDATED 1 DAY AGO"
    if days < 30:
        return f"UPDATED {days} DAYS AGO"
    months = days // 30
    return f"UPDATED {months} MONTH" + ("" if months == 1 else "S")

rows = []
for i, repo in enumerate(recent):
    y = 192 + i * 31
    name = escape(repo.get("name", "Repository"))[:30]
    description = escape(repo.get("description") or "No description provided.")[:52]
    pushed = ago(repo.get("pushed_at"))
    rows.append(
        f'<g transform="translate(30 {y})">'
        f'<circle cx="4" cy="-4" r="3" fill="#A21D3B"/>'
        f'<text x="17" y="0" class="repo">{name}</text>'
        f'<text x="17" y="13" class="desc">{description}</text>'
        f'<text x="620" y="0" text-anchor="end" class="date">{pushed}</text>'
        f'</g>'
    )

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="680" height="310" viewBox="0 0 680 310" role="img" aria-labelledby="title desc">
<title id="title">NOOCOKS // Repository Pulse</title>
<desc id="desc">Live repository overview: {len(owned)} public repositories, {stars} stars and {forks} forks. Recently pushed projects are listed below.</desc>
<defs>
 <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#121317"/><stop offset=".56" stop-color="#080809"/><stop offset="1" stop-color="#18070C"/></linearGradient>
 <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#790018"/><stop offset=".5" stop-color="#3B252C"/><stop offset="1" stop-color="#858B93"/></linearGradient>
 <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="#858B93" stroke-opacity=".07"/></pattern>
 <radialGradient id="glow"><stop stop-color="#790018" stop-opacity=".25"/><stop offset="1" stop-color="#790018" stop-opacity="0"/></radialGradient>
 <style>
 text{font-family:'JetBrains Mono','SFMono-Regular',Consolas,monospace}
 .micro{font-size:9px;letter-spacing:2px;fill:#858B93}
 .label{font-size:9px;letter-spacing:1.3px;fill:#A6ABB2}
 .value{font-size:25px;font-weight:900;fill:#E4E6E9}
 .repo{font-size:11px;font-weight:700;fill:#D8DADD}
 .desc{font-size:8px;fill:#777E87}
 .date{font-size:8px;letter-spacing:.5px;fill:#858B93}
 </style>
</defs>
<rect x="1" y="1" width="678" height="308" rx="12" fill="url(#bg)" stroke="#555B63" stroke-opacity=".65"/>
<rect x="1" y="1" width="678" height="308" rx="12" fill="url(#grid)"/>
<rect x="1" y="1" width="678" height="4" rx="2" fill="url(#edge)"/>
<path d="M20 18V292" stroke="#790018" stroke-width="3"/>
<ellipse cx="560" cy="95" rx="175" ry="110" fill="url(#glow)"/>
<text x="30" y="28" class="micro">NOOCOKS // OPEN SOURCE MONITOR</text>
<g transform="translate(548 15)"><rect width="102" height="23" rx="4" fill="#790018" fill-opacity=".18" stroke="#790018"/><circle cx="12" cy="11.5" r="3.5" fill="#A21D3B"/><text x="23" y="15" font-size="9" fill="#D8DADD" letter-spacing="1">REPO PULSE</text></g>
<text x="30" y="72" font-size="29" font-weight="900" fill="#E4E6E9" letter-spacing="1">REPOSITORY</text>
<text x="30" y="101" font-size="29" font-weight="900" fill="#790018" letter-spacing="1">PULSE_</text>
<g transform="translate(30 119)">
 <rect width="190" height="51" rx="6" fill="#790018" fill-opacity=".12" stroke="#790018" stroke-opacity=".7"/>
 <text x="14" y="18" class="label">PUBLIC PROJECTS</text><text x="14" y="43" class="value">{len(owned)}</text>
 <rect x="205" width="190" height="51" rx="6" fill="#111216" stroke="#555B63" stroke-opacity=".7"/>
 <text x="219" y="18" class="label">TOTAL STARS</text><text x="219" y="43" class="value">{stars}</text>
 <rect x="410" width="190" height="51" rx="6" fill="#111216" stroke="#555B63" stroke-opacity=".7"/>
 <text x="424" y="18" class="label">TOTAL FORKS</text><text x="424" y="43" class="value">{forks}</text>
</g>
<path d="M30 181H650" stroke="#858B93" stroke-opacity=".25"/>
<text x="30" y="188" class="micro">RECENTLY PUSHED // LATEST PROJECT SIGNALS</text>
{''.join(rows)}
<text x="650" y="298" text-anchor="end" font-size="8" letter-spacing="2" fill="#555B63">LIVE GITHUB API // OWNER REPOSITORIES</text>
</svg>'''
Path("profile/repositories.svg").write_text(svg, encoding="utf-8")
print(f"Generated repository pulse for {len(owned)} public repositories.")
