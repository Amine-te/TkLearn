# TkLearn Studio

**TkLearn Studio** is an interactive, low-code/no-code learning environment built with Python and Tkinter. It serves as both a playground for experimenting with Tkinter UI widgets and an educational platform for learning Python GUI concepts.

## 🚀 Features

- **Integrated Code Editor**: Write Python and Tkinter code with a clean, modern interface.
- **✨ AI Assistant (Groq-powered)**: Prompt an AI right in the app to generate Tkinter code, then auto-insert it into your editor.
- **Live Preview Engine**: Instantly render and preview the Tkinter widgets you build.
- **Educational Lessons**: Load predefined lessons to learn step-by-step.
- **Logging Console**: A read-only, color-coded console (Info, Success, Error) to track execution output.
- 🛡️ **Secure Code Execution**: The `exec()` function running user scripts is hardened with an AST-level sandbox. It strictly prohibits potentially dangerous operations (like file I/O, `eval`, unauthorized imports, or escaping the environment) using a meticulously restricted `__builtins__` namespace.

## 📋 Requirements

- Python >= 3.10
- No external dependencies required! (Uses standard `tkinter` library).

## 🛠️ How to Use

1. Clone or download this repository.
2. Run the main controller:
   ```bash
   python main.py
   ```
3. Use the Editor to write Tkinter code, and click **Lancer** (or press F5) to see your UI rendered live in the Preview section.

## 📁 Project Structure

- `main.py`: The entry point that wires all components together.
- `src/ui/`: Contains the UI components (`editor.py`, `preview.py`, `console.py`, `menus.py`).
- `src/core/`: Contains logic for file management and lesson loading.
- `src/utils/`: Constants and configuration.

## 🔒 Security

We prioritize safety. Because this is an educational tool that executes dynamic code, the `PreviewEngine` enforces strict constraints:
- **No Imports**: `import` and `from ... import` statements are blocked.
- **Restricted Builtins**: Functions like `open()`, `exec()`, `eval()`, `__import__()`, `getattr()`, `setattr()`, and `delattr()` are disabled.
- **Property Access Control**: Access to "dunder" attributes (e.g., `__class__`) is prevented at the AST level.

Enjoy learning Tkinter safely!
