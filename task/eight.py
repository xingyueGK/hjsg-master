#!/usr/bin/env python
#-*- coding:utf-8 -*-


from base import SaoDangFb


class eight(SaoDangFb):
    def reset(self):
        self.action(c='eight_diagram',m='reset_point')
        self.action(c='eight_diagram',m='level_index',level=3)#level：八卦等级，分为1,2,3重

    def eight_index(self):
        level_index = self.action(c='eight_diagram',m='level_index',level=3)
        return level_index

    def pk(self):
        self.action(c='eight_diagram', m='pk', level=3)

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
    def update_matrix(self,uid1,mid=2):
        genral_info = self.matrix()
        #lists = '14900000063990,14901000013870,14900000065197,-1,14900000065196,-1,-1,14900000054739,-1'
        lists = '%s,%s,%s,-1,%s,-1,-1,%s,-1'%(
            14900000063990,
            14901000013870,
            uid1,
            14900000065196,
            14900000054739,
            )
        print lists
        self.action(c='matrix',m='update_matrix',list=lists,mid=mid)

def main():
    ei = eight(num=149, user='pock520', passwd='5553230')
    genral = ei.matrix()
    ei.use_matrix()#使用固定阵法
    point = ei.eight_index()['cost']['point']
    print '当前位置',point
    if point == '9':
        ei.reset()
    for i in range(12):
        point = ei.eight_index()['cost']['point']
        if point == '7':
            # 上谋士 u'神刘表'
            ei.update_matrix(genral[u'神鲁肃'])
            ei.use_matrix(2)
            ei.pk()
            print '当前位置', point
        elif point == '8':
            ei.use_matrix()
            ei.pk()
        else:
            ei.pk()
            print '当前位置', point


    ei.update_matrix(genral[u'神左慈'],genral[u'神卢植'])
if __name__ == '__main__':
    main()