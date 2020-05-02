#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/18 14:19
# @Author  : xingyue
# @File    : blackmarket.py

#每日三次刷新黑市，主要是购买军令

from task.base import SaoDangFb
import time, threading,json
import os,redis
from Queue import Queue

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
_redis = redis.StrictRedis(connection_pool=pool)

class blackmarket(SaoDangFb):
    # buy_type 1 是银币  2 是元宝 3 是蓝石头 4 是黄石头 5 是紫石头
    buy_item = ['中级卡', '初级卡', '军令']
    buy_type = [1, 3, 4, 5]
    def refresh(self):
        try:
            refresh = self.action(c='blackmarket', m='refresh')
            self.p(refresh['list'])
            return refresh['list']
        except:
            time.sleep(0.3)
            self.refresh()
    def buy(self,user,refresh=0):
        times, item = self.blackmarket()
        for k, v in item.items():
            self.buyitem(user,k,v)

    def buyitem(self,user,id,item):
        if item['name'] in self.buy_item and int(item['buy_type']) in self.buy_type:
            status = self.action(c='blackmarket', m='buy', id=int(item['id']))
            if status['status'] != 1 and status['status'] != 101:
                self.p('buyitem exit %s %s'%(item['name'],int(item['id'])),status)
                exit(3)
            elif status['status'] == 101 :
                status = self.action(c='blackmarket', m='buy', id=int(item['id']))
                self.p('buyitem exit %s %s' % (item['name'], int(item['id'])), status)
                if status['status'] !=1:
                    self.p('buyitem exit %s %s' % (item['name'], int(item['id'])), status)
                    exit(1)
            print user, '够买' + item['name'], int(item['value'])
            try:
                self.buyitem(user,id,status['list'][id])
            except:
                self.p(status)
        else:
            print 'None'
            return None
    def blackmarket(self):  # 黑市购买军令，突飞卡
        index = self.action(c='blackmarket', m='index')
        times = index['info']['times']
        return times, index['list']
        # 免费刷新次数
    def tavern(self):#批量银币贸易
        self.action(c='tavern',m='trade_batch',option=1)
def run(user, apass, addr,lockpwd):
    action = blackmarket(user, apass, addr)
    action.unlock(lockpwd)
    # action.tavern()
    refresh = 200
    for i in range(refresh):
        print '刷新次数', i
        action.buy(user,refresh=refresh)
        action.refresh()
if __name__ == '__main__':
    q = Queue()
    filepath = os.path.dirname(os.path.abspath(__file__)).rsplit('\\',1)[0]

    cont = ['junling.txt']
    for t in cont:
        with open('%s/users/%s' % (filepath, t), 'r') as f:
            for i in f:
                if i.strip() and not i.startswith('#'):
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