#!/usr/bin/env python3
import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import shutil


SEARCH_SCRIPT = shutil.which("showMeEverything")
if not SEARCH_SCRIPT:
    SEARCH_SCRIPT = "/usr/local/bin/showMeEverything"  # fallback

# Allowed arguments (example: only some flags)
ALLOWED_ARGS = [
    "--all",
    "-A",
    "--aliases",
    "-a",
    "--builtins",
    "-B",
    "--command",
    "-c",
    "--files",
    "-F",
    "--functions",
    "-f",
    "--help",
    "-h",
    "--home",
    "-H",
    "--installed",
    "-i",
    "--manpages",
    "--man",
    "--modules",
    "-m",
    "--not-installed",
    "-n",
    "--process",
    "-x",
    "--packages",
    "-p",
    "--pkg",
    "--path",
    "-P",
    "--systemd",
    "-s",
    "--system",
    "-R",
]
ARG_MAP = {arg.lstrip("-").lower(): arg for arg in ALLOWED_ARGS}


def append_text(line):
    output_text.configure(state="normal")
    output_text.insert(tk.END, line)
    output_text.see(tk.END)
    output_text.configure(state="disabled")


def run_search_thread(arg):
    parts = arg.split()
    if parts[0] not in ALLOWED_ARGS:
        append_text(f"Argument '{parts[0]}' not allowed\n")
        return

    cmd = [SEARCH_SCRIPT] + parts
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
            tk.END, "Please enter a Valid argument try [--help] for options\n"
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
