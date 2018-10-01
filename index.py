#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/29 11:37
# @Author  : xingyue
# @File    : index.py

#返回各种消息的首页

from task.base import SaoDangFb
import time, threading
import os, json
from Queue import  Queue

class task(SaoDangFb):
    def springshop(self):
        return self.action(c='springshop',m='index')


result = task('zhaoyue123a',413728161,150)

