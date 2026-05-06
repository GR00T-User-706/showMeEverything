#!/usr/bin/env python3
# SME_SIGNATURE=gr00t-user-706
import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import shutil


SEARCH_SCRIPT = shutil.which("showMeEverything")
if not SEARCH_SCRIPT:
    SEARCH_SCRIPT = "/usr/local/bin/showMeEverything"  # fallback

FLAG_GROUPS = {
    "ALL": ["--ALL", "-A", "ALL", "A"],
    "all": ["--all", "all"],
    "aliases": ["--aliases", "-a", "aliases", "a"],
    "builtins": ["--builtins", "-b", "builtins", "b"],
    "command": ["--command", "-c", "command", "c"],
    "files": ["--files", "-F", "files", "F"],
    "functions": ["--functions", "-f", "functions", "f"],
    "help": ["--help", "-h", "help", "h"],
    "home": ["--home", "-H", "home", "H"],
    "installed": ["--installed", "-i", "installed", "i"],
    "manpages": ["--manpages", "--man", "-M", "manpages", "man", "M"],
    "modules": ["--modules", "-m", "modules", "m"],
    "process": ["--process", "-x", "process", "x"],
    "packages": ["--packages", "-p", "--pkg", "packages", "pkg", "p"],
    "path": ["--path", "-P", "path", "P"],
    "systemd": ["--systemd", "-s", "systemd", "s"],
    "system": ["--system", "-R", "system", "R"],
    "excludeDotFiles": ["--excludeDotFiles", "--nodot", "excludeDotFiles", "nodot"],
    "usr": ["--usr", "-U", "usr", "U"],
    "etc": ["--etc", "-E", "etc", "E"],
    "var": ["--var", "-V", "var", "V"],
    "opt": ["--opt", "-O", "opt", "O"],
    "boot": ["--boot", "-B", "boot", "B"],
    "lib": ["--lib", "-L", "lib", "L"],
    "bin": ["--bin", "bin"],
    "sbin": ["--sbin", "sbin"],
}
ALLOWED_ARGS = [arg for group in FLAG_GROUPS.values() for arg in group]
ARG_MAP = {arg.lstrip("-").lower(): arg for arg in ALLOWED_ARGS}


def append_text(line):
    output_text.configure(state="normal")
    output_text.insert(tk.END, line)
    output_text.see(tk.END)
    output_text.configure(state="disabled")


def run_search_thread(arg):
    parts = arg.strip().split(maxsplit=1)

    key = parts[0].lstrip("-").lower()

    if key not in ARG_MAP:
        append_text(f"Argument '{parts[0]}' not allowed\n")
        return
    flag = ARG_MAP[key]
    search = parts[1] if len(parts) > 1 else ""

    cmd = [SEARCH_SCRIPT, flag]

    if search:
        cmd.append(search)
    try:
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        for line in process.stdout:
            append_text(line)
        for line in process.stderr:
            append_text(f" --- ERRORS ---\n{line}")
    except Exception as e:
        append_text(f"Exception: {e}\n")


def run_search(event=None):
    arg = entry.get().strip()
    if not arg:
        output_text.configure(state="normal")
        output_text.delete(1.0, tk.END)
        output_text.insert(
            tk.END, "Please enter a Valid argument press the help button for more options\n"
        )
        output_text.configure(state="disabled")
        return
    output_text.configure(state="normal")
    output_text.delete(1.0, tk.END)
    output_text.configure(state="disabled")
    threading.Thread(target=run_search_thread, args=(arg,), daemon=True).start()


def run_help():
    threading.Thread(target=run_search_thread, args=("--help",), daemon=True).start()


# GUI setup
root = tk.Tk()
root.title("Show Me Everything")

tk.Label(root, text="Argument:").pack(padx=5, pady=5)
entry = tk.Entry(root, width=50)
entry.pack(padx=5, pady=5)
entry.bind("<Return>", run_search)
help_text = tk.Label(root, text="For a list of builtin flags press [Help].", fg="blue")
help_text.pack(padx=5, pady=5)

run_button = tk.Button(root, text="Search", command=run_search)
run_button.pack(padx=5, pady=5)
help_button = tk.Button(root, text="Help", command=run_help)
help_button.pack(padx=5, pady=5)

output_text = scrolledtext.ScrolledText(root, width=100, height=30)
output_text.pack(padx=5, pady=5)

root.mainloop()
