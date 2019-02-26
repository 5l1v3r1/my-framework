#!usr/bin/python
# encoding: utf-8
"""
coded by zevtyardt @ 18:23:21 /2019-02-16/
"""

from core import interpreter
import colorlog
import logging

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

if __name__ == '__main__':
    interpreter.run(setup_logger())
