#!/usr/bin/env python
#-*- coding:utf-8 -*-
import time
from base import SaoDangFb

class muster(SaoDangFb):
    def muster(self):
        index = self.action(c='muster',m='index',page=1,perpage=999)
        list = index['list']#武将列表以及创带装备列表
        equipments = index['equipments']#未穿戴的列表
    def cultivate(self):#培养首页
        self.action(c='cultivate',m='index')#
        self.action(c='cultivate', m='roll', gid=251000019943, mode=1)
        self.action(c='cultivate',m='giveup',gid=251000019943)
        self.action(c='cultivate',m='save',gid=251000019943)