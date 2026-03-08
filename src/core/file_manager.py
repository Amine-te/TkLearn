# ──────────────────────────────────────────────
# TkLearn Studio v1.0 — File Manager (I/O)
# ──────────────────────────────────────────────
from tkinter import filedialog


def save_file(content: str) -> str | None:
    """Open a Save-As dialog and write *content* to the chosen path.

    Returns the path on success, or None if the user cancels.
    """
    path = filedialog.asksaveasfilename(
        defaultextension=".py",
        filetypes=[("Python files", "*.py"), ("All files", "*.*")],
        title="Sauvegarder le fichier",
    )
    if not path:
        return None

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def open_file() -> tuple[str, str] | None:
    """Open a file dialog and return *(path, content)*.

    Returns None if the user cancels.
    """
    path = filedialog.askopenfilename(
        filetypes=[("Python files", "*.py"), ("All files", "*.*")],
        title="Ouvrir un fichier",
    )
    if not path:
        return None

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return path, content
