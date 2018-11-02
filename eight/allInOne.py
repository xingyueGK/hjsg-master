#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/31 11:06
# @Author  : xingyue
# @File    : allInOne.py

from task.base import SaoDangFb
import  time,threading
import os,json

class eight(SaoDangFb):
    def __init__(self, level, user, passwd, num):
        super(eight, self).__init__(user, passwd, num)
        self.level = level
    def muster(self):
        #所有将领数量
        muster=self.action(c='muster', m='index',page= 1,perpage=999)['list']
        return muster
    def reset(self):
        self.action(c='eight_diagram', m='reset_point')
        self.action(c='eight_diagram', m='level_index', level=self.level)  # level：八卦等级，分为1,2,3重

    def eight_index(self):
        now_level = self.action(c='eight_diagram', m='index')['now_level']
        level_index = self.action(c='eight_diagram', m='level_index', level=now_level)
        return level_index,now_level

    def pk(self):
        self.action(c='eight_diagram', m='pk', level=self.level)

    def matrix(self):
        #出征将领
        genral_dict = {}
        matrix_index = self.action(c='matrix', m='index')
        general = matrix_index['general']
        for k, v in general.items():
            name = v['name']
            genral_dict[name] = v['id']
        return genral_dict

    def use_matrix(self, mid=4):
        # boss固定4
        self.action(c='matrix', m='use_matrix', mid=mid)

    def update_matrix(self, uid1, uid2, uid3, uid4, uid5, mid=2):
        genral_info = self.matrix()
        lists2 = '%s,%s,%s,-1,%s,-1,-1,%s,-1' % (
            genral_info[uid1],
            genral_info[uid2],
            genral_info[uid3],
            genral_info[uid4],
            genral_info[uid5],
        )
        lists4 = '%s,-1,%s,-1,%s,-1,%s,-1,%s' % (
            genral_info[uid1],
            genral_info[uid2],
            genral_info[uid3],
            genral_info[uid4],
            genral_info[uid5],
        )
        if mid == 2:
            self.action(c='matrix', m='update_matrix', list=lists2, mid=mid)
        elif mid == 4:
            self.action(c='matrix', m='update_matrix', list=lists4, mid=mid)


def run(user,apass, addr):
    ei = eight(num=addr, user=user, passwd=apass, level=3)
    # ei.use_matrix(4)  # 使用固定阵法
    index,now_level = ei.eight_index()
    reset_times = int(index['reset_times'])
    point = index['cost']['point']
    print '%s 八卦等级 %s 当前位置%s 重置八卦次数%s'%(user,now_level,point,reset_times)
    if point == '9' and reset_times == 1:
        ei.reset()
    else:
        print '已经通关没有次数了'
        exit(1)
    for i in range(12):
        ei.pk()
    ei.use_matrix(4)
if __name__ == '__main__':
    print os.path.split(os.path.abspath(__file__))
    filepath = os.path.dirname(os.path.abspath(__file__))
    cont = ['eight.txt']
    for t in cont:
        with open('%s/users/%s'%(filepath,t),'r') as f:
            for i in f:
                if i.strip() :
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    t1 = threading.Thread(target=run, args=(name, passwd, addr))
                    t1.start()