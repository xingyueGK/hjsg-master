#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/5 14:49
# @Author  : xingyue
# @File    : arena.py

#每周晚自动pk top榜

from task.base import SaoDangFb
import threading
import os,time
import redis
import hashlib

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
_redis = redis.StrictRedis(connection_pool=pool)
lock = threading.RLock()

class task(SaoDangFb):
    rank = 0
    def index(self):
        index = self.action(c='arena',m='index')
        global rank
        rank = index['log']['rank']
        return index
    def pk(self,t):
        reult = self.action(c='arena',m='action',t=t)
        if reult['status'] != 1:
            exit(3)
        return reult
    def autoPk(self):
        global rank
        data = self.index()
        times = int(data['log']['times'])
        for i in range(times):
            data = self.index()
            for k,v in data['list'].items():
                t = v['uid']
                result = self.pk(t)
                if result['info']['win'] >0:
                    rank = data['log']['rank']
                    print 'PK 胜利，排名',rank
                    break

if __name__ == '__main__':
    def act(user, apass, addr):
        action = task(user, apass, addr)
        action.autoPk()
        print action.rank
    filepath = os.path.dirname(os.path.abspath(__file__))
    # cont = ['21user.txt', 'autouser.txt','gmnewyear.txt', 'user.txt', 'alluser.txt']
    cont = ['user.txt','21user.txt','gmhai']
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