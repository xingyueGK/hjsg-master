#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/5 11:13
# @Author  : xingyue
# @File    : scramble.py

#scramble 古迹争夺

from task.base import SaoDangFb
import threading
import os,time
import redis
import hashlib

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
_redis = redis.StrictRedis(connection_pool=pool)
lock = threading.RLock()

class task(SaoDangFb):
    def index(self):
        index = self.action(c='scramble',m='index')
        # signId = hex_md5(hex_md5(xGame.token) + hex_md5(B.serverid) + hex_md5(B.uid) + B.authkey)
        signId = hashlib.md5(hashlib.md5(self.token).hexdigest()+hashlib.md5(str(index['serverid'])).hexdigest()+hashlib.md5(str(index['uid'])).hexdigest()+hashlib.md5(index['authkey']).hexdigest()).hexdigest()
        return index,signId
    def enter(self):
        A,signId = self.index()
        self.p(A)
        formdata = {
            "diy" :0 ,
            "serverid" :  A['serverid'],
            "uid" : A['uid'] ,
            "sign" : signId
        }
        self.action(c='scramble',m='enter',body=formdata)
    def move(self):
        formdata = {
            "cid" :5 ,
            "clear_cd" : 0,
        }
        self.action(c='scramble',m='move',body=formdata)
if __name__ == '__main__':
    def act(user, apass, addr):
        action = task(user, apass, addr)
        action.enter()
        action.move()
    filepath = os.path.dirname(os.path.abspath(__file__))
    #cont = ['21user.txt', 'autouser.txt','gmnewyear.txt', 'user.txt', 'alluser.txt']
    cont = ['scramble.txt']
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