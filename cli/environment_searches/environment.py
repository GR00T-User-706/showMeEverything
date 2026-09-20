import os
import re
import subprocess
from pathlib import Path

from ..output.filtering import matches

_ENV_NAME = re.compile(r"\b[A-Z][A-Z0-9_]{2,}\b")
_ASSIGNMENT = re.compile(r"\b(export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*(?:=|:)")

SYSTEM_ENV_FILES = (
    "/etc/environment",
    "/etc/profile",
    "/etc/bash.bashrc",
    "/etc/zshenv",
    "/etc/zprofile",
    "/etc/zshrc",
    "/etc/profile.d",
    "/etc/environment.d",
    "/usr/lib/environment.d",
    "/usr/local/lib/environment.d",
    "/run/environment.d",
)


def _emit(name, value, source, pattern):
    line = f"{name}={value} [{source}]"
    if matches(line, pattern):
        yield line


def _current_environment(pattern):
    for name in sorted(os.environ):
        yield from _emit(name, os.environ.get(name, ""), "current environment", pattern)


def _systemd_environment(pattern):
    commands = (["systemctl", "show-environment"], ["systemctl", "--user", "show-environment"])
    for command in commands:
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=False, timeout=2)
        except (OSError, subprocess.TimeoutExpired):
            continue
        if result.returncode != 0:
            continue
        source = " ".join(command)
        for line in result.stdout.splitlines():
            if "=" not in line:
                continue
            name, value = line.split("=", 1)
            yield from _emit(name, value, source, pattern)


def _process_environments(pattern):
    proc = Path("/proc")
    if not proc.is_dir():
        return
    for entry in proc.iterdir():
        if not entry.name.isdigit():
            continue
        environ = entry / "environ"
        try:
            data = environ.read_bytes()
        except (OSError, PermissionError):
            continue
        for item in data.split(b"\0"):
            if b"=" not in item:
                continue
            name, value = item.split(b"=", 1)
            try:
                name = name.decode(errors="replace")
                value = value.decode(errors="replace")
            except Exception:
                continue
            yield from _emit(name, value, f"/proc/{entry.name}/environ", pattern)


def _environment_files(pattern):
    for raw_path in SYSTEM_ENV_FILES:
        path = Path(raw_path)
        paths = sorted(path.glob("*")) if path.is_dir() else ([path] if path.exists() else [])
        for file_path in paths:
            if not file_path.is_file():
                continue
            try:
                text = file_path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for line in text.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                match = _ASSIGNMENT.search(line)
                if not match:
                    continue
                name = match.group(2)
                value = line.split("=", 1)[1].strip() if "=" in line else ""
                yield from _emit(name, value, str(file_path), pattern)


def _application_variables(pattern):
    # Discover documented/configured variable names without executing applications.
    roots = [Path.home() / ".config", Path("/etc"), Path("/usr/share/doc"), Path("/usr/share/man")]
    seen = set()
    for root in roots:
        if not root.exists():
            continue
        try:
            candidates = root.rglob("*")
        except OSError:
            continue
        count = 0
        for path in candidates:
            if count >= 5000:
                break
            if not path.is_file() or path in seen:
                continue
            seen.add(path)
            count += 1
            try:
                if path.stat().st_size > 2 * 1024 * 1024:
                    continue
                text = path.read_text(encoding="utf-8", errors="ignore")
            except (OSError, UnicodeDecodeError):
                continue
            if not re.search(r"(?i)(environment variable|env(?:ironment)?\s+var|export\s+)", text):
                continue
            for name in _ENV_NAME.findall(text):
                yield from _emit(name, "<defined/documented>", str(path), pattern)


def search_environment(pattern=""):
    seen = set()
    sources = (
        _current_environment(pattern),
        _systemd_environment(pattern),
        _process_environments(pattern),
        _environment_files(pattern),
        _application_variables(pattern),
    )
    for source in sources:
        for line in source:
            key = line
            if key in seen:
                continue
            seen.add(key)
            yield line
