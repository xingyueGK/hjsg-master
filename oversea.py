#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/18 17:44
# @Author  : xingyue
# @File    : oversea.py

from task.base  import SaoDangFb
import  threading
import json,time,os
import redis

tasks ={}
lock = threading.RLock()

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
_redis = redis.StrictRedis(connection_pool=pool)
class MyThread(threading.Thread):
    def __init__(self,func,args=()):
        super(MyThread,self).__init__()
        self.func = func
        self.arg = args
    def run(self):
        self.func(*self.arg)

def timesCount(name,passwd,addr):#返回贸易次数
    task = SaoDangFb(name,passwd,addr)
    result = task.action(c='overseastrade',m='index')
    try:
        times = result['info']['times']
    except:
        times = 0
    key = 'overseastrade' + str(addr)
    TIME = time.strftime("%Y-%m-%d")
    extime = TIME + " 23:59:59"
    timeArray = time.strptime(extime, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    _redis.hset(key,name,times)
    _redis.expireat(key, timeStamp)

def jierihaiyun(name, passwd, addr,flag=True):  # 节日海外贸易
    '''
    :param name:
    :param passwd:
    :param addr:
    :param flag: 是否刷金色船
    :return:
    '''
    task = SaoDangFb(name, passwd, addr)
    task.action(c='message', m='index')
    index = task.action(c='overseastrade', m='index')
    #购买粮食，花费银币的，id=1为粮食，id2-5为花费元宝的玛瑙等
    if int(index['info']['times']) > 0:
        while True:
            try:
                if flag:
                    info = task.action(c='overseastrade', m='renew', v=2018061901)
                    print json.dumps(info)
                    if info['reward']> '3': #and info['renew'] < '880':#封顶200元宝，如果不限制元宝要注释renew
                       task.action(c='overseastrade', m='buy_item', id=int(info['reward']))
                       break
                else:
                    task.action(c='overseastrade', m='buy_item', id=1)
                    break
            except Exception as e:
                break
        # 组队 ，检查是否有对， 有则加入，没有则创建 ，开始贸易
        # 1获取组队列表
        list_country = task.action(c='overseastrade', m='get_list_by_country', p=4)['list']

            # 加入贸易队伍，每页有四个框，为place：1-4，每个框有两个位置site:1-2，页数为page:1-5默认为1即可，
        if list_country:
            status = task.action(c="overseastrade", m='join_team', id=0, place=3, site=2, page=4)
        else:
            status = task.action(c="overseastrade", m='join_team', id=0, place=4, site=2, page=4)
        task.action(c="overseastrade", m='trade', v=0)  # 开启
    index = task.action(c='overseastrade', m='index')
    print '{0} 剩余贸易次数：{1}'.format(name,index['info']['times'])

def makeTask(name, passwd, addr):
    t1 = MyThread(timesCount, args=(name, passwd, addr))
    t1.start()
def main(file,addr,flag,FlushCount =40):
    """
    :param FlushCount: 每次同时刷船次数,默认1个
    """
    filepath = os.path.dirname(os.path.abspath(__file__))
    with open('%s/users/%s' % (filepath, file), 'r') as f:
        for i in f:
            if i.strip():
                user = i.split()[0]
                passwd = i.split()[1]
                key = 'overseastrade' + str(addr)
                if _redis.hget(key,user):
                    userTimes = _redis.hget(key,user)
                    print 'username {0} 还剩 {1}'.format(user, userTimes)
                    if int(userTimes) <= 0:
                        continue
                    if FlushCount >0:
                        t1 = threading.Thread(target=jierihaiyun, args=(user,passwd,addr,flag))
                        t1.start()
                        time.sleep(0.3)
                        FlushCount -= 1
                        times = int(userTimes) -1
                        _redis.hset(key,user,times)
                    else:
                        break
                else:
                    makeTask(user,passwd,addr)

if __name__ == '__main__':
    main('149gmjrhy.txt',149,True,10)