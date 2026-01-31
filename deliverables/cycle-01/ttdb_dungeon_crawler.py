#!/usr/bin/env python3
"""TTDB Dungeon Crawler (UNIHIKER K10)

A touchscreen-friendly, tap-to-choose, text-first dungeon crawler.

UI approach:
- Uses tkinter (standard library) with a big text area and large buttons.

DB approach:
- Uses a dedicated MyMentalPalaceDB markdown file (TTDB RFC v0.2 draft).
- Parses record headers in the same spirit as tte_monitor.py.

This file is intended to be placed in an installation bundle and run on-device.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import tkinter as tk
from tkinter import ttk


# -----------------------------
# TTDB parsing (minimal)
# -----------------------------

@dataclass
class TTDBRecord:
    record_id: str
    header: str
    body: str
    edges: List[dict]


def parse_ttdb_markdown(path: Path) -> Dict[str, TTDBRecord]:
    """Parse a TTDB markdown file into records.

    This is intentionally lightweight: it extracts record blocks separated by
    --- and reads the first line beginning with '@' as the record header.

    It also parses a subset of `relates:` entries from the header.
    """
    content = path.read_text(encoding="utf-8")
    records: Dict[str, TTDBRecord] = {}

    for block in re.split(r"^\s*---+\s*$", content, flags=re.M):
        lines = [ln.rstrip("\n") for ln in block.splitlines()]
        header_index = None
        for i, ln in enumerate(lines):
            if ln.strip().startswith("@"):  # record header line
                header_index = i
                break
        if header_index is None:
            continue

        header_line = lines[header_index].strip()
        record_id = header_line.split()[0]
        body = "\n".join(lines[header_index + 1 :]).strip("\n")

        edges: List[dict] = []
        relates_match = re.search(r"relates:([^|]+)", header_line)
        if relates_match:
            for token in relates_match.group(1).split(","):
                token = token.strip()
                if not token:
                    continue
                if ">" in token:
                    edge_type, target = token.split(">", 1)
                    edges.append({"type": edge_type.strip(), "target": target.strip()})
                else:
                    edges.append({"type": "relates", "target": token})

        records[record_id] = TTDBRecord(
            record_id=record_id,
            header=header_line,
            body=body,
            edges=edges,
        )

    return records


# -----------------------------
# Story graph
# -----------------------------

STORY_NODES = {
    "N0": {
        "title": "Cave Entrance / Campfire",
        "text": (
            "A cave opens like a yawn in the hillside.\n\n"
            "Inside: a small campfire, already lit, as if expecting you.\n"
            "A little sign is stuck in the sand: ‘WELCOME, HERO. PLEASE WIPE FEET OR AT LEAST PRETEND.’\n"
        ),
        "choices": [
            {"label": "Warm hands by the fire", "to": "N1"},
            {"label": "Step into the corridor of labeled stones", "to": "N100"},
            {"label": "Squeeze through the star-slit crack", "to": "N200"},
            {"label": "Follow the smell of soup", "to": "N300"},
        ],
    },
    "N1": {
        "title": "Campfire Tutorial Voice",
        "text": (
            "The fire crackles like it’s reading from a manual written by someone who is very proud of bullet points.\n\n"
            "‘Tap a choice. Reality will comply… within budget.’\n"
        ),
        "choices": [
            {"label": "Ask the fire for advice", "to": "N0"},
            {"label": "Roast a marshmallow you definitely brought", "to": "N1_END"},
        ],
    },
    "N1_END": {
        "title": "Marshmallow Victory",
        "text": (
            "You roast a marshmallow with the calm competence of a hero who has practiced on lesser marshmallows.\n\n"
            "You win one (1) perfectly toasted marshmallow. Inventory: Emotional Stability +1.\n"
        ),
        "ending": True,
        "choices": [
            {"label": "Play again (back to the campfire)", "to": "N0"},
            {"label": "Quit", "to": "QUIT"},
        ],
    },
    # --- mmpdb tutorial path ---
    "N100": {
        "title": "Corridor of Labeled Stones",
        "text": (
            "The stones here are engraved with @-symbols and tiny arrows.\n"
            "It feels less like a dungeon and more like a filing system with ambitions.\n"
        ),
        "choices": [
            {"label": "Read the nearest stone", "to": "N101"},
            {"label": "Pocket a stone (bad idea)", "to": "N109"},
            {"label": "Return to the campfire", "to": "N0"},
        ],
    },
    "N101": {
        "title": "What Is a Record?",
        "text": (
            "A record is a ‘room’ in your mental palace.\n"
            "It has an ID (a label), and a body (the stuff you write down).\n\n"
            "The dungeon whispers: ‘A room without a label is just… vibes.’\n"
        ),
        "choices": [
            {"label": "Show me a real record", "to": "N102"},
            {"label": "Return to the campfire", "to": "N0"},
        ],
    },
    "N102": {
        "title": "Record Anatomy",
        "text": (
            "A stone tablet displays a tiny example: a header line starting with an @id, then markdown below.\n\n"
            "If a dedicated TTDB file is installed, you can also peek at actual records from it.\n"
        ),
        "choices": [
            {"label": "Peek at the TTDB records", "to": "N102_DB"},
            {"label": "How do links work?", "to": "N103"},
        ],
    },
    "N102_DB": {
        "title": "TTDB Peek",
        "text": "(The dungeon waits patiently while you browse the database.)\n",
        "action": "OPEN_DB",
        "choices": [
            {"label": "Back", "to": "N102"},
        ],
    },
    "N103": {
        "title": "Edges (Relationships)",
        "text": (
            "An edge is a relationship from one record to another.\n"
            "Typed edges add meaning. Example: uses> @something.\n\n"
            "The corridor becomes a spiderweb of string. It is… organized.\n"
        ),
        "choices": [
            {"label": "How do I navigate?", "to": "N104"},
            {"label": "Return to the campfire", "to": "N0"},
        ],
    },
    "N104": {
        "title": "Cursor Semantics",
        "text": (
            "The dungeon hands you a cursor-lantern.\n\n"
            "- The cursor tracks which record is selected.\n"
            "- Selecting a record updates a preview.\n"
            "- A history of selection lets you backtrack.\n"
        ),
        "choices": [
            {"label": "Give me a tiny workflow example", "to": "N105"},
            {"label": "Return to the campfire", "to": "N0"},
        ],
    },
    "N105": {
        "title": "Tiny Workflow",
        "text": (
            "1) Capture an idea as a record.\n"
            "2) Add edges to connect it.\n"
            "3) Retrieve it later by following relationships.\n"
        ),
        "choices": [
            {"label": "What can I use this for?", "to": "N106"},
            {"label": "Return to the campfire", "to": "N0"},
        ],
    },
    "N106": {
        "title": "Applications",
        "text": (
            "The dungeon offers a menu of practical magic:\n\n"
            "- Project planning (quests)\n"
            "- Personal knowledge base (spellbook)\n"
            "- Research notes (librarian golem)\n"
            "- Relationship maps (constellations)\n"
            "- Creative worldbuilding (yes, this dungeon)\n"
        ),
        "choices": [
            {"label": "I feel… organized. Is that allowed?", "to": "N107"},
            {"label": "Return to the campfire", "to": "N0"},
        ],
    },
    "N107": {
        "title": "Certificate of Coherence",
        "text": (
            "The cave stamps your forehead: ‘CERTIFIED: MOSTLY COHERENT.’\n\n"
            "You exit with a glowing index card that reads:\n"
            "‘Start small. Link often.’\n"
        ),
        "ending": True,
        "choices": [
            {"label": "Play again", "to": "N0"},
            {"label": "Quit", "to": "QUIT"},
        ],
    },
    "N109": {
        "title": "Pocketing Consequences",
        "text": (
            "You pocket a stone.\n\n"
            "The corridor politely collapses into a single pebble in your pocket.\n"
            "‘Congrats,’ the dungeon says. ‘You stole the entire concept of organization. Now nobody has it.’\n"
        ),
        "ending": True,
        "choices": [
            {"label": "Play again", "to": "N0"},
            {"label": "Quit", "to": "QUIT"},
        ],
    },
    # --- cosmic eyeball path ---
    "N200": {
        "title": "Star-Slit Crack",
        "text": "You squeeze through the crack in the rock and fall upward into starlight.\n",
        "choices": [
            {"label": "Blink first", "to": "N201"},
            {"label": "Refuse to blink on principle", "to": "N209"},
        ],
    },
    "N201": {
        "title": "Eyeball Node Sea",
        "text": (
            "A void filled with floating eyeballs, each labeled like a node ID.\n"
            "They cast longing gazes along invisible edges.\n"
        ),
        "choices": [
            {"label": "Follow the gaze-line", "to": "N202"},
        ],
    },
    "N202": {
        "title": "Edges as Yearning",
        "text": (
            "Each edge is a desire to be understood.\n"
            "Typed edges are *specific* longing: misses>, adores>, regrets>.\n"
        ),
        "choices": [
            {"label": "Introduce yourself as a new node", "to": "N203"},
            {"label": "Hide behind a comet", "to": "N208"},
        ],
    },
    "N203": {
        "title": "You Are Labeled",
        "text": "A gentle eyeball stamps you: @adventurer. You feel oddly indexed.\n",
        "choices": [
            {"label": "Choose your first connection", "to": "N204"},
        ],
    },
    "N204": {
        "title": "Pick a Typed Edge",
        "text": "Your choices form an edge. The cosmos holds its breath (wetly).\n",
        "choices": [
            {"label": "friends_with> @mysterious_orb", "to": "N205"},
            {"label": "afraid_of> @mysterious_orb", "to": "N206"},
            {"label": "hungry_for> @mysterious_orb", "to": "N300"},
        ],
    },
    "N205": {
        "title": "Friendship Graph",
        "text": (
            "The eyeballs cheer silently (a horrifying soundlessness).\n\n"
            "You gain: ‘Belonging (vaguely damp).’\n"
        ),
        "ending": True,
        "choices": [
            {"label": "Play again", "to": "N0"},
            {"label": "Quit", "to": "QUIT"},
        ],
    },
    "N206": {
        "title": "Fear Edge Feedback Loop",
        "text": (
            "Your afraid_of> edge multiplies into a fractal of panic.\n"
            "A cosmic librarian hands you a tiny brochure: ‘Consider pruning.’\n"
        ),
        "ending": True,
        "choices": [
            {"label": "Play again", "to": "N0"},
            {"label": "Quit", "to": "QUIT"},
        ],
    },
    "N208": {
        "title": "Comet Hiding",
        "text": (
            "You hide behind a comet so well you become metadata.\n"
            "Someone tags you: @lost_but_vibes.\n"
        ),
        "ending": True,
        "choices": [
            {"label": "Play again", "to": "N0"},
            {"label": "Quit", "to": "QUIT"},
        ],
    },
    "N209": {
        "title": "Never Blink",
        "text": (
            "Reality respects your stubbornness and renders you as a perfect still image.\n"
            "You are immortalized as a loading screen tip.\n"
        ),
        "ending": True,
        "choices": [
            {"label": "Play again", "to": "N0"},
            {"label": "Quit", "to": "QUIT"},
        ],
    },
    # --- food/digestion path ---
    "N300": {
        "title": "Smell of Soup",
        "text": (
            "The smell is delicious. Too delicious.\n"
            "It’s coming from deeper in the cave… or possibly from your own destiny.\n"
        ),
        "choices": [
            {"label": "Investigate the bubbling pot", "to": "N301"},
            {"label": "Taste the air suspiciously", "to": "N302"},
            {"label": "Return to the campfire", "to": "N0"},
        ],
    },
    "N301": {
        "title": "Kitchen of Fate",
        "text": (
            "A giant ladle hangs overhead like a moon.\n"
            "A voice says: ‘Ah, the entrée arrives.’\n"
        ),
        "choices": [
            {"label": "Object, politely", "to": "N303"},
        ],
    },
    "N302": {
        "title": "Flavor Foreshadowing",
        "text": (
            "You taste the air.\n"
            "It tastes… you-adjacent.\n"
        ),
        "choices": [
            {"label": "Look down at your hands", "to": "N304"},
        ],
    },
    "N303": {
        "title": "Consent for Consumption",
        "text": (
            "A clipboard appears, as clipboards do in moments of cosmic importance.\n\n"
            "A) I consent to being a snack (under protest).\n"
            "B) I request to be a garnish instead.\n"
        ),
        "choices": [
            {"label": "Snack (under protest)", "to": "N305"},
            {"label": "Garnish", "to": "N306"},
        ],
    },
    "N304": {
        "title": "You Are a Dumpling",
        "text": (
            "You look down. Your hands are dough.\n"
            "Your heart is broth.\n\n"
            "You are, unmistakably, a dumpling.\n"
        ),
        "choices": [
            {"label": "Roll with it", "to": "N305"},
        ],
    },
    "N305": {
        "title": "Digestion Epilogue",
        "text": (
            "You are eaten.\n\n"
            "Inside the belly-dungeon, you find a small campfire.\n"
            "The stomach politely asks you to leave a review.\n"
        ),
        "ending": True,
        "choices": [
            {"label": "Play again", "to": "N0"},
            {"label": "Quit", "to": "QUIT"},
        ],
    },
    "N306": {
        "title": "Legendary Garnish",
        "text": (
            "You are sprinkled across the soup like heroic parsley.\n"
            "Bards sing: ‘They added depth.’\n"
        ),
        "ending": True,
        "choices": [
            {"label": "Play again", "to": "N0"},
            {"label": "Quit", "to": "QUIT"},
        ],
    },
}


# -----------------------------
# UI
# -----------------------------

class GameApp(tk.Tk):
    def __init__(self, db_path: Path):
        super().__init__()
        self.title("TTDB Dungeon Crawler")
        self.geometry("800x480")  # common small touchscreen-ish layout
        self.minsize(640, 360)

        self.db_path = db_path
        self.records: Dict[str, TTDBRecord] = {}
        if self.db_path.exists():
            try:
                self.records = parse_ttdb_markdown(self.db_path)
            except Exception:
                self.records = {}

        self.current_node_id = "N0"

        self._build_ui()
        self.show_node(self.current_node_id)

    def _build_ui(self) -> None:
        self.configure(background="#0f0f12")

        outer = ttk.Frame(self, padding=10)
        outer.pack(fill="both", expand=True)

        self.title_var = tk.StringVar(value="")
        title_lbl = ttk.Label(outer, textvariable=self.title_var)
        title_lbl.pack(anchor="w")

        self.text = tk.Text(
            outer,
            wrap="word",
            height=14,
            padx=12,
            pady=12,
            background="#0f0f12",
            foreground="#e9e9f0",
            insertbackground="#e9e9f0",
            relief="flat",
        )
        self.text.pack(fill="both", expand=True, pady=(8, 8))
        self.text.configure(state="disabled")

        self.choices_frame = ttk.Frame(outer)
        self.choices_frame.pack(fill="x")

        footer = ttk.Frame(outer)
        footer.pack(fill="x", pady=(8, 0))

        ttk.Button(footer, text="Home", command=lambda: self.show_node("N0")).pack(
            side="left"
        )
        ttk.Button(footer, text="DB", command=self.open_db_browser).pack(side="left", padx=(8, 0))
        ttk.Button(footer, text="Quit", command=self.destroy).pack(side="right")

    def set_text(self, s: str) -> None:
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("end", s)
        self.text.configure(state="disabled")

    def show_node(self, node_id: str) -> None:
        if node_id == "QUIT":
            self.destroy()
            return

        node = STORY_NODES.get(node_id)
        if not node:
            self.set_text(f"Missing node: {node_id}")
            return

        self.current_node_id = node_id
        self.title_var.set(node.get("title", node_id))

        text = node.get("text", "")
        self.set_text(text)

        action = node.get("action")
        if action == "OPEN_DB":
            self.open_db_browser()

        for child in self.choices_frame.winfo_children():
            child.destroy()

        for choice in node.get("choices", []):
            btn = ttk.Button(
                self.choices_frame,
                text=choice["label"],
                command=lambda to=choice["to"]: self.show_node(to),
            )
            btn.pack(fill="x", pady=4)

    def open_db_browser(self) -> None:
        """A very small DB viewer: listbox + text, inspired by tte_monitor.py."""
        win = tk.Toplevel(self)
        win.title("TTDB Browser")
        win.geometry("900x600")

        pane = ttk.Panedwindow(win, orient="horizontal")
        pane.pack(fill="both", expand=True)

        left = ttk.Frame(pane, padding=8)
        right = ttk.Frame(pane, padding=8)
        pane.add(left, weight=1)
        pane.add(right, weight=3)

        ttk.Label(left, text=f"Records ({self.db_path.name})").pack(anchor="w")
        lb = tk.Listbox(left)
        lb.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(left, orient="vertical", command=lb.yview)
        sb.pack(side="right", fill="y")
        lb.configure(yscrollcommand=sb.set)

        text = tk.Text(
            right,
            wrap="word",
            padx=12,
            pady=12,
            background="#0f0f12",
            foreground="#e9e9f0",
            insertbackground="#e9e9f0",
            relief="flat",
        )
        text.pack(fill="both", expand=True)
        text.configure(state="disabled")

        record_ids = sorted(self.records.keys())
        for rid in record_ids:
            lb.insert("end", rid)

        def render_record(_event=None):
            sel = lb.curselection()
            if not sel:
                return
            rid = record_ids[sel[0]]
            rec = self.records.get(rid)
            if not rec:
                return
            text.configure(state="normal")
            text.delete("1.0", "end")
            text.insert("end", rec.header + "\n\n" + rec.body)
            text.configure(state="disabled")

        lb.bind("<<ListboxSelect>>", render_record)
        if record_ids:
            lb.selection_set(0)
            lb.event_generate("<<ListboxSelect>>")


def main() -> None:
    here = Path(__file__).resolve().parent
    db_path = here / "ttdb_dungeon_db.md"
    app = GameApp(db_path=db_path)
    app.mainloop()


if __name__ == "__main__":
    main()
