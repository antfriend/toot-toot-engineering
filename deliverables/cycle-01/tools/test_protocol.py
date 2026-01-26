#!/usr/bin/env python3
# Minimal smoke tests for protocol framing (CPython)

import socket
import time


def recv_until(sock, token, timeout=2.0):
    sock.settimeout(0.2)
    start = time.time()
    buf = b""
    while time.time() - start < timeout:
        try:
            chunk = sock.recv(4096)
            if not chunk:
                break
            buf += chunk
            if token in buf:
                return buf
        except Exception:
            pass
    return buf


def test_hello(host="127.0.0.1", port=2323):
    s = socket.socket()
    s.connect((host, port))
    recv_until(s, b"HANDLE?")
    s.sendall(b"HELLO\r\n")
    out = recv_until(s, b"END\r\n")
    assert b"OK HELLO" in out
    s.close()


def test_login_menu(host="127.0.0.1", port=2323):
    s = socket.socket()
    s.connect((host, port))
    recv_until(s, b"HANDLE?")
    s.sendall(b"LOGIN dan\r\n")
    out = recv_until(s, b"END\r\n")
    assert b"OK LOGIN" in out
    assert b"SCR MENU MAIN" in out
    s.close()


if __name__ == "__main__":
    test_hello()
    test_login_menu()
    print("OK")
