#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 14:36
# @Author  : xingyue
# @File    : sign.py

from task.base import SaoDangFb
import threading
import os,redis
from Queue import Queue

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
_redis = redis.StrictRedis(connection_pool=pool)

class qiandao(SaoDangFb):
    def sign(self):  # 够买签到声望
        index = self.action(c='sign', m='sign_index')
        shop = self.action(c='sign', m='sale_shop')
        for i in shop['reward']:
            self.action(c='sign', m='get_reward', type=2, id=i['id'])
def run(user, apass, addr,lockpwd):
    action = qiandao(user, apass, addr)
    action.unlock(lockpwd)
    action.sign()
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
                    try:
                        lockpwd = i.split()[3]
                    except:
                        lockpwd = None
                    t1 = threading.Thread(target=run, args=(name, passwd, addr,lockpwd))
                    q.put(t1)
    while not q.empty():
        print q.qsize()
        thread = []
        for i in xrange(10):
            try:
                thread.append(q.get_nowait())
            except:
                pass
        for i in thread:
            i.start()
        for i in thread:
            i.join()
