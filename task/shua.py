#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/10 19:07
# @Author  : xingyue
# @File    : shua.py


import threading
import os, time


from task.base import SaoDangFb


class duanwu(SaoDangFb):
    '龙舟比赛'

    def longzhou(self, id):
        self.action(c='dragon_boat', m='meter_reward', id=id)


if __name__ == '__main__':
    s1 = threading.Semaphore(3)


    def act(user, apass, addr):
        s1.acquire()
        action = duanwu(user, apass, addr)
        action.longzhou()
        s1.release()


    filepath = os.path.dirname(os.path.abspath(__file__))
    # cont = ['21user.txt', 'autouser.txt','gmnewyear.txt', 'user.txt', 'alluser.txt']
    cont = ['qingbing.txt']
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
