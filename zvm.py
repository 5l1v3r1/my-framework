#!usr/bin/python
# encoding: utf-8
"""
coded by zevtyardt @ 18:23:21 /2019-02-16/
"""

from core import interpreter

if __name__ == '__main__':
    try:
        interpreter.run()
    except KeyboardInterrupt:
        print ('') # new line
        logger.error('interrupt by user.. exiting')
    except Exception as e:
        logger.critical(str(e))
