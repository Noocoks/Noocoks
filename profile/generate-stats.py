#!/usr/bin/env python3
"""Render the custom GitHub telemetry panel using live upstream stats."""
from pathlib import Path
import re
source = Path("profile/stats-upstream.svg").read_text(encoding="utf-8")
template = Path("profile/templates/stats.svg").read_text(encoding="utf-8")
def metric(name, default="0"):
    match = re.search(r'data-testid="' + re.escape(name) + r'"[^>]*>\s*([\d,]+)\s*</text>', source)
    return match.group(1).replace(",", "") if match else default
values = {
    "TOTAL_STARS": metric("stars"),
    "TOTAL_COMMITS": metric("commits"),
    "TOTAL_PRS": metric("prs"),
    "TOTAL_ISSUES": metric("issues"),
    "TOTAL_CONTRIBUTED": metric("contribs"),
}
rank = re.search(r"Rank:\s*([A-Z])", source)
template = template.replace("RANK_LETTER", rank.group(1) if rank else "C")
for key, value in values.items():
    template = template.replace(key, value)
Path("profile/stats.svg").write_text(template, encoding="utf-8")
print("Rendered custom stats panel:", values)
