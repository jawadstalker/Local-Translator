# Local-Translator
![Project Logo](logo.png)

A lightweight tool that lets you translate your **clipboard's text on-demand** using a keyboard shortcut.

## Features

- **Detects Source Language:** Automatically identifies the language of your clipboard's text.
- **Translates To Desired Language:** Translates it into your preferred target language.
- **Hotkeys:**  
  - `Ctrl + Alt + T`: Translate whatever is currently in your clipboard.  
  - `Ctrl + Alt + Y`: Change the target language on the fly.

- **GUI Display:** Shows the translation in a GUI window with an option to copy it back to your clipboard.

## Installation

python -m venv .venv
source .venv/Scripts/activate  # Windows
source .venv/bin/activate     # macOS and Linux
pip install -r requirements.txt
