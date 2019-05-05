#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/29 14:43
# @Author  : xingyue
# @File    : haiyun.py

#防止被判断脚本 自动调度刷船函数，打劫次数


import redis

from celery import Celery


broker = 'redis://127.0.0.1:6379/7'
backend = 'redis://127.0.0.1:6379/8'

app = Celery('haiyun',broker=broker,backend=backend)

@app.task
def add(x,y):
    return x,y

