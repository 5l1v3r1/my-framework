import re

def Build(file):
    file = open(file).read()
    base = re.findall(r'__init__\((.*?)\)', file)[0]
    log = False

    if ', logging' in base:
        base = base[:-9]
        log = True

    try:
        return {i: arg.__dict__[i] for i in base.split(', ')}, log
    except NameError:
        return {i: None for i in base.split(', ')}, log
