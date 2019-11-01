#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/26 13:55
# @Author  : xingyue
# @File    : country_celery.py

#定时调度国家任务

from utils.scheduler import schdeuler
from utils.mylog import MyLog
from task.country.autoCountryBanquet import autoCountryBanquet
from task.base import SaoDangFb
import os,threading
import redis


class banquet(SaoDangFb,autoCountryBanquet):
    def a(self,r,job,job_id):
        index = self.index
        if index == 403:
            #如果账号异常就退出
            job.remove_job(job_id)
            return
        if int(index['info']['times']) > 0:
            if not self.join_team(r):
                #如果队伍创建失败，就退出任务
                job.remove_job(job_id)
                return
        else:
            print 'times is 0'
            job.remove_job(job_id)
    def run(self,r,job,job_id):
        job.add_job(self.a, 'interval', seconds=1, id=job_id,args=(r,job,job_id))

#实例化redis 实例对象
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.StrictRedis(connection_pool=pool)

s1 = threading.Semaphore(10)
l = threading.Lock()
log = MyLog(logpath='banquet',logname='banquet.log')
schdeuler =schdeuler(log)

def act(user, apass, addr,job,job_id,r):
    s1.acquire()
    action = banquet(user, apass, addr)
    action.run(r,job,job_id)
    s1.release()
filepath = os.path.dirname(os.path.abspath(__file__))
cont = ['banquetuser.txt']
# cont = ['qingbing.txt']
for t in cont:
    with open('%s/users/%s' % (filepath, t), 'r') as f:
        for i in f:
            if i.strip() and not i.startswith('#'):
                name = i.split()[0]
                passwd = i.split()[1]
                addr = i.split()[2]
                # addr = 147
                job_id = name + addr
                # 添加任务，循环调用act 函数，以便动态添加定时任务
                target=act(name,passwd,addr,schdeuler,job_id,r)


schdeuler.start()
while True:
    if not schdeuler.get_jobs():
        break

