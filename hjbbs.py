#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/16 13:49
# @Author  : xingyue
# @File    : hjbbs.py.py

#获取账号信息

from lxml import etree
import requests
def get_username(star_num,end_num):
    for num  in xrange(star_num,end_num):
        url = 'http://bbs.hjsg.zhanyougame.com/?%s'%num
        res = requests.get(url)
        context = res.text
        # print  context
        dom_tree = etree.HTML(context)
        result = dom_tree.xpath('//*[@id="uhd"]/div[2]/h2')
        print result[0].text

#get_username(2389,4891)

