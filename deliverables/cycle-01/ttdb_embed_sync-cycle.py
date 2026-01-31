#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent
HTML_PATH = ROOT / "ttdb_dungeon_graph-cycle.html"
DB_PATH = ROOT / "ttdb_dungeon_db.md"

START_MARKER = "/* DB_EMBED_START */"
END_MARKER = "/* DB_EMBED_END */"


def escape_template_literal(text: str) -> str:
    return text.replace("`", "\\`").replace("${", "\\${")


def main() -> int:
    if not HTML_PATH.exists():
        print(f"Missing HTML file: {HTML_PATH}")
        return 1
    if not DB_PATH.exists():
        print(f"Missing DB file: {DB_PATH}")
        return 1

    html = HTML_PATH.read_text(encoding="utf-8")
    db_text = DB_PATH.read_text(encoding="utf-8")

    start_index = html.find(START_MARKER)
    end_index = html.find(END_MARKER)
    if start_index == -1 or end_index == -1 or end_index <= start_index:
        print("Embed markers not found in HTML.")
        return 1

    start_index += len(START_MARKER)
    replacement = (
        "\n      const dbText = `\n"
        + escape_template_literal(db_text)
        + "\n`;\n"
    )
    new_html = html[:start_index] + replacement + html[end_index:]
    HTML_PATH.write_text(new_html, encoding="utf-8")

    print("Embedded DB content into HTML.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
