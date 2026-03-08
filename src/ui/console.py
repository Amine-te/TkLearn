# ──────────────────────────────────────────────
# TkLearn Studio v1.0 — Logging Console
# ──────────────────────────────────────────────
import tkinter as tk
from tkinter import ttk

from ..utils.constants import (
    CONSOLE_BG,
    CONSOLE_ERROR_COLOR,
    CONSOLE_FG,
    CONSOLE_INFO_COLOR,
    CONSOLE_SUCCESS_COLOR,
    EDITOR_FONT,
)


class Console(ttk.Frame):
    """Read-only, color-coded logging console."""

    def __init__(self, parent: tk.Widget, **kwargs):
        super().__init__(parent, **kwargs)
        self._build_ui()
        self._configure_tags()

    # ── Construction ──────────────────────────

    def _build_ui(self):
        title = ttk.Label(self, text="  📋 Console", style="Title.TLabel")
        title.pack(fill="x", pady=(0, 2))

        container = ttk.Frame(self, style="Card.TFrame")
        container.pack(fill="both", expand=True)

        self.text = tk.Text(
            container,
            bg=CONSOLE_BG,
            fg=CONSOLE_FG,
            font=EDITOR_FONT,
            relief="flat",
            state="disabled",      # read-only
            wrap="word",
            height=8,
            padx=6,
            pady=4,
            borderwidth=0,
            highlightthickness=0,
        )

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.text.yview)
        scrollbar.pack(side="right", fill="y")

        self.text.pack(side="left", fill="both", expand=True)
        self.text.configure(yscrollcommand=scrollbar.set)

    # ── Tag Configuration ─────────────────────

    def _configure_tags(self):
        self.text.tag_configure("info", foreground=CONSOLE_INFO_COLOR)
        self.text.tag_configure("success", foreground=CONSOLE_SUCCESS_COLOR)
        self.text.tag_configure("error", foreground=CONSOLE_ERROR_COLOR)

    # ── Public API ────────────────────────────

    def log(self, message: str, tag: str = "info"):
        """Append *message* to the console with the given *tag* and auto-scroll.

        Valid tags: ``'info'``, ``'success'``, ``'error'``.
        """
        self.text.configure(state="normal")
        self.text.insert("end", message + "\n", tag)
        self.text.configure(state="disabled")
        self.text.see("end")  # auto-scroll

    def clear(self):
        """Wipe all console content."""
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")
