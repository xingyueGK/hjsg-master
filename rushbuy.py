#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/13 17:53
# @Author  : xingyue
# @File    : rushbuy.py

# 抢购指定商品
from task.base import SaoDangFb
import time, threading
import os, json
from Queue import  Queue
import requests
import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
_redis = redis.StrictRedis(connection_pool=pool)

tasks = {}
lock = threading.RLock()


class task(SaoDangFb):

    def unlock(self, pwd):  # 解锁密码
        print json.dumps(self.action(c='member', m='resource_unlock',pwd=pwd)),self.user

    def springmap(self):
        SpringMap = {}
        self.index = self.action(c='springshop',m='index')
        for i in self.index['list']:
            SpringMap[i['name']] = i['id']
        return SpringMap
    def springshop(self, name):  # 周末武將商城
        # id 列表对应 1-20 即为购买武将1-20
        #获取指定名字购买
        d = self.springmap()
        global lock
        _redis.hsetnx(self.user, name, 0)
        print _redis.hget(self.user, name)
        if _redis.hget(self.user, name) == '0':
            id = d[name]
            result = self.action(c='springshop', m='buy', id=id)
            self.p(result)
            if result['status'] == 1:
                _redis.hset(self.user, id, 1)
                TIME = time.strftime("%Y-%m-%d")
                extime = TIME + " 23:59:59"
                lock.acquire()
                timeArray = time.strptime(extime, "%Y-%m-%d %H:%M:%S")
                timeStamp = int(time.mktime(timeArray))
                lock.release()
                _redis.expireat(self.user, timeStamp)

    def shoppingFeastSecKill(self,time_limit, rid1, rid2):#双十一秒杀活动
        try:
            #print 'sleep secend time',cdtime
            #print rid1,rid2,time_limit
            #time.sleep(cdtime-3)
            url1 = 'http://s{addr}.game.hanjiangsanguo.com/index.php?v=0&c=shopping_feast&' \
                  'time_limit={time_limit}&rid={rid2}&' \
                  'm=seckill&&token_uid=14900008572777&' \
                  'token={token}&channel=150&lang=zh-cn&rand=154200349070171'.format(addr=self.num,time_limit=time_limit,rid2=rid1,token=self.token)
            url2 = 'http://s{addr}.game.hanjiangsanguo.com/index.php?v=0&c=shopping_feast&' \
                  'time_limit={time_limit}&rid={rid2}&' \
                  'm=seckill&&token_uid=14900008572777&' \
                  'token={token}&channel=150&lang=zh-cn&rand=154200349070171'.format(addr=self.num,time_limit=time_limit,rid2=rid2,token=self.token)
            _redis.hsetnx(self.user,rid1,0)
            _redis.hsetnx(self.user, rid2,0)
            if _redis.hget(self.user,rid1) == '0':
                result =requests.get(url1).json()
                print result
                if result['status'] == 1:
                     _redis.hset(self.user,rid1,1)
                elif result['status'] == -9:
                     _redis.hset(self.user,rid1,9)
            if _redis.hget(self.user,rid2) == 0:
                print result
                result =requests.get(url2).json()
                if result['status'] == 1:
                     _redis.hset(self.user,rid2,1)
                elif result['status'] == -9:
                     _redis.hset(self.user,rid1,9)
        except Exception as e:
            print e
            self.shoppingFeastSecKill(time_limit, rid1, rid2)
    def shoppingFeastSecKill1(self,time_limit, rid1, rid2):#双十一秒杀活动
        try:
            #print 'sleep secend time',cdtime
            #print rid1,rid2,time_limit
            #time.sleep(cdtime-3)
            url1 = 'http://s{addr}.game.hanjiangsanguo.com/index.php?v=0&c=shopping_feast&' \
                  'time_limit={time_limit}&rid={rid2}&' \
                  'm=seckill&&token_uid=14900008572777&' \
                  'token={token}&channel=150&lang=zh-cn&rand=154200349070171'.format(addr=self.num,time_limit=time_limit,rid2=rid1,token=self.token)
            url2 = 'http://s{addr}.game.hanjiangsanguo.com/index.php?v=0&c=shopping_feast&' \
                  'time_limit={time_limit}&rid={rid2}&' \
                  'm=seckill&&token_uid=14900008572777&' \
                  'token={token}&channel=150&lang=zh-cn&rand=154200349070171'.format(addr=self.num,time_limit=time_limit,rid2=rid2,token=self.token)

            result1 =requests.get(url1).json()
            print result1
            result2 =requests.get(url2).json()
            print result2
        except Exception as e:
            print e
            self.shoppingFeastSecKill1(time_limit, rid1, rid2)

    def generalpool(self):  # 武将池
        #self.action(c='act_generalpool', m='index')
        #result = self.action(c='act_generalpool', m='general_chip')

        # 免费武将1谋士，2武将
        #self.action(c='act_generalpool', m='lottery', type=1)
        #self.action(c='act_generalpool', m='lottery', type=2)
        #self.action(c='act_generalpool', m='lottery_ten', type=2,shop=2)#10次卢植刘璋
        self.p(self.action(c='tavern',m='buy',generalid=1001,num=10000))
        #self.p(self.action(c='tavern', m='buy', generalid=1001, num=100000))
        #self.p(self.action(c='tavern', m='buy', generalid=1002, num=100000))
def run(name, passwd, addr,lockpwd,general):
    action = task(name, passwd, addr)
    action.unlock(lockpwd)
    count =0
    while True:
        count +=1
        print count
        threading.Thread(target=action.generalpool).start()
        #for id in general:
        #    threading.Thread(target=action.springshop, args=(id,)).start()
        #time.sleep(0.3)
    # time_limit, rid1, rid2 = action.SecKillInfo()
    # while True:
    #     threading.Thread(target=action.shoppingFeastSecKill, args=(time_limit, rid1, rid2)).start()
if __name__ == '__main__':
    q = Queue()
    filepath = os.path.dirname(os.path.abspath(__file__))
    cont = ['rush.txt']
    for t in cont:
        with open('%s/users/%s' % (filepath, t), 'r') as f:
            for i in f:
                if i.strip() and not i.startswith('#'):
                    print i
                    name = i.split()[0]
                    passwd = i.split()[1]
                    try:
                        lockpwd = i.split()[3]
                    except:
                        lockpwd = None
                    try:
                        general = eval(i.split()[4])
                    except:
                        general = None
                    addr = i.split()[2]
                    threading.Thread(target=run,args=(name, passwd, addr,lockpwd,general)).start()