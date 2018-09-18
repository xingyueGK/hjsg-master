#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/17 18:27
# @Author  : xingyue
# @File    : test.py


def condition():
    # level 3 ['神黄权','神陆抗'] [['神卢植','神刘璋'],['神文丑','神董卓']]
    a = ['神黄权', '神陆抗']
    b = [['神卢植', '神刘璋'], ['神文丑', '神董卓']]
    condition = [(i, k[0], k[1]) for i in a for k in b]


    # genral_info = self.matrix()
    # for k, v in genral_info.items():
    #     pass

condition()
y = set(['h', 'a','c', 'm',1])
z= set(['a', 'h', 'm','c','a'])
print y.issubset(z)