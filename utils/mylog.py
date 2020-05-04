#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/19 18:04
# @Author  : xingyue
# @File    : mylog.py

import  os
from logging.handlers import RotatingFileHandler
from logging import  StreamHandler
from apscheduler.util import  undefined

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import logging
class ContextFilter(logging.Filter):

    username = 'USER'
    addr = 'ADDR'

    def filter(self, record):

        record.addr = self.addr
        record.username = self.username
        return True

def my_listener(event):
    if event.exception:
        print('The job crashed :(') # or logger.fatal('The job crashed :(')
    else:
        print('The job worked :)')



def MyLog(logpath=None,logname='mylog.log'):
    """
    :param logpath: dir
    :param logname: str(name)
    :return: logger
    """
    if logpath :
        if  not os.path.exists(logpath):
            os.makedirs(logpath)
            _log = os.path.join(logpath,logname)
        else:
            _log = os.path.join(logpath,logname)
    else:
        _log = logname

    format = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] [%(username)s:%(addr)s] %(levelname)s %(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(_log,mode='a',maxBytes=1024*1024*1024,backupCount=3,encoding='utf-8')
    handler.setLevel(logging.INFO)
    handler.setFormatter(format)
    logger.addHandler(handler)
    filter = ContextFilter()
    logger.addFilter(filter)
    return logger





