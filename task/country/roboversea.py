#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/29 11:49
# @Author  : xingyue
# @File    : roboversea.py

#节日海运打劫
from task.base import SaoDangFb
import time, threading
import os, json,hashlib

from Queue import  Queue

import redis


pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
_redis = redis.StrictRedis(connection_pool=pool)



class task(SaoDangFb):
    def rob(self, name, user):  # 海运打劫
        # publis_name = 'roboversea'
        # # name 就是打劫的国家[list]
        # robtimes = 1
        # while robtimes > 0:
        #     time.sleep(0.3)
        #     index_result = self.action(c='overseastrade', m='index')
        #     try:
        #         robtimes = int(index_result['info']['robtimes'])  # 获取打劫次数
        #         msg = '剩余打劫次数{robtimes}'.format(robtimes=robtimes)
        #         print msg
        #         _redis.publish(publis_name,msg)
        #     except Exception as e:
        #         print e
        #     try:
        #         refresh_result = self.action(c='overseastrade', m='refresh', p=1)['team']  # 获取刷新船信息
        #         if refresh_result['allpage'] > 1:  # 船页数大于1页需要遍历
        #             for i in range(refresh_result['allpage']):
        #                 team_list = self.action(c='overseastrade', m='refresh', p=i + 1)['team']['list']
        #                 for team in team_list:
        #                     if team['country_name'] in name:
        #                         id = team['id']
        #                         rob_result = self.action(c='overseastrade', m='rob', id=id)
        #                         msg = json.dumps(rob_result)
        #                         print msg
        #                         _redis.publish(publis_name, msg)
        #         else:
        #             team_list = refresh_result['list']
        #             for team in team_list:
        #                 if team['country_name'] in name:
        #                     id = team['id']
        #                     rob_result = self.action(c='overseastrade', m='rob', id=id)
        #                     msg = json.dumps(rob_result)
        #                     print msg
        #                     _redis.publish(publis_name,msg)
        #     except Exception as e:
        #         print e
        robkey = "zykj"
        uid = self.get_act()['uid']
        publis_name = 'roboversea'
        # name 就是打劫的国家[list]
        ip149 = [i for i in range(145, 150)]
        ip21 = [21, 22, 25, 26, 29, 30]
        worldkey = 'set:worldstrade:{addr}'.format(addr=149)
        ip = int(self.num)
        oip = None
        if ip in ip149:
            print '大区为149'
            oip = 149
            worldkey = 'set:worldstrade:{addr}'.format(addr=149)
        elif ip in ip21:
            print '大区为 21'
            oip = 21
        robtimes = 1
        while robtimes > 0:
            index_result = self.action(c='overseastrade', m='index')
            try:
                robtimes = int(index_result['info']['robtimes'])  # 获取打劫次数
                msg = '剩余打劫次数{robtimes}'.format(robtimes=robtimes)
                print msg
            except Exception as e:
                print e
            try:
                teamid = _redis.rpop('teamid{oip}'.format(oip=oip))
                print '获取Team_id',teamid
                if teamid:
                    while True:
                        key = "world_rob" + uid + robkey + teamid
                        authorization = hashlib.md5(key).hexdigest()
                        print authorization,teamid
                        rob_result = self.action(c='overseastrade', m='world_rob',
                                                 body={"id": teamid, "authorization": authorization})
                        msg = json.dumps(rob_result)
                        print msg
                        if rob_result['status'] != 1:
                            break
                else:
                    print '还没有船'
                _redis.publish(publis_name, msg)
            except Exception as e:
                print e
if __name__ == '__main__':
    def dajie(user, apass, addr):
        action = task(user, apass, addr)
        action.rob(['体检了', '8523', '英雄', '是你学姐', '杰克傻bi','杰克吃翔'], user)


    filepath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    cont = ['xing.txt']
    for t in cont:
        with open('%s/users/%s' % (filepath, t), 'r') as f:
            for i in f:
                if i.strip():
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    t1 = threading.Thread(target=dajie, args=(name, passwd, addr))
                    t1.start()
                    # t1.join()
                    time.sleep(0.2)
        time.sleep(60)