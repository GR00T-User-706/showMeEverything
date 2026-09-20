from .environment import search_environment as _search_environment
from .shell_variables import search_shell_variables


def search_environment(pattern=""):
    yield from _search_environment(pattern)
    yield from search_shell_variables(pattern)


__all__ = ["search_environment", "search_shell_variables"]
