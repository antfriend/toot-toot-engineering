#!/usr/bin/env python3
# Simple interactive test client for the BBS (CPython).

import socket
import sys


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 2323

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    def recv_some():
        s.settimeout(0.2)
        try:
            data = s.recv(4096)
            if data:
                sys.stdout.write(data.decode("ascii", "ignore"))
                sys.stdout.flush()
        except Exception:
            pass

    try:
        while True:
            recv_some()
            line = sys.stdin.readline()
            if not line:
                break
            if line.strip().startswith("POST "):
                # user must type: POST area nbytes
                parts = line.strip().split()
                nbytes = int(parts[2])
                s.sendall((line.strip() + "\r\n").encode("ascii", "ignore"))
                body = sys.stdin.read(nbytes)
                s.sendall(body.encode("ascii", "ignore"))
            else:
                s.sendall((line.rstrip("\n") + "\r\n").encode("ascii", "ignore"))
    finally:
        s.close()


if __name__ == "__main__":
    main()
