# ──────────────────────────────────────────────
# TkLearn Studio v1.0 — Lesson Loader
# ──────────────────────────────────────────────

LESSONS: dict[str, str] = {
    # ── 1. Labels ─────────────────────────────
    "Labels": '''\
import tkinter as tk
from tkinter import ttk

# === Leçon : Labels ===
# Un Label affiche du texte ou une image.

label1 = ttk.Label(root, text="Bonjour, TkLearn !")
label1.pack(pady=10)

label2 = ttk.Label(root, text="Je suis un Label avec du style",
                   font=("Segoe UI", 14, "bold"),
                   foreground="#6C63FF")
label2.pack(pady=5)

label3 = ttk.Label(root, text="Texte en italique",
                   font=("Segoe UI", 11, "italic"))
label3.pack(pady=5)
''',

    # ── 2. Buttons ────────────────────────────
    "Buttons": '''\
import tkinter as tk
from tkinter import ttk

# === Leçon : Buttons ===
# Un Button déclenche une action au clic.

compteur = tk.IntVar(master=root, value=0)

def incrementer():
    compteur.set(compteur.get() + 1)

label = ttk.Label(root, textvariable=compteur,
                  font=("Segoe UI", 24, "bold"))
label.pack(pady=15)

btn = ttk.Button(root, text="Cliquer +1", command=incrementer)
btn.pack(pady=5)

btn_reset = ttk.Button(root, text="Réinitialiser",
                       command=lambda: compteur.set(0))
btn_reset.pack(pady=5)
''',

    # ── 3. Entry ──────────────────────────────
    "Entry": '''\
import tkinter as tk
from tkinter import ttk

# === Leçon : Entry ===
# Un Entry permet la saisie de texte.

ttk.Label(root, text="Votre nom :", font=("Segoe UI", 11)).pack(pady=(15, 2))

entry = ttk.Entry(root, width=30, font=("Segoe UI", 11))
entry.pack(pady=5)

result_label = ttk.Label(root, text="", font=("Segoe UI", 12, "bold"),
                         foreground="#50C878")
result_label.pack(pady=10)

def saluer():
    nom = entry.get().strip()
    if nom:
        result_label.config(text=f"Bonjour, {nom} ! 👋")
    else:
        result_label.config(text="Veuillez entrer un nom.")

ttk.Button(root, text="Saluer", command=saluer).pack(pady=5)
''',

    # ── 4. Formulaires ────────────────────────
    "Formulaires": '''\
import tkinter as tk
from tkinter import ttk

# === Leçon : Formulaires ===
# Combiner Label, Entry et Button pour un formulaire.

frame = ttk.LabelFrame(root, text="Inscription", padding=15)
frame.pack(padx=20, pady=20, fill="x")

# Nom
ttk.Label(frame, text="Nom :").grid(row=0, column=0, sticky="w", pady=4)
nom_entry = ttk.Entry(frame, width=25)
nom_entry.grid(row=0, column=1, pady=4, padx=(10, 0))

# Email
ttk.Label(frame, text="Email :").grid(row=1, column=0, sticky="w", pady=4)
email_entry = ttk.Entry(frame, width=25)
email_entry.grid(row=1, column=1, pady=4, padx=(10, 0))

# Niveau
ttk.Label(frame, text="Niveau :").grid(row=2, column=0, sticky="w", pady=4)
niveau = ttk.Combobox(frame, values=["Débutant", "Intermédiaire", "Avancé"],
                      state="readonly", width=22)
niveau.grid(row=2, column=1, pady=4, padx=(10, 0))
niveau.current(0)

# Résultat
result = ttk.Label(root, text="", font=("Segoe UI", 10),
                   foreground="#4A90D9")
result.pack(pady=10)

def soumettre():
    n = nom_entry.get().strip()
    e = email_entry.get().strip()
    nv = niveau.get()
    if n and e:
        result.config(text=f"✓ Inscrit : {n} ({e}) — niveau {nv}")
    else:
        result.config(text="⚠ Veuillez remplir tous les champs.")

ttk.Button(root, text="S\\'inscrire", command=soumettre).pack(pady=5)
''',

    # ── 5. Layout (Grid & Pack) ───────────────
    "Layout": '''\
import tkinter as tk
from tkinter import ttk

# === Leçon : Layout ===
# Utiliser pack() et grid() pour organiser les widgets.

# --- Section pack ---
pack_frame = ttk.LabelFrame(root, text="pack() — empiler", padding=10)
pack_frame.pack(padx=10, pady=10, fill="x")

for color, text in [("#E74C3C", "Rouge"), ("#3498DB", "Bleu"), ("#2ECC71", "Vert")]:
    lbl = tk.Label(pack_frame, text=text, bg=color, fg="white",
                   font=("Segoe UI", 10, "bold"), padx=10, pady=5)
    lbl.pack(fill="x", pady=2)

# --- Section grid ---
grid_frame = ttk.LabelFrame(root, text="grid() — grille", padding=10)
grid_frame.pack(padx=10, pady=10, fill="x")

for r in range(3):
    for c in range(3):
        btn = ttk.Button(grid_frame, text=f"({r},{c})")
        btn.grid(row=r, column=c, padx=3, pady=3)
''',

    # ── 6. Events ─────────────────────────────
    "Events": '''\
import tkinter as tk
from tkinter import ttk

# === Leçon : Événements ===
# Réagir aux actions de l\\'utilisateur avec bind().

info_label = ttk.Label(root, text="Interagissez avec les widgets ci-dessous",
                       font=("Segoe UI", 11, "italic"))
info_label.pack(pady=15)

# Détection d\\'un clic
canvas = tk.Canvas(root, width=300, height=150, bg="#F0F0F0",
                   highlightthickness=1, highlightbackground="#CCC")
canvas.pack(pady=10)

def on_click(event):
    canvas.delete("all")
    canvas.create_oval(event.x - 10, event.y - 10,
                       event.x + 10, event.y + 10,
                       fill="#6C63FF", outline="")
    info_label.config(text=f"Clic à ({event.x}, {event.y})")

canvas.bind("<Button-1>", on_click)

# Détection du clavier
key_label = ttk.Label(root, text="Appuyez sur une touche…",
                      font=("Courier New", 12), foreground="#E74C3C")
key_label.pack(pady=10)

def on_key(event):
    key_label.config(text=f"Touche : {event.keysym}")

root.bind("<Key>", on_key)
root.focus_set()
''',
}


def get_lesson_names() -> list[str]:
    """Return the ordered list of lesson titles."""
    return list(LESSONS.keys())


def get_lesson_code(name: str) -> str:
    """Return the starter code for the given lesson name.

    Raises KeyError if the lesson does not exist.
    """
    return LESSONS[name]
