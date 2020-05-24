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
    reward_type ={
        '2':'银币',
        '4':'紫',
        '7':'声望',
        '33':'战功',
    }

    def __init__(self, *args):
        super(OverseaStrade, self).__init__(*args)
        self.log = MyLog(logname='oversea.log')

    def index(self):
        index = self.action(c='overseastrade',m='index')
        return  index

    def world_index(self):
        index = self.action(c='overseastrade',m='world_index')
        if index['status'] !=1:
            self.log.error('world_index status not :%s'%index)
            time.sleep(0.5)
            index = self.action(c='overseastrade', m='world_index')
        self.log.info('world_index　result %s'%index)
        return  index

    def world_refresh(self,page):
        formdata = {
            "page":page,
        }
        world_refresh = self.action(c='overseastrade',m='world_refresh',body=formdata)
        return world_refresh

    def ship_list(self):
        #商船选择
        ship_list = self.action(c='overseastrade',m='ship_list')
        self.log.info('ship_list status:%s'%ship_list)
        return ship_list
    def renovate_ship(self):
        #刷新商船
        ship_list = self.ship_list()
        price = int(ship_list['price'])
        renovate_ship = ''
        while price == 0:
            renovate_ship = self.action(c='overseastrade',m='renovate_ship')
            try:
                price = int(renovate_ship['price'])
            except:
                break
        return renovate_ship


    def renovate_world_goods(self):
        #刷新商品
        """
        :return:
        """
        self.log.info('renovate_world_goods')
        num = 0
        while num < 5:
            result = self.action(c='overseastrade', m=self.get__function_name())
            if result['status'] ==1:
                return result
            elif result['status'] ==11:
                num += 1
                time.sleep(0.5)
            return ""


    def world_goods_list(self):
        self.log.info(self.get__function_name())
        result = self.action(c='overseastrade',m=self.get__function_name())
        self.log.info("%s:%s"%(self.get__function_name(),result))
        return result

    def harbour_list(self):
        result = self.action(c='overseastrade',m=self.get__function_name())
        self.log.info("%s:%s"%(self.get__function_name(),result))
        return result


    def get_list_from_world(self,page=10):
        formdata= {
            "page":page
        }
        result = self.action(c='overseastrade',m=self.get__function_name(),body=formdata)
        self.log.info("%s:%s"%(self.get__function_name(),result))
        return result

    def quit(self):
        #退出
        result = self.action(c='overseastrade',m=self.get__function_name())
        self.log.info("%s:%s"%(self.get__function_name(),result))
        return result

    def choose_world_goods(self,goods_id=6):
        #选择商品 1
        #默认ID 6 为镔铁长刀
        formdata= {
            "goods_id":goods_id
        }
        result = self.action(c='overseastrade',m=self.get__function_name(),body=formdata)
        self.log.info("%s:%s" % (self.get__function_name(), result))
        self.choose_harbour()
        return result

    def choose_harbour(self,harbour_id=2):
        #选择港口 1 银币 2 紫 3 声望 4战功
        #默认ID 2 为紫石头加成
        self.harbour_list()
        formdata= {
            "harbour_id":harbour_id
        }
        result = self.action(c='overseastrade',m=self.get__function_name(),body=formdata)
        self.log.info("%s:%s"%(self.get__function_name(),result))
        return result

    def join_world_team(self,site,place,page,id=0):
        #加入团队id 为0，创建队伍
        self.harbour_list()
        formdata= {
            "id":id,
            "site":site,
            "place":place,
            "page": page,
        }
        result = self.action(c='overseastrade',m=self.get__function_name(),body=formdata)
        self.log.info("%s:%s"%(self.get__function_name(),result))
        return result
    def world_start(self):
        #开始
        print '开始跑船'
        result = self.action(c='overseastrade',m=self.get__function_name())
        if result['status']!=1:
            self.log.error('world_start error %s' %result['msg'])
            for item in self.world_goods_list()['list']:
                if int(item['status']) ==1:
                    self.choose_harbour(item['harbour'])
            result = self.action(c='overseastrade', m=self.get__function_name())
        self.log.info("%s:%s"%(self.get__function_name(),result))
        return result

    def run(self):
        self.world_goods_list()