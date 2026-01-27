"""bbs/session.py

Session lifecycle and state.

A session corresponds to one client connection.
"""

import time


class Session:
    def __init__(self, sid, conn):
        self.sid = sid
        self.conn = conn  # must implement send/recv/close
        self.handle = None
        self.last_activity = time.time()
        # state for multi-step operations
        self.pending_post = None  # dict when expecting a POST body

    def touch(self):
        self.last_activity = time.time()

    @property
    def logged_in(self):
        return self.handle is not None
