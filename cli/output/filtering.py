import re
from .. import config

def matches(value,pattern):
    if not pattern: return True
    if config.REGEX: return re.search(pattern,value,re.IGNORECASE) is not None
    return pattern.casefold() in value.casefold()

def filter_results(items,pattern):
    for item in items:
        if matches(item,pattern): yield item
