#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/12 11:54
# @Author  : xingyue
# @File    : logformat.py

#日志文件配置

import  logging

logger = logging.getLogger('my_logger')

logger.setLevel(logging.INFO)


hander = logging.FileHandler('a.log')

hander.setFormatter()