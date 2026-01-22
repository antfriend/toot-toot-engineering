#!/usr/bin/env python3
import re
import time
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

PLAN_PATH = Path("PLAN.md")
LOG_PATH = Path("LOG.md")
DB_PATH = Path("tte/MyMentalPalaceDB.md")

REFRESH_MS = 1500
LOG_LINE_LIMIT = 200


class MonitorApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("TTE Monitor")
        self.geometry("1200x800")
        self.minsize(900, 600)

        self._file_mtimes = {}
        self._auto_refresh = tk.BooleanVar(value=True)

        self._init_fonts()
        self._build_ui()
        self._refresh_all(force=True)
        self.after(REFRESH_MS, self._poll_files)

    def _init_fonts(self) -> None:
        base = tkfont.nametofont("TkDefaultFont")
        self.font_body = base.copy()
        self.font_body.configure(size=11)

        self.font_h1 = base.copy()
        self.font_h1.configure(size=18, weight="bold")
        self.font_h2 = base.copy()
        self.font_h2.configure(size=16, weight="bold")
        self.font_h3 = base.copy()
        self.font_h3.configure(size=14, weight="bold")
        self.font_h4 = base.copy()
        self.font_h4.configure(size=13, weight="bold")

        self.font_code = tkfont.Font(
            family="Courier New",
            size=10,
        )

    def _build_ui(self) -> None:
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        self.current_step_var = tk.StringVar(value="Current step: (loading)")
        current_step = ttk.Label(
            top,
            textvariable=self.current_step_var,
            font=("TkDefaultFont", 12, "bold"),
        )
        current_step.pack(side="left")

        refresh_btn = ttk.Button(top, text="Refresh", command=self._refresh_all)
        refresh_btn.pack(side="right")

        auto_refresh = ttk.Checkbutton(
            top,
            text="Auto refresh",
            variable=self._auto_refresh,
            onvalue=True,
            offvalue=False,
        )
        auto_refresh.pack(side="right", padx=(0, 12))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.plan_view = self._add_tab("Plan")
        self.log_view = self._add_tab("Log")
        self.db_view = self._add_tab("DB")

    def _add_tab(self, title: str) -> tk.Text:
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)

        text = tk.Text(
            frame,
            wrap="word",
            font=self.font_body,
            padx=12,
            pady=12,
            background="#0f0f12",
            foreground="#e9e9f0",
            insertbackground="#e9e9f0",
            relief="flat",
        )
        text.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
        scroll.pack(side="right", fill="y")
        text.configure(yscrollcommand=scroll.set)

        self._apply_text_tags(text)
        text.configure(state="disabled")
        return text

    def _apply_text_tags(self, text: tk.Text) -> None:
        text.tag_configure("h1", font=self.font_h1, foreground="#ffd166")
        text.tag_configure("h2", font=self.font_h2, foreground="#f4a261")
        text.tag_configure("h3", font=self.font_h3, foreground="#e76f51")
        text.tag_configure("h4", font=self.font_h4, foreground="#e9c46a")
        text.tag_configure("bullet", lmargin1=18, lmargin2=36)
        text.tag_configure("quote", foreground="#a7a7b3", lmargin1=18, lmargin2=36)
        text.tag_configure("code", font=self.font_code, foreground="#c4f1ff")
        text.tag_configure("fence", font=self.font_code, foreground="#6c7a89")
        text.tag_configure("rule", foreground="#39424e")
        text.tag_configure("muted", foreground="#a7a7b3")

    def _poll_files(self) -> None:
        if self._auto_refresh.get():
            self._refresh_all()
        self.after(REFRESH_MS, self._poll_files)

    def _refresh_all(self, force: bool = False) -> None:
        plan_text = self._read_if_changed(PLAN_PATH, force=force)
        if plan_text is not None:
            self._render_markdown(self.plan_view, plan_text)
            self._update_current_step(plan_text)

        log_text = self._read_if_changed(LOG_PATH, force=force)
        if log_text is not None:
            log_text = self._limit_lines(log_text, LOG_LINE_LIMIT)
            self._render_markdown(self.log_view, log_text)

        db_text = self._read_if_changed(DB_PATH, force=force)
        if db_text is not None:
            self._render_markdown(self.db_view, db_text)

    def _read_if_changed(self, path: Path, force: bool = False) -> str | None:
        try:
            stat = path.stat()
        except FileNotFoundError:
            return f"File not found: {path}"

        last = self._file_mtimes.get(path)
        if not force and last == stat.st_mtime:
            return None

        self._file_mtimes[path] = stat.st_mtime
        return path.read_text(encoding="utf-8")

    def _render_markdown(self, widget: tk.Text, content: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", "end")

        in_code = False
        for raw_line in content.splitlines():
            line = raw_line.rstrip("\n")

            if line.startswith("```"):
                in_code = not in_code
                widget.insert("end", line + "\n", ("fence",))
                continue

            if in_code:
                widget.insert("end", line + "\n", ("code",))
                continue

            heading_match = re.match(r"^(#{1,6})\s+(.*)$", line)
            if heading_match:
                level = len(heading_match.group(1))
                tag = f"h{min(level, 4)}"
                widget.insert("end", heading_match.group(2) + "\n", (tag,))
                continue

            if re.match(r"^\s*(-|\*|\d+\.)\s+", line):
                widget.insert("end", line + "\n", ("bullet",))
                continue

            if re.match(r"^\s*>\s+", line):
                widget.insert("end", line + "\n", ("quote",))
                continue

            if re.match(r"^\s*---+\s*$", line):
                widget.insert("end", line + "\n", ("rule",))
                continue

            widget.insert("end", line + "\n")

        widget.configure(state="disabled")

    def _update_current_step(self, content: str) -> None:
        step = "Current step: (not found)"
        in_section = False
        for line in content.splitlines():
            if line.strip().lower().startswith("## current step"):
                in_section = True
                continue
            if in_section and line.strip().startswith("##"):
                break
            if in_section:
                match = re.search(r"\[[ xX]\]\s+(.*)", line)
                if match:
                    step = f"Current step: {match.group(1).strip()}"
                    break
        self.current_step_var.set(step)

    def _limit_lines(self, text: str, max_lines: int) -> str:
        if max_lines <= 0:
            return text
        lines = text.splitlines()
        if len(lines) <= max_lines:
            return text
        return "\n".join(lines[-max_lines:]) + "\n"


def main() -> None:
    app = MonitorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
