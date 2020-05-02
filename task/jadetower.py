#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/29 9:15
# @Author  : xingyue
# @File    : jadetower.py
#封宝楼

from task.base import SaoDangFb
from utils.mylog import MyLog

import threading
import os,time

class JadeTower(SaoDangFb):
    def __init__(self,*args):
        super(JadeTower,self).__init__(*args)
        self.log = MyLog(logname="JadeTower")
    def index(self):
        index = self.action(c='jade_tower',m='index')
        return  index
    def start(self):
        start = self.action(c='jade_tower', m='start')
        return start
    def create_room(self,name=111,limit_type=0,floor=2,min_level=0,password=""):
        formdata ={
            "name": name,
            "limit_type": limit_type,
            "floor": floor,
            "min_level": min_level,
            "password":password,
        }
        status = self.action(c='jade_tower',m='create_room',body=formdata)
        return status
    def fight(self):
        while True:
            index = self.index()
            if int(index['monster_number'])<=0:
                break
            self.log.info("figth_index:%s"%index)
            fight = self.action(c='jade_tower', m='fight')
            self.log.info("fight:%s" % fight)
            time.sleep(0.5)

    def fight_refine(self,id=30):
        #默认是炼化南明离火剑30
        #炼化
        index = self.index()
        formdata = {
            "refine_id":id
        }
        if index['phase'] ==3 and index['refine_info']:
            while True:
                index = self.index()
                self.log.info('fight_refine_index:%s'%index)
                if int(index['refine_info']['times'])==0:
                    self.log.info('fight_refine:炼化结束')
                    break

                fight_refine = self.action(c='jade_tower',m='fight_refine',body=formdata)
                self.log.info('fight_refine:%s'%fight_refine)
                time.sleep(1)
        else:
            self.log.error('fight_refine:还没有到炼化步骤')

    def run(self,floor):
        index = self.index()
        if index['join_room']:
            join_room = index['join_room']
            if int(join_room['member2_ready']) ==1 and int(join_room['member1_ready']) ==1:
                #所有人员都准备
                self.start()
                self.fight()
                self.fight_refine()
        else:
            status = self.create_room(floor=floor)
            self.log.info('create_room:%s'%(status))
            return
        self.fight_refine()
def main(name, passwd, addr,floor):
    a = JadeTower(name, passwd, addr)
    a.run(floor)
if __name__ == '__main__':

    filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # cont = ['21user.txt', 'autouser.txt','gmnewyear.txt', 'user.txt', 'alluser.txt']
    cont = ['jadetower.txt']
    for t in cont:
        with open('%s/users/%s' % (filepath, t), 'r') as f:
            for i in f:
                if i.strip() and not i.startswith('#'):
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    floor = i.split()[3]
                    t1 = threading.Thread(target=main, args=(name, passwd, addr,floor))
                    t1.start()