#!/usr/bin/env python3
"""Render the custom contribution reactor using live upstream streak stats."""
from pathlib import Path
import html
import re
source = Path("profile/streak-upstream.svg").read_text(encoding="utf-8")
template = Path("profile/templates/streak.svg").read_text(encoding="utf-8")
def extract(comment, default="0"):
    parts = source.split("<!-- " + comment + " -->", 1)
    if len(parts) < 2:
        return default
    match = re.search(r'>\s*([\d,]+)\s*</text>', parts[1])
    return match.group(1).replace(",", "") if match else default
def extract_period():
    parts = source.split("<!-- Total Contributions range -->", 1)
    if len(parts) < 2:
        return "CURRENT PERIOD"
    match = re.search(r'>\s*([^<>]+?)\s*</text>', parts[1])
    return html.escape(match.group(1).strip()) if match else "CURRENT PERIOD"
total = extract("Total Contributions big number")
current = extract("Current Streak big number")
longest = extract("Longest Streak big number")
template = template.replace("TOTAL_CONTRIBUTIONS", total)
template = template.replace("CURRENT_STREAK", current)
template = template.replace("LONGEST_STREAK", longest)
template = template.replace("TOTAL_PERIOD", extract_period())
Path("profile/streak.svg").write_text(template, encoding="utf-8")
print("Rendered contribution reactor:", total, current, longest)
