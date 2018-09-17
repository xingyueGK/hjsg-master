#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/17 10:28
# @Author  : xingyue
# @File    : caikuang.py

from task.base import SaoDangFb
import  time,threading
import os,json
class task(SaoDangFb):
    def caikuang(self):
        mineinfo = self.action(c='mine', m='index')
        dateline = mineinfo['dateline']
        log = mineinfo['log']
        if log:
            log_dateline = log['dateline']
            lasttime = int(dateline) - int(log_dateline)
            if lasttime > 14400:
                self.action(c='mine', m='get_silver', s=mineinfo['log']['site'])
                self.action(c='mine', m='give_up')
                for i in range(3, 5):
                    mineinfo = self.action(c='mine', m='index', p=i)['list']
                    for l in mineinfo:
                        if l['status'] == 0:
                            self.action(c='mine', m='caikuang', p=l['page'], id=l['id'], t=l['type'])
                            exit(2)
        else:
            for i in range(3, 5):
                mineinfo = self.action(c='mine', m='index', p=i)['list']
                for l in mineinfo:
                    if l['status'] == 0:
                        self.action(c='mine', m='caikuang', p=l['page'], id=l['id'], t=l['type'])
                        exit(2)


if __name__ == '__main__':
    def act(user,apass,addr):
        action = task(user,apass,addr)
        action.caikuang()
    filepath = os.path.dirname(os.path.abspath(__file__))
    cont = ['autocaikuang.txt']
    for t in cont:
        with open('%s/users/%s'%(filepath,t),'r') as f:
            for i in f:
                if i.strip():
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    t1 = threading.Thread(target=act, args=(name,passwd,addr))
                    t1.start()