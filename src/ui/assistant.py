# ──────────────────────────────────────────────
# TkLearn Studio v1.0 — AI Assistant
# ──────────────────────────────────────────────
import threading
import tkinter as tk
from tkinter import messagebox, ttk

import groq

from ..utils.constants import (
    BG_PRIMARY,
    BG_SECONDARY,
    BTN_AI,
    BTN_INFO,
    CONSOLE_ERROR_COLOR,
    EDITOR_FONT,
    GROQ_API_KEY,
    TEXT_PRIMARY,
)

SYSTEM_PROMPT = """You are a Tkinter expert assistant. 
The user will ask you to build a UI component or perform an action in Tkinter.
You MUST respond with pure executable Python code ONLY. 
DO NOT INCLUDE ANY MARKDOWN formatting like ```python. 
DO NOT INCLUDE EXPLANATIONS, ONLY raw python source code.
Assume `tk` and `ttk` are already imported.
Assume the parent window/container is named `root`.
Do NOT call `root.mainloop()`.
"""

class AIAssistantWindow(tk.Toplevel):
    """A floating window that allows users to prompt an AI for Tkinter code."""

    prompt_text: tk.Text
    btn_generate: ttk.Button
    loading_label: ttk.Label
    result_text: tk.Text
    btn_insert: ttk.Button

    def __init__(self, parent: tk.Widget, on_insert_code=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.title("🤖 Assistant Tkinter")
        self.geometry("500x600")
        self.configure(bg=BG_PRIMARY)
        self.minsize(400, 400)
        self.transient(master=parent) # type: ignore
        
        self.on_insert_code = on_insert_code
        self.generated_code = ""

        # Initialize Groq client with clear error when no API key is configured
        if not GROQ_API_KEY:
            self.client = None
            messagebox.showerror(
                "Clé API manquante",
                "Aucune clé Groq n'a été trouvée.\n\n"
                "Veuillez définir la variable d'environnement 'GROQ_API_KEY' "
                "avec votre clé API Groq, puis relancer l'application.",
                parent=self,
            )
        else:
            try:
                self.client = groq.Groq(api_key=GROQ_API_KEY)
            except Exception as e:
                self.client = None
                messagebox.showerror(
                    "Erreur Groq",
                    f"Impossible d'initialiser le client Groq.\n\nDétail : {e}",
                    parent=self,
                )

        self._build_ui()

    def _build_ui(self):
        # ── Input Area ──
        input_frame = ttk.LabelFrame(self, text="Votre demande (Prompt)")
        input_frame.pack(fill="x", padx=10, pady=10)

        self.prompt_text = tk.Text(
            input_frame, 
            height=4, 
            font=("Segoe UI", 10), 
            bg=BG_SECONDARY, 
            fg=TEXT_PRIMARY,
            wrap="word",
        )
        self.prompt_text.pack(fill="x", padx=5, pady=5)

        self.btn_generate = ttk.Button(
            input_frame, 
            text="✨ Générer le code", 
            command=self._on_generate, 
            style="AI.TButton"
        )
        self.btn_generate.pack(side="right", padx=5, pady=5)
        
        self.loading_label = ttk.Label(input_frame, text="", foreground=BTN_INFO)
        self.loading_label.pack(side="right", padx=5, pady=5)

        # ── Footer Area ──
        footer = ttk.Frame(self)
        footer.pack(side="bottom", fill="x", padx=10, pady=(0, 10))
        
        self.btn_insert = ttk.Button(
            footer, 
            text="⬇️ Insérer dans l'éditeur", 
            command=self._on_insert,
            state="disabled",
            style="Accent.TButton"
        )
        self.btn_insert.pack(side="right")

        # ── Output Area ──
        output_frame = ttk.LabelFrame(self, text="Code généré (Python)")
        output_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.result_text = tk.Text(
            output_frame,
            font=EDITOR_FONT,
            bg="#FAFAFA",
            fg="#111827",
            wrap="none",
            state="disabled",
            padx=5,
            pady=5,
        )
        
        scroll_y = ttk.Scrollbar(output_frame, orient="vertical", command=self.result_text.yview)
        scroll_x = ttk.Scrollbar(output_frame, orient="horizontal", command=self.result_text.xview)
        self.result_text.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set) # type: ignore
        
        self.result_text.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)

    def _on_generate(self):
        prompt = self.prompt_text.get("1.0", "end").strip()
        if not prompt:
            return
            
        if not self.client:
            messagebox.showerror("Erreur", "Le client API n'est pas initialisé.", parent=self)
            return

        self.btn_generate.configure(state="disabled")
        self.loading_label.configure(text="Chargement...")
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.configure(state="disabled")
        self.btn_insert.configure(state="disabled")

        # Run API call in a thread to keep GUI responsive
        threading.Thread(target=self._fetch_code, args=(prompt,), daemon=True).start()

    def _fetch_code(self, user_prompt: str):
        try:
            if not self.client:
                return

            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile", 
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=1024,
            )
            
            # The strictly pure code approach might still leave markdown sometimes.
            # So perform a naive cleanup just in case.
            msg = completion.choices[0].message.content
            code: str = str(msg) if msg else ""
            code = code.strip()
            
            if code.startswith("```python"):
                code = code[9:] # type: ignore
            elif code.startswith("```"):
                code = code[3:] # type: ignore
            if code.endswith("```"):
                code = code[:-3] # type: ignore
            code = code.strip()

            self.after(0, self._on_fetch_success, code)
        except Exception as e:
            self.after(0, self._on_fetch_error, str(e))

    def _on_fetch_success(self, code: str):
        self.generated_code = code
        
        self.result_text.configure(state="normal")
        self.result_text.insert("1.0", code)
        self.result_text.configure(state="disabled")
        
        self.loading_label.configure(text="")
        self.btn_generate.configure(state="normal")
        self.btn_insert.configure(state="normal")

    def _on_fetch_error(self, err: str):
        self.loading_label.configure(text="Erreur!", foreground=CONSOLE_ERROR_COLOR)
        self.btn_generate.configure(state="normal")
        
        self.result_text.configure(state="normal")
        self.result_text.insert("1.0", f"# Erreur lors de la génération:\n# {err}")
        self.result_text.configure(state="disabled")

    def _on_insert(self):
        if self.on_insert_code and self.generated_code:
            self.on_insert_code(self.generated_code)
            self.destroy()
