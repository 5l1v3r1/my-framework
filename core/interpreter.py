from . import formatter
from . import build_exec
import sys
import re
import logging
import colorlog
import readline

f = formatter.Formatter()

def setup_logger():
    """Return a logger with a default ColoredFormatter."""
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s[+] %(reset)s%(message)s",
        log_colors={
            'DEBUG':    'green',
            'INFO':     'blue',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'bold_red',
        }
    )

    logger = logging.getLogger('example')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger

class run(object):
    # <-- basic -->
    def _author(self):
        cnt = open('modules/{}.py'.format(self.name)).read()
        return re.findall('# author: (.*?)\n', cnt)

    def _get_default(self):
        # <-- get parameter and value -->
        default, self.log = build_exec.Build('modules/{}.py'.format(self.name))
        temp = dict(re.findall(r'(?i):> (.*?): (.*?)\n',
                open('modules/{}.py'.format(self.name)).read()))

        # <-- check again -->
        if temp:
            for value in temp:
                if value in list(default.keys()):
                    default[value] = temp[value]

        if 'logging' in list(default.keys()):
            default['logging'] = self.logger

        # <-- returning data -->
        return default

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
        f.option(self.default, self.name, self.logger)

    # <-- check -->
    def _check_parameter(self, default):
        if len(default.keys()) == 1 and list(default.keys())[0] == '' or 'None' not in [str(self.default[i]) for i in self.default]:
            return True

    # <-- load -->
    def _load_module(self):
        # <-- data -->
        author_name = self._author()
        self.default = self._get_default()
        subcommand = {'help': self._print_sub_help,
                      'show': self._print_options }
        mod = self.name.split('/')

        text_text = 'load scripts from modules/{}.py'.format(self.name)
        if author_name:
            text_text += ' | author: {}'.format(author_name[0])

        self.logger.info(text_text)

        # <-- shell -->
        if len(mod) >= 2:
            text = '{0} {1}(\x1b[31m{2}\x1b[0m) >> '.format(
                         self.codename, '.'.join(mod[0:-1]), mod[-1])
        else:
            text = '{0} general(\x1b[31m{1}\x1b[0m) >> '.format(self.codename, self.name)

        while True:
            inp = input(text)
            set_ = inp.split()

            if inp in subcommand:
                subcommand[inp]()

            elif ' '.join(set_[:2]) in ['set {}'.format(i) for i in self.default]:
                if len(set_) >= 3:
                    if set_[1] != 'logging':
                        new_value = ' '.join(set_[2:])
                        self.default[set_[1]] = new_value
                        self.logger.info('%s => %s', set_[1], new_value)
                    else:
                        self.logger.warning('can\'t change built-in Object')

            elif inp == 'run':
                if self._check_parameter(self.default):
                    self.logger.info('executing script')

                    # first ( reinitializing ) <-- generating script -->
                    if len(mod) >= 2:
                        imp = 'from modules.{0} import {1}; {1}.__init__('.format(
                             '.'.join(mod[0:-1]), mod[-1])
                    else:
                        imp = 'from modules import {0}; {0}.__init__('.format(mod[0])


                    # <-- generating script -->
                    imp += ', '.join(['{0}="{1}"'.format(i, self.default[i]) for i in self.default])
                    if self.log:
                        imp += ', logging=self.logger'
                    imp += ')'

                    # debugging <-- generating script -->
                    imp = imp.replace('(="None")', '()')
                    imp = imp.replace('"<Logger example (INFO)>"', 'self.logger') # built-in

                    # finnaly <-- executing script -->
                    try:
                        exec (imp)
                    except Exception as e:
                        self.logger.critical(str(e))

                else:
                    for i in self.default:
                        if str(self.default[i]) == 'None':
                            self.logger.error('%s: parameter can\'t be empty', i); break

            elif inp == 'back':
                break

    def __init__(self, cde='zvm'):
        self.codename = cde
        self.logger = setup_logger()
        self.modules = formatter.listing_files('modules')
        if not self.modules:
            self.logger.warning('module not found !!')
            sys.exit(self.logger.info("tips: create a 'modules' folder and add a new module there"))

        self.zerodiv = ['use {}'.format(ex) for ex in self.modules]
        self.command = {'help': self._print_help,
                        'modules': self._print_modules,
                        'exit': exit}

        try:
            self.logger.info('run as interactive shell, type help for more information!')
            self.logger.info('follow me: https://m.facebook.com/zvtyrdt.id')
            while True:
                inp = input('{0} >> '.format(self.codename))

                if inp in self.command:
                    self.command[inp]()

                elif inp in self.zerodiv:
                    self.name = inp[4:]
                    self._load_module()
        except KeyboardInterrupt:
            self.logger.error('interrupt by user.. exiting')
        except Exception as e:
            self.logger.critical(str(e))
