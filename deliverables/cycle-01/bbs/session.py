# session.py - session lifecycle and state

import time


class Session:
    def __init__(self, sid, transport):
        self.sid = sid
        self.transport = transport
        self.handle = None
        self.created = int(time.time())
        self.last_activity = self.created

        # Paging state for LIST and similar operations
        self._page_lines = None
        self._page_index = 0

    def touch(self):
        self.last_activity = int(time.time())

    def set_paged_lines(self, lines):
        # lines: list[str] without CRLF
        self._page_lines = lines or []
        self._page_index = 0

    def has_more(self):
        return self._page_lines is not None and self._page_index < len(self._page_lines)

    def next_page(self, max_lines):
        if self._page_lines is None:
            return []
        start = self._page_index
        end = min(len(self._page_lines), start + max_lines)
        self._page_index = end
        return self._page_lines[start:end]
