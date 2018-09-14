#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/10 10:37
# @Author  : xingyue
# @File    : task.py
#周年庆喊话

from task.base import SaoDangFb
import time, threading
import os, json


class task(SaoDangFb):
    def chat(self, ms):  # 获取聊天信息
        chat_index = self.action(c='chat', m='index')
        self.action(c='chat', m='send', message=ms)  # 发送消息
    def znhh(self):
        # 周年喊话
        result = self.action(c='act_halloween', m='index')
        hammer = result['hammer']
        for i in range(int(result['candy'])):
            self.action(c='act_halloween', m='action_candy')
        for i in range(10):
            for i in range(1, 10):
                self.action(c='act_halloween', m='action_pumpkin', id=i)
def run(user, apass, addr):
    action = task(user, apass, addr)
    action.chat(u"悍将三国六周年快乐")
    action.znhh()#全部点燃蜡烛
if __name__ == '__main__':
    filepath = os.path.dirname(os.path.abspath(__file__))
    cont = ['autouser.txt','alluser.txt',
            '21user.txt','user.txt','150gx.txt']
    for t in cont:
        with open('%s/users/%s' % (filepath, t), 'r') as f:
            for i in f:
                if i.strip():
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    t1 = threading.Thread(target=run, args=(name, passwd, addr))
                    t1.start()
                    time.sleep(0.2)