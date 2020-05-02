#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/6 7:30
# @Author  : xingyue
# @File    : gx.py

#贡献号50级
from __future__ import unicode_literals
from task.base import SaoDangFb
import time, threading
import os, sys
from Queue import Queue
q = Queue()
reload(sys)
sys.setdefaultencoding('utf-8')


class fuben(SaoDangFb):
    def muster(self):#添加武将并出征
        # gid武将id，pid那个槽位训练获取
        caiid=''
        liaoid=''
        gid=''
        practtice_info = self.action(c='practice', m='index')
        # 初期都是两个训练槽位，
        pid = practtice_info['place']['1']['id']
        self.action(c = 'practice' , m = 'practice_stop ',pid = pid)#终止训练
        #获取武将
        self.action(c='levelgift',m='index')
        wujiang_index = self.action(c='muster',m='index',page=1,perpage=999)['list']
        for  k,v in wujiang_index.items():
            if v['name']=='蔡文姬':#蔡文姬
                print '孙权出站'
                gid = v['id']
                self.action(c='muster',m='go_battle',gid=v['id'])
                self.action(c='matrix',m='index')
                caiid =  v['id']
            elif v['name']=='廖化':
                self.action(c='muster', m='go_battle', gid=v['id'])
                liaoid = v['id']
        lists = '0,%s,0,%s,0,0,0,0,0'%(caiid,liaoid)
        self.action(c='matrix',m='update_matrix',list=lists,mid=1)
        #队武将突飞
        status=1
        index_info = self.action(c='practice',m='index')
        #训练武将，
        self.action(c='practice',m='practice_start',gid= gid,pid=pid,type=2)
        freetimes = index_info['freetimes']#突飞卡
        isturn = index_info['list']['1']['isturn']#武将师是否到转生级别
        wjlevel = index_info['list']['1']['level']
        print '武将等级',wjlevel
        time.sleep(1)
        while status == 1 and freetimes != '0':#队伍将进行突飞
            if int(isturn) == 1 and int(wjlevel) <= 60:
                print '武将转生'
                print self.action(c='practice',m='onekey_turn',gid=gid)
            self.action(c='practice', m='mop', times = 100,gid=gid)
            self.action(c='practice', m='mop', times=50, gid=gid)
            self.action(c='practice', m='mop', times=10, gid=gid)
            self.action(c='practice', m='mop', times=5, gid=gid)
            index_info = self.action(c='practice', m='index')
            freetimes = index_info['freetimes']
            info = self.action(c = 'practice',m='go_leap',gid=gid)#武将突飞一次
            status = info['status']
    def general(self,type):#获取武将id和装备id,并返回输入获取的等级
        #装备信息栏
        info = self.action(c='general',m='index')
        gid = info['list']['1']['id']  # 武将id
        etype1 = self.action(c='general', m='get_info',gid=gid,etype=1)
        etype3 = self.action(c='general', m='get_info',gid=gid,etype=3)#获取披风
        etype2 = self.action(c='general', m='get_info', gid=gid, etype=2)#获取铠甲
        eid = []#装备列表
        if info['list']['1']['eid1'] == 0 or info['list']['1']['eid1'] == "0":
            for k,v in  etype1['equipments'].items():#初期获得最高级装备为2级别
                if v['needlevel'] == str(type) and v['etype']== 1:
                    eid.append({"1":v['id']})
                    break
        else:
            eid.append({"1":info['list']['1']['eid1']['id']})
        if info['list']['1']['eid2'] == 0 or info['list']['1']['eid2'] == "0":
            for k,v in  etype2['equipments'].items():#初期获得最高级装备为2级别
                if v['needlevel'] == str(type) and v['etype']== 2:
                    eid.append({"2":v['id']})
                    break
        else:
            eid.append({"2":info['list']['1']['eid2']['id']})
        if info['list']['1']['eid3'] == 0 or info['list']['1']['eid3'] == "0":
            for k, v in etype3['equipments'].items():  # 初期获得最高级装备为2级别
                if v['needlevel'] == str(type) and v['etype']== 3:
                    eid.append({"3":v['id']})
                    break
        else:
            eid.append({"3":info['list']['1']['eid3']['id']})

        return gid,eid
    def get_general(self):#获取武将信息
        general_index=self.action(c='general',m='index')
        return general_index
    def strengthen(self,id):#强化装备
        print id
        levelinfo = self.level()
        print levelinfo
        self.action(c='general',m='index')
        self.action(c='strengthen',m='index')
        id_info = self.action(c='strengthen',m='strengthen_info',id=id)
        self.action(c='strengthen', m='onekey_strenthen', id=id, ratetype=0)
    def eqip(self,gid,eid,etype):#给武将穿戴装备
        self.action(c='general',m='equip',gid=gid,eid=eid,etype=etype)
    def mapscene(self):#领取通关奖励
        self.action(c='map',m='get_scene_list',l=1,v=2018071801)
        self.action(c='map',m='get_newreward_index',levelid=1,v=2018071801)
        self.action(c='map',m='get_newreward',id=1,v=2018071801)
        self.action(c='map', m='get_newreward', id=2, v=2018071801)
        self.action(c='map', m='get_newreward', id=3, v=2018071801)
        self.action(c='map', m='get_newreward', id=4, v=2018071801)
    def levelgift(self,level):#获取等级奖励
        self.action(c = 'levelgift' , m = 'index')#打开奖励页面
        self.action(c='levelgift',m='get_reward',level=level)#获取30级奖励
    def saodang(self,num):#攻击小兵
        map = self.action(c='map',m='get_mission_list')
        memberindex = self.action(c='member',m='index')
        num = int(memberindex['missionlevel'])
        exit_code = 1
        if exit_code == 1 :
            for level in range(num,3):#遍历每一个图
                print '开始攻击第 %s 个图'%level
                print  self.action(c='map',m='get_scene_list',l=level)
                site = len(self.action(c='map',m='get_scene_list',l=level)['list'])
                for i in range(0,site):#遍历关卡图次数
                    print '关卡',i
                    status = 1
                    for id in range(1,11):  # 遍历10个小兵
                        try:
                            #获取首杀状态，1为首杀，-1为已经击杀
                            first = self.action(c='map', m='mission', l=level, s=i+1, id=id)['info']['first']
                        except KeyError as e :
                            continue
                        if first == 1 and status == 1:#
                            status = self.action(c='map',m='action',l=level,s=i+1,id=id)['status']
                            print status
                            if  first == 1 and status == -5:
                                print '退出'
                                exit_code = 2
                                return exit_code
                        else:
                            print '已经击杀'
    def saodang1(self):#攻击小兵
        map = self.action(c='map',m='get_mission_list')
        memberindex = self.action(c='member',m='index')
        num = int(memberindex['missionlevel'])
        exit_code = 1
        status = 1
        if exit_code == 1 :
            for id in range(1,9):  # 遍历10个小兵
                try:
                    #获取首杀状态，1为首杀，-1为已经击杀
                    first = self.action(c='map', m='mission', l=3, s=1, id=id)['info']['first']
                except KeyError as e :
                    continue
                if first == 1 and status == 1:#
                    status = self.action(c='map',m='action',l=3,s=1,id=id)['status']
                    print status
                    if  first == 1 and status == -5:
                        print '退出'
                        exit_code = 2
                        return exit_code
                else:
                    print '已经击杀'
    def mainquest(self):  # 领取所有活动奖励
        mainquest_info = self.action(c='mainquest', m='index')
        print '领奖'
        for i in mainquest_info['list']:
            if int(i['status']) == 1:  # 获取奖励
                self.action(c='mainquest', m='get_task_reward', id=i['task_id'])
                print '领取奖励', i['task_id']
    def gjzb(self):#国家争霸
        self.action(c='country_gvg',m='index')
        self.action(c='country_gvg',m='member_entry')
