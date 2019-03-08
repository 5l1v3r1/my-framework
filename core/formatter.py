from . import build_exec
import configparser
import os
import re

# <-- code -->
text_warn = '# add function __zvm__ with one or more parameters\n# example:\n# >>> def __zvm__(param):\n# ...    # do something\n#\n# generated by zvtyrdt.id\n\n'

# <-- listing files -->
def _check(file):
    if os.path.isfile(file):
        cnt = open(file).read()
        return re.search(r'\ndef __zvm__\(.*?\)', cnt)

def _add_warn(file):
    file_content = open(file).read()
    if not re.search(r'generated by zvtyrdt.id', file_content):
        with open(file, 'w') as f:
            f.write(text_warn + file_content)

def listing_files(startpath):
    files = []
    for dirpath, dirs, file in os.walk(startpath):
        for i in file:
            x = os.path.join(dirpath, i)[8:-3]
            if '__pycache__' not in x:
                if _check('modules/{}.py'.format(x)):
                    files.append(x)
                else:
                    _add_warn('modules/{}.py'.format(x))
    return files

# <-- read config -->
conf = configparser.ConfigParser()
conf.read('conf.ini')

class Formatter(object):
    def modules(self, body, head=None):
        F = '  {0:<%s}  {1}' %  max([len(i) for i in body] + [6])
        print ('\n' + F.format('module', 'description') + \
               '\n' + F.format('======', '==========='))
        for name in body:
            desc = re.findall(r'# desc: (.*?)\n', open('modules/{}.py'.format(name)).read())
            if not desc:
                desc = ['no file description added']

            print (F.format(name, desc[0]))
        print ('')

    def help(self, **kwargs):
        lenght = max([len(i) for i in kwargs] + [7])
        F = '  {0:<%s}  {1}' % lenght

        print ('\n' + F.format('option', 'description') + \
               '\n' + F.format('======', '==========='))
        for i in kwargs:
            print (F.format(i, kwargs[i]))
        print ('') # new line

    def option(self, default, name, logging):
        if len(default.keys()) == 1 and list(default.keys())[0] == '':
            logging.warning("not require any parameters, type 'run' to execute module")
        else:
            lenght = [ max([len(i) for i in default] + [5]),
                       max([len(str(default[i])) for i in default] + [5])]
            if lenght[1] >= 25:
                lenght[1] = 25
            F = '  {0:<%s}  {1:<%s}  {2}' % (lenght[0], lenght[1])

            print ('\n' + \
                   F.format('param', 'value', 'description') + '\n' + \
                   F.format('=====', '=====', '==========='))

            for i in default:
                value = str(default[i]).replace('None', '')
                desc = conf.get('description', i) if conf.has_option('description', i) else 'no description added'
                if i == 'logging':
                    desc = 'built-in object'

                print (F.format(i,
                       value if len(value) < 25 else '{}..'.format(value[:23]),
                       desc))
            print ('')
