"""Generate the cycle-01 SVG badge ("foundry token") for Toot-Toot Engineering.

This script is intentionally dependency-free (Python stdlib only) to keep cycle-01 portable.

Output:
- deliverables/cycle-01/assets/cycle-01-badge.svg
"""

from __future__ import annotations

from pathlib import Path


OUT_PATH = Path(__file__).parent / "assets" / "cycle-01-badge.svg"


def build_svg() -> str:
    w, h = 800, 300
    bg = "#0b1020"
    fg = "#e8eefc"
    accent = "#66d9ef"
    warm = "#f4b942"

    # Simple rails + gear-like ring motif (pure vector, no external refs).
    return f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{w}\" height=\"{h}\" viewBox=\"0 0 {w} {h}\">
  <title>TTE cycle-01 badge</title>
  <desc>Generated badge for Toot-Toot Engineering cycle-01. Motto: One step. One role. One artifact.</desc>

  <rect x=\"0\" y=\"0\" width=\"{w}\" height=\"{h}\" rx=\"28\" fill=\"{bg}\" />
  <rect x=\"24\" y=\"24\" width=\"{w-48}\" height=\"{h-48}\" rx=\"22\" fill=\"none\" stroke=\"{accent}\" stroke-width=\"3\" opacity=\"0.9\" />

  <!-- Rails -->
  <g opacity=\"0.9\">
    <rect x=\"90\" y=\"210\" width=\"620\" height=\"10\" rx=\"5\" fill=\"{fg}\" opacity=\"0.18\" />
    <rect x=\"90\" y=\"235\" width=\"620\" height=\"10\" rx=\"5\" fill=\"{fg}\" opacity=\"0.18\" />
    <g fill=\"{fg}\" opacity=\"0.22\">
      <rect x=\"140\" y=\"205\" width=\"8\" height=\"45\" rx=\"3\" />
      <rect x=\"220\" y=\"205\" width=\"8\" height=\"45\" rx=\"3\" />
      <rect x=\"300\" y=\"205\" width=\"8\" height=\"45\" rx=\"3\" />
      <rect x=\"380\" y=\"205\" width=\"8\" height=\"45\" rx=\"3\" />
      <rect x=\"460\" y=\"205\" width=\"8\" height=\"45\" rx=\"3\" />
      <rect x=\"540\" y=\"205\" width=\"8\" height=\"45\" rx=\"3\" />
      <rect x=\"620\" y=\"205\" width=\"8\" height=\"45\" rx=\"3\" />
    </g>
  </g>

  <!-- Gear-ish ring -->
  <g transform=\"translate(120,110)\">
    <circle cx=\"0\" cy=\"0\" r=\"54\" fill=\"none\" stroke=\"{warm}\" stroke-width=\"10\" opacity=\"0.95\" />
    <circle cx=\"0\" cy=\"0\" r=\"28\" fill=\"none\" stroke=\"{accent}\" stroke-width=\"6\" opacity=\"0.95\" />
    <circle cx=\"0\" cy=\"0\" r=\"6\" fill=\"{fg}\" opacity=\"0.85\" />
  </g>

  <!-- Text -->
  <g font-family=\"system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif\" fill=\"{fg}\">
    <text x=\"430\" y=\"110\" font-size=\"46\" font-weight=\"700\" text-anchor=\"middle\">TTE cycle-01</text>
    <text x=\"430\" y=\"155\" font-size=\"18\" opacity=\"0.92\" text-anchor=\"middle\">Toot-Toot Engineering • Workshop Run</text>
    <text x=\"430\" y=\"192\" font-size=\"20\" fill=\"{accent}\" text-anchor=\"middle\">One step. One role. One artifact.</text>
  </g>
</svg>
"""


def main() -> None:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    svg = build_svg()
    OUT_PATH.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
