# ──────────────────────────────────────────────
# TkLearn Studio v1.0 — Configuration & Constants
# ──────────────────────────────────────────────

import os

# ── Window ────────────────────────────────────
APP_TITLE = "TkLearn Studio v1.0"
WINDOW_GEOMETRY = "1200x700"
MIN_WIDTH = 900
MIN_HEIGHT = 500

# ── Fonts ─────────────────────────────────────
EDITOR_FONT_FAMILY = "Consolas"
EDITOR_FONT_SIZE = 11
EDITOR_FONT_SIZE_MIN = 8
EDITOR_FONT_SIZE_MAX = 24
EDITOR_FONT = (EDITOR_FONT_FAMILY, EDITOR_FONT_SIZE)
LABEL_FONT = ("Segoe UI", 10, "bold")
UI_FONT = ("Segoe UI", 9)

# ── Keyboard Shortcuts ────────────────────────
KEY_RUN = "<F5>"
KEY_SAVE = "<Control-s>"

# ── Light Theme Palette ───────────────────────
# Subtle, card-based light theme inspired by modern IDEs
BG_PRIMARY = "#E5E7EB"          # app background (soft gray)
BG_SECONDARY = "#F9FAFB"        # panels / cards
BG_TOOLBAR = "#FFFFFF"          # clean white toolbar
BORDER_COLOR = "#D1D5DB"        # slightly stronger, still subtle border
TEXT_PRIMARY = "#111827"        # almost black for high contrast
TEXT_SECONDARY = "#6B7280"      # soft gray for labels
ACCENT = "#2563EB"              # vibrant blue
ACCENT_HOVER = "#1D4ED8"
ACCENT_GREEN = "#10B981"        # modern emerald green
ACCENT_GREEN_HOVER = "#059669"
BTN_DANGER = "#EF4444"          # red for clear
BTN_DANGER_HOVER = "#DC2626"
BTN_INFO = "#3B82F6"            # lighter blue for load
BTN_INFO_HOVER = "#2563EB"
BTN_SAVE = "#8B5CF6"            # purple for save
BTN_SAVE_HOVER = "#7C3AED"
BTN_AI = "#F59E0B"              # amber for AI assistance
BTN_AI_HOVER = "#D97706"

# ── API Keys ──────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# ── Syntax Highlighting ──────────────────────
# Slightly softer, VS Code–inspired palette
KEYWORD_COLOR = "#2563EB"       # blue
BUILTIN_COLOR = "#0F766E"       # teal
STRING_COLOR = "#16A34A"        # green
COMMENT_COLOR = "#9CA3AF"       # muted gray
DECORATOR_COLOR = "#7C3AED"     # purple
NUMBER_COLOR = "#0284C7"        # cyan/blue
CLASS_NAME_COLOR = "#7C3AED"    # purple
FUNC_NAME_COLOR = "#4C1D95"     # deep purple
SELF_COLOR = "#DC2626"          # red

# ── Console Tag Colors ────────────────────────
CONSOLE_INFO_COLOR = "#2563EB"      # blue
CONSOLE_SUCCESS_COLOR = "#10B981"   # green
CONSOLE_ERROR_COLOR = "#EF4444"     # red

# ── Editor ────────────────────────────────────
EDITOR_BG = "#F9FAFB"           # softer than pure white
EDITOR_FG = "#111827"
EDITOR_INSERT_COLOR = "#2563EB"
EDITOR_SELECT_BG = "#DBEAFE"    # accent-tinted selection
CURRENT_LINE_BG = "#E5E7EB"     # clearer current-line highlight
LINE_NUMBER_BG = "#E5E7EB"
LINE_NUMBER_FG = "#6B7280"

# ── Console ───────────────────────────────────
# Darker console for contrast against light editor
CONSOLE_BG = "#020617"
CONSOLE_FG = "#E5E7EB"

# ── Preview ───────────────────────────────────
PREVIEW_BG = "#F9FAFB"

# ── Python Keywords for Highlighting ──────────
PYTHON_KEYWORDS = [
    "False", "None", "True", "and", "as", "assert", "async", "await",
    "break", "class", "continue", "def", "del", "elif", "else",
    "except", "finally", "for", "from", "global", "if", "import",
    "in", "is", "lambda", "nonlocal", "not", "or", "pass", "raise",
    "return", "try", "while", "with", "yield",
]

PYTHON_BUILTINS = [
    "print", "range", "len", "int", "str", "float", "list", "dict",
    "tuple", "set", "bool", "type", "isinstance", "enumerate", "zip",
    "map", "filter", "sorted", "reversed", "input", "open", "super",
]
