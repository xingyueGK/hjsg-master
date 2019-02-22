# -*- coding: utf-8 -*-
# @Time    : 2019/2/1 13:44
# @Author  : xingyue
# @File    : newyear_city.py


from task.base import SaoDangFb
import threading
import os,time
import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
_redis = redis.StrictRedis(connection_pool=pool)
lock = threading.RLock()

class task(SaoDangFb):

    def index(self):
        OCCUPY = 'newyear:occupy' + str(self.num)
        ROB = 'newyear:rob' + str(self.num)
        if _redis.hget(OCCUPY, self.user) and _redis.hget(ROB, self.user):
            occupy = _redis.hget(OCCUPY, self.user)
            rob = _redis.hget(ROB, self.user)
            print 'username {0} 占矿次数还剩 {1}，打劫次数还剩 {2}'.format(self.user, occupy, rob)
            return occupy, rob
        else:
            TIME = time.strftime("%Y-%m-%d")
            extime = TIME + " 23:59:59"
            lock.acquire()
            timeArray = time.strptime(extime, "%Y-%m-%d %H:%M:%S")
            timeStamp = int(time.mktime(timeArray))
            lock.release()
            self.action(c='newyear_act',m='index')
            city_index = self.action(c='newyear_act',m='city_index')
            occupy = city_index['occupy']
            rob = city_index['rob']
            _redis.hset(OCCUPY,self.user,occupy)
            _redis.expireat(OCCUPY, timeStamp)
            _redis.hset(ROB, self.user, occupy)
            _redis.expireat(ROB, timeStamp)
            return occupy, rob

    def occupy_city(self,flag='first'):#开始采矿
        global lock
        print '开始占领城市',flag
        #城市人数 5 8 15 20 30
        OCCUPY = 'newyear:occupy' + str(self.num)

        citylist = [6,11]
        for id in citylist:
            print '遍历城市',id
            result = self.action(c='newyear_act', m='city', id=id)
            now_num = result['now_num']
            limit_num = result['city']['limit_num']
            if int(now_num) < int(limit_num):#表示没有满员
                print '准备占领城市',id
                lock.acquire()
                status = self.action(c='newyear_act', m='occupy_city', id=id)
                _redis.hincrby(OCCUPY, self.user, -1)
                lock.release()
                if status['status'] ==1:
                    print '占领成功'
                    exit(1)
                else:
                    print '占领失败，重新占领'
                    self.occupy_city(flag='reset')
                    return None
        self.rob()
    def harvest(self,id):#开始收矿
        result = self.action(c='newyear_act', m='city', id=id)
        if result['remain_time'] < 30:
            print '收获奖励'
            status = self.action(c='newyear_act', m='harvest', id=id)
            self.occupy_city()
        else:
            print self.user,'占矿剩余时间',result['remain_time']
        exit(1)
    def rob(self):
        ROB = 'newyear:rob' + str(self.num)
        citylist = [6,11]
        topname = ['杰克斯派罗', '冯慕青', '独行侠', '汪东城', '恋凡琼', '独孤怡']
        for id in citylist:
            result = self.action(c='newyear_act', m='occupy_list', id=id)
            for item in result['list']:
                if item['nickname'] not in  topname and item['reward']['num2'] >= 16:
                    uid = item['id']
                    cid = id
                    status = self.action(c='newyear_act',m='rob',id=uid,cid=cid)
                    _redis.hincrby(ROB, self.user, -1)
                    if status['status'] == 1:
                        return None
                    else:
                        continue
    def run(self):
        try:
            occupy,rob = self.index()
            if occupy > "0":#剩余占领次数不为0，继续占领
                self.action(c='newyear_act', m='index')
                city_index = self.action(c='newyear_act', m='city_index')
                for item in city_index['city']:
                    #遍历完成后没有为1项，表示没有占领任何矿
                    if item['is_on'] == 1:
                        id = item['id']
                        self.harvest(id)
                self.occupy_city()
            elif rob > '0':
                print '没有次数，查看是否占矿未收'
                self.action(c='newyear_act', m='index')
                city_index = self.action(c='newyear_act', m='city_index')
                for item in city_index['city']:
                    if item['is_on'] == 1:
                        id = item['id']
                        self.harvest(id)
                self.rob()
            else:
                print '没有次数，查看是否占矿未收'
                self.action(c='newyear_act', m='index')
                city_index = self.action(c='newyear_act', m='city_index')
                for item in city_index['city']:
                    if item['is_on'] == 1:
                        id = item['id']
                        self.harvest(id)
        except Exception as e:
            print e
if __name__ == '__main__':
    def act(user,apass,addr):
        action = task(user,apass,addr)
        action.run()
    filepath = os.path.dirname(os.path.abspath(__file__))
    cont = ['self.txt']
    for t in cont:
        with open('%s/users/%s'%(filepath,t),'r') as f:
            for i in f:
                if i.strip() and not i.startswith('#'):
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    t1 = threading.Thread(target=act, args=(name,passwd,addr))
                    t1.start()