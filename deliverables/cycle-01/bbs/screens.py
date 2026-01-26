# screens.py - deterministic text UI generators

from . import config


def banner_lines():
    return config.BANNER_LINES


def banner_text():
    return "\r\n".join(banner_lines()) + "\r\n\r\n"


def menu_main_text():
    # Intentionally small and instructional
    lines = [
        "MENU:",
        "  LIST AREAS",
        "  LIST <area>",
        "  READ <id> [OFFSET n]",
        "  POST <area> <nbytes>",
        "  MORE",
        "  BYE",
    ]
    return "\r\n".join(lines) + "\r\n"


def help_text():
    lines = [
        "HELP:",
        "  HELLO",
        "  LOGIN <handle>",
        "  MENU",
        "  LIST AREAS",
        "  LIST <area>",
        "  READ <id> [OFFSET n]",
        "  POST <area> <nbytes>",
        "  MORE",
        "  BYE",
    ]
    return "\r\n".join(lines) + "\r\n"
