#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/18 17:44
# @Author  : xingyue
# @File    : oversea.py

from task.base import SaoDangFb
import threading
import json, time, os,random
import redis

tasks = {}
lock = threading.RLock()

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
_redis = redis.StrictRedis(connection_pool=pool)


class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.arg = args

    def run(self):
        self.func(*self.arg)


def timesCount(name, passwd, addr):  # 返回贸易次数
    global lock
    task = SaoDangFb(name, passwd, addr)
    result = task.action(c='holiday_seatrade', m='index')
    try:
        times = result['info']['times']
    except:
        times = 0
    key = 'holiday_seatrade' + str(addr)
    TIME = time.strftime("%Y-%m-%d")
    extime = TIME + " 23:59:59"
    lock.acquire()
    timeArray = time.strptime(extime, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    lock.release()
    _redis.hset(key, name, times)
    _redis.expireat(key, timeStamp)


def jierihaiyun(name, passwd, addr, flag=True):  # 节日海外贸易
    '''
    :param name:
    :param passwd:
    :param addr:
    :param flag: 是否刷金色船
    :return:
    '''
    task = SaoDangFb(name, passwd, addr)
    task.action(c='message', m='index')
    index = task.action(c='holiday_seatrade', m='index')
    if index['btn_status'] == 1 :#
        #已经购买，还没有来级的开始就退出了
        try:
            get_list_by_country = task.action(c='holiday_seatrade', m='get_list_by_country')
            if get_list_by_country['teamid'] == "0":
                #如果没有队伍择组队
                list_country = get_list_by_country['list']
                if not list_country:
                    #表示一个队伍没有
                    status = task.action(c="holiday_seatrade", m='join_team', id=0, place=1, site=1, page=1)
                elif len(list_country)<4:
                    for i in range(1,5):
                        if i not in list_country:
                            status = task.action(c="holiday_seatrade", m='join_team', id=0, place=i, site=1, page=1)
                # 加入贸易队伍，每页有四个框，为place：1-4，每个框有两个位置site:1-2，页数为page:1-5默认为1即可，
                # if list_country:
                #     status = task.action(c="holiday_seatrade", m='join_team', id=0, place=3, site=2, page=4)
                # else:
                #     status = task.action(c="holiday_seatrade", m='join_team', id=0, place=4, site=2, page=1)
                a = task.action(c="holiday_seatrade", m='trade', v=0)  # 开启
                task.p(name, a) # 开启
                return
            else:
                #有队伍直接开始
                a = task.action(c="holiday_seatrade", m='trade', v=0)  # 开启
                task.p(name, a) # 开启
                return
        except:
            print '获取组队列表错误%s'%name
    ite = task.action(c='holiday_seatrade', m='item_list')

    try:
        renew = ite['member_info']['renew']
    except:
        try :
            exit_flag = False
            for page in range(1,5):
                get_list_by_country = task.action(c='holiday_seatrade', m='get_list_by_country',page = page)
                list_country = get_list_by_country['list']
                if not list_country:
                    # 表示一个队伍没有
                    status = task.action(c="holiday_seatrade", m='join_team', id=0, place=1, site=1, page=page)
                    break
                elif len(list_country) < 4:
                    for i in range(1, 5):
                        if i not in list_country:
                            status = task.action(c="holiday_seatrade", m='join_team', id=0, place=i, site=1, page=page)
                            break
                            exit_flag = True
                if exit_flag:
                    break
            a = task.action(c="holiday_seatrade", m='trade', v=0)  # 开启
            task.p(name, a)  # 开启
            return
        except:
            print name
    # 购买粮食，花费银币的，id=1为粮食，id2-5为花费元宝的玛瑙等
    if int(index['info']['times']) > 0 and int(renew) <= 3:
        while True:
            try:
                if flag:
                    info = task.action(c='holiday_seatrade', m='renew', v=2018061901)
                    if info['status'] == -4:
                        return
                    time.sleep(3)
                    print json.dumps(info)
                    if info['reward'] > '3':  # and info['renew'] < '880':#封顶200元宝，如果不限制元宝要注释renew
                        time.sleep(random.random())
                        task.action(c='holiday_seatrade', m='buy_item', id=int(info['reward']))
                        break
                else:
                    task.action(c='holiday_seatrade', m='buy_item', id=1)
                    break
            except Exception as e:
                break
        # 组队 ，检查是否有对， 有则加入，没有则创建 ，开始贸易
        # 1获取组队列表
        try:
            exit_flag = False
            for page in range(1, 5):
                get_list_by_country = task.action(c='holiday_seatrade', m='get_list_by_country', page=page)
                list_country = get_list_by_country['list']
                if not list_country:
                    # 表示一个队伍没有
                    status = task.action(c="holiday_seatrade", m='join_team', id=0, place=1, site=1, page=page)
                    break
                elif len(list_country) < 4:
                    for i in range(1, 5):
                        if i not in list_country:
                            status = task.action(c="holiday_seatrade", m='join_team', id=0, place=i, site=1, page=page)
                            break
                            exit_flag = True
                if exit_flag:
                    break
            a = task.action(c="holiday_seatrade", m='trade', v=0)  # 开启
            task.p(name, a)  # 开启
            return
        except:
            print name
    elif  int(index['info']['times']) > 0 and int(renew) > 3:
        task.action(c='holiday_seatrade', m='buy_item', id=renew)
        try:
            exit_flag = False
            for page in range(1, 5):
                get_list_by_country = task.action(c='holiday_seatrade', m='get_list_by_country', page=page)
                list_country = get_list_by_country['list']
                if not list_country:
                    # 表示一个队伍没有
                    status = task.action(c="holiday_seatrade", m='join_team', id=0, place=1, site=1, page=page)
                    break
                elif len(list_country) < 4:
                    for i in range(1, 5):
                        if i not in list_country:
                            status = task.action(c="holiday_seatrade", m='join_team', id=0, place=i, site=1, page=page)
                            break
                            exit_flag = True
                if exit_flag:
                    break
            a = task.action(c="holiday_seatrade", m='trade', v=0)  # 开启
            task.p(name, a)  # 开启
            return
        except:
            print name
    index = task.action(c='holiday_seatrade', m='index')
    print '{0} {1} 剩余贸易次数：{2}'.format(name,addr, index['info']['times'])


def makeTask(name, passwd, addr):
    t1 = MyThread(timesCount, args=(name, passwd, addr))
    t1.start()


def main(file, flag,FlushCount=40,addr=None,):
    """
    :param FlushCount: 每次同时刷船次数,默认1个
    """
    filepath = os.path.dirname(os.path.abspath(__file__))
    with open('%s/users/%s' % (filepath, file), 'r') as f:
        for i in f:
            if i.strip():
                user = i.split()[0]
                passwd = i.split()[1]
                # if addr:
                #     addr = addr
                # else:
                #     addr = i.split()[2]
                addr = i.split()[2]
                # addr = 148
                key = 'holiday_seatrade' + str(addr)
                if _redis.hget(key, user):
                    userTimes = _redis.hget(key, user)
                    print 'username {0} 还剩 {1}'.format(user, userTimes)
                    if int(userTimes) <= 0:
                        continue
                    if FlushCount > 0:
                        time.sleep(random.random()
                                )
                        t1 = threading.Thread(target=jierihaiyun, args=(user, passwd, addr, flag))
                        t1.start()
                        FlushCount -= 1
                        times = int(userTimes) - 1
                        _redis.hset(key, user, times)
                    else:
                        break
                else:
                    makeTask(user, passwd, addr)


if __name__ == '__main__':
    _redis.flushall()
    for i in range(300):
        if i % 30 == 0:
            _redis.flushall()
        # main('haiyun.txt', True,200)
        # main('dc.txt', True,20)
        # main('dc.txt', True,20)
        # main('149cnm.txt', True,50)
        main('didui.txt',True, 50)
        # main('gmhy1.txt', True, 50,)
        # main('gmhy.txt', True, 20,)
        # main('21user.txt', True, 50,)
        time.sleep(random.randint(10, 19))