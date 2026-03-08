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
            font=EDITOR_FONT,
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
            font=EDITOR_FONT,
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
        self.text.tag_configure("number", foreground=NUMBER_COLOR)
        self.text.tag_configure("class_name", foreground=CLASS_NAME_COLOR, font=(EDITOR_FONT[0], EDITOR_FONT[1], "bold"))
        self.text.tag_configure("func_name", foreground=FUNC_NAME_COLOR, font=(EDITOR_FONT[0], EDITOR_FONT[1], "bold"))
        self.text.tag_configure("self_kw", foreground=SELF_COLOR, font=(EDITOR_FONT[0], EDITOR_FONT[1], "italic"))
        self.text.tag_configure("keyword", foreground=KEYWORD_COLOR, font=(EDITOR_FONT[0], EDITOR_FONT[1], "bold"))
        self.text.tag_configure("builtin", foreground=BUILTIN_COLOR)
        self.text.tag_configure("decorator", foreground=DECORATOR_COLOR)
        self.text.tag_configure("string", foreground=STRING_COLOR)
        self.text.tag_configure("comment", foreground=COMMENT_COLOR, font=(EDITOR_FONT[0], EDITOR_FONT[1], "italic"))
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
