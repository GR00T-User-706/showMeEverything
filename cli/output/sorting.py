from .. import config

def sort_results(items):
    if not config.SORT_MODE: yield from items; return
    values=list(items); values.sort(key=str.casefold); yield from values
