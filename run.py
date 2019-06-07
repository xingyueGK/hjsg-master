#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/21 11:15
# @Author  : xingyue
# @File    : run.py

#运行方法

import threading
import os,time

from task.base import  SaoDangFb
from task.talent import  Talent
from task.hero_soul import  DragonBoat
from task.glory_front import  glory_front

class run(SaoDangFb,Talent):
    #'天赋卷轴'
    pass

class duanwu(SaoDangFb,DragonBoat):
    '龙舟比赛'
    pass
class dongxizhanxian(SaoDangFb,glory_front):
    '东西战线'
    pass
if __name__ == '__main__':
    def act(user, apass, addr):
        action = dongxizhanxian(user, apass, addr)
        action.zhanxian()
    filepath = os.path.dirname(os.path.abspath(__file__))
    # cont = ['21user.txt', 'autouser.txt','gmnewyear.txt', 'user.txt', 'alluser.txt']
    cont = ['user.txt']
    for t in cont:
        with open('%s/users/%s' % (filepath, t), 'r') as f:
            for i in f:
                if i.strip() and not i.startswith('#'):
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    # addr = 147
                    t1 = threading.Thread(target=act, args=(name, passwd, addr))
                    t1.start()
                    t1.join()
                    time.sleep(0.2)
