#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/10 10:37
# @Author  : xingyue
# @File    : task.py


from task.base import SaoDangFb
import  time,threading
import os,json
class task(SaoDangFb):
    def worldboss(self):  # 世界boss领取
        # 银币鼓舞
        now_time = time.strftime('%H:%M:%S')
        if '12:00:00' < now_time < '12:15:00':
            boss_info = self.action(c='worldboss', m='index')
            print boss_info
            countdown = boss_info['countdown']
            powerup = boss_info['powerup']
            if powerup != 200:
                for i in range(10):
                    self.action(c='worldboss', m='powerup', gold=0)
            while countdown > 0:
                # 获取boss退出世界
                countdown = boss_info['countdown']
                self.action(c='worldboss', m='battle')
                time.sleep(61)
            if countdown == 0:
                self.action(c='worldboss', m='reward')  # reward领取奖励
        else:
            print '世界boos未开始'
def run(user,apass, addr):
    action = task(user,apass, addr)
    action.worldboss()
if __name__ == '__main__':
    filepath = os.path.dirname(os.path.abspath(__file__))
    cont = ['boss.txt']
    for t in cont:
        with open('%s/users/%s'%(filepath,t),'r') as f:
            for i in f:
                if i.strip() :
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    t1 = threading.Thread(target=run, args=(name, passwd, addr))
                    t1.start()
                    # t1.join()
                    time.sleep(0.2)
        time.sleep(60)