"""bbs/screens.py

Deterministic text screens.

Screens return plain text with \r\n line endings.
The protocol layer decides whether to page/chunk.
"""

from . import config


def _lns(lines):
    return config.LINE_ENDING.join(lines) + config.LINE_ENDING


def welcome():
    lines = []
    lines.extend(config.BANNER_LINES)
    lines.append("")
    lines.append("HELLO")
    lines.append("LOGIN <handle>")
    lines.append("MENU")
    lines.append("BYE")
    return "SCR WELCOME", _lns(lines)


def menu_main(handle=None):
    h = handle or "(guest)"
    lines = [
        "MAIN MENU - %s" % h,
        "1) Areas",
        "2) Read",
        "3) Post",
        "4) Help",
        "5) Bye",
        "",
        "TIP: TYPE MENU AT ANY TIME",
        "> ",
    ]
    return "SCR MENU MAIN", _lns(lines)


def help_screen():
    lines = [
        "HELP",
        "COMMANDS:",
        "  HELLO",
        "  LOGIN <handle>",
        "  MENU or ?",
        "  LIST AREAS",
        "  LIST AREA <name>",
        "  READ <msg_id> [OFFSET <n>]",
        "  POST <area> <nbytes>",
        "  BYE",
    ]
    return "SCR HELP", _lns(lines)


def areas(areas_list):
    lines = ["AREAS"]
    if not areas_list:
        lines.append("(none)")
    for nid, name in areas_list:
        lines.append("%s %s" % (name, nid))
    lines.append("")
    lines.append("LIST AREA <name>")
    return "SCR AREAS", _lns(lines)


def list_area(area_name, messages):
    lines = ["AREA %s" % area_name]
    if not messages:
        lines.append("(no messages)")
    for n in messages:
        f = n.get("fields") or {}
        mid = f.get("id") or n.get("_id")
        author = f.get("author") or "?"
        ts = f.get("timestamp") or "0"
        body = f.get("body") or ""
        preview = body.replace("\r", " ").replace("\n", " ")[:30]
        lines.append("%s %s %s %s" % (mid, author, ts, preview))
    lines.append("")
    lines.append("READ <msg_id>")
    return "SCR LIST AREA", _lns(lines)


def read_message(n, offset=0, continued=False):
    f = n.get("fields") or {}
    mid = f.get("id") or n.get("_id")
    author = f.get("author") or "?"
    ts = f.get("timestamp") or "0"
    area = f.get("area_name") or ""
    body = f.get("body") or ""

    if offset < 0:
        offset = 0
    body_part = body[offset:]

    lines = []
    hdr = "MESSAGE %s" % mid
    if continued:
        hdr += " (CONTINUED)"
    lines.append(hdr)
    lines.append("FROM %s" % author)
    lines.append("TIME %s" % ts)
    lines.append("AREA %s" % area)
    lines.append("OFFSET %d" % int(offset))
    lines.append("")
    # body as-is; normalize to CRLF cheaply
    body_part = body_part.replace("\n", config.LINE_ENDING)
    payload = _lns(lines) + body_part + config.LINE_ENDING
    return "SCR READ", payload
