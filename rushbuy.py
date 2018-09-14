#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/13 17:53
# @Author  : xingyue
# @File    : rushbuy.py

#抢购指定商品
from task.base import SaoDangFb
import  time,threading
import os,json
class task(SaoDangFb):
    def unlock(self, pwd):#解锁密码
        self.action(c='member', m='resource_unlock', token_uid=210000353508, pwd=pwd)
    def springshop(self, name=u'聊得'):  # 周末武將商城
        #id 列表对应 1-20 即为购买武将1-20
        spring = self.action(c='springshop', m='index')['list']
        self.action(c='springshop', m='buy', id=1)
        #self.action(c='springshop', m='buy', id=1)
        self.action(c='springshop', m='buy', id=3)
        self.action(c='springshop', m='buy', id=10)
        self.action(c='springshop', m='buy', id=17)


if __name__ == '__main__':
    filepath = os.path.dirname(os.path.abspath(__file__))
    with open('users/%s'%(filepath),'r') as f:
        for i in f:
            if i.strip():
                name = i.split()[0]
                passwd = i.split()[1]
                unlock = i.split()[2]
                addr = i.split()[3]
                action = SaoDangFb(name, passwd, addr)
                action.unlock(unlock)
                now_time = time.strftime('%H:%M:%S')
                while True:
                    now_time = time.strftime('%H:%M:%S')
                    if now_time >= '16:01:00' or now_time < '15:58:00':
                        break
                    else:
                        threading.Thread(target=action.springshop).start()