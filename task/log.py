#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/10 11:33
# @Author  : xingyue
# @File    : log.py

import logging

# 通过下面的方式进行简单配置输出方式与日志级别
logging.basicConfig(filename='logger.log', level=logging.INFO)

logging.debug('debug message')
logging.info('info message')
logging.warn('warn message')
logging.error('error message')
logging.critical('critical message')

logger = logging.getLogger('logger_name')