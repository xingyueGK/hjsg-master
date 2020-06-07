#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/30 9:16
# @Author  : xingyue
# @File    : tanxian.py

from task.base import  SaoDangFb
from utils.mylog import MyLog
class Tanxian(object):

    def index(self):
        self.logger.info('探险首页')
        index = self.action(c='magicpet_explore',m=self.get__function_name())
        self.logger.info("{name}:{rest}".format(name=self.get__function_name(),rest=index))
        return index
    def area_reward_into(self,area_id=1):
        self.logger.info('探险首页')
        index = self.action(c='magicpet_explore',m=self.get__function_name(),area_id=area_id)
        return index
    def explore_receive_reward(self,area_id=1):
        self.logger.info('收获')
        index = self.action(c='magicpet_explore',m=self.get__function_name(),area_id=area_id)
        return index
    def one_button_join(self,area_id=1):
        self.logger.info('一键加入')
        index = self.action(c='magicpet_explore',m=self.get__function_name(),area_id=area_id)
        return index
    def explore_start(self,area_id=1):
        self.logger.info('开始')
        index = self.action(c='magicpet_explore',m=self.get__function_name(),area_id=area_id)
        return index



class RunTanxian(SaoDangFb,Tanxian):
    def __init__(self,*args):
        super(RunTanxian, self).__init__(*args)
        self.logger = MyLog(logname="tanxian.log")
    def run(self):
        index  =self.index()
        explore_now = index['explore_now']
        for item in explore_now:
            if int(item['explore_status'])==2:
                id = item['area_id']
                self.explore_receive_reward(id)
                self.one_button_join(id)
                self.explore_start(id)
                return True
            elif int(item['explore_status'])==3:
                self.logger.info('您还在探索中!')
                return True
        area_now = index['area_now']
        area_now = sorted(area_now,key=lambda x:x['area_level'])
        id = area_now[0]['area_id']
        self.p(id)
        self.area_reward_into(id)
        self.explore_receive_reward(id)
        self.one_button_join(id)
        self.explore_start(id)
