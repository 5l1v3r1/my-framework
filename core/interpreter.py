from . import formatter
from . import build_exec
import re
import readline

f = formatter.Formatter()

class run(object):
    def _get_default(self, module):
        return (dict(re.findall(r'(?i):> (.*?): (.*?)\n',
              open('modules/{}.py'.format(module)).read())))

    # <-- basic -->
    def _print_modules(self):
        f.modules(self.modules)

    def _print_help(self):
        f.help(help='show this help message',
               modules='list a module',
               use='load script, module name is needed',
               exit='exit the interactive shell')

    # <-- sub -->
    def _print_sub_help(self):
        f.help(help='show this help message',
               show='show options',
               set='set value by name',
               run='executing the module',
               back='back to the previous shell')

    def _print_options(self):
        f.option(self.default, self.name)

    # <-- load -->
    def _load_module(self, name):
        self.default = (self._get_default(name))
        if not self.default:
            self.default = build_exec.Build('modules/{}.py'.format(self.name))[0]

        subcommand = {'help': self._print_sub_help,
                      'show': self._print_options }
        try:
            text = 'zvm {0}(\x1b[31m{1}\x1b[0m) >> '.format(*name.split('/'))
        except IndexError:
            text = 'zvm general(\x1b[31m{0}\x1b[0m) >> '.format(name)

        while True:
            inp = input(text)
            set_ = inp.split()

            if inp in subcommand:
                subcommand[inp]()

            elif ' '.join(set_[:2]) in ['set {}'.format(i) for i in self.default]:
                if len(set_) >= 3:
                    new_value = ' '.join(set_[2:])
                    self.default[set_[1]] = new_value
                    self.logging.info('%s => %s', set_[1], new_value)

            elif inp == 'run':
                if 'None' not in [str(self.default[i]) for i in self.default]:
                    self.logging.info('executing script')

                    # <-- generating script -->
                    mod = self.name.split('/')
                    if len(mod) >= 2:
                        imp = 'from modules.{0} import {1}; {1}.__init__('.format(
                              '.'.join(mod[0:-1]), mod[-1])
                    else:
                        imp = 'from modules import {0}; {0}.__init__('.format(mod[0])

                    # sub <-- generating script -->
                    imp += ', '.join(['{0}="{1}"'.format(i, self.default[i]) for i in self.default])
                    if re.search('def __init__\(.*?, logging\)', open('modules/{}.py'.format(self.name)).read()):
                        imp += ', logging=self.logging'
                    imp += ')'

                    # finnaly <-- executing script -->
                    exec (imp)

                else:
                    for i in self.default:
                        if str(self.default[i]) == 'None':
                            self.logging.error('%s: parameter can\'t be empty', i); break

            elif inp == 'back':
                break

    def __init__(self, logging):
        self.logging = logging
        self.modules = formatter.listing_files('modules')
        self.zerodiv = ['use {}'.format(ex) for ex in self.modules]
        self.command = {'help': self._print_help,
                        'modules': self._print_modules,
                        'exit': exit}

        while True:
            inp = input('zvm >> ')

            if inp in self.command:
                self.command[inp]()

            elif inp in self.zerodiv:
                self.name = inp[4:]
                self.logging.info('load module %s', self.name)
                self._load_module(self.name)
