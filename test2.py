import pyperclip
import tkinter as tk
import threading
import torch
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
from langdetect import detect
import keyboard

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_name = "facebook/m2m100_418M"
tokenizer = M2M100Tokenizer.from_pretrained(model_name)
model = M2M100ForConditionalGeneration.from_pretrained(model_name).to(device)

print("Supported languages (examples): en = English, fa = Persian, de = German, fr = French, ja = Japanese")
print("Full list of supported language codes:", list(tokenizer.lang_code_to_id.keys()))

target_lang = input("Enter target language code (e.g., fa, en, de, etc.): ").strip()
while target_lang not in tokenizer.lang_code_to_id:
    print(f"Language code '{target_lang}' not supported.")
    target_lang = input("Please enter a valid language code (like en, fa, de): ").strip()

def translate_and_show():
    try:
        text = pyperclip.paste()
        if not text.strip():
            print("Clipboard is empty.")
            return

        source_lang = detect(text)
        print(f"Detected source language: {source_lang}")

        if source_lang not in tokenizer.lang_code_to_id:
            print(f"Source language '{source_lang}' not supported by the model.")
            return
        if target_lang not in tokenizer.lang_code_to_id:
            print(f"Target language '{target_lang}' not supported by the model.")
            return

        tokenizer.src_lang = source_lang
        encoded = tokenizer(text, return_tensors="pt").to(device)
        generated = model.generate(**encoded, forced_bos_token_id=tokenizer.lang_code_to_id[target_lang])
        translation = tokenizer.decode(generated[0], skip_special_tokens=True)

        root = tk.Tk()
        root.title("Translation")
        root.geometry("500x200")
        root.resizable(False, False)

        text_box = tk.Text(root, wrap="word", font=("Helvetica", 12))
        text_box.insert("1.0", translation)
        text_box.pack(expand=True, fill="both", padx=10, pady=10)

        copy_button = tk.Button(root, text="Copy", command=lambda: pyperclip.copy(translation))
        copy_button.pack(pady=5)

        root.mainloop()

    except Exception as e:
        print("Error:", e)

def change_target_language():
    global target_lang
    new_lang = input("Enter new target language code: ").strip()
    while new_lang not in tokenizer.lang_code_to_id:
        print("This language code is not supported.")
        new_lang = input("Please enter a valid language code: ").strip()
    target_lang = new_lang
    print(f"Target language changed to: {target_lang}")

def listen_keys():
    keyboard.add_hotkey('ctrl+alt+t', lambda: threading.Thread(target=translate_and_show).start())
    keyboard.add_hotkey('ctrl+alt+y', lambda: threading.Thread(target=change_target_language).start())
    print("Press Ctrl+Alt+T to translate clipboard text.")
    print("Press Ctrl+Alt+Y to change the target language.")
    keyboard.wait()

listen_keys()
