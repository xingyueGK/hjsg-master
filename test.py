#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/17 18:27
# @Author  : xingyue
# @File    : test.py
#
#
# def condition():
#     # level 3 ['神黄权','神陆抗'] [['神卢植','神刘璋'],['神文丑','神董卓']]
#     a = ['神黄权', '神陆抗']
#     b = [['神卢植', '神刘璋'], ['神文丑', '神董卓']]
#     condition = [(i, k[0], k[1]) for i in a for k in b]
#
#
#     # genral_info = self.matrix()
#     # for k, v in genral_info.items():
#     #     pass
# #
# # condition()
# # y = set(['h', 'a','c', 'm',1])
# # z= set(['a', 'h', 'm','c','a'])
#
#
# import redis
# import datetime
# import time
# import  requests
# import os
#
# # a = "2018-10-10 23:40:00"
# #
# # import time
# # timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
# #
# # timeStamp = int(time.mktime(timeArray))
# # print timeStamp
# #
# # pool=redis.ConnectionPool(host='127.0.0.1',port=6379,db=0)
# # r = redis.StrictRedis(connection_pool=pool)
# #
# # print r.expireat('231', timeStamp)
# # def buy(user, refresh=0):
# #     buy_item = ['中级卡', '初级卡', '高级卡', '军令']
# #     buy_type = [1, 3, 4, 5]
# #     print refresh
# #     buy(user)
# #     for i in range(refresh):
# #         print '刷新次数', i
# #         buy(user)
# #
# # buy('aa',30)
# #
# # import socket
# #
# # s = socket.socket(socket.AF_INET)
# #
# # basejs_list=["js/language.js","js/core/base.js","js/core/timer.js","js/core/player.js","js/core/audio.js","js/view/cd.js","js/view/movieclip.js","js/view/helper.js","js/view/guide.js","js/view/loginworld.js","js/view/roleworld.js","js/view/cityworld.js","js/view/mapworld.js","js/view/chatpop.js","js/view/miscpop.js","js/view/mailpop.js","js/view/mailboxpop.js","js/view/trendspop.js","js/view/battleworld.js","js/data/mapini.js","js/data/ini.js","js/obj/battle_hero.js","js/obj/battle_num.js","js/obj/battle_team.js","js/core/jsMorph-0.5.0.min.js","js/core/socket.io.min.js","js/core/PxLoader.js","js/core/PxLoaderImage.js","js/core/gamestart.js"]
# #
# # baseurl = 'http://img2.hanjiangsanguo.com/h5cdn/20151225172/static/'
# #
# # for i in basejs_list:
# #     path_list = os.path.split(i)
# #     url  = baseurl+"/"+i
# #     if not os.path.exists(path_list[0]):
# #         os.mkdir(path_list[0])
# #     r = requests.get(url,verify = False)
# #     with open(i, "wb") as code:
# #             code.write(r.content)
#
#
# import requests
# import os
# from bs4 import BeautifulSoup
# os.chdir(r'C:\Users\Administrator\Desktop\scrapy\proxy')
# # headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}
# url = 'http://s1.game.shaline8.com:8101'
# fp = open('host.txt','r')
# ips = fp.readlines()
# proxys = list()
# for p in ips:
#     ip =p.strip('\n').split('\t')
#     proxy = 'http://' +  ip[0] + ':' + ip[1]
#     proxies = {'http':proxy}
#     proxys.append(proxies)
# for pro in proxys:
#     try :
#         s = requests.get(url,proxies = pro,timeout=0.3)
#         a = s.text
#         if a == u'403':
#             print pro
#     except Exception as e:
#         pass
# print proxys
#
# class Book(object):
#
#     def __init__(self, title):
#         self.title = title
#
#     @classmethod
#     def create(cls, title):
#         book = cls(title=title)
#         return book
#
# book1 = Book("python")
# book2 = Book.create("python and django")
# print(book1.title)
# print(book2.title)



# class Foo(object):
#     X = 3
#     Y = 5
#
#     @staticmethod
#     def averag(*mixes):
#         return sum(mixes) / len(mixes)
#
#     @staticmethod
#     def static_method():
#         return Foo.averag(Foo.X, Foo.Y)
#
#     @classmethod
#     def class_method(cls):
#         return cls.averag(cls.X, cls.Y)
#
# foo = Foo()
# print(foo.static_method())
# print(foo.class_method())


# -*- coding: utf-8 -*-
# Time: 2018/10/13 19:01:30
# File Name: ex_interval.py
import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler


# def job1(f):
#     print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), f
#
# def job2(arg1, args2, f):
#     print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#     f.add_job(job2, next_run_time=(datetime.datetime.now() + datetime.timedelta(minutes=0.1)), args=('s','b',f,),
#                       id='test_job3')
#     print f.get_job('test_job3')
#
#
# def job3(**args):
#     print args
#
#
# scheduler = BlockingScheduler()
#
# #一次性任务示例
# print datetime.datetime.now()
# print datetime.datetime.now() + datetime.timedelta(minutes=0.6)
# scheduler.add_job(job2, next_run_time=(datetime.datetime.now() + datetime.timedelta(minutes=0.1)), args=('s','b',scheduler,),
#                       id='test_job3')
# print scheduler.get_job('test_job3')
# scheduler.start()
# print 'fffffffffffffff'
# scheduler.add_job(job1, next_run_time=(datetime.datetime.now() + datetime.timedelta(minutes=0.6)), args=('一次',), id='tesadjob3')
#
#
# print scheduler.get_jobs()
import threading,random
from threading import  Semaphore,Thread
def func():
    sm.acquire()
    print('%s get sm' )%threading.activeCount()

    time.sleep(random.randint(1,9))
    print('fffffffffff')
    sm.release()
if __name__ == '__main__':
    sm=Semaphore(3)
    with open('users/gmuser.txt', 'r') as f:
        # with open('../users/duguyi.txt', 'r') as f:
        for i in f:
            if i.strip() and not i.startswith('#'):
                name = i.split()[0]
                # name = i.split()[0]
                passwd = i.split()[1]
                addr = i.split()[2]
                try:
                    lockpwd = i.split()[3]
                except:
                    lockpwd = None
                # addr = 21
                t1 = threading.Thread(target=func,)
                t1.start()
