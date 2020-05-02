#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/19 15:49
# @Author  : xingyue
# @File    : yuanbao.py

#元宝放送活动
from task.blackmarket import blackmarket
from base import SaoDangFb
import time, threading
import os, json
from Queue import  Queue
import  redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
_redis = redis.StrictRedis(connection_pool=pool)

studfarmNum=0

class task(SaoDangFb):
    def draw(self):#摇奖
        self.action(c='act_solt',m='draw',times=1)
    def act_solt(self):
        index = self.action(c='act_solt',m='index')
        task1 = int(index['info']['task1'])
        task2 = int(index['info']['task2'])
        task3 = int(index['info']['task3'])
        return task1,task2,task3
    def refresh(self):
        ref = self.action(c='business',m='refresh')
        return ref['trader']
    def buytimes(self):
        #购买次数并缓存到redis，三日内最多购买24次
        '''redis 存储hash key 如下格式
            区+‘类型’  账号  次数
            149business xingyue123 21
        '''
        key = self.num + 'business'
        fild = self.user
        Alreadybuy = _redis.hget(key, fild) or 0  # 已经购买过的次数
        if int(Alreadybuy)  < 24:#总购买次数大于24 不合适，不购买
            business_index = self.action(c='business', m='index')
            business_times = business_index['times']  # 当前次数
            NeedBuyTimes = 24 - int(business_times)  # 需要购买的
            for i in range(NeedBuyTimes):
                buy = self.action(c='business', m='buy')
            business_index = self.action(c='business', m='index')
            business_times = business_index['times']
            _redis.hset(key, fild, business_times)
            _redis.expire(key, 259200)
        else:
            print '已经购买',Alreadybuy

    def business(self):  #
        # 获取通商次数
        business_index = self.action(c='business', m='index')
        business_list = business_index['list'][0]
        business_times = business_index['times']
        if len(business_list) != 2:
            print '不合适，退出'
            exit(1)
        #需要完成24次
        if int(business_times) >0:
            business_trader = business_index['trader']
            print '通商次数为{times}'.format(times=business_times)
            for item in business_trader:#遍历通商列表
                if business_list[0]['finish'] == 0 and item['id'] == business_list[0]['id'] :
                        self.action(c='business', m='go_business', id=item['id'])
                        self.business()
                elif business_list[0]['finish'] ==1 and business_list[1]['finish'] == 0 and item['id'] == business_list[1]['id']:
                    self.action(c='business', m='go_business', id=item['id'])
                    self.business()
        if business_times > 0:
            self.refresh()
            self.business()

    def zuoji(self):  # 购买三次坐骑
        self.action(c='studfarm', m='index')
        key = self.num + 'studfarm'
        fild = self.user
        for i in range(3):
            studfarmNum = _redis.hget(key, fild) or 0
            if int(studfarmNum) < 3:
                print self.action(c='studfarm', m='action', new=1, id=3)
                studfarmNum = int(studfarmNum)
                studfarmNum += 1
                _redis.hset(key,fild,studfarmNum)
                _redis.expire(key,259200)
            else:
                print '今天已经刷了{num} 次了'.format(num=studfarmNum)
                break

def run(user, apass, addr,lockpwd):
    action = task(user, apass, addr)
    task1,task2,task3 = action.act_solt()
    if action.level() > 120:
        action.unlock(lockpwd)
        action.buytimes()
        action.zuoji()
        action.business()
    else:
        print '等级不够'
        exit(2)
    print task1
    if task1 < 1000:
        black = blackmarket(user, apass, addr)
        blackmarkets = (1000 - int(task1))//10+1
        for i in range(blackmarkets):
            print '刷新次数', i
            black.buy(user, refresh=blackmarkets)
            black.refresh()

    action.draw()
if __name__ == '__main__':

    filepath = os.path.dirname(os.path.abspath(__file__)).rsplit('\\',1)[0]
    cont = ['alluser.txt','user.txt']
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
                    t1.start()