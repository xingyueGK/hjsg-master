#!/usr/bin/env python
#-*- coding:utf-8 -*-
import time
from base import SaoDangFb

class matrix(SaoDangFb):
    def matrix(self):
        genral_dict = {}
        matrix_index = self.action(c='matrix',m='index')
        general = matrix_index['general']
        for  k,v in general.items():
            name = v['name']
            genral_dict[name] = v['id']
        return genral_dict
    def use_matrix(self,mid=4):
        #boss固定4
        self.action(c='matrix',m='use_matrix',mid=mid)
    def update_matrix(self,uid,mid=4):
        genral_info = self.matrix()
        if genral_info[u'神孙权']:
            lists = '%s,-1,%s,-1,%s,-1,%s,-1,%s'%(
                genral_info[u'神曹植'],
                genral_info[u'阎圃'],
                genral_info[u'廉颇'],
                genral_info[u'神孙权'],
                uid,
                )
        else:
            lists = '%s,-1,%s,-1,%s,-1,%s,-1,%s' % (
            genral_info[u'神大乔'], genral_info[u'神曹植'], genral_info[u'阎圃'], uid, genral_info[u'廉颇'])
        self.action(c='matrix',m='update_matrix',list=lists,mid=mid)
if __name__ == '__main__':
    a=matrix(num=148, user='xingyue123a', passwd='413728161')
    cont= a.matrix()
    print