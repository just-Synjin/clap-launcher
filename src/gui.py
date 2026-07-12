import tkinter as tk
from tkinter import messagebox
from src.config import load_config, save_config

def save():
    appid = appid_var.get().strip()
    if not appid.isdigit():
        messagebox.showerror("Invalid input", "Steam App ID must be a number.")
        return
    config = load_config()
    config["steam_appid"] = appid
    save_config(config)
    messagebox.showinfo("Saved", "Steam App ID saved!")

def main():
    global appid_var
    root = tk.Tk()
    root.title("Clap Launcher — Settings")

    appid_var = tk.StringVar(value=load_config().get("steam_appid", ""))

    tk.Label(root, text="Steam App ID:").pack(padx=10, pady=(10, 0))
    tk.Entry(root, textvariable=appid_var, width=30).pack(padx=10, pady=5)
    tk.Label(root, text="(found in the store URL: store.steampowered.com/app/<ID>)", fg="gray").pack(padx=10, pady=(0, 5))
    tk.Button(root, text="Save", command=save).pack(pady=(0, 10))

    root.mainloop()

if __name__ == "__main__":
    main()