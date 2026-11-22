#!/usr/bin/env python3
"""Render the custom GitHub telemetry panel using live upstream stats."""
from html import escape
from pathlib import Path
import re

source = Path("profile/stats-upstream.svg").read_text(encoding="utf-8")
template = Path("profile/templates/stats.svg").read_text(encoding="utf-8")


def metric(name, default="0"):
    match = re.search(
        r'data-testid="' + re.escape(name) + r'"[^>]*>\s*([\d,]+)\s*</text>',
        source,
    )
    return match.group(1).replace(",", "") if match else default


values = {
    "TOTAL_STARS": metric("stars"),
    "TOTAL_COMMITS": metric("commits"),
    "TOTAL_PRS": metric("prs"),
    "TOTAL_ISSUES": metric("issues"),
    "TOTAL_CONTRIBUTED": metric("contribs"),
}
rank = re.search(r"Rank:\s*([A-Z])", source)
rank_letter = rank.group(1) if rank else "C"
template = template.replace("RANK_LETTER", rank_letter)

for key, value in values.items():
    template = template.replace(key, value)

description = (
    "GitHub profile statistics: "
    f'{values["TOTAL_COMMITS"]} commits, '
    f'{values["TOTAL_STARS"]} stars, '
    f'{values["TOTAL_PRS"]} pull requests, '
    f'{values["TOTAL_ISSUES"]} issues, '
    f'{values["TOTAL_CONTRIBUTED"]} repositories contributed to in the last year. '
    f"Rank {rank_letter}."
)
template, count = re.subn(
    r"<desc id=\"desc\">.*?</desc>",
    f'<desc id="desc">{escape(description)}</desc>',
    template,
    count=1,
    flags=re.DOTALL,
)
if count != 1:
    raise SystemExit("Could not update the stats SVG accessibility description.")

Path("profile/stats.svg").write_text(template, encoding="utf-8")
print("Rendered custom stats panel:", values, "rank", rank_letter)
