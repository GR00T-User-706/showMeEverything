import os
import socket
from datetime import datetime
from pathlib import Path

SME_SIGNATURE = "gr00t-user-706"
VERSION_FILE = Path(__file__).resolve().parents[1] / "VERSION"
SME_VERSION = VERSION_FILE.read_text(encoding="utf-8").strip()

PIPE_MODE = False
COLOR_MODE = True
REGEX = True
SORT_MODE = False
EXCLUDE_DOTFILES = False
INCLUDE_MOUNTS = False
CURRENT_SHELL = os.path.basename(os.environ.get("SHELL", "")) or "sh"


def terminal_info():
    return "{} {} {} {}".format(
        datetime.now().strftime("%c"),
        os.environ.get("SHELL", ""),
        os.environ.get("USER", ""),
        socket.gethostname(),
    )
