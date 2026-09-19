from .. import config
from .header import header

def footer():
    if not config.PIPE_MODE: header(config.terminal_info())
