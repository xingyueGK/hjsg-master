#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/7 17:53
# @Author  : xingyue
# @File    : sifu.py

import requests
import time
import json
import threading
import random
import  sys
import  redis
import os
reload(sys)
sys.setdefaultencoding('utf-8')
headers = {
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Upgrade-Insecure-Requests':'1',
    'Content-Type':'application/json',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

class TokenErr(Exception):
    pass


class SaoDangFb(object):
    def  __init__(self,user,passwd,num):
        #随机请求参数
        self.num = num
        self.user = user
        self.passwd = passwd
        self.rand = int(time.time()*1000)
        self.token_uid = '210000353508'
        self.token = self.get_token(self.num, self.user, self.passwd)
        #POST基础URL地址
        self.url = 'http://s{0}.game.shaline8.com:8101/index.php?v=0&channel=150&lang=zh-cn&token={1}&token_uid={2}&rand={3}&'.format(self.num,self.token,self.token_uid,self.rand)
    @staticmethod
    def get_token(num, user, passwd):

        url = 'http://s{num}.game.shaline8.com:8101/index.php?c=login&&m=user&u={user}&p={passwd}&v=2018083101&token=&channel=11&lang=zh-cn&rand=150959405499450'.format(
            num=num, user=user, passwd=passwd)
        pool = redis.ConnectionPool(host='localhost', port=6379,db=0)
        _redis = redis.StrictRedis(connection_pool=pool)
        try:
            if _redis.hget(num,user):
                token = _redis.hget(num,user)
                login = 'http://s{num}.game.shaline8.com:8101/index.php?c=member&m=index&v=0&token={token}&channel=150&lang=zh-cn&rand=150959405499450'.format(
                    num=num, token=token)
                r = requests.get(login)
                print r.text
                if r.text == '403':
                    raise TokenErr('token expire')
                else:
                    return token
            else:
                raise TokenErr('token expire')
        except TokenErr:
                try:
                    result= requests.get(url).json()
                    if result['status'] == 1:
                        token = result['token']
                        _redis.hset(num,user,token)
                        return token
                    else:
                        print user,'账号密码不对'
                        exit(2)
                except Exception as e:
                    print e

    def post_url(self,data):
        self.data = ''
        for k,v in data.items():
            self.data += '&%s=%s'%(k,v)
        self.url = 'http://s%s.game.shaline8.com:8101/index.php?%s&v=2017111501&v=2017111501&channel=11&imei=NoDeviceId&platform=android&lang=zh-cn&token=%s&token_uid=%s&rand=%s' % (
            self.num, self.data, self.token, self.token_uid, self.rand)
        keep_request = True
        while keep_request:
            try:
                r = requests.post(self.url,headers=headers,timeout=20)
                keep_request = False
                if r.status_code != 200:
                    r = requests.post(self.url, headers=headers,timeout=20)
                    return r.json(encoding="UTF-8")
                else:
                    return r.json( encoding="UTF-8")
            except Exception as e:
                print e
                time.sleep(0.3)
    def action(self,**kwargs):
        """动作参数m={'index':'获取基础账号密码等信息',‘get_monster_list’：“获取副本怪物列表信息”}
        """
        action_data = kwargs
        serverinfo = self.post_url(action_data)
        return serverinfo
    def saodang(self, num=12):  # 攻击小兵
        memberindex = self.action(c='member', m='index')
        missionlevel = int(memberindex['missionlevel'])
        missionsite = int(memberindex['missionsite'])
        missionstage = int(memberindex['missionstage'])
        map = self.action(c='map', m='get_mission_list')
        exit_code = 1
        if exit_code == 1:
            for level in range(missionlevel, num):  # 遍历每一个图
                print '开始攻击第 %s 个图' % level
                self.action(c='map', m='get_scene_list', l=level)

                site = len(self.action(c='map', m='get_scene_list', l=level)['list']) + 1
                for i in range(missionstage, site):  # 遍历关卡图次数
                    print '关卡', i
                    status = 1
                    for id in range(1, 11):  # 遍历10个小兵
                        try:
                            # 获取首杀状态，1为首杀，-1为已经击杀
                            first = self.action(c='map', m='mission', l=level, s=i, id=id)['info']['first']
                        except KeyError as e:
                            continue
                        if first == 1 and status == 1:  #
                            status = self.action(c='map', m='action', l=level, s=i, id=id)['status']
                            print status
                            if first == 1 and status == -5:
                                print '退出'
                                exit_code = 2
                                return exit_code
                        else:
                            print '已经击杀'
        else:
            print 'dabuduole'
            return
    def tufei(self, name, level):  # 对武将突飞
        try:
            gid = ''
            practtice_info = self.action(c='practice', m='index')
            # 初期都是两个训练槽位，
            pid = practtice_info['place']['1']['id']
            self.action(c='practice', m='practice_stop ', pid=pid)  # 终止训练
            wujiang_index = self.action(c='muster', m='index', page=1, perpage=999)['list']
            for k, v in wujiang_index.items():
                if v['name'] == name:  # 蔡文姬
                    print u'武将出征', name
                    result = self.action(c='muster', m='go_battle', gid=v['id'])
                    print result['status']
                    gid = v['id']
            status = 1
            index_info = self.action(c='practice', m='index')
            # 训练武将，
            self.action(c='practice', m='practice_start', gid=gid, pid=pid, type=2)
            freetimes = index_info['freetimes']  # 突飞卡
            for k, v in index_info['list'].items():
                if v['name'] == name:
                    isturn = v['isturn']  # 武将师是否到转生级别
                    wjlevel = v['level']
            print '武将等级', wjlevel
            print freetimes
            while status == 1 and freetimes != '0':  # 队伍将进行突飞
                if int(isturn) == 1 and int(wjlevel) <= level:
                    print '武将转生'
                    self.action(c='practice', m='turn', gid=gid)
                self.action(c='practice', m='mop', times=100, gid=gid)
                self.action(c='practice', m='mop', times=50, gid=gid)
                self.action(c='practice', m='mop', times=10, gid=gid)
                self.action(c='practice', m='mop', times=5, gid=gid)
                index_info = self.action(c='practice', m='index')
                freetimes = index_info['freetimes']
                info = self.action(c='practice', m='go_leap', gid=gid)  # 武将突飞一次
                status = info['status']
        except:
            pass
    def advance(self):
        result=self.action(c='advanced', m='index')
        for item in result['list']:
            gid=item['id']
            for i in range(6):
                for t in range(1,5):
                    for w in range(6):
                        print self.action(c='advanced',m='level_up',gid=gid,t=t)
                self.p(self.action(c='advanced', m='start_advanced', gid=gid))
    def change(self):
        self.action(c='tavern', m='buy', generalid=1002, num=100000)
    def herothrone(self):  # 英雄王座
        print '英雄王座'
        try:
            vip = self.action(c='member', m='index')['vip']
            print vip
            if int(vip) < 19:
                # status = self.action(c='herothrone', m='index')['status']
                # print status
                # if status != 1:
                #     return None
                for i in range(3):
                    self.action(c='herothrone', m='start')  # 开始王座
                    # 攻击:
                    while True:
                        flag = self.action(c='herothrone', m='action')['status']
                        print  '攻击王座副本'
                        if flag == -2:
                            break
            else:
                self.action(c='herothrone', m='index')
                for i in range(3):
                    self.action(c='herothrone', m='start')  # 开始王座
                    self.action(c='herothrone', m='end_battle')
                    self.action(c='herothrone', m='go_back')

        except Exception as e:
            print e
def task():
    action = SaoDangFb('kankan', '123456', 1)
    # action.herothrone()
    action.saodang(17)
    # count = 0
    # while True:
    #     count += 1
    #     print count
    #     threading.Thread(target=action.change).start()
if __name__ == '__main__':
    # action = SaoDangFb('kankan','123456',1)
    # for i in ['韩信', '项羽', '李广',
    #           '廖化', '鲁肃', '小乔', '曹洪',
    #           '韩遂', '张梁', '张角', '周泰',
    #           '周泰', '张梁', '张角', '周泰'
    #           ]:
    #     action.tufei(i, 300)
    task()