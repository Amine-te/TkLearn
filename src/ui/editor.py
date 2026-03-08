# ──────────────────────────────────────────────
# TkLearn Studio v1.0 — Code Editor
# ──────────────────────────────────────────────
import re
import tkinter as tk
from tkinter import ttk

from ..utils.constants import (
    BORDER_COLOR,
    BUILTIN_COLOR,
    CLASS_NAME_COLOR,
    COMMENT_COLOR,
    CURRENT_LINE_BG,
    DECORATOR_COLOR,
    EDITOR_BG,
    EDITOR_FG,
    EDITOR_FONT,
    EDITOR_FONT_SIZE,
    EDITOR_FONT_SIZE_MAX,
    EDITOR_FONT_SIZE_MIN,
    EDITOR_INSERT_COLOR,
    EDITOR_SELECT_BG,
    FUNC_NAME_COLOR,
    KEYWORD_COLOR,
    LINE_NUMBER_BG,
    LINE_NUMBER_FG,
    NUMBER_COLOR,
    PYTHON_BUILTINS,
    PYTHON_KEYWORDS,
    SELF_COLOR,
    STRING_COLOR,
)


class CodeEditor(ttk.Frame):
    """Syntax-highlighted text editor for Python code."""

    def __init__(self, parent: tk.Widget, **kwargs):
        super().__init__(parent, **kwargs)
        self._cursor_callback = None
        self._font_size = EDITOR_FONT_SIZE
        self._build_ui()
        self._configure_tags()
        self._bind_events()

    # ── Construction ──────────────────────────

    def _build_ui(self):
        # Title
        title = ttk.Label(self, text="  📝 Éditeur de Code", style="Title.TLabel")
        title.pack(fill="x", pady=(0, 2))

        # Container for text + scrollbars
        container = ttk.Frame(self, style="Card.TFrame")
        container.pack(fill="both", expand=True)

        # Line numbers
        self._line_numbers = tk.Text(
            container,
            width=4,
            bg=LINE_NUMBER_BG,
            fg=LINE_NUMBER_FG,
            font=(EDITOR_FONT[0], self._font_size),
            relief="flat",
            state="disabled",
            takefocus=0,
            cursor="arrow",
            padx=8,
            pady=4,
            spacing1=2,
            spacing3=2,
            borderwidth=0,
            highlightthickness=0,
        )
        self._line_numbers.tag_configure("right", justify="right")
        self._line_numbers.pack(side="left", fill="y", padx=(2, 0))

        # Main text widget
        self.text = tk.Text(
            container,
            bg=EDITOR_BG,
            fg=EDITOR_FG,
            font=(EDITOR_FONT[0], self._font_size),
            insertbackground=EDITOR_INSERT_COLOR,
            selectbackground=EDITOR_SELECT_BG,
            relief="flat",
            wrap="none",
            undo=True,
            padx=10,
            pady=4,
            spacing1=2,
            spacing3=2,
            borderwidth=0,
            highlightthickness=0,
            tabs=("4c",),  # 4-char tab stops
        )

        # Vertical scrollbar
        v_scroll = ttk.Scrollbar(container, orient="vertical", command=self._on_scroll_y)
        v_scroll.pack(side="right", fill="y")

        # Horizontal scrollbar
        h_scroll = ttk.Scrollbar(self, orient="horizontal", command=self.text.xview)
        h_scroll.pack(side="bottom", fill="x")

        self.text.pack(side="left", fill="both", expand=True)
        self.text.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

    def _on_scroll_y(self, *args):
        """Sync line numbers scroll with text scroll."""
        self.text.yview(*args)
        self._line_numbers.yview(*args)

    # ── Syntax Tag Configuration ──────────────

    def _configure_tags(self):
        fam, sz = EDITOR_FONT[0], self._font_size
        self.text.tag_configure("number", foreground=NUMBER_COLOR)
        self.text.tag_configure("class_name", foreground=CLASS_NAME_COLOR, font=(fam, sz, "bold"))
        self.text.tag_configure("func_name", foreground=FUNC_NAME_COLOR, font=(fam, sz, "bold"))
        self.text.tag_configure("self_kw", foreground=SELF_COLOR, font=(fam, sz, "italic"))
        self.text.tag_configure("keyword", foreground=KEYWORD_COLOR, font=(fam, sz, "bold"))
        self.text.tag_configure("builtin", foreground=BUILTIN_COLOR)
        self.text.tag_configure("decorator", foreground=DECORATOR_COLOR)
        self.text.tag_configure("string", foreground=STRING_COLOR)
        self.text.tag_configure("comment", foreground=COMMENT_COLOR, font=(fam, sz, "italic"))
        self.text.tag_configure("current_line", background=CURRENT_LINE_BG)
        
        self.text.tag_lower("current_line")
        self.text.tag_raise("string")
        self.text.tag_raise("comment")

    # ── Event Bindings ────────────────────────

    def _bind_events(self):
        self.text.bind("<KeyRelease>", self._on_key_release)
        self.text.bind("<ButtonRelease-1>", self._on_cursor_move)
        self.text.bind("<MouseWheel>", self._on_mousewheel)
        self.text.bind("<<Modified>>", self._on_modified)

    def _on_key_release(self, _event=None):
        self._highlight_syntax()
        self._on_cursor_move()
        self._update_line_numbers()

    def _on_cursor_move(self, _event=None):
        self.text.tag_remove("current_line", "1.0", "end")
        self.text.tag_add("current_line", "insert linestart", "insert lineend+1c")
        if self._cursor_callback:
            line, col = self._get_cursor_position()
            self._cursor_callback(line, col)

    def _get_cursor_position(self) -> tuple[int, int]:
        idx = self.text.index("insert")
        parts = idx.split(".")
        line = int(parts[0])
        col = int(parts[1]) + 1  # 1-based column for display
        return line, col

    def set_cursor_callback(self, callback):
        """Set a callback(line, column) called when the cursor moves."""
        self._cursor_callback = callback
        if callback:
            line, col = self._get_cursor_position()
            callback(line, col)

    def _on_modified(self, _event=None):
        if self.text.edit_modified():
            self._update_line_numbers()
            self.text.edit_modified(False)

    def _on_mousewheel(self, event):
        self._line_numbers.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ── Syntax Highlighting ───────────────────

    def _highlight_syntax(self):
        code = self.text.get("1.0", "end-1c")

        # Remove all previous tags
        tags = ("keyword", "builtin", "string", "comment", "decorator", "number", "class_name", "func_name", "self_kw")
        for tag in tags:
            self.text.tag_remove(tag, "1.0", "end")

        # Numbers
        for m in re.finditer(r"\b\d+(\.\d*)?\b", code):
            self._apply_tag("number", m)

        # Keywords
        for kw in PYTHON_KEYWORDS:
            for m in re.finditer(rf"\b{kw}\b", code):
                self._apply_tag("keyword", m)

        # Builtins
        for bi in PYTHON_BUILTINS:
            for m in re.finditer(rf"\b{bi}\b", code):
                self._apply_tag("builtin", m)

        # Class names
        for m in re.finditer(r"\bclass\s+([a-zA-Z_]\w*)", code):
            start = f"1.0+{m.start(1)}c"
            end = f"1.0+{m.end(1)}c"
            self.text.tag_add("class_name", start, end)

        # Function names
        for m in re.finditer(r"\bdef\s+([a-zA-Z_]\w*)", code):
            start = f"1.0+{m.start(1)}c"
            end = f"1.0+{m.end(1)}c"
            self.text.tag_add("func_name", start, end)

        # self
        for m in re.finditer(r"\bself\b", code):
            self._apply_tag("self_kw", m)

        # Decorators  ( @something )
        for m in re.finditer(r"@\w+", code):
            self._apply_tag("decorator", m)

        # Strings  ( "…" , '…' , '''…''' , \"\"\"…\"\"\" )
        for m in re.finditer(r'(\"\"\"[\s\S]*?\"\"\"|\'\'\'[\s\S]*?\'\'\'|\"[^\"\\]*(?:\\.[^\"\\]*)*\"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')', code):
            self._apply_tag("string", m)

        # Comments  ( # … )
        for m in re.finditer(r"#[^\n]*", code):
            self._apply_tag("comment", m)

    def _apply_tag(self, tag: str, match: re.Match):
        start = f"1.0+{match.start()}c"
        end = f"1.0+{match.end()}c"
        self.text.tag_add(tag, start, end)

    # ── Line Numbers ──────────────────────────

    def _update_line_numbers(self):
        self._line_numbers.configure(state="normal")
        self._line_numbers.delete("1.0", "end")
        line_count = int(self.text.index("end-1c").split(".")[0])
        line_text = "\n".join(str(i) for i in range(1, line_count + 1))
        self._line_numbers.insert("1.0", line_text)
        self._line_numbers.tag_add("right", "1.0", "end")
        self._line_numbers.configure(state="disabled")

    # ── Public API ────────────────────────────

    def get_code(self) -> str:
        """Return all text in the editor."""
        return self.text.get("1.0", "end-1c")

    def set_code(self, code: str):
        """Replace editor contents with *code* and re-highlight."""
        self.text.delete("1.0", "end")
        self.text.insert("1.0", code)
        self._highlight_syntax()
        self._update_line_numbers()

    def clear(self):
        """Clear the editor."""
        self.text.delete("1.0", "end")
        self._update_line_numbers()

    # ── Font zoom ─────────────────────────────

    def zoom_font(self, delta: int):
        """Change font size: +1 increase, -1 decrease, 0 reset to default."""
        if delta == 0:
            new_size = EDITOR_FONT_SIZE
        else:
            new_size = self._font_size + delta
        new_size = max(EDITOR_FONT_SIZE_MIN, min(EDITOR_FONT_SIZE_MAX, new_size))
        if new_size == self._font_size:
            return
        self._font_size = new_size
        fam = EDITOR_FONT[0]
        self.text.configure(font=(fam, new_size))
        self._line_numbers.configure(font=(fam, new_size))
        self.text.tag_configure("number", font=(fam, new_size))
        self.text.tag_configure("class_name", font=(fam, new_size, "bold"))
        self.text.tag_configure("func_name", font=(fam, new_size, "bold"))
        self.text.tag_configure("self_kw", font=(fam, new_size, "italic"))
        self.text.tag_configure("keyword", font=(fam, new_size, "bold"))
        self.text.tag_configure("builtin", font=(fam, new_size))
        self.text.tag_configure("decorator", font=(fam, new_size))
        self.text.tag_configure("string", font=(fam, new_size))
        self.text.tag_configure("comment", font=(fam, new_size, "italic"))
        self._highlight_syntax()

    # ── Search ─────────────────────────────────

    def show_search(self):
        """Open the search dialog."""
        if hasattr(self, "_search_dialog") and self._search_dialog.winfo_exists():
            self._search_dialog.focus_set()
            return
        self._search_dialog = tk.Toplevel(self.winfo_toplevel())
        self._search_dialog.title("Rechercher")
        self._search_dialog.transient(self.winfo_toplevel())
        self._search_dialog.geometry("400x80")
        self._search_dialog.resizable(False, False)
        frame = ttk.Frame(self._search_dialog, padding=8)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Rechercher :").pack(side="left", padx=(0, 4))
        self._search_entry = ttk.Entry(frame, width=30)
        self._search_entry.pack(side="left", padx=4, fill="x", expand=True)
        self._search_entry.focus_set()
        self._search_entry.bind("<Return>", lambda e: self._find_next())
        self._search_entry.bind("<Escape>", lambda e: self._search_dialog.destroy())
        ttk.Button(frame, text="Suivant", command=self._find_next).pack(side="left", padx=2)
        ttk.Button(frame, text="Précédent", command=self._find_prev).pack(side="left", padx=2)
        ttk.Button(frame, text="Fermer", command=self._search_dialog.destroy).pack(side="left", padx=2)
        self.text.tag_configure("search_match", background="#FEF08A")
        self._search_dialog.protocol("WM_DELETE_WINDOW", self._search_dialog.destroy)

    def _find_next(self):
        if not hasattr(self, "_search_dialog") or not self._search_dialog.winfo_exists():
            return
        self._do_find(forward=True)

    def _find_prev(self):
        if not hasattr(self, "_search_dialog") or not self._search_dialog.winfo_exists():
            return
        self._do_find(forward=False)

    def _do_find(self, forward: bool):
        query = self._search_entry.get()
        if not query:
            return
        self.text.tag_remove("search_match", "1.0", "end")
        self.text.tag_remove("sel", "1.0", "end")
        if forward:
            pos = self.text.search(query, "insert+1c", "end", nocase=True)
            if not pos:
                pos = self.text.search(query, "1.0", "end", nocase=True)
        else:
            pos = self.text.search(query, "insert", "1.0", nocase=True, backwards=True)
            if not pos:
                pos = self.text.search(query, "end-1c", "1.0", nocase=True, backwards=True)
        if pos:
            end = f"{pos}+{len(query)}c"
            self.text.tag_add("search_match", pos, end)
            self.text.tag_add("sel", pos, end)
            self.text.see(pos)
            self.text.mark_set("insert", end if forward else pos)
        else:
            self.text.bell()
