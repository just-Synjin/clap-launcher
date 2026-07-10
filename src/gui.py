import tkinter as tk
from tkinter import filedialog, messagebox
from src.config import load_config, save_config

def browse_file():
    path = filedialog.askopenfilename(filetypes=[("Executable", "*.exe")])
    if path:
        path_var.set(path)

def save():
    config = load_config()
    config["game_path"] = path_var.get()
    save_config(config)
    messagebox.showinfo("Saved", "Path saved!")

def main():
    global path_var
    root = tk.Tk()
    root.title("Clap Launcher — Settings")

    path_var = tk.StringVar(value=load_config().get("game_path", ""))

    tk.Label(root, text="Game path:").pack(padx=10, pady=(10, 0))
    tk.Entry(root, textvariable=path_var, width=50).pack(padx=10, pady=5)
    tk.Button(root, text="Browse...", command=browse_file).pack(pady=5)
    tk.Button(root, text="Save", command=save).pack(pady=(0, 10))

    root.mainloop()
