"""Shared package-manager subprocess execution and diagnostics."""
import os
import shlex
import subprocess
from datetime import datetime
from pathlib import Path

def error_log_path():
    override = os.environ.get("SME_ERROR_LOG")
    if override:
        return Path(override).expanduser()
    state_home = os.environ.get("XDG_STATE_HOME")
    if state_home:
        return Path(state_home).expanduser() / "showmeeverything" / "errors.log"
    return Path.home() / ".local" / "state" / "showmeeverything" / "errors.log"

ERRORS_LOGGED = False
ERROR_LOG = None

def run_backend(manager, operation, pattern, command):
    global ERRORS_LOGGED, ERROR_LOG
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        stdout, stderr, status = result.stdout, result.stderr, result.returncode
    except OSError as exc:
        stdout, stderr, status = "", str(exc), 127
    if status != 0 or stderr.strip():
        path = error_log_path()
        entry = (
            f"[{datetime.now().astimezone().isoformat(timespec='seconds')}]\n"
            f"MANAGER: {manager}\nOPERATION: {operation}\nSEARCH_TERM: {pattern}\n"
            f"COMMAND: {shlex.join(command)}\nEXIT_STATUS: {status}\nSTDERR:\n"
            f"{stderr.rstrip()}\n----------------------------------------\n"
        )
        ERRORS_LOGGED = True
        ERROR_LOG = str(path)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as stream:
                stream.write(entry)
        except OSError:
            pass
    return stdout

def diagnostics():
    return ERRORS_LOGGED, ERROR_LOG
