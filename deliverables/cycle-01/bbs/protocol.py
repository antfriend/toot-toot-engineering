# protocol.py - command parsing and server responses

import time

from . import config
from . import screens
from . import storage


def _crlf(s):
    # Accept str and return bytes with CRLF normalization.
    if isinstance(s, bytes):
        return s
    return s.replace("\n", "\r\n").encode("ascii", "ignore")


def _send_line(io, line):
    io.send(_crlf(line + "\r\n"))


def _send_block(io, header_line, text):
    # text is str (may contain \r\n)
    payload = text.encode("ascii", "ignore")
    _send_line(io, header_line)
    _send_line(io, "TXT %d" % len(payload))
    io.send(payload)
    if not payload.endswith(b"\r\n"):
        io.send(b"\r\n")
    _send_line(io, "END")


def _err(io, code, use_line=None):
    _send_line(io, "ERR %s" % code)
    if use_line:
        _send_line(io, use_line)


def handle_connect(session, db_path):
    # On connect, display banner and prompt for handle.
    session.transport.send(screens.banner_text().encode("ascii", "ignore"))
    session.transport.send(b"HANDLE? ")


def handle_line(session, line, nodes, db_path):
    # line is a decoded ASCII line without CRLF.
    session.touch()

    if not line:
        return

    parts = line.strip().split()
    if not parts:
        return

    cmd = parts[0].upper()
    args = parts[1:]
    io = session.transport

    if cmd == "HELLO":
        _send_line(io, "OK HELLO")
        _send_block(io, "SCR BANNER", screens.banner_text())
        return

    if cmd == "LOGIN":
        if not args:
            _err(io, "ARGS", "USE: LOGIN <handle>")
            return
        session.handle = args[0][:16]
        _send_line(io, "OK LOGIN")
        _send_block(io, "SCR MENU MAIN", screens.menu_main_text())
        return

    if cmd == "MENU":
        _send_block(io, "SCR MENU MAIN", screens.menu_main_text())
        return

    if cmd == "HELP":
        _send_block(io, "SCR HELP", screens.help_text())
        return

    if cmd == "BYE":
        _send_line(io, "OK BYE")
        io.close()
        return

    if cmd == "MORE":
        if not session.has_more():
            _err(io, "NO MORE")
            return
        page = session.next_page(config.PAGE_MAX_LINES)
        _send_block(io, "OK MORE", "\r\n".join(page) + "\r\n")
        return

    # below here: require login for any data ops
    if not session.handle:
        _err(io, "LOGIN REQUIRED")
        return

    if cmd == "LIST":
        if not args:
            _err(io, "ARGS", "USE: LIST AREAS | LIST <area>")
            return

        sub = args[0].upper()
        if sub == "AREAS":
            # areas are nodes with area_name and no body
            areas = []
            for rid, n in nodes.items():
                if n.get("area_name") and ("body" not in n):
                    areas.append(n.get("area_name"))
            areas = sorted(list(set(areas)))
            session.set_paged_lines(areas)
            page = session.next_page(config.PAGE_MAX_LINES)
            _send_block(io, "OK AREAS", "\r\n".join(page) + "\r\n")
            return
        else:
            area = args[0]
            msgs = []
            for n in nodes.values():
                if "body" not in n:
                    continue
                if n.get("area_name") != area:
                    continue
                snippet = (n.get("body") or "")[:32]
                msgs.append("%s %s %s %s" % (n.get("id"), n.get("author", "?"), n.get("timestamp", "?"), snippet))
            session.set_paged_lines(msgs)
            page = session.next_page(config.PAGE_MAX_LINES)
            _send_block(io, "OK LIST %s" % area, "\r\n".join(page) + "\r\n")
            return

    if cmd == "READ":
        if not args:
            _err(io, "ARGS", "USE: READ <id> [OFFSET n]")
            return
        rid = args[0]
        offset = 0
        if len(args) >= 3 and args[1].upper() == "OFFSET":
            try:
                offset = int(args[2])
            except ValueError:
                _err(io, "ARGS", "USE: READ <id> [OFFSET n]")
                return
        node = nodes.get(rid)
        if not node:
            _err(io, "NOT FOUND")
            return
        body = (node.get("body") or "")
        if offset < 0:
            offset = 0
        body_part = body[offset:]
        _send_line(io, "OK READ %s OFFSET %d" % (rid, offset))
        _send_block(io, "SCR MSG", body_part + "\r\n")
        return

    if cmd == "POST":
        if len(args) < 2:
            _err(io, "ARGS", "USE: POST <area> <nbytes>")
            return
        area = args[0]
        try:
            nbytes = int(args[1])
        except ValueError:
            _err(io, "ARGS", "USE: POST <area> <nbytes>")
            return
        if nbytes < 1 or nbytes > config.MAX_BODY_BYTES:
            _err(io, "LIMIT", "MAX %d" % config.MAX_BODY_BYTES)
            return

        _send_line(io, "OK POST SEND %d" % nbytes)
        data = io.recv_exact(nbytes, timeout_s=config.POST_TIMEOUT_S)
        if data is None:
            _err(io, "TIMEOUT")
            return
        body = data.decode("ascii", "ignore")

        # generate a simple coordinate-ish id: @LAT<unix_mod> LON<counter>
        # On constrained devices, keep it deterministic enough.
        ts = int(time.time())
        rid = "@LAT%dLON%d" % (ts % 100000, (ts // 2) % 100000)

        msg = {
            "id": rid,
            "author": session.handle,
            "timestamp": str(ts),
            "area_name": area,
            "body": body,
            "relates": [],
        }
        storage.insert_node(db_path, msg)
        # reload nodes so future operations see it (simple correctness > performance)
        nodes.update(storage.load_db(db_path))

        _send_line(io, "OK STORED %s" % rid)
        return

    _err(io, "UNKNOWN", "TYPE HELP")
