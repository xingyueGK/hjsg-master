#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/18 14:19
# @Author  : xingyue
# @File    : blackmarket.py

#每日三次刷新黑市，主要是购买军令

from task.base import SaoDangFb
import time, threading
import os, json
from Queue import Queue


class blackmarket(SaoDangFb):
    # buy_type 1 是银币  2 是元宝 3 是蓝石头 4 是黄石头 5 是紫石头


    def refresh(self):

        refresh = self.action(c='blackmarket', m='refresh')
        return refresh['list']

    def buy(self,user):
        buy_item = ['中级卡', '初级卡', '高级卡', '军令']
        buy_type = [1, 3, 4, 5]
        times, item = self.blackmarket()
        for k, v in item.items():
            if v['name'] in buy_item and int(v['buy_type']) in buy_type:
                print
                status = self.action(c='blackmarket', m='buy', id=v['id'])
                if status['status'] !=1:
                    exit(3)
                print user,'够买'+ v['name'],int(v['value'])
                self.buy(user)
        print times
        if int(times) > 0:
            self.refresh()
            self.buy(user)

    def blackmarket(self):  # 黑市购买军令，突飞卡
        index = self.action(c='blackmarket', m='index')
        times = index['info']['times']
        return times, index['list']
        # 免费刷新次数
    def tavern(self):#批量银币贸易
        self.action(c='tavern',m='trade_batch',option=1)
    def unlock(self, pwd):
        self.action(c='member', m='resource_unlock', token_uid=210000353508, pwd=pwd)
def run(user, apass, addr,lockpwd):
    action = blackmarket(user, apass, addr)
    action.unlock(lockpwd)
    # action.tavern()
    action.buy(user)
if __name__ == '__main__':
    q = Queue()
    filepath = os.path.dirname(os.path.abspath(__file__))
    cont = ['user.txt']
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
