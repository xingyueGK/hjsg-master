#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

from base import SaoDangFb


class eight(SaoDangFb):
    def __init__(self, level, user, passwd, num):
        super(eight, self).__init__(user, passwd, num)
        self.level = level

    def condition(self):
        #level 3 ['神黄权','神陆抗'] [['神卢植','神刘璋'],['神文丑','神董卓']]
        a=['神黄权','神陆抗']
        b= [['神卢植','神刘璋'],['神文丑','神董卓']]
        condition = [ (i,k[0],k[1]) for i in a for k in b]

        print json.dumps(condition)
        genral_info = self.matrix()
        for k,v in genral_info.items():
            pass

    def reset(self):
        self.action(c='eight_diagram', m='reset_point')
        self.action(c='eight_diagram', m='level_index', level=self.level)  # level：八卦等级，分为1,2,3重

    def eight_index(self):
        level_index = self.action(c='eight_diagram', m='level_index', level=self.level)
        return level_index

    def pk(self):
        self.action(c='eight_diagram', m='pk', level=self.level)

    def matrix(self):
        genral_dict = {}
        matrix_index = self.action(c='matrix', m='index')
        general = matrix_index['general']
        print json.dumps(general)
        for k, v in general.items():
            name = v['name']
            genral_dict[name] = v['id']
        return genral_dict

    def use_matrix(self, mid=4):
        # boss固定4
        self.action(c='matrix', m='use_matrix', mid=mid)

    def update_matrix(self, uid1, uid2, uid3, uid4, uid5, mid=2):
        genral_info = self.matrix()
        lists2 = '%s,%s,%s,-1,%s,-1,-1,%s,-1' % (
            genral_info[uid1],
            genral_info[uid2],
            genral_info[uid3],
            genral_info[uid4],
            genral_info[uid5],
        )
        lists4 = '%s,-1,%s,-1,%s,-1,%s,-1,%s' % (
            genral_info[uid1],
            genral_info[uid2],
            genral_info[uid3],
            genral_info[uid4],
            genral_info[uid5],
        )
        if mid == 2:
            self.action(c='matrix', m='update_matrix', list=lists2, mid=mid)
        elif mid == 4:
            self.action(c='matrix', m='update_matrix', list=lists4, mid=mid)


def main():
    ei = eight(num=148, user='xingyue123z', passwd='413728161', level=2)
    ei.use_matrix(4)  # 使用固定阵法
    ei.condition()
    ei.update_matrix(u'神甘宁',u'神刘璋',u'神袁尚',u'神刘表',u'神卢植',4)
    point = ei.eight_index()['cost']['point']
    print '当前位置', point
    if point == '9':
        ei.reset()
    for i in range(12):
        point = ei.eight_index()['cost']['point']
        if point == '7':#武将减低
            # 上谋士 u'神刘表'
            ei.update_matrix(u'神甘宁', u'神刘璋', u'神袁尚', u'神刘表', u'神卢植', 4)
            ei.pk()
            print '当前位置', point
        elif point == '8':#谋士降低
            ei.update_matrix(u'神甘宁', u'神刘璋', u'神袁尚', u'夏侯杰', u'神刘表', 4)
            ei.pk()
        else:
            ei.pk()
            print '当前位置', point
    ei.update_matrix(u'神刘表', u'神刘璋', u'神袁尚', u'神甘宁', u'神卢植', 4)
    ei.use_matrix(4)
if __name__ == '__main__':
    main()