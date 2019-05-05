#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/26 16:09
# @Author  : xingyue
# @File    : recruit_followers.py

from task.base import SaoDangFb
import time, threading
import os, json
from Queue import  Queue

class task(SaoDangFb):
    def sign(self):  # 玉石收集
        # 收取
        print '将领签到'
        try:
            for i in range(1,4):
                self.action(c='recruit_followers', m='index')
                formdata = {
                    "p" : i
                }
                self.action(c='recruit_followers', m='sign',body=formdata)
        except Exception as e:
            print e



def run(user, apass, addr):
    action = task(user, apass, addr)
    action.sign()
if __name__ == '__main__':
    q = Queue()
    filepath = os.path.dirname(os.path.abspath(__file__))
    cont = ['21user.txt', 'autouser.txt', 'user.txt','alluser.txt',]
    # cont = ['factory.txt']
    for t in cont:
        with open('%s/users/%s' % (filepath, t), 'r') as f:
            for i in f:
                if i.strip() and not i.startswith('#'):
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    t1 = threading.Thread(target=run, args=(name, passwd, addr))
                    q.put(t1)
    while not q.empty():
        thread = []
        for i in xrange(50):
            try:
                thread.append(q.get_nowait())
            except Exception as e:
                print e
        for i in thread:
            i.start()
        for i in thread:
            i.join()