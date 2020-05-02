#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/1 9:54
# @Author  : xingyue
# @File    : treasure.py


from task.base import SaoDangFb
import time, threading
import os, json
from Queue import Queue


class treasure(SaoDangFb):
    """双旦夺宝活动"""
    def send_gift_index(self):
        """双旦夺宝
        send_gift_index 挂礼物 choice_snow  {snow_type 1，2,3}选择礼物
        """
        try:
            self.action(c='treasure', m='index')
            send_gift_index = self.action(c='treasure', m='send_gift_index')
            white = send_gift_index['white']
            gold = send_gift_index['gold']
            colour = send_gift_index['colour']
            return white,gold,colour
        except KeyError as e:
            print e
    def choice_snow(self):
        """选择礼物"""
        white, gold, colour  = self.send_gift_index()
        if white ==1:
            self.send_gift(1,1,6)
        if gold ==1:
            self.send_gift(2,2,8)
        if colour ==1:
            self.send_gift(3,3,12)
    def send_gift(self,snow_type,sid,tid):
        """发送两次送"""
        print 'seng_gift'
        data = {"snow_type": snow_type,
                "sid": sid,
                "tid": tid,
                "check": 1}
        self.action(c='treasure', m='send_gift', body=data)
        data = {"snow_type": snow_type,
                "sid": sid,
                "tid": tid,
                }
        self.action(c='treasure', m='send_gift', body=data)

    def pick_index(self):
        """摘礼物"""
        try:
            self.action(c='treasure', m='index')
            pick_index = self.action(c='treasure', m='pick_index')
            white_pick = pick_index['white_pick']
            gold_pick = pick_index['gold_pick']
            colour_pick = pick_index['colour_pick']
            return white_pick, gold_pick, colour_pick
        except TypeError as e:
            print e

    def pick(self,snow_type,page=1):
        try:
            FormData = {
                "snow_type": snow_type,
                "page": page
            }
            pick_list = self.action(c='treasure',m='pick_list',body=FormData)
            if pick_list['list']:
                id = pick_list['list'][0]['id']
                FormData = {
                    "id": id,
                    "check": 1
                }
                status =11
                while status != 1:
                    status = self.action(c='treasure', m='pick',body=FormData)['status']
                    print self.user,status
                    time.sleep(0.5)
                    if status == -8:
                        self.pick(snow_type)
                        break
                FormData = {
                    "id": id,
                }
                self.action(c='treasure', m='pick', body=FormData)
        except KeyError as e:
            print e
            #self.pick(snow_type)
    def pick_list(self):
        white_pick, gold_pick, colour_pick = self.pick_index()
        print self.pick_index()
        if white_pick == 1:
            self.pick(1)
        if gold_pick == 1:
            self.pick(2)
        if colour_pick == 1:
            self.pick(3)
    def rob_list(self,snow_type,page=1):
        """抢夺礼物"""
        FormData = {
            "snow_type": snow_type,
            "page": page
        }
        result = self.action(c='treasure',m='rob_list',body=FormData)
        return result
    def rob(self):
        """三种类型1,2,3"""
        for i in range(1,4):
            rob_list = self.rob_list(i)
            if rob_list['list']:
                lists = rob_list['list']
                pages= rob_list['pages']
                for i in reversed(pages):
                    pass
                id = 4
                FormData = {
                    "id": id,
                    "check": 1
                }
                status = 11
                while status != 1:
                    status = self.action(c='treasure', m='rob', body=FormData)['status']
                    print self.user, status
                    time.sleep(0.5)
                    if status == -8:
                        break
                FormData = {
                    "id": id,
                }
                self.action(c='treasure', m='rob', body=FormData)


    def boss_index(self):
        """打boss"""
        try:
            result = self.action(c='treasure',m='boss_index')
            if result['act_blood'] != result['all_blood']:
                robnum = int(result['robnum'])
                for i in range(robnum):
                    while True:
                        status = self.action(c='treasure', m='boss_fight')
                        if status['status'] == 1:
                            break
            else:
                result = self.action(c='treasure', m='get_boss_reward',id=1)
                result = self.action(c='treasure', m='get_boss_reward', id=2)
                result = self.action(c='treasure', m='get_boss_reward', id=3)
                result = self.action(c='treasure', m='get_boss_reward', id=4)
                result = self.action(c='treasure', m='get_boss_reward', id=5)
        except KeyError as e:
            print self.user,result
def task(user, apass, addr):
    action = treasure(user, apass, addr)
    action.choice_snow()
    action.pick_list()
    # action.boss_index()
if __name__ == '__main__':
    q = Queue()
    filepath = os.path.dirname(os.path.abspath(__file__))
    cont = ['user.txt']
    for t in cont:
        with open('%s/users/%s' % (filepath, t), 'r') as f:
            for i in f:
                if i.strip() and not i.startswith('#'):
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    #addr = 150
                    t1 = threading.Thread(target=task, args=(name, passwd, addr))
                    q.put(t1)
    while not q.empty():
        thread = []
        for i in xrange(6):
            try:
                thread.append(q.get_nowait())
            except Exception as e:
                print e
        for i in thread:
            i.start()
        for i in thread:
            i.join()