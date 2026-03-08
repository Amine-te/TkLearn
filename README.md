## TkLearn Studio

**TkLearn Studio** is an interactive learning environment built with Python and Tkinter.  
It serves as both a playground for experimenting with Tkinter widgets and an educational platform for learning Python GUI concepts.

---

## ✨ Main Features

- **Integrated code editor**: Clean, modern editor tailored for Python/Tkinter.
- **Groq‑powered AI assistant**: Generate Tkinter code from natural language and insert it directly into the editor.
- **Live preview engine**: Render your Tkinter UI live inside the app.
- **Guided lessons**: Load predefined lessons to explore Tkinter step by step.
- **Color‑coded console**: Read‑only console with info/success/error messages.
- 🛡️ **Hardened execution sandbox**: User code is executed with a restricted `__builtins__` and AST‑level checks to block dangerous operations.

---

## 📋 Requirements

- Python ≥ 3.10
- `tkinter` (comes with most standard Python installs)
- `groq` Python package (for the AI assistant):

```bash
pip install groq
```

---

## 🚀 Getting Started

1. **Clone or download** this repository.
2. In a terminal at the project root, install dependencies:

   ```bash
   pip install -e .
   ```

   or, minimally:

   ```bash
   pip install groq
   ```

3. **Run the app**:

   ```bash
   python main.py
   ```

4. Use the editor to write Tkinter code, then click **Lancer** (or press `F5`) to execute and preview the UI.

---

## 🤖 AI Assistant & Groq API Key

The AI assistant relies on the Groq API. For security, the API key is **not** stored in the code; it is read from the `GROQ_API_KEY` environment variable.

- If no key is configured, the assistant window will show a clear message:
  it will tell you that **no Groq key was found** and that you must set `GROQ_API_KEY`.

### 1. Create / obtain a Groq API key

1. Sign in to your Groq account.
2. Create a new API key.
3. Copy the key (keep it secret; do **not** commit it into the repo).

### 2. Configure `GROQ_API_KEY` on Windows (PowerShell)

You can set the key **only for the current terminal**:

```powershell
$env:GROQ_API_KEY = "your-groq-api-key-here"
python main.py
```

Or set it **persistently for your user** (new terminals will see it):

```powershell
setx GROQ_API_KEY "your-groq-api-key-here"
```

Then close the terminal, open a new one, go back to the project folder, and run:

```powershell
python main.py
```

Once `GROQ_API_KEY` is set, the assistant should initialize successfully and generate Tkinter code directly inside the app.

---

## 📁 Project Structure

- `main.py` – Entry point that wires editor, preview, console, toolbar, and AI assistant.
- `src/ui/` – UI components (`editor.py`, `preview.py`, `console.py`, `menus.py`, `assistant.py`).
- `src/core/` – File management and lesson loading.
- `src/utils/` – Constants and configuration.

---

## 🔒 Security Notes

Because this tool executes dynamic code, the `PreviewEngine` enforces strict constraints:

- **No arbitrary imports**: `import` and `from ... import` are blocked.
- **Restricted builtins**: Functions like `open()`, `exec()`, `eval()`, `__import__()`, `getattr()`, `setattr()`, and `delattr()` are disabled.
- **Protected attributes**: Access to dangerous “dunder” attributes (e.g. `__class__`) is prevented at the AST level.

Enjoy learning Tkinter safely and interactively!
