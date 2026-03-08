# ──────────────────────────────────────────────
# TkLearn Studio v1.0 — Main Controller
# ──────────────────────────────────────────────
import tkinter as tk
from tkinter import ttk

from src.core.file_manager import open_file, save_file
from src.core.lesson_loader import get_lesson_code
from src.ui.assistant import AIAssistantWindow
from src.ui.console import Console
from src.ui.editor import CodeEditor
from src.ui.menus import LessonMenu, Toolbar
from src.ui.preview import PreviewEngine
from src.utils.constants import (
    ACCENT,
    ACCENT_GREEN,
    ACCENT_GREEN_HOVER,
    ACCENT_HOVER,
    APP_TITLE,
    BG_PRIMARY,
    BG_SECONDARY,
    BG_TOOLBAR,
    BORDER_COLOR,
    BTN_AI,
    BTN_AI_HOVER,
    BTN_DANGER,
    BTN_DANGER_HOVER,
    BTN_INFO,
    BTN_INFO_HOVER,
    BTN_SAVE,
    BTN_SAVE_HOVER,
    KEY_RUN,
    KEY_SAVE,
    MIN_HEIGHT,
    MIN_WIDTH,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    WINDOW_GEOMETRY,
)


class TkLearnStudio:
    """Main application controller — wires Editor, Preview, Console, and Toolbar."""

    def __init__(self):
        # ── Root Window ───────────────────────
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_GEOMETRY)
        self.root.minsize(MIN_WIDTH, MIN_HEIGHT)
        self.root.configure(bg=BG_PRIMARY)
        self._set_window_icon()

        self._apply_theme()
        self._build_layout()
        self._bind_shortcuts()

        # Log welcome message
        self.console.log("Bienvenue dans TkLearn Studio v1.0 !", "info")
        self.console.log("Appuyez sur F5 ou cliquez sur « Lancer » pour exécuter votre code.", "info")

    # ── Window Icon ───────────────────────────

    def _set_window_icon(self):
        """Set a window icon using an image from the static folder."""
        try:
            img = tk.PhotoImage(file="static/image.png")  # Load the image from static folder
            self.root.iconphoto(True, img)
            self._icon_ref = img  # keep reference to avoid GC
        except Exception as e:
            print(f"Failed to set window icon: {e}")
            self._icon_ref = None

    # ── Theme ─────────────────────────────────

    def _apply_theme(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")

        # General frame / label styling
        style.configure("TFrame", background=BG_PRIMARY)
        style.configure(
            "TLabel",
            background=BG_PRIMARY,
            foreground=TEXT_PRIMARY,
            font=("Segoe UI", 9),
        )

        # Card-like containers for main sections
        style.configure(
            "Card.TFrame",
            background=BG_SECONDARY,
            borderwidth=1,
            relief="solid",
        )

        # Top toolbar background
        style.configure(
            "Toolbar.TFrame",
            background=BG_TOOLBAR,
        )

        # Section titles (Editor / Preview / Console)
        style.configure(
            "Title.TLabel",
            background=BG_SECONDARY,
            foreground=TEXT_PRIMARY,
            font=("Segoe UI", 10, "bold"),
        )

        # Buttons — clean, flat, blue
        style.configure(
            "TButton",
            background=BG_TOOLBAR,
            foreground=TEXT_PRIMARY,
            bordercolor=BORDER_COLOR,
            padding=(12, 5),
            font=("Segoe UI", 9),
            relief="flat",
        )
        style.map(
            "TButton",
            background=[("active", BORDER_COLOR), ("pressed", "#D0D0D0")],
        )

        # Accent button for "Lancer" — emerald green
        style.configure(
            "Accent.TButton",
            background=ACCENT_GREEN,
            foreground="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            borderwidth=0,
        )
        style.map(
            "Accent.TButton",
            background=[("active", ACCENT_GREEN_HOVER), ("pressed", "#047857")],
        )

        # Danger button for "Effacer" — red
        style.configure(
            "Danger.TButton",
            background=BTN_DANGER,
            foreground="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            borderwidth=0,
        )
        style.map(
            "Danger.TButton",
            background=[("active", BTN_DANGER_HOVER), ("pressed", "#B91C1C")],
        )

        # Save button for "Sauvegarder" — purple
        style.configure(
            "Save.TButton",
            background=BTN_SAVE,
            foreground="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            borderwidth=0,
        )
        style.map(
            "Save.TButton",
            background=[("active", BTN_SAVE_HOVER), ("pressed", "#6D28D9")],
        )

        # Info button for "Charger" — blue
        style.configure(
            "Info.TButton",
            background=BTN_INFO,
            foreground="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            borderwidth=0,
        )
        style.map(
            "Info.TButton",
            background=[("active", BTN_INFO_HOVER), ("pressed", "#1D4ED8")],
        )

        # AI button — amber accent
        style.configure(
            "AI.TButton",
            background=BTN_AI,
            foreground="#111827",
            font=("Segoe UI", 9, "bold"),
            borderwidth=0,
        )
        style.map(
            "AI.TButton",
            background=[("active", BTN_AI_HOVER), ("pressed", "#B45309")],
        )

        # Combobox — light field with blue outline on focus
        style.configure(
            "TCombobox",
            fieldbackground=BG_SECONDARY,
            background=BG_SECONDARY,
            foreground=TEXT_PRIMARY,
            bordercolor=BORDER_COLOR,
            lightcolor=BG_SECONDARY,
            darkcolor=BG_SECONDARY,
            arrowcolor=TEXT_SECONDARY,
            arrowsize=14,
            padding=5,
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", BG_SECONDARY)],
            bordercolor=[("focus", ACCENT), ("active", TEXT_SECONDARY)],
        )

        # Style the popup listbox of the Combobox
        self.root.option_add("*TCombobox*Listbox.background", BG_SECONDARY)
        self.root.option_add("*TCombobox*Listbox.foreground", TEXT_PRIMARY)
        self.root.option_add("*TCombobox*Listbox.selectBackground", ACCENT)
        self.root.option_add("*TCombobox*Listbox.selectForeground", "#FFFFFF")
        self.root.option_add("*TCombobox*Listbox.font", ("Segoe UI", 10))
        self.root.option_add("*TCombobox*Listbox.relief", "solid")
        self.root.option_add("*TCombobox*Listbox.borderWidth", "1")

        # PanedWindow sash — subtle light divider
        style.configure("TPanedwindow", background=BG_PRIMARY)
        style.configure(
            "Sash",
            sashthickness=5,
            sashrelief="flat",
            background=BORDER_COLOR,
        )

        # LabelFrame
        style.configure(
            "TLabelframe",
            background=BG_SECONDARY,
            foreground=TEXT_PRIMARY,
            borderwidth=1,
            relief="solid",
        )
        style.configure(
            "TLabelframe.Label",
            background=BG_SECONDARY,
            foreground=TEXT_PRIMARY,
            font=("Segoe UI", 9),
        )

        # Scrollbar — minimal
        style.configure("Vertical.TScrollbar", background=BG_TOOLBAR,
                         troughcolor=BG_PRIMARY, bordercolor=BG_PRIMARY,
                         arrowcolor=TEXT_SECONDARY)
        style.configure("Horizontal.TScrollbar", background=BG_TOOLBAR,
                         troughcolor=BG_PRIMARY, bordercolor=BG_PRIMARY,
                         arrowcolor=TEXT_SECONDARY)

        # Status bar
        style.configure("StatusBar.TLabel", background=BG_PRIMARY, foreground=TEXT_SECONDARY, font=("Segoe UI", 9))

    # ── Layout ────────────────────────────────

    def _build_layout(self):
        # ── Top bar: Toolbar + LessonMenu ─────
        top_bar = ttk.Frame(self.root, style="Toolbar.TFrame")
        top_bar.pack(fill="x", padx=4, pady=(4, 0))

        self.toolbar = Toolbar(
            top_bar,
            style="Toolbar.TFrame",
            on_run=self._on_run,
            on_clear=self._on_clear,
            on_save=self._on_save,
            on_assistant=self._on_assistant,
        )
        self.toolbar.pack(side="left")

        self.lesson_menu = LessonMenu(
            top_bar,
            style="Toolbar.TFrame",
            on_load_lesson=self._on_load_lesson,
        )
        self.lesson_menu.pack(side="right")

        # ── Main horizontal PanedWindow: Editor | Preview ──
        main_pane = ttk.PanedWindow(self.root, orient="horizontal")
        main_pane.pack(fill="both", expand=True, padx=4, pady=4)

        # Left: Editor
        self.editor = CodeEditor(main_pane, style="Card.TFrame")
        main_pane.add(self.editor, weight=1)

        # Right: Preview + Console (stacked vertically)
        right_pane = ttk.PanedWindow(main_pane, orient="vertical")
        main_pane.add(right_pane, weight=1)

        self.preview = PreviewEngine(right_pane, style="Card.TFrame")
        right_pane.add(self.preview, weight=3)

        self.console = Console(right_pane, style="Card.TFrame")
        right_pane.add(self.console, weight=1)

        # ── Status bar ─────────────────────────
        self._status_var = tk.StringVar(value="Ligne 1, Colonne 1")
        status_bar = ttk.Label(self.root, textvariable=self._status_var, style="StatusBar.TLabel")
        status_bar.pack(side="bottom", fill="x", padx=6, pady=(0, 4))
        self.editor.set_cursor_callback(self._on_editor_cursor_change)

    def _on_editor_cursor_change(self, line: int, column: int):
        self._status_var.set(f"Ligne {line}, Colonne {column}")

    # ── Keyboard Shortcuts ────────────────────

    def _bind_shortcuts(self):
        self.root.bind(KEY_RUN, lambda e: self._on_run())
        self.root.bind(KEY_SAVE, lambda e: self._on_save())
        self.root.bind("<Control-plus>", lambda e: self._on_font_zoom(1))
        self.root.bind("<Control-equal>", lambda e: self._on_font_zoom(1))
        self.root.bind("<Control-minus>", lambda e: self._on_font_zoom(-1))
        self.root.bind("<Control-0>", lambda e: self._on_font_zoom(0))
        self.root.bind("<Control-f>", lambda e: self.editor.show_search())

    # ── Callbacks ─────────────────────────────

    def _on_run(self):
        """F5 workflow: get code → clear preview → execute → log result."""
        code = self.editor.get_code()
        if not code.strip():
            self.console.log("⚠ L'éditeur est vide.", "info")
            return

        self.preview.clear()
        self.console.log("⏳ Exécution en cours…", "info")

        success, error = self.preview.execute_code(code)

        if success:
            self.console.log("✅ Exécution réussie ✓", "success")
        else:
            self.console.log("❌ Erreur lors de l'exécution :", "error")
            self.console.log(error, "error")

    def _on_clear(self):
        """Clear both the preview area and the console."""
        self.preview.clear()
        self.console.clear()
        self.console.log("🗑 Aperçu et console effacés.", "info")

    def _on_save(self):
        """Save current editor content to a file."""
        code = self.editor.get_code()
        path = save_file(code)
        if path:
            self.console.log(f"💾 Fichier sauvegardé : {path}", "success")
        else:
            self.console.log("⚠ Sauvegarde annulée.", "info")

    def _on_load_lesson(self, name: str):
        """Load the selected lesson's code into the editor."""
        try:
            code = get_lesson_code(name)
            self.editor.set_code(code)
            self.preview.clear()
            self.console.log(f"📚 Leçon chargée : {name}", "info")
        except KeyError:
            self.console.log(f"❌ Leçon introuvable : {name}", "error")

    def _on_font_zoom(self, delta: int):
        """Zoom editor font: +1 increase, -1 decrease, 0 reset."""
        self.editor.zoom_font(delta)

    def _on_assistant(self):
        """Open the AI Assistant window."""
        def insert_code(code: str):
            self.editor.set_code(code)
            self.console.log("✨ Code AI inséré avec succès.", "success")
            
        AIAssistantWindow(parent=self.root, on_insert_code=insert_code)

    # ── Run ───────────────────────────────────

    def run(self):
        self.root.mainloop()


# ── Entry Point ───────────────────────────────
if __name__ == "__main__":
    app = TkLearnStudio()
    app.run()
