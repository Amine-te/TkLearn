# ──────────────────────────────────────────────
# TkLearn Studio v1.0 — Menus & Toolbar
# ──────────────────────────────────────────────
import tkinter as tk
from tkinter import ttk

from ..core.lesson_loader import get_lesson_names


class Toolbar(ttk.Frame):
    """Top toolbar with Run / Clear / Save buttons."""

    def __init__(
        self,
        parent: tk.Widget,
        on_run=None,
        on_clear=None,
        on_save=None,
        on_assistant=None,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)

        self.btn_run = ttk.Button(
            self, text="▶ Lancer (F5)", command=on_run, style="Accent.TButton",
        )
        self.btn_run.pack(side="left", padx=(0, 4), pady=4)

        self.btn_clear = ttk.Button(
            self, text="🗑 Effacer", command=on_clear, style="Danger.TButton"
        )
        self.btn_clear.pack(side="left", padx=4, pady=4)

        self.btn_save = ttk.Button(
            self, text="💾 Sauvegarder", command=on_save, style="Save.TButton"
        )
        self.btn_save.pack(side="left", padx=4, pady=4)
        
        # ── Optional Assistant Callback ──
        if on_assistant:
            self.btn_ai = ttk.Button(
                self, text="🤖 Assistant AI", command=on_assistant, style="AI.TButton"
            )
            self.btn_ai.pack(side="left", padx=4, pady=4)


class LessonMenu(ttk.Frame):
    """Dropdown to pick a lesson and load it into the editor."""

    def __init__(
        self,
        parent: tk.Widget,
        on_load_lesson=None,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)
        self._on_load_lesson = on_load_lesson

        ttk.Label(self, text="📚 Leçon :", font=("Segoe UI", 10)).pack(side="left", padx=(8, 4))

        self._lesson_var = tk.StringVar()
        lessons = get_lesson_names()
        if lessons:
            self._lesson_var.set(lessons[0])

        self._dropdown = ttk.Combobox(
            self,
            textvariable=self._lesson_var,
            values=lessons,
            state="readonly",
            width=18,
            font=("Segoe UI", 10),
        )
        self._dropdown.pack(side="left", padx=4, pady=4)

        self.btn_load = ttk.Button(
            self, text="Charger", command=self._load_selected, style="Info.TButton"
        )
        self.btn_load.pack(side="left", padx=4, pady=4)

    def _load_selected(self):
        lesson_name = self._lesson_var.get()
        if lesson_name and self._on_load_lesson:
            self._on_load_lesson(lesson_name)
