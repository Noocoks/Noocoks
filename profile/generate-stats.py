#!/usr/bin/env python3
"""Turn the upstream GitHub Readme Stats SVG into the custom Noocoks dashboard."""
from pathlib import Path
import re
p = Path("profile/stats.svg")
src = p.read_text(encoding="utf-8")
def metric(testid, default="0"):
    m = re.search(r'data-testid="' + re.escape(testid) + r'"[^>]*>([\\d,]+)</text>', src)
    return (m.group(1).replace(",", "") if m else default)
stars, commits, prs, issues, contributed = [metric(k) for k in ("stars", "commits", "prs", "issues", "contribs")]
rank_match = re.search(r"Rank:\\s*([A-Z])", src)
rank = rank_match.group(1) if rank_match else "C"
svg = r'''<svg xmlns="http://www.w3.org/2000/svg" width="680" height="310" viewBox="0 0 680 310" role="img" aria-labelledby="title desc">
<title id="title">NOOCOKS // GitHub Core Stats</title><desc id="desc">GitHub profile statistics: 23 commits, 0 stars, 0 pull requests, 0 issues, 0 repositories contributed to last year. Rank C.</desc>
<defs>
 <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#121317"/><stop offset=".55" stop-color="#080809"/><stop offset="1" stop-color="#19070D"/></linearGradient>
 <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#790018"/><stop offset=".52" stop-color="#3B252C"/><stop offset="1" stop-color="#858B93"/></linearGradient>
 <linearGradient id="red" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#A21D3B"/><stop offset="1" stop-color="#4D0011"/></linearGradient>
 <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="#858B93" stroke-opacity=".07"/></pattern>
 <radialGradient id="glow"><stop stop-color="#790018" stop-opacity=".25"/><stop offset="1" stop-color="#790018" stop-opacity="0"/></radialGradient>
 <filter id="blur"><feGaussianBlur stdDeviation="8"/></filter>
 <style>
 text{font-family:'JetBrains Mono','SFMono-Regular',Consolas,monospace}
 .micro{font-size:9px;letter-spacing:2px;fill:#858B93}.label{font-size:10px;letter-spacing:1.5px;fill:#A6ABB2}.value{font-size:27px;font-weight:800;fill:#E4E6E9}.tiny{font-size:8px;letter-spacing:1.5px;fill:#666D75}
 .metric{opacity:0;animation:rise .65s ease-out forwards}.m1{animation-delay:.12s}.m2{animation-delay:.22s}.m3{animation-delay:.32s}.m4{animation-delay:.42s}
 .scan{animation:scan 6s linear infinite}.pulse{animation:pulse 2.5s ease-in-out infinite}
 @keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}@keyframes scan{from{transform:translateX(-120px)}to{transform:translateX(800px)}}@keyframes pulse{0%,100%{opacity:.35}50%{opacity:1}}
 </style>
</defs>
<rect x="1" y="1" width="678" height="308" rx="12" fill="url(#bg)" stroke="#555B63" stroke-opacity=".65"/><rect x="1" y="1" width="678" height="308" rx="12" fill="url(#grid)"/><rect x="1" y="1" width="678" height="4" rx="2" fill="url(#edge)"/><path d="M20 18V292" stroke="#790018" stroke-width="3"/>
<ellipse cx="560" cy="105" rx="175" ry="125" fill="url(#glow)" filter="url(#blur)"/>
<text x="30" y="28" class="micro">NOOCOKS // GITHUB TELEMETRY</text>
<g transform="translate(557 15)"><rect width="94" height="23" rx="4" fill="#790018" fill-opacity=".18" stroke="#790018"/><circle cx="12" cy="11.5" r="3.5" fill="#A21D3B" class="pulse"/><text x="23" y="15" fill="#D8DADD" font-size="9" letter-spacing="1">RANK / C</text></g>
<text x="30" y="75" fill="#E4E6E9" font-size="30" font-weight="900" letter-spacing="1">GITHUB</text><text x="30" y="105" fill="#790018" font-size="30" font-weight="900" letter-spacing="1">CORE_STATS_</text>
<text x="32" y="132" class="micro">ACTIVITY // REPOSITORY IMPACT // CONTRIBUTIONS</text>
<path d="M30 145H650" stroke="#858B93" stroke-opacity=".25"/>
<g transform="translate(30 162)">
 <rect width="298" height="112" rx="7" fill="#790018" fill-opacity=".12" stroke="#790018" stroke-opacity=".75"/>
 <rect x="0" y="0" width="4" height="112" rx="2" fill="url(#red)"/>
 <text x="19" y="24" class="label">TOTAL COMMITS</text><text x="19" y="72" class="value">23</text>
 <text x="19" y="94" class="tiny">CODE / PUSH / HISTORY</text>
 <path d="M205 20V92" stroke="#858B93" stroke-opacity=".22"/>
 <path d="M222 83L239 66L253 73L272 42" fill="none" stroke="#A21D3B" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
 <path d="M222 83L239 66L253 73L272 42V91H222Z" fill="#790018" fill-opacity=".18"/>
 <circle cx="272" cy="42" r="3.5" fill="#A21D3B"/>
</g>
<g class="metric m1" transform="translate(348 162)"><rect width="142" height="52" rx="6" fill="#111216" stroke="#555B63" stroke-opacity=".7"/><text x="13" y="19" class="label">STARS</text><text x="13" y="43" class="value">0</text><path d="M113 14l4 8 9 1-7 6 2 9-8-4-8 4 2-9-7-6 9-1z" fill="#790018" opacity=".8"/></g>
<g class="metric m2" transform="translate(506 162)"><rect width="144" height="52" rx="6" fill="#111216" stroke="#555B63" stroke-opacity=".7"/><text x="13" y="19" class="label">PULL REQUESTS</text><text x="13" y="43" class="value">0</text><path d="M119 15v19m0-19l-6 6m6-6l6 6m-6 13l-6-6m6 6l6-6" stroke="#858B93" stroke-width="2" fill="none" stroke-linecap="round"/></g>
<g class="metric m3" transform="translate(348 222)"><rect width="142" height="52" rx="6" fill="#111216" stroke="#555B63" stroke-opacity=".7"/><text x="13" y="19" class="label">ISSUES</text><text x="13" y="43" class="value">0</text><circle cx="120" cy="28" r="9" fill="none" stroke="#858B93" stroke-width="2"/><path d="M120 22v7m0 4v1" stroke="#858B93" stroke-width="2" stroke-linecap="round"/></g>
<g class="metric m4" transform="translate(506 222)"><rect width="144" height="52" rx="6" fill="#111216" stroke="#555B63" stroke-opacity=".7"/><text x="13" y="19" class="label">CONTRIBUTED</text><text x="13" y="43" class="value">0</text><path d="M112 34l7-7 7 7m-7-7v16" fill="none" stroke="#A21D3B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g>
<text x="650" y="296" text-anchor="end" class="tiny">CRIMSON / STEEL // PROFILE NODE 001</text>
</svg>'''
svg = svg.replace("TOTAL_STARS", stars).replace("TOTAL_COMMITS", commits).replace("TOTAL_PRS", prs).replace("TOTAL_ISSUES", issues).replace("TOTAL_CONTRIBUTED", contributed).replace("RANK_LETTER", rank)
p.write_text(svg, encoding="utf-8")
