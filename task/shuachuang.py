#!/usr/bin/env python
#-*- coding:utf-8 -*-


from base  import SaoDangFb
import  threading
import json,time
import redis
tasks ={}
lock = threading.RLock()

_redis = redis.Redis(host='localhost', port=6379, decode_responses=True)
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
    key = 'overseastrade'+name
    _redis.hset(addr,key,times)
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
        list_country = task.action(c='overseastrade', m='get_list_by_country', p=1)['list']

            # 加入贸易队伍，每页有四个框，为place：1-4，每个框有两个位置site:1-2，页数为page:1-10默认为1即可，
        status = task.action(c="overseastrade", m='join_team', id=0, place=4, site=2, page=4)
        task.action(c="overseastrade", m='trade', v=0)  # 开启
        time.sleep(0.2)
    index = task.action(c='overseastrade', m='index')
    print '{0} 剩余贸易次数：{1}'.format(name,index['info']['times'])

def makeTask(file,addr):#批量生成次数
    with open('../users/{0}'.format(file), 'r') as f:
        for i in f:
            if i.strip():
                str = i.strip().split()[0]
                name = str
                passwd = i.split()[1]
                addr = addr
                t1 = MyThread(timesCount, args=(name, passwd, addr))
                t1.start()
    while 1:#阻塞主进程确保任务生成
        if threading.activeCount() == 1:
            break
def main(passwd,addr,file,flag,FlushCount =40):
    """
    :param FlushCount: 每次同时刷船次数,默认1个
    """
    try:
            try:
                userTimes = _redis.hget()
                for k,v in userTimes.items():
                    print 'username {0} 还剩 {1}'.format(k, v)
                    if int(v) == 0:
                        continue
                    if FlushCount >0:
                        jierihaiyun(k,passwd,addr,flag)#开始打劫
                        FlushCount -= 1
                        with open("chuaninfo.txt", 'w') as fw:
                            userTimes[k] = int(v) - 1
                            json.dump(userTimes, fw)
                    else:
                        break
            except:
                makeTask(file,addr)
                with open('chuaninfo.txt', 'w') as f:
                    json.dump(tasks, f)
    except IOError:
        makeTask(file,addr)
        with open('chuaninfo.txt', 'w') as f:
            json.dump(tasks,f)
if __name__ == '__main__':
    main(666666,149,'149gmjrhy.txt',True,50)