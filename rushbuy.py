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


class task(SaoDangFb):
    def unlock(self, pwd):  # 解锁密码
        self.action(c='member', m='resource_unlock', token_uid=210000353508, pwd=pwd)

    def springshop(self, name=u'聊得'):  # 周末武將商城
        # id 列表对应 1-20 即为购买武将1-20
        spring = self.action(c='springshop', m='index')['list']
        self.action(c='springshop', m='buy', id=1)
        # self.action(c='springshop', m='buy', id=1)
        self.action(c='springshop', m='buy', id=3)
        self.action(c='springshop', m='buy', id=10)
        self.action(c='springshop', m='buy', id=17)

    def countryshop(self):  # 抢购国家商城
        # id 2 20税金，300蓝石头，13 40税金600蓝石头
        # id 3 40税金150黄石头   14 80 300黄
        # id 7 80两千声望   18 150 4000声望
        self.action(c='country_taxes_shop', m='index')
        self.action(c='country_taxes_shop', m='buy', id=2)  #
        self.action(c='country_taxes_shop', m='buy', id=3)  #
        self.action(c='country_taxes_shop', m='buy', id=7)  # 购买声望80个税金2000个
        self.action(c='country_taxes_shop', m='buy', id=13)
        self.action(c='country_taxes_shop', m='buy', id=14)  #
        self.action(c='country_taxes_shop', m='buy', id=18)


if __name__ == '__main__':
    q = Queue()
    filepath = os.path.dirname(os.path.abspath(__file__))
    cont = ['rush.txt']
    for t in cont:
        with open('%s/users/%s' % (filepath, t), 'r') as f:
            for i in f:
                if i.strip():
                    name = i.split()[0]
                    passwd = i.split()[1]
                    try:
                        lockpwd = i.split()[3]
                    except:
                        lockpwd = None
                    addr = i.split()[2]
                    action = task(name, passwd, addr)
                    action.unlock(lockpwd)
                    now_time = time.strftime('%H:%M:%S')
                    while True:
                        now_time = time.strftime('%H:%M:%S')
                        # if now_time >= '16:01:00' or now_time < '15:58:00':
                        #     break
                        # else:
                        threading.Thread(target=action.countryshop).start()
