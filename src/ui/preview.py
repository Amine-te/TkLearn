# ──────────────────────────────────────────────
# TkLearn Studio v1.0 — Preview Engine
# ──────────────────────────────────────────────
import tkinter as tk
from tkinter import ttk

from ..utils.constants import PREVIEW_BG


class PreviewEngine(ttk.Frame):
    """Executes student code and renders its Tkinter widgets inside the app."""

    def __init__(self, parent: tk.Widget, **kwargs):
        super().__init__(parent, **kwargs)
        self._build_ui()

    # ── Construction ──────────────────────────

    def _build_ui(self):
        title = ttk.Label(self, text="  🖥️ Aperçu", style="Title.TLabel")
        title.pack(fill="x", pady=(0, 2))

        # The render area where student widgets will appear
        self.render_area = tk.Frame(self, bg=PREVIEW_BG, relief="flat", bd=0, highlightthickness=1, highlightbackground=PREVIEW_BG)
        self.render_area.pack(fill="both", expand=True)

    # ── Public API ────────────────────────────

    def execute_code(self, code: str):
        """Execute *code* with tk, ttk, and the render_area injected as ``root``.

        Returns (True, "") on success, or (False, traceback_str) on error.
        """
        import traceback
        import ast

        try:
            tree = ast.parse(code)
        except SyntaxError:
            return False, traceback.format_exc()

        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
                return False, f"Security Error: Access to '{node.attr}' is prohibited."
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name):
                    func_id = func.id
                    if func_id in ("exec", "globals", "locals", "open", "getattr", "setattr", "delattr"):
                        return False, f"Security Error: Function '{func_id}()' is prohibited."

        import builtins
        safe_builtins = {
            "print": print, "range": range, "int": int, "str": str, "float": float,
            "bool": bool, "len": len, "list": list, "dict": dict, "set": set,
            "tuple": tuple, "enumerate": enumerate, "zip": zip, "abs": abs,
            "min": min, "max": max, "sum": sum, "round": round, "type": type,
            "isinstance": isinstance, "issubclass": issubclass, "Exception": Exception,
            "ValueError": ValueError, "TypeError": TypeError, "KeyError": KeyError,
            "IndexError": IndexError, "AttributeError": AttributeError,
            "any": any, "all": all, "eval": eval, "__build_class__": builtins.__build_class__,
            "__import__": builtins.__import__,
        }

        class SafeRootWrapper:
            """Wraps a tk.Frame but safely ignores tk.Tk window methods."""
            def __init__(self, frame):
                self._frame = frame

            def __getattr__(self, name):
                if name in ("title", "geometry", "resizable", "iconbitmap", "protocol", "minsize", "maxsize"):
                    return lambda *args, **kwargs: None
                return getattr(self._frame, name)

        safe_root = SafeRootWrapper(self.render_area)

        namespace = {
            "__builtins__": safe_builtins,
            "__name__": "__main__",
            "tk": tk,
            "ttk": ttk,
            "tkinter": tk,
            "root": safe_root,
        }

        try:
            exec(code, namespace)
            return True, ""
        except Exception:
            return False, traceback.format_exc()

    def clear(self):
        """Destroy all widgets inside the render area."""
        for widget in self.render_area.winfo_children():
            widget.destroy()
