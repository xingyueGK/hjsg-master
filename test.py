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




class A:
    def func(self):
        print 'name'



a = A()

a.name = 'faad'









