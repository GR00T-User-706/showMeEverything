import os
import re
from pathlib import Path

from ..output.filtering import matches

_ASSIGNMENT = re.compile(
    r"^(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*(?:\+?=)\s*(.*)$"
)

STARTUP_FILES = (
    "~/.zshenv",
    "~/.zprofile",
    "~/.zshrc",
    "~/.zlogin",
    "~/.bash_profile",
    "~/.bash_login",
    "~/.bashrc",
    "~/.profile",
)


def _startup_files():
    for raw in STARTUP_FILES:
        path = Path(raw).expanduser()
        if path.is_file():
            yield path


def _shell_variables_from_file(path, pattern):
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return
    for number, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = _ASSIGNMENT.match(line)
        if not match:
            continue
        name, value = match.groups()
        exported = line.startswith("export ")
        state = "exported" if exported else "shell variable"
        result = f"{name}={value} [{state}; {path}:{number}]"
        if matches(result, pattern):
            yield result


def search_shell_variables(pattern=""):
    seen = set()

    # Python cannot inspect the parent shell's private, non-exported variables.
    # It can reliably report variables discoverable from shell startup files.
    for path in _startup_files():
        for result in _shell_variables_from_file(path, pattern):
            if result not in seen:
                seen.add(result)
                yield result

    # Include the environment inherited by this CLI, while identifying it as exported.
    for name in sorted(os.environ):
        result = f"{name}={os.environ.get(name, '')} [exported; inherited]"
        if matches(result, pattern) and result not in seen:
            seen.add(result)
            yield result
