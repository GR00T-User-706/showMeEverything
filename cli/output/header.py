from .. import config

def header(info):
    if config.PIPE_MODE: return
    print('#=========================================================#')
    print(info)
    print('#=========================================================#')
