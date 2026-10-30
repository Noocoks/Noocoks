#!/usr/bin/env python3
"""Rebuild the custom Language Matrix SVG from the generated GitHub Readme Stats card."""
from pathlib import Path
import html
import re

card = Path("profile/top-langs.svg")
source = card.read_text(encoding="utf-8")
# Extract language label and percentage from the upstream compact card.
pairs = re.findall(r">\s*([A-Za-z][A-Za-z0-9+#.]*)\s+(\d+(?:\.\d+)?)%\s*</text>", source)
langs = []
seen = set()
for name, percentage in pairs:
    key = name.casefold()
    if key not in seen:
        seen.add(key)
        langs.append((name, float(percentage)))
if not langs:
    raise SystemExit("Could not parse languages from generated upstream SVG; keeping existing card.")
langs = sorted(langs, key=lambda item: item[1], reverse=True)[:5]
total = sum(value for _, value in langs)
if total <= 0:
    raise SystemExit("Language percentages sum to zero.")

palette = [
    ("#790018", "#A21D3B"),
    ("#555B63", "#858B93"),
    ("#641326", "#9B4258"),
    ("#686E76", "#B0B5BC"),
    ("#3F252C", "#858B93"),
]
width = 620
bar_x, bar_y, bar_w, bar_h = 30, 143, 620, 16
x = bar_x
segments = []
rows = []
for index, (name, value) in enumerate(langs):
    share = value / total
    segment_w = bar_w * share
    c1, c2 = palette[index % len(palette)]
    segments.append(f'<rect x="{x:.2f}" y="{bar_y}" width="{segment_w:.2f}" height="{bar_h}" fill="{c1}"/>')
    x += segment_w
    y = 210 + index * 35
    display_name = html.escape(name.upper())
    pct = f"{value:.2f}"
    rows.append(f"""
<g class="row r{index+1}" transform="translate(30 {y})">
 <text x="0" y="0" class="label">{display_name}</text>
 <text x="620" y="0" text-anchor="end" class="num">{pct}<tspan font-size="11" fill="#858B93">%</tspan></text>
 <rect x="0" y="11" width="620" height="8" rx="3" fill="#24262B"/>
 <rect class="bar" x="0" y="11" width="{620*share:.2f}" height="8" rx="3" fill="{c1}"/>
 <path d="M0 25H620" stroke="#858B93" stroke-opacity=".12"/>
</g>""")
# Adjust canvas height and row spacing to fit 3-5 languages.
row_gap = 35
last_y = 210 + (len(langs)-1)*row_gap
height = last_y + 42
rows_svg = "\n".join(rows)
segments_svg = "\n ".join(segments)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="680" height="{height}" viewBox="0 0 680 {height}" role="img" aria-labelledby="title desc">
<title id="title">NOOCOKS // Language Matrix</title>
<desc id="desc">Language distribution: {html.escape(", ".join(f"{n} {v:.2f} percent" for n,v in langs))}.</desc>
<defs>
 <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#111216"/><stop offset=".56" stop-color="#080809"/><stop offset="1" stop-color="#18080D"/></linearGradient>
 <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#790018"/><stop offset=".5" stop-color="#3A2028"/><stop offset="1" stop-color="#858B93"/></linearGradient>
 <radialGradient id="orb"><stop stop-color="#790018" stop-opacity=".28"/><stop offset="1" stop-color="#790018" stop-opacity="0"/></radialGradient>
 <pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22 0H0V22" fill="none" stroke="#858B93" stroke-opacity=".09"/></pattern>
 <filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <clipPath id="clip"><rect x="30" y="143" width="620" height="16" rx="4"/></clipPath>
 <style>
 text{{font-family:'JetBrains Mono','SFMono-Regular',Consolas,monospace}}
 .micro{{font-size:9px;letter-spacing:2px;fill:#858B93}}
 .label{{font-size:13px;font-weight:700;fill:#D8DADD;letter-spacing:1px}}
 .num{{font-size:22px;font-weight:800;fill:#E4E6E9}}
 .row{{opacity:0;animation:fade .65s ease-out forwards}}
 .r1{{animation-delay:.15s}}.r2{{animation-delay:.3s}}.r3{{animation-delay:.45s}}.r4{{animation-delay:.6s}}.r5{{animation-delay:.75s}}
 .bar{{transform-box:fill-box;transform-origin:left;animation:grow 1.25s cubic-bezier(.16,1,.3,1) both}}
 .scan{{animation:scan 5s linear infinite}}
 .pulse{{animation:pulse 2.6s ease-in-out infinite}}
 @keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
 @keyframes fade{{to{{opacity:1}}}}
 @keyframes scan{{from{{transform:translateX(-160px)}}to{{transform:translateX(820px)}}}}
 @keyframes pulse{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
 </style>
</defs>
<rect x="1" y="1" width="678" height="{height-2}" rx="12" fill="url(#bg)" stroke="#555B63" stroke-opacity=".65"/>
<rect x="1" y="1" width="678" height="{height-2}" rx="12" fill="url(#grid)"/>
<ellipse cx="580" cy="82" rx="190" ry="130" fill="url(#orb)"/>
<rect x="1" y="1" width="678" height="4" rx="2" fill="url(#edge)"/>
<path d="M22 18V{height-18}" stroke="#790018" stroke-width="3"/>
<path d="M30 112H650" stroke="#858B93" stroke-opacity=".25"/>
<text x="31" y="28" class="micro">NOOCOKS // SYSTEM ANALYTICS</text>
<g transform="translate(526 15)"><rect width="124" height="23" rx="4" fill="#790018" fill-opacity=".2" stroke="#790018" stroke-opacity=".8"/><circle cx="12" cy="11.5" r="3.5" fill="#A21D3B" filter="url(#glow)" class="pulse"/><text x="23" y="15" font-size="9" fill="#D8DADD" letter-spacing="1">LIVE PROFILE</text></g>
<text x="30" y="76" font-size="34" font-weight="900" letter-spacing="1.5" fill="#E4E6E9">LANGUAGE</text>
<text x="30" y="105" font-size="34" font-weight="900" letter-spacing="1.5" fill="#790018" filter="url(#glow)">MATRIX_</text>
<g transform="translate(525 57)"><circle cx="49" cy="27" r="39" fill="none" stroke="#555B63"/><circle cx="49" cy="27" r="31" fill="none" stroke="#790018" stroke-width="4" stroke-dasharray="132 63" transform="rotate(-90 49 27)"/><circle cx="49" cy="27" r="21" fill="none" stroke="#858B93" stroke-opacity=".5" stroke-dasharray="2 5"/><text x="49" y="24" text-anchor="middle" font-size="16" font-weight="800" fill="#E4E6E9">{len(langs):02d}</text><text x="49" y="36" text-anchor="middle" font-size="7" letter-spacing="1" fill="#858B93">LANGS</text></g>
<text x="31" y="132" class="micro">CODE COMPOSITION / RELATIVE SHARE</text>
<g clip-path="url(#clip)">{segments_svg}<path class="scan" d="M0 143V159" stroke="#FFFFFF" stroke-opacity=".75" stroke-width="2" filter="url(#glow)"/></g>
<text x="30" y="182" class="micro">01 / DOMINANT</text><text x="650" y="182" text-anchor="end" class="micro">DISTRIBUTION INDEX // 100%</text>
{rows_svg}
<text x="650" y="{height-12}" text-anchor="end" font-size="8" fill="#555B63" letter-spacing="2">CRIMSON / STEEL / 001</text>
</svg>'''
card.write_text(svg, encoding="utf-8")
print(f"Generated Language Matrix with {len(langs)} languages: {', '.join(n for n,_ in langs)}")
