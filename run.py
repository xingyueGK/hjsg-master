#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/21 11:15
# @Author  : xingyue
# @File    : run.py

#运行方法

import threading
import os,time,apscheduler


from task.base import  SaoDangFb
from task.talent import  Talent
from task.hero_soul import  DragonBoat,GoBoat
from task.glory_front import  glory_front
from task.caomujiebing import Flag
from task.autoCountryBanquet import autoCountryBanquet
class run(SaoDangFb,Talent):
    #'天赋卷轴'
    pass

class duanwu(SaoDangFb,DragonBoat):
    #'龙舟比赛'
    pass
class longzhou(SaoDangFb,GoBoat):
    pass
class dongxizhanxian(SaoDangFb,glory_front):
    #'东西战线'
    pass
class banquet(SaoDangFb,autoCountryBanquet):
    pass

class cmjb(SaoDangFb,Flag):
    pass

if __name__ == '__main__':
    s1 = threading.Semaphore(3)
    def act(user, apass, addr):
        s1.acquire()
        action = dongxizhanxian(user, apass, addr)
        if action.level()< 150:
            s1.release()
            return False
        action.zhanxian(s1)
        s1.release()

    def flag(user, apass, addr):
        s1.acquire(blocking=False)
        action = cmjb(user, apass, addr)
        schedule = action.get_today_schedule()
        if schedule['status'] == -2:
            print schedule['msg']
            exit(1)
        elif schedule['status'] != 1:
            print schedule['msg']
            exit(1)
        try:
            self_server = schedule['data']['self_server']
        except:
            exit(3)
        get_enter_list = action.get_enter_list(self_server)
        enter_cd = get_enter_list['enter_cd']
        print enter_cd
        time.sleep(enter_cd)
        action.enter(self_server,1)
        s1.release()

    def lz(user, apass, addr):
        s1.acquire()
        action = longzhou(user, apass, addr)
        # action.buytimes(1)
        action.longzhou()
        action.meter_reward()
        # action.bug_meter_reward()
        s1.release()
    def guoyan(user, apass, addr):
        s1.acquire()
        action = banquet(user, apass, addr)
        action.jion_team()
        s1.release()
    filepath = os.path.dirname(os.path.abspath(__file__))
    # cont = ['21user.txt', 'autouser.txt','gmnewyear.txt', 'user.txt', 'alluser.txt']
    cont = ['xing.txt']
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
      