def act(username,passwd,addr):
    action = fuben(username,passwd,addr)
    try:
        print '账号：%s   等级为：%s' % (username, action.level())
    except :
        print 'zhanghao ###################################### ',username
    if action.level() >= 260:
        exit()
    if action.level() >= 50:
        # action.saodang(6)
        exit()
    if  action.level() <10:
        action.saodang(1)#16级 失败退出
        action.levelgift(16)  # 领取16级奖励
    #扫荡失败以后获取2级别装备，然后强化后并穿戴上去
    if action.level() < 25:
        gid,uid = action.general(7)#第一次的都是2级装备
        print gid,uid
        for i in uid:
            for etype,v in i.items():
                action.strengthen(v)
                action.eqip(gid,v,etype)
        action.saodang(1)#26级失败退出
        for i in uid:
            for etype, v in i.items():
                action.strengthen(v)
    if action.level() < 35:
        action.mapscene()#领取通关奖励
        action.levelgift(30)  # 领取30级奖励
        action.muster()  # 武将出征并上阵，并突飞到30级
        #action.morra()#节节高
        gid, uid = action.general(25)#获取三级装备，再次强化，并给武将穿戴上
        for i in uid:
            for etype, v in i.items():
                action.strengthen(v)
                action.eqip(gid, v, etype)
            action.saodang(2)  # 级失败退出
        for i in uid:
            for etype, v in i.items():
                action.strengthen(v)
                action.eqip(gid, v, etype)
        action.saodang(2)#30级失败退出从第二个图开始
    if action.level() < 50:
        for i in range(2):
            action.mainquest()#获取所有活动
        gid, uid = action.general(25)#获取25级需要穿戴的装备强化
        for i in uid:
            for etype, v in i.items():
                action.strengthen(v)
                action.eqip(gid, v, etype)
        action.muster()  # 再次突飞
        action.saodang(2)
        action.saodang1()
    # action.saodang1()
def chuan():
    with open('../users/dd.txt', 'r') as f:
        # with open('../users/duguyi.txt', 'r') as f:
        for i in f:
            if i.strip():
                name = i.split()[0]
                # name = i.split()[0]
                passwd = i.split()[1]
                addr = i.split()[2]
                #addr = 145
                try:
                    lockpwd = i.split()[3]
                except:
                    lockpwd = None
                #addr = 150
                t1 = threading.Thread(target=act, args=(name, passwd, addr))
                q.put(t1)
chuan()
while not q.empty():
        thread = []
        for i in xrange(200):
            try:
                thread.append(q.get_nowait())
            except:
                pass
        for i in thread:
            i.start()
            # i.join()
        for i in thread:
           i.join()
