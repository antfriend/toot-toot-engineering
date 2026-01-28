"""Convenience helper.

This script prints the three commands you should run in three terminals.
We avoid spawning subprocesses automatically to keep behavior consistent across OSes.

Usage:
  python scripts/run_three_nodes.py
"""

from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    node_py = "python -m ttn.node"

    print("Open THREE terminals and run:")
    print(f"  {node_py} --config config/node_a.env listen")
    print(f"  {node_py} --config config/node_b.env listen")
    print(f"  {node_py} --config config/node_c.env listen")
    print("")
    print("Then send demo messages from a 4th terminal (or reuse one):")
    print(f"  {node_py} --config config/node_a.env direct node-b \"Hello node-b\"")
    print(f"  {node_py} --config config/node_b.env direct node-a \"Hi node-a\"")
    print(f"  {node_py} --config config/node_c.env broadcast \"Hello everyone\"")


if __name__ == "__main__":
    main()
