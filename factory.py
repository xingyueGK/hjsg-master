#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/26 16:09
# @Author  : xingyue
# @File    : factoy.py

from task.base import SaoDangFb
import time, threading
import os, json
from Queue import  Queue

class task(SaoDangFb):
    def workshop(self):  # 玉石收集
        # 收取
        print '玉石收集'
        for i in range(1, 10):
            try:
                self.action(c='workshop', m='get_reward', s=i)
            except Exception as e:
                print e

    def exploit_tree(self):  # 木材收集
        print '木材收集'
        try:
            # exploit_stone，m:{gather收集,action，采集}site:1,第一个框,有三个
            index = self.action(c='exploit_tree', m='index')
            for item in index['list']:
                if item['cd'] == 0 :
                    task.p(self.action(c='exploit_tree', m='gather', site=item['site']))
                    print self.action(c='exploit_tree', m='action', site=item['site'])
                elif item['cd'] <100:
                    time.sleep(item['cd']+4)
                    task.p(self.action(c='exploit_tree', m='gather', site=item['site']))
                    task.p(self.action(c='exploit_tree', m='action', site=item['site']))
                else:
                    print '需要',item['cd']
        except Exception as e:
            print e

    def exploit_stone(self):  # 石头收集
        print '石头收集'
        try:
            # exploit_stone，m:{gather收集,action，采集}site:1,第一个框,有三个
            index = self.action(c='exploit_stone', m='index')
            for item in index['list']:
                if item['cd'] == 0 :
                    task.p(self.action(c='exploit_stone', m='gather', site=item['site']))
                    print self.action(c='exploit_stone', m='action', site=item['site'])
                elif item['cd'] <100:
                    time.sleep(item['cd']+4)
                    task.p(self.action(c='exploit_stone', m='gather', site=item['site']))
                    task.p(self.action(c='exploit_stone', m='action', site=item['site']))
                else:
                    print '需要',item['cd']
        except Exception as e:
            print e

def run(user, apass, addr):
    action = task(user, apass, addr)
    action.workshop()
    action.exploit_stone()
    action.exploit_tree()
if __name__ == '__main__':
    q = Queue()
    filepath = os.path.dirname(os.path.abspath(__file__))
    # cont = ['autouser.txt', 'user.txt','alluser.txt', 'duguyi.txt', '149cnm.txt', '149dgj.txt', '149gx1.txt', '149xx.txt',
    #         '149xb.txt', '149lwzs.txt','21user.txt','150.txt','150nm.txt','150num.txt']
    cont = ['factory.txt']
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
            except Exception as e:
                print e
        for i in thread:
            i.start()
        for i in thread:
            i.join()