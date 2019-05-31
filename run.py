#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/21 11:15
# @Author  : xingyue
# @File    : run.py

#运行方法

import threading
import os,time

from task.base import  SaoDangFb
from task.talent import  Talent


class run(SaoDangFb,Talent):
    pass

if __name__ == '__main__':
    def act(user, apass, addr):
        action = run(user, apass, addr)
        action.talent_action(3)
    filepath = os.path.dirname(os.path.abspath(__file__))
    # cont = ['21user.txt', 'autouser.txt','gmnewyear.txt', 'user.txt', 'alluser.txt']
    cont = ['rush.txt']
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
                    time.sleep(0.2)
