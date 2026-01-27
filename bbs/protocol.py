"""bbs/protocol.py

Command parsing and response framing.

This module is the BBS "engine" surface: it consumes lines and uses storage + screens.
Transport is responsible for feeding it complete lines and sending bytes.
"""

from . import config
from . import screens


def _b(s):
    if isinstance(s, bytes):
        return s
    return s.encode("ascii", "ignore")


def frame_ok(verb, screen_name=None, payload_text=None):
    out = []
    out.append("OK %s" % verb)
    if screen_name and payload_text is not None:
        pb = payload_text.encode("ascii", "ignore")
        out.append(screen_name)
        out.append("TXT %d" % len(pb))
        # payload must be exact bytes length, so append separately
        head = config.LINE_ENDING.join(out) + config.LINE_ENDING
        tail = config.LINE_ENDING + "END" + config.LINE_ENDING
        return _b(head) + pb + _b(tail)
    else:
        return _b(config.LINE_ENDING.join(out) + config.LINE_ENDING + "END" + config.LINE_ENDING)


def frame_err(reason):
    return _b("ERR %s" % reason + config.LINE_ENDING + "END" + config.LINE_ENDING)


def parse_line(line):
    """Parse a command line into (cmd, args).

    Accepts aliases:
    - "?" => MENU
    - "R <id>" => READ <id>
    - "1" => LIST AREAS
    """
    line = (line or "").strip()
    if not line:
        return None, []
    if line == "?":
        return "MENU", []
    if line == "1":
        return "LIST", ["AREAS"]
    if line.startswith("R "):
        return "READ", [line.split(" ", 1)[1].strip()]

    parts = line.split()
    cmd = parts[0].upper()
    args = parts[1:]
    return cmd, args


class Protocol:
    def __init__(self, db):
        self.db = db

    def handle_line(self, session, line):
        # Multi-step POST body handling
        if session.pending_post is not None:
            return self._handle_post_body(session, line)

        cmd, args = parse_line(line)
        if cmd is None:
            # ignore empty line
            return None

        # Basic command routing
        if cmd == "HELLO":
            sc, txt = screens.welcome()
            return frame_ok("HELLO", sc, txt)

        if cmd == "LOGIN":
            if not args:
                return frame_err("MISSING HANDLE")
            handle = args[0]
            if len(handle) > config.MAX_HANDLE_LEN:
                return frame_err("HANDLE TOO LONG")
            session.handle = handle
            return frame_ok("LOGIN")

        if cmd in ("MENU",):
            sc, txt = screens.menu_main(handle=session.handle)
            return frame_ok("MENU", sc, txt)

        if cmd == "HELP":
            sc, txt = screens.help_screen()
            return frame_ok("HELP", sc, txt)

        if cmd == "LIST":
            if not args:
                return frame_err("LIST WHAT")
            sub = args[0].upper()
            if sub == "AREAS":
                sc, txt = screens.areas(self.db.list_areas())
                return frame_ok("AREAS", sc, txt)
            if sub == "AREA":
                if len(args) < 2:
                    return frame_err("MISSING AREA")
                area_name = args[1]
                msgs = self.db.list_messages_in_area(area_name=area_name, limit=20)
                sc, txt = screens.list_area(area_name, msgs)
                return frame_ok("LIST", sc, txt)
            return frame_err("BAD LIST")

        if cmd == "READ":
            if not args:
                return frame_err("MISSING ID")
            msg_id = args[0]
            offset = 0
            if len(args) >= 3 and args[1].upper() == "OFFSET":
                try:
                    offset = int(args[2])
                except ValueError:
                    return frame_err("BAD OFFSET")
            n = self.db.find_node(msg_id)
            if not n:
                return frame_err("NOT FOUND")
            sc, txt = screens.read_message(n, offset=offset, continued=(offset > 0))
            return frame_ok("READ", sc, txt)

        if cmd == "POST":
            if not session.logged_in:
                return frame_err("NOT LOGGED IN")
            if len(args) < 2:
                return frame_err("POST USAGE")
            area_name = args[0]
            try:
                nbytes = int(args[1])
            except ValueError:
                return frame_err("BAD NBYTES")
            if nbytes < 1 or nbytes > config.MAX_POST_BYTES:
                return frame_err("BAD SIZE")
            # Create draft message now (recoverable)
            draft_id = self.db.post_message(session.handle, area_name, body="", draft=True)
            self.db.save_db()
            session.pending_post = {"id": draft_id, "need": nbytes, "buf": ""}
            return frame_ok("POST READY")

        if cmd == "BYE":
            return frame_ok("BYE")

        # Menu numeric shortcuts
        if cmd == "2":
            return frame_ok("READ", *screens.help_screen())
        if cmd == "3":
            return frame_ok("POST", *screens.help_screen())
        if cmd == "4":
            sc, txt = screens.help_screen()
            return frame_ok("HELP", sc, txt)
        if cmd == "5":
            return frame_ok("BYE")

        return frame_err("UNKNOWN CMD")

    def _handle_post_body(self, session, chunk):
        p = session.pending_post
        if p is None:
            return None
        # chunk is a line from transport; to allow raw bytes including newlines,
        # the transport should provide raw bytes mode. For MVP, we accept line-based body.
        # We accumulate until >= need bytes.
        buf = p["buf"] + (chunk or "")
        if len(buf) < p["need"]:
            p["buf"] = buf + "\n"  # preserve user line breaks
            session.pending_post = p
            return None
        body = buf[: p["need"]]
        self.db.update_message_body(p["id"], body=body, finalize=True)
        self.db.save_db()
        session.pending_post = None
        return frame_ok("POSTED %s" % p["id"])
