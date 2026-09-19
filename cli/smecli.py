#!/usr/bin/env python3
import os,sys,shutil,tempfile,termios,tty
from . import config
from .help.help import show_help
from .search.arguments import parse_arguments
from .search.actions import action_names
from .search.search import execute

def pager(path):
    if not(sys.stdin.isatty() and sys.stdout.isatty()):
        with open(path,encoding='utf-8',errors='replace') as f: shutil.copyfileobj(f,sys.stdout)
        return
    rows=max(1,shutil.get_terminal_size((80,24)).lines-1); fd=sys.stdin.fileno(); old=termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        with open(path,encoding='utf-8',errors='replace') as f:
            buf=[]
            while True:
                while len(buf)<rows:
                    line=f.readline()
                    if not line: break
                    buf.append(line.rstrip('\n'))
                if not buf: break
                sys.stdout.write('\x1b[H\x1b[2J'+'\n'.join(buf)+'\n\x1b[7m-- SME pager -- q quit, Space page, Enter line --\x1b[0m'); sys.stdout.flush()
                k=os.read(fd,1)
                if k in (b'q',b'Q'): break
                buf=[] if k==b' ' else buf[1:]
    finally:
        termios.tcsetattr(fd,termios.TCSADRAIN,old); print()

def emit(actions,pattern,use_pager):
    f=tempfile.NamedTemporaryFile('w+',encoding='utf-8',delete=False); path=f.name
    try:
        for name,results in execute(actions,pattern):
            if not config.PIPE_MODE: f.write('#=========================================================#\nSearching '+name+' for '+pattern+'...\n#=========================================================#\n')
            for result in results: f.write(result+'\n')
        if not config.PIPE_MODE: f.write('#=========================================================#\n'+config.terminal_info()+'\n#=========================================================#\n')
        f.close()
        if use_pager: pager(path)
        else:
            with open(path,encoding='utf-8') as out: shutil.copyfileobj(out,sys.stdout)
    finally:
        try: os.unlink(path)
        except OSError: pass

def main(argv=None):
    argv=list(sys.argv[1:] if argv is None else argv); args,unknown=parse_arguments(argv)
    if args.help: show_help(); return 0
    if args.version:
        print('SME_VERSION: '+config.SME_VERSION); print('SME_SIGNATURE: '+config.SME_SIGNATURE); return 0
    broad={'--ALL','-A','--all','--system','-R'}
    if sum(x in argv for x in broad)>1:
        print('WARNING: conflicting flags detected: ALL|all|system are mutually exclusive.'); return 1
    actions=action_names(argv)
    if not actions:
        print('smecli: No search flags given'); print('smecli: for more information try [smecli --help]'); return 1
    config.PIPE_MODE=args.pipe; config.COLOR_MODE=not args.pipe; config.REGEX=not args.glob; config.SORT_MODE=args.sort; config.EXCLUDE_DOTFILES=args.exclude_dotfiles
    terms=argv[argv.index('--')+1:] if '--' in argv else list(args.search_terms)+list(unknown)
    try: emit(actions,' '.join(terms),args.less)
    except BrokenPipeError: return 0
    except Exception as exc: print('smecli: '+str(exc),file=sys.stderr); return 1
    return 0

if __name__=='__main__': main()
