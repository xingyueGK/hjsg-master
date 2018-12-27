#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/17 10:28
# @Author  : xingyue
# @File    : caikuang.py


from task.base import SaoDangFb
import  time,threading
import os,json
class task(SaoDangFb):
    def caikuang(self):
        """银币矿"""
        mineinfo = self.action(c='mine', m='index')
        dateline = mineinfo['dateline']
        log = mineinfo['log']
        if log:
            log_dateline = log['dateline']
            lasttime = int(dateline) - int(log_dateline)
            if lasttime > 14400:
                self.action(c='mine', m='get_silver', s=mineinfo['log']['site'])
                self.action(c='mine', m='give_up')
                for i in range(3, 5):
                    mineinfo = self.action(c='mine', m='index', p=i)['list']
                    for l in mineinfo:
                        if l['status'] == 0:
                            self.action(c='mine', m='caikuang', p=l['page'], id=l['id'], t=l['type'])
                            exit(2)
        else:
            for i in range(3, 5):
                mineinfo = self.action(c='mine', m='index', p=i)['list']
                for l in mineinfo:
                    if l['status'] == 0:
                        self.action(c='mine', m='caikuang', p=l['page'], id=l['id'], t=l['type'])
                        exit(2)

    def countrymine(self):
        """国家矿"""
        try:
            mineinfo =  self.action(c='countrymine', m='index')
            dateline = mineinfo['dateline']
            log = mineinfo['log']
            times = log['times']
            p = log['page']
            s = log['site']
            t = log['type']
            fukuangstatus = log['site']  # 为空说明没有下矿，反之已经占领矿
        except:
            print '未加入国家，或是等级不足'
            exit()
        if times == '0' and fukuangstatus == '0':
            print self.user,'未占矿，剩余次数为0'
            exit(1)
        elif times == '0' and fukuangstatus != '0':
            # 收取占领的矿
            lasttime = self.get_countrymine_info(p,s,t)
            if lasttime == 0:
                print self.user,'收矿'
                self.p(self.action(c='countrymine', m='get_reward', s=s))
                print '退出'
                exit(2)
            elif lasttime < 120:
                time.sleep(lasttime)
                print '时间未到，等待%s s'%lasttime
                self.p(self.action(c='countrymine', m='get_reward', s=s))
                print '退出'
                exit(2)
            else:
                print '时间未到，等待 %ss'%lasttime
        elif times != "0" and fukuangstatus != '0':
            lasttime = self.get_countrymine_info(p, s, t)
            if lasttime == 0:
                self.p(self.action(c='countrymine', m='get_reward', s=s))
                for i in range(10, 0, -1):
                    mineinfo = self.action(c='countrymine', m='index', p=i)['list']
                    for l in mineinfo:
                        if l['status'] == 0:
                            status = self.action(c='countrymine', m='caikuang', p=i, id=l['id'], t=l['type'])
                            if status['status'] != 1:
                                continue
                            else:
                                print '占矿'
                    #             exit(3)
        else:
            for i in range(10, 0, -1):
                mineinfo = self.action(c='countrymine', m='index', p=i)['list']
                for l in mineinfo:
                    if l['status'] == 0:
                        status = self.action(c='countrymine', m='caikuang', p=i, id=l['id'], t=l['type'])
                        if status['status'] != 1:
                            continue
                        else:
                            print '占矿'
    def countryCaiKuang(self,p,id,t):
        """开采国家矿"""
        self.action(c='countrymine', m='caikuang', p=p, id=id, t=t)
    def get_countrymine_info(self,p,id,t):
        """获取信息采矿剩余时间信息"""
        result = self.action(c='countrymine', m='get_countrymine_info', p=p, id=id, t=t)
        if result['status'] ==1:
            return result['info']['time']

    def robfukuang(self, username, countryname):  # 打劫周年礦城
        self.action(c='fukubukuro', m='index')
        self.action(c='fukubukuro', m='get_mine_discription')
        mineinfo = self.action(c='fukubukuro', m='mine')
        robtimes = mineinfo['log']['robtimes']  # 打劫次数
        dateline = mineinfo['dateline']
        log = mineinfo['log']
        times = log['times']
        fukuangstatus = log['site']
        print '剩余打劫次数为{times}'.format(times=times)
        if robtimes == "0" and fukuangstatus == "0":

            exit(1)
        elif robtimes != "0" and fukuangstatus == "0":
            for page in range(10, 0, -1):
                try:
                    info = self.action(c='fukubukuro', m='mine', p=page)['list']
                    for item in info:
                        try:
                            if item['status'] == 1 and item['country'] in countryname:
                                print '打劫'
                                status = self.action(c='fukubukuro', m='loot_mine', p=item['page'], id=item['id'],
                                                     t=item['type'])
                                if status['status'] != 1:
                                    continue
                                else:
                                    exit(3)
                        except Exception as e:
                            print 'aaaaaaaaaaaaaa', e
                except Exception as e:
                    print 'wwwwwwwwwww', e
        else:
            print '收矿'
            self.zhounianfukuang(username)

if __name__ == '__main__':
    def act(user,apass,addr):
        action = task(user,apass,addr)
        action.countrymine()
    filepath = os.path.dirname(os.path.abspath(__file__))
    cont = ['alluser.txt']
    for t in cont:
        with open('%s/users/%s'%(filepath,t),'r') as f:
            for i in f:
                if i.strip() and not i.startswith('#'):
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    addr = 150
                    t1 = threading.Thread(target=act, args=(name,passwd,addr))
                    t1.start()