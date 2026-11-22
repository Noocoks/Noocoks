#!/usr/bin/env python3
"""Apply the profile's crimson/steel palette to every generated trophy SVG color."""
from pathlib import Path
import re

path = Path("profile/trophy.svg")
svg = path.read_text(encoding="utf-8")


def recolor(match):
    token = match.group(0)
    value = token[1:]
    if len(value) == 3:
        value = "".join(char * 2 for char in value)
    if len(value) == 8:
        rgb, alpha = value[:6], value[6:]
    else:
        rgb, alpha = value, ""

    red, green, blue = (int(rgb[index:index + 2], 16) for index in (0, 2, 4))
    high, low = max(red, green, blue), min(red, green, blue)
    saturation = 0 if high == 0 else (high - low) / high

    if high < 42:
        replacement = "#080809"
    elif saturation >= 0.16:
        replacement = "#790018" if high < 205 else "#A21D3B"
    elif high >= 220:
        replacement = "#D8DADD"
    elif high >= 125:
        replacement = "#858B93"
    else:
        replacement = "#555B63"

    return replacement + (alpha if alpha else "")


# Restrict replacement to SVG color literals; IDs, URLs and geometry stay intact.
svg = re.sub(r"#[0-9A-Fa-f]{8}\b|#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b", recolor, svg)
named = {
    "white": "#D8DADD",
    "black": "#080809",
    "red": "#790018",
    "green": "#790018",
    "blue": "#790018",
    "yellow": "#858B93",
    "cyan": "#790018",
    "magenta": "#790018",
}
for old, new in named.items():
    svg = re.sub(rf'(?i)(?<![\w-]){old}(?![\w-])', new, svg)

# The upstream trophy generator places 100px icons over the caption zone.
# Scale and center each nested icon so its artwork ends above the title at y=85.
svg = re.sub(
    r'<svg x="28" y="20" width="100" height="100" viewBox="0 0 30 30"',
    '<svg x="25" y="20" width="60" height="60" viewBox="0 0 30 30"',
    svg,
)

path.write_text(svg, encoding="utf-8")
print("Recolored generated trophy SVG using the crimson/steel palette.")
