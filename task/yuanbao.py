#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/19 15:49
# @Author  : xingyue
# @File    : yuanbao.py

from .base import SaoDangFb
import time, threading
import os, json
from Queue import  Queue
import  redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
_redis = redis.StrictRedis(connection_pool=pool)

studfarmNum=0

class task(SaoDangFb):
    def unlock(self, pwd):  # 解锁密码
        self.action(c='member', m='resource_unlock', token_uid=210000353508, pwd=pwd)
    def refresh(self):
        ref = self.action(c='member',m='refresh')
        return ref['trader']
    def buytimes(self):
        #购买次数并缓存到redis，三日内最多购买24次
        '''redis 存储hash key 如下格式
            区+‘类型’  账号  次数
            149business xingyue123 21
        '''
        business_index = self.action(c='business', m='index')
        business_times = business_index['times']
        key = self.num + 'business'
        fild = self.user
        Alreadybuy = _redis.gset(key, fild) or 0#已经购买过的次数
        NeedBuyTimes = 24 - int(business_times)#需要购买的
        if int(Alreadybuy) + int(NeedBuyTimes) < 24:#总购买次数大于24 不合适，不购买
            for i in range(NeedBuyTimes):
                buy = self.action(c='business', m='buy')
                if buy['status'] != 1:
                    exit(3)
                else:
                    Alreadybuy +=1
            _redis.hset(key, fild, Alreadybuy)
            _redis.expire(key, 259200)

    def business(self):  #
        # 获取通商次数
        business_index = self.action(c='business', m='index')
        business_list = business_index['list'][0]
        business_times = business_index['times']
        if len(business_list) != 2:
            exit(1)
        #需要完成24次
        if int(business_times) >0:
            business_trader = business_index['trader']
            for item in business_trader:
                if business_list[0]['finish'] == 0 and item['id'] == business_list[0]['id'] :
                        self.action(c='business', m='go_business', id=item['id'])
                        self.business()
                elif business_list[1]['finish'] == 0 and item['id'] == business_list[1]['id']:
                    self.action(c='business', m='go_business', id=item['id'])
                    self.business()

    def zuoji(self):  # 首次购买坐骑并穿戴
        self.action(c='studfarm', m='index')
        key = self.num + 'studfarm'
        fild = self.user
        for i in range(3):
            studfarmNum = _redis.hget(key, fild) or 0
            if int(studfarmNum) < 3:
                self.action(c='studfarm', m='action', new=1, id=3)
                studfarmNum += 1
                _redis.hset(key,fild,staticmethod)
                _redis.expire(key,259200)
            else:
                print '今天已经刷了{num} 次了'.format(num=studfarmNum)