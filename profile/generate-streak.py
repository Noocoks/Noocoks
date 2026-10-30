#!/usr/bin/env python3
"""Turn upstream streak stats into the custom Noocoks Contribution Reactor."""
from pathlib import Path
import re
p = Path("profile/streak.svg")
src = p.read_text(encoding="utf-8")
def after(comment, default="0"):
    part = src.split("<!-- " + comment + " -->", 1)
    if len(part) < 2:
        return default
    m = re.search(r'>(\\s*)([\\d,]+)(\\s*)</text>', part[1])
    return m.group(2).replace(",", "") if m else default
total = after("Total Contributions big number")
current = after("Current Streak big number")
longest = after("Longest Streak big number")
def date_after(comment, default="CURRENT PERIOD"):
    part = src.split("<!-- " + comment + " -->", 1)
    if len(part) < 2:
        return default
    m = re.search(r'>([^<>]+)</text>', part[1])
    return m.group(1).strip() if m else default
period = date_after("Total Contributions range")
svg = r'''<svg xmlns="http://www.w3.org/2000/svg" width="680" height="260" viewBox="0 0 680 260" role="img" aria-labelledby="title desc">
<title id="title">NOOCOKS // Contribution Reactor</title><desc id="desc">Contribution streak: 34 total contributions, current streak 1 day, longest streak 3 days.</desc>
<defs>
 <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#121317"/><stop offset=".56" stop-color="#080809"/><stop offset="1" stop-color="#18070C"/></linearGradient>
 <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#790018"/><stop offset=".5" stop-color="#3B252C"/><stop offset="1" stop-color="#858B93"/></linearGradient>
 <linearGradient id="fire" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#C02A4B"/><stop offset="1" stop-color="#4D0011"/></linearGradient>
 <radialGradient id="core"><stop stop-color="#790018" stop-opacity=".42"/><stop offset="1" stop-color="#790018" stop-opacity="0"/></radialGradient>
 <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="#858B93" stroke-opacity=".07"/></pattern>
 <filter id="glow"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <style>
 text{font-family:'JetBrains Mono','SFMono-Regular',Consolas,monospace}.micro{font-size:9px;letter-spacing:2px;fill:#858B93}.label{font-size:10px;letter-spacing:1.4px;fill:#A6ABB2}.value{font-size:35px;font-weight:900;fill:#E4E6E9}.small{font-size:9px;letter-spacing:1px;fill:#858B93}
 .ring{transform-origin:center;animation:rotate 16s linear infinite}.pulse{animation:pulse 2.5s ease-in-out infinite}.rise{opacity:0;animation:appear .7s ease-out forwards}.d1{animation-delay:.1s}.d2{animation-delay:.25s}.d3{animation-delay:.4s}
 @keyframes rotate{to{transform:rotate(360deg)}}@keyframes pulse{0%,100%{opacity:.35}50%{opacity:1}}@keyframes appear{to{opacity:1}}
 </style>
</defs>
<rect x="1" y="1" width="678" height="258" rx="12" fill="url(#bg)" stroke="#555B63" stroke-opacity=".65"/><rect x="1" y="1" width="678" height="258" rx="12" fill="url(#grid)"/><rect x="1" y="1" width="678" height="4" rx="2" fill="url(#edge)"/><path d="M20 18V242" stroke="#790018" stroke-width="3"/>
<text x="30" y="28" class="micro">NOOCOKS // CONTRIBUTION ENGINE</text><g transform="translate(548 15)"><rect width="102" height="23" rx="4" fill="#790018" fill-opacity=".18" stroke="#790018"/><circle cx="12" cy="11.5" r="3.5" fill="#A21D3B" class="pulse"/><text x="23" y="15" font-size="9" fill="#D8DADD" letter-spacing="1">STREAK SYS</text></g>
<text x="30" y="72" font-size="29" font-weight="900" fill="#E4E6E9" letter-spacing="1">CONTRIBUTION</text><text x="30" y="101" font-size="29" font-weight="900" fill="#790018" letter-spacing="1">REACTOR_</text>
<ellipse cx="340" cy="168" rx="185" ry="72" fill="url(#core)"/>
<g transform="translate(130 177)">
 <rect x="-95" y="-48" width="190" height="92" rx="7" fill="#111216" stroke="#555B63" stroke-opacity=".65"/>
 <text x="0" y="-21" text-anchor="middle" class="label">TOTAL CONTRIBUTIONS</text><text x="0" y="20" text-anchor="middle" class="value">34</text><text x="0" y="36" text-anchor="middle" class="small">MAY 31 — PRESENT</text>
</g>
<g transform="translate(340 168)">
 <circle r="65" fill="none" stroke="#35383E" stroke-width="1.5" stroke-dasharray="3 6"/>
 <circle class="ring" r="55" fill="none" stroke="#790018" stroke-width="3" stroke-dasharray="90 18 34 18 54 18" opacity=".85"/>
 <circle r="43" fill="#790018" fill-opacity=".08" stroke="#858B93" stroke-opacity=".3"/>
 <path d="M0 -24C0 -24 14 -7 14 5C14 17 7 26 0 26C-9 26 -16 18 -16 8C-16 0 -10 -11 -4 -17C-4 -8 2 -5 3 0C8 -9 0 -24 0 -24Z" fill="url(#fire)" filter="url(#glow)" class="pulse"/>
 <text x="0" y="50" text-anchor="middle" class="small">ACTIVE</text>
</g>
<g transform="translate(550 177)">
 <rect x="-95" y="-48" width="190" height="92" rx="7" fill="#111216" stroke="#555B63" stroke-opacity=".65"/>
 <text x="0" y="-21" text-anchor="middle" class="label">CURRENT STREAK</text><text x="0" y="20" text-anchor="middle" class="value">1<tspan font-size="15" fill="#858B93"> DAY</tspan></text><text x="0" y="36" text-anchor="middle" class="small">LONGEST // 3 DAYS</text>
</g>
<text x="650" y="245" text-anchor="end" font-size="8" letter-spacing="2" fill="#555B63">CRIMSON / STEEL // KEEP THE SIGNAL ALIVE</text>
</svg>'''
svg = svg.replace("TOTAL_CONTRIBUTIONS", total).replace("CURRENT_STREAK", current).replace("LONGEST_STREAK", longest).replace("TOTAL_PERIOD", period)
p.write_text(svg, encoding="utf-8")
