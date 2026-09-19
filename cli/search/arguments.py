from types import SimpleNamespace

FLAGS={'--ALL':'all_aggressive','-A':'all_aggressive','--all':'all','--aliases':'aliases','-a':'aliases','--bin':'bin','--boot':'boot','-B':'boot','--builtins':'builtins','-b':'builtins','--command':'command','-c':'command','--etc':'etc','-E':'etc','--files':'files','-F':'files','--functions':'functions','-f':'functions','--home':'home','-H':'home','--installed':'installed','-i':'installed','--lib':'lib','-L':'lib','--manpages':'manpages','--man':'manpages','-M':'manpages','--modules':'modules','-m':'modules','--not-installed':'not_installed','-n':'not_installed','--process':'process','-x':'process','--packages':'packages','-p':'packages','--pkg':'packages','--path':'path','-P':'path','--sbin':'sbin','--systemd':'systemd','-s':'systemd','--system':'system','-R':'system','--usr':'usr','-U':'usr','--var':'var','-V':'var','--opt':'opt','-O':'opt'}
MODIFIERS={'--less':'less','--sort':'sort','--pipe':'pipe','--glob':'glob','--excludeDotFiles':'exclude_dotfiles','--nodot':'exclude_dotfiles'}

def parse_arguments(argv):
    values={k:False for k in set(FLAGS.values())}
    values.update({k:False for k in ('help','version','less','sort','pipe','glob','exclude_dotfiles')})
    terms=[]; stop=False
    for arg in argv:
        if stop:
            terms.append(arg); continue
        if arg=='--':
            stop=True; continue
        if arg in ('-h','--help'):
            values['help']=True; continue
        if arg in ('-v','--version'):
            values['version']=True; continue
        if arg in FLAGS:
            values[FLAGS[arg]]=True; continue
        if arg in MODIFIERS:
            values[MODIFIERS[arg]]=True; continue
        terms.append(arg)
    return SimpleNamespace(**values,search_terms=terms), []
