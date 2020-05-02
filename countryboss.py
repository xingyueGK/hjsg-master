#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/10 10:37
# @Author  : xingyue
# @File    : task.py

from task.base import SaoDangFb
from utils.mylog import MyLog

import threading
import os, time

logger = MyLog()

class CountryBoss(SaoDangFb):

    def index(self):
        index = self.action(c='countryboss', m='index')
        return index

    def powerup(self):
        logger.info('开始银币强化攻击')
        boss_info = self.index()
        try:
            powerup = int(boss_info['powerup'])
        except:
            self.p(boss_info)
        if powerup < 200:
            for i in range((200 - powerup) / 10):
                status= self.action(c='countryboss', m='powerup', gold=0)
                logger.info('powerup:%s'%status)
        else:
            logger.info('powerup已经强化到%s'%powerup)
    def get_reward(self):
        logger.info('get_reward')
        r1 = self.action(c='countryboss', m='get_reward_preview')
        r1 = self.action(c='countryboss', m='get_reward', body={"type":1})
        if r1['status'] ==1:
            logger.info('get_reward_type1 %s'%r1)
        else:
            logger.error('get_reward_type1 %s'%r1['msg'])
        r2 = self.action(c='countryboss', m='get_reward',body={"type":2})
        if r2['status'] == 1:
            logger.info('get_reward_type2 %s' % r2)
        else:
            logger.error('get_reward_type2 %s' % r2['msg'].encode('utf8'))

    def get_city_id(self):
        logger.info('get_city_id')
        index = self.index()
        try:
            for item in index['city_list']:
                if item['status'] == 1:
                    city_id = item['city_id']
                    logger.info('return city_id %s'%city_id)
                    return city_id
        except:
            self.p(index)
    def join_group(self,city_id,group_id=''):
        logger.info('jion_group')
        formdata = {
            "city_id":city_id,
            "group_id":group_id,
        }
        status = self.action(c='countryboss',m='join_group',body=formdata)
        logger.info('jion_group status %s'%status)
    def fight(self):
        self.action(c='countryboss',m='fight')

    def countryboss(self):  # 世界boss领取
        # 银币鼓舞

        if self.get_act()['country'] != "0":

            now_time = time.strftime('%H:%M:%S')
            print now_time
            if now_time < '20:00:00':
                r = self.index()
                if r['hit_times'] == 0:
                    logger.info('已经没有次数了')
                    return False
                self.powerup()
                self.join_group(self.get_city_id())
                self.fight()
            else:
                self.get_reward()


def run(user, apass, addr):
    action = CountryBoss(user, apass, addr)
    action.countryboss()


if __name__ == '__main__':
    filepath = os.path.dirname(os.path.abspath(__file__))
    cont = ['boss.txt']
    for t in cont:
        with open('%s/users/%s' % (filepath, t), 'r') as f:
            for i in f:
                if i.strip():
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    t1 = threading.Thread(target=run, args=(name, passwd, addr))
                    t1.start()
                    # t1.join()
                    time.sleep(0.2)
