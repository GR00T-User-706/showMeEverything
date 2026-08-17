#!/usr/bin/env python
import os
import sys
import re
import argparse
import subprocess

# ============================================================
# SME IDENTIFICATION
# ============================================================

SME_SIGNATURE = "gr00t-user-706"
SME_VERSION = "v2.1.1"


# ============================================================
# TERMINAL COLORS
# ============================================================

RED = "\033[31m"
GRN = "\033[32m"
YLW = "\033[33m"
BLU = "\033[34m"
NC = "\033[0m"


# ============================================================
# GLOBAL CONFIG DEFAULT STATE
#
# PIPE_MODE=0 COLOR_MODE=1 -> human readable ANSI output
# PIPE_MODE=1 COLOR_MODE=0 -> machine parseable output
# ============================================================

PIPE_MODE = False
COLOR_MODE = True
HEADER = True
FOOTER = True
REGEX = True


# ============================================================
# SHELL DETECTION
# ============================================================

SHELL = os.environ.get("SHELL", "")
current_shell = os.path.basename(SHELL)


# ============================================================
# COMMON EXCLUDE RULES
# ============================================================

EXCLUDES = [
    ("not", "path", "*/.cache/*"),
]


# ============================================================
# COMMON SEARCH ENGINE
# ============================================================

def sme_search(items, pattern=""):
    """
    Search an iterable of strings.

    Empty pattern:
        matches everything.

    REGEX=True:
        case-insensitive regular expression matching.

    REGEX=False:
        case-insensitive literal substring matching.

    Returns:
        A list of matching strings.
    """

    if not pattern:
        return list(items)

    if REGEX:
        try:
            matcher = re.compile(pattern, re.IGNORECASE)
        except re.error as exc:
            raise ValueError(
                f"Invalid regular expression: {exc}"
            ) from exc

        return [
            item for item in items
            if matcher.search(item)
        ]

    pattern = pattern.casefold()

    return [
        item for item in items
        if pattern in item.casefold()
    ]


# ============================================================
# SHELL BUILTINS
# ============================================================

def search_shell_builtins(pattern=""):
    if current_shell == "zsh":
        shell_command = [
            SHELL,
            "-ic",
            "print -l ${(k)builtins}",
        ]

    elif current_shell == "bash":
        shell_command = [
            SHELL,
            "-ic",
            "compgen -b",
        ]

    else:
        raise RuntimeError(
            f"Unsupported shell for builtin search: {current_shell}"
        )

    result = subprocess.run(
        shell_command,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Unable to query {current_shell}: "
            f"{result.stderr.strip()}"
        )

    builtin_names = sorted({
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    })

    return sme_search(builtin_names, pattern)


# ============================================================
# SHELL FUNCTIONS
# ============================================================

def search_shell_functions(pattern=""):
    if current_shell == "zsh":
        shell_command = [
            SHELL,
            "-ic",
            "print -l ${(k)functions}",
        ]

    elif current_shell == "bash":
        shell_command = [
            SHELL,
            "-ic",
            "compgen -A function",
        ]

    else:
        raise RuntimeError(
            f"Unsupported shell for function search: {current_shell}"
        )

    result = subprocess.run(
        shell_command,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Unable to query {current_shell}: "
            f"{result.stderr.strip()}"
        )

    function_names = sorted({
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    })

    return sme_search(function_names, pattern)


# ============================================================
# SHELL ALIASES
# ============================================================

def search_aliases(pattern=""):
    shell_command = [
        SHELL,
        "-ic",
        "alias",
    ]

    result = subprocess.run(
        shell_command,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Unable to query {current_shell}: "
            f"{result.stderr.strip()}"
        )

    alias_names = sorted({
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    })

    return sme_search(alias_names, pattern)


# ============================================================
# LOADED SHELL COMMANDS
# ============================================================

def search_loaded_commands(pattern=""):
    """
    Search commands known to the user's shell.

    pattern:
        empty string -> return all known commands
        non-empty -> case-insensitive regex search

    returns:
        a sorted list of matching command names
    """

    if current_shell == "zsh":
        shell_command = [
            SHELL,
            "-ic",
            "print -l ${(k)commands}",
        ]

    elif current_shell == "bash":
        shell_command = [
            SHELL,
            "-ic",
            "compgen -c",
        ]

    else:
        command_names = set()

        for directory in os.environ.get("PATH", "").split(os.pathsep):
            if not directory:
                directory = "."

            try:
                for entry in os.scandir(directory):
                    if entry.is_file() and os.access(entry.path, os.X_OK):
                        command_names.add(entry.name)
            except (OSError, PermissionError):
                continue

        command_names = sorted(command_names)

        return sme_search(command_names, pattern)

    result = subprocess.run(
        shell_command,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Unable to query {current_shell}: "
            f"{result.stderr.strip()}"
        )

    command_names = sorted({
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    })

    return sme_search(command_names, pattern)


# ============================================================
# PATH SEARCH
# ============================================================

def search_path(pattern=""):
    """
    Search files inside directories listed in PATH.
    """

    path_files = []

    for directory in os.environ.get("PATH", "").split(os.pathsep):
        if not os.path.isdir(directory):
            continue

        for root, dirs, files in os.walk(directory):
            dirs[:] = [
                directory_name
                for directory_name in dirs
                if directory_name != ".cache"
            ]

            for filename in files:
                path_files.append(
                    os.path.join(root, filename)
                )

    return sme_search(path_files, pattern)


# ============================================================
# COMMAND LINE ARGUMENTS
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="smecli",
        description="Show Me Everything Search Tool",
        allow_abbrev=False,
    )

    parser.add_argument(
        "--commands",
        action="store_true",
        help="Search commands known to the current shell",
    )

    parser.add_argument(
        "--path",
        action="store_true",
        help="Search files in PATH directories",
    )

    parser.add_argument(
        "--builtins",
        action="store_true",
        help="Search shell builtins",
    )

    parser.add_argument(
        "--aliases",
        action="store_true",
        help="Search known aliases",
    )

    parser.add_argument(
        "--functions",
        action="store_true",
        help="Search shell functions",
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Search all currently implemented domains",
    )

    parser.add_argument(
        "pattern",
        nargs="*",
        help="Search pattern",
    )

    args = parser.parse_args()

    pattern = " ".join(args.pattern)

    if args.commands:
        results = search_loaded_commands(pattern)
        print("\n".join(results))

    if args.path:
        results = search_path(pattern)
        print("\n".join(results))

    if args.builtins:
        results = search_shell_builtins(pattern)
        print("\n".join(results))

    if args.functions:
        results = search_shell_functions(pattern)
        print("\n".join(results))

    if args.aliases:
        results = search_aliases(pattern)
        print("\n".join(results))

    if args.all:
        results = []

        results.extend(search_loaded_commands(pattern))
        results.extend(search_path(pattern))
        results.extend(search_shell_builtins(pattern))
        results.extend(search_shell_functions(pattern))
        results.extend(search_aliases(pattern))

        print("\n".join(results))