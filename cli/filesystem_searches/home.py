import os

from .. import config
from ..output.filtering import filter_results


def search_home_directory(pattern=""):
    """Search HOME while respecting hidden-dir and mount traversal options."""
    home = os.path.expanduser("~")
    home_device = os.stat(home).st_dev

    for root, dirs, files in os.walk(home, topdown=True, followlinks=False):
        dirs[:] = [
            name for name in dirs
            if name != ".cache"
            and not (config.EXCLUDE_DOTFILES and name.startswith("."))
        ]

        if not config.INCLUDE_MOUNTS:
            dirs[:] = [
                name for name in dirs
                if _same_device(os.path.join(root, name), home_device)
            ]

        for name in files:
            if config.EXCLUDE_DOTFILES and name.startswith("."):
                continue
            path = os.path.join(root, name)
            if not config.INCLUDE_MOUNTS and not _same_device(path, home_device):
                continue
            yield from filter_results([path], pattern)


def _same_device(path, device):
    try:
        return os.stat(path, follow_symlinks=False).st_dev == device
    except OSError:
        return False
