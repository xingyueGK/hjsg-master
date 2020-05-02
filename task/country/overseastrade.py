#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/2 10:26
# @Author  : xingyue
# @File    : overseastrade.py

from task.base import SaoDangFb
from utils.mylog import MyLog

import threading
import os, time

class OverseaStrade(SaoDangFb):
    def __init__(self, *args):
        super(OverseaStrade, self).__init__(*args)
        self.log = MyLog(logname='oversea.log')

    def index(self):
        index = self.action(c='overseastrade',m='index')
        return  index

    def world_index(self):
        index = self.action(c='overseastrade',m='world_index')
        return  index

    def world_refresh(self,page):
        formdata = {
            "page":page,
        }
        world_refresh = self.action(c='overseastrade',m='world_refresh',body=formdata)
        return world_refresh

    def ship_list(self):
        self.log.info('ship_list')
        ship_list = self.action(c='overseastrade',m='ship_list')
        self.log.info('ship_list status:%s'%ship_list)
        return ship_list
    def renovate_ship(self):
        #刷新商船
        ship_list = self.ship_list()
        price = int(ship_list['price'])
        while price == 0:
            renovate_ship = self.action(c='overseastrade',m='renovate_ship')
            try:
                price = int(renovate_ship['price'])
            except:
                break
        return renovate_ship

    def world_goods_list(self):
        self.log.info('world_goods_list')
        world_goods_list = self.action(c='overseastrade', m='world_goods_list')
        return  world_goods_list

    def renovate_world_goods(self):
        self.log.info('renovate_world_goods')
        result = self.action(c=self.get__function_name(), m='renovate_ship')
        return  result

    def world_goods_list(self):
        self.log.info(self.get__function_name())

        result = self.action(c=self.get__function_name(), m='renovate_ship')
        self.log.info("%s:%s"%(self.get__function_name(),result))
        return result

    def run(self):
        self.world_goods_list()