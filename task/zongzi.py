#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/26 13:55
# @Author  : xingyue
# @File    : country_celery.py

# 定时调度国家任务

from utils.mylog import MyLog
from task.base import SaoDangFb
import os, datetime, threading
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ProcessPoolExecutor


class banquet(SaoDangFb):
    def quyuan_festival(self):
        self.action(c='quyuan_festival', m='index')
        resutl = self.action(c='quyuan_festival', m='poll_index')
        formdata = {
            "zongzi": 1,
        }
        self.action(c='quyuan_festival', m='poll', body=formdata)
        resutl = self.action(c='quyuan_festival', m='poll_index')
        try:
            crontime = resutl['user_info']['time_poll']
        except:
            return 86000

        print self.user, '剩余%s秒' % (crontime)
        return crontime

    def poll_reward(self):
        self.action(c='quyuan_festival', m='poll_index')
        self.action(c='quyuan_festival', m='poll_reward')
        self.action(c='quyuan_festival', m='take_poll')


s1 = threading.Semaphore(20)
l = threading.Lock()
log = MyLog(logpath='quyuan', logname='quyuan.log')

if __name__ == '__main__':
    s1 = threading.Semaphore(5)
    scheduler = BlockingScheduler()
    executors = {
        'default': {'type': 'threadpool', 'max_workers': 20},
        'processpool': ProcessPoolExecutor(max_workers=5)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 50,
        'misfire_grace_time': 100,
    }
    scheduler.configure(executors=executors, job_defaults=job_defaults)


    def act(user, apass, addr, job):
        s1.acquire()
        print user, addr
        action = banquet(user, apass, addr)
        num = int(action.quyuan_festival())
        job_id = user + addr
        # 添加任务，循环调用act 函数，以便动态添加定时任务
        try:
            log.info(job.add_job(act, next_run_time=(datetime.datetime.now() + datetime.timedelta(seconds=num)),
                                 args=(user, apass, addr, job), id=job_id))
        except:
            pass
        s1.release()


    #filepath = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.dirname(os.path.abspath(__file__)).rsplit('\\', 1)[0]
    # cont = ['user.txt','21user.txt','autouser.txt','alluser.txt']
    cont = ['xing.txt']
    for t in cont:
        with open('%s/users/%s' % (filepath, t), 'r') as f:
            for i in f:
                if i.strip() and not i.startswith('#'):
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    # addr = 147
                    t1 = threading.Thread(target=act, args=(name, passwd, addr, scheduler))
                    t1.start()
    scheduler.start()
