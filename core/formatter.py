from . import build_exec
import configparser
import os
import re

def listing_files(startpath):
    files = []
    for dirpath, dirs, file in os.walk(startpath):
        for i in file:
            x = os.path.join(dirpath, i)[8:-3]
            if '__pycache__' not in x:
                files.append(x)
    return files

conf = configparser.ConfigParser()
conf.read('conf.ini')

class Formatter(object):
    def modules(self, body, head=None):
        if not head:
            head = ('num', 'module', 'description')
        head_lenght = [len(i) for i in head]
        body_lenght = max([len(i) for i in body])

        len_num = len(str(len(body))) + 1
        F = '   {0:>%s}   {1:<%s}   {2}' % (
                          head_lenght[0] if len_num <= head_lenght[0] else len_num,
                          head_lenght[1] if body_lenght <= head_lenght[1] else body_lenght)

        print ('\n' + F.replace('>', '^').format(*head))
        print (F.format('=' * int(re.findall(r'{0:>(.*?)}', F)[0]), *['=' * len(i) for i in head][1:]))
        for num, name in enumerate(body, start=1):
            desc = re.findall(r'# desc: (.*?)\n', open('modules/{}.py'.format(name)).read())
            if not desc:
                desc = ['no file description added']

            print (F.format('{}.'.format(num), name, desc[0]))
        print ('')

    def help(self, **kwargs):
        lenght = max([len(i) for i in kwargs] + [7])
        F = '   {0:<%s}   {1}' % lenght

        print ('\n' + \
               F.format('option', 'description') + '\n' + \
               F.format('======', '==========='))
        for i in kwargs:
            print (F.format(i, kwargs[i]))
        print ('') # new line

    def option(self, default, name):
        lenght = [ max([len(i) for i in default] + [5]),
                   max([len(str(default[i])) for i in default] + [5])]
        if lenght[1] >= 23:
            lenght[1] = 23

        F = '   {0:<%s}   {1:<%s}   {2}' % (lenght[0], lenght[1])

        print ('\n' + \
               F.format('param', 'value', 'description') + '\n' + \
               F.format('=====', '=====', '==========='))

        for i in default:
            value = str(default[i]).replace('None', '')
            desc = conf.get('description', i) if conf.has_option('description', i) else 'no description added'

            print (F.format(i,
                   value if len(value) < 23 else '{}..'.format(value[:21]),
                   desc))
        print ('')