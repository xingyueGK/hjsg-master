#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/20 10:56
# @Author  : xingyue
# @File    : steadily.py

from task.base import SaoDangFb
import time, threading
import os, json
from Queue import  Queue

class task(SaoDangFb):
    def act_steadily(self):  # 节节高
        print '节节高'
        try:
            info = self.action(c='act_steadily', m='index')
            status = info['status']
            reward_cd = info['reward_cd']
            t = info['reward']['time']
            if reward_cd == 0 and status == 1:
                self.action(c='act_steadily', m='get_online_reward', t=t)
            elif reward_cd == 0 and status != 1:
                exit(2)
            else:
                print '%s分钟后领取,%s' % (reward_cd / 60, reward_cd)
                time.sleep(reward_cd + 1)
                self.action(c='act_steadily', m='get_online_reward', t=t)
            return True
        except:
            return False
def run(user, apass, addr):
    action = task(user, apass, addr)
    action = action.act_steadily()
if __name__ == '__main__':
    q = Queue()
    filepath = os.path.dirname(os.path.abspath(__file__))
    cont = ['autouser.txt', 'user.txt','alluser.txt', 'duguyi.txt','21user.txt']
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
        for i in xrange(200):
            try:
                thread.append(q.get_nowait())
            except:
                pass
        for i in thread:
            i.start()
        for i in thread:
            i.join()
