import re

def Build(file):
    file = open(file).read()
    base = re.findall(r'def __zvm__\((.*?)\)', file)[-1]
    log = False

    if base.endswith(', logging'):
        base = base[:-9]
        log = True

    if base.endswith(',logging'):
        base = base[:-8]
        log = True

    final = [i if not i.startswith(' ') else i[1:] for i in base.split(',')]
    try:
        return {i: arg.__dict__[i] for i in final}, log
    except NameError:
        return {i: None for i in final}, log
