#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/23 8:42
# @Author  : xingyue
# @File    : glory_front.py
# 运行方法

import threading
import os, time

from task.base import SaoDangFb
from task.glory_front import glory_front


class dongxizhanxian(SaoDangFb, glory_front):
    # '东西战线'
    pass

if __name__ == '__main__':
    s1 = threading.Semaphore(3)
    def act(user, apass, addr):
        s1.acquire()
        action = dongxizhanxian(user, apass, addr)
        if action.level() < 150:
            s1.release()
            return False
        t = action.get_attribute()
        action.zhanxian(t)
        s1.release()
    filepath = os.path.dirname(os.path.abspath(__file__))
    # cont = ['21user.txt', 'autouser.txt','gmnewyear.txt', 'user.txt', 'alluser.txt']
    cont = ['xing.txt']
    for t in cont:
        with open('%s/users/%s' % (filepath, t), 'r') as f:
            for i in f:
                if i.strip() and not i.startswith('#'):
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    # addr = 147
                    t1 = threading.Thread(target=act, args=(name, passwd, addr))
                    t1.start()
