#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/17 15:55
# @Author  : xingyue
# @File    : autochangeGuyu.py

from task.base import SaoDangFb
import time, threading
import os, json
from Queue import  Queue

class task(SaoDangFb):
    def sign(self):  # 够买签到声望
        index = self.action(c='sign', m='sign_index')
        shop = self.action(c='sign', m='sale_shop')
        for i in shop['reward']:
            self.action(c='sign', m='get_reward', type=2, id=i['id'])
    def guyu(self):  # 古玉换银币
        info = self.action(c='actguyu', m='index')
        reputation = int(info['reputation'])
        if info['vip'] == "1":
            if reputation / 220000 >= 2:
                self.action(c='actguyu', m='reward_index ', id=6, num=2)
            elif reputation / 220000 == 1:
                self.action(c='actguyu', m='reward_index ', id=6, num=1)
            info = self.action(c='actguyu', m='index')
            reputation = int(info['reputation'])
            if reputation / 55000 >= 2:
                self.action(c='actguyu', m='reward_index ', id=5, num=2)
            elif reputation / 55000 == 1:
                self.action(c='actguyu', m='reward_index ', id=5, num=1)
            info = self.action(c='actguyu', m='index')
            reputation = int(info['reputation'])
            if reputation / 11000 >= 2:
                self.action(c='actguyu', m='reward_index ', id=4, num=2)
            elif reputation / 11000 == 1:
                self.action(c='actguyu', m='reward_index ', id=4, num=1)
            self.action(c='actguyu', m='reward_index ', id=1, num=2)
            self.action(c='actguyu', m='reward_index ', id=2, num=2)
            self.action(c='actguyu', m='reward_index ', id=3, num=2)
        else:
            self.action(c='actguyu', m='reward_index ', id=1, num=1)
            self.action(c='actguyu', m='reward_index ', id=2, num=1)
            self.action(c='actguyu', m='reward_index ', id=3, num=1)
            self.action(c='actguyu', m='reward_index ', id=6, num=1)
            self.action(c='actguyu', m='reward_index ', id=5, num=1)
            self.action(c='actguyu', m='reward_index ', id=4, num=1)
            self.action(c='actguyu', m='reward_index ', id=7, num=1)
            self.action(c='actguyu', m='reward_index ', id=8, num=1)
            self.action(c='actguyu', m='reward_index ', id=9, num=1)
        # #所有 古玉够买声望
        info = self.action(c='actguyu', m='index')
        num = info['guyu']
        self.action(c='actguyu', m='reward_index', id=34, num=num)
def run(user, apass, addr):
    action = task(user, apass, addr)
    action.sign()
    action.guyu()
if __name__ == '__main__':
    q = Queue()
    filepath = os.path.dirname(os.path.abspath(__file__))
    cont = ['1000share.txt','149cnm.txt', '149dgj.txt', '149gx1.txt', '149xx.txt', '149xb.txt', '149lwzs.txt','150.txt', '150num.txt', '150nm.txt', '150taohua.txt', '150bank.txt']
    for t in cont:
        with open('%s/users/%s' % (filepath, t), 'r') as f:
            for i in f:
                if i.strip():
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
            except:
                pass
        for i in thread:
            i.start()
        for i in thread:
            i.join()