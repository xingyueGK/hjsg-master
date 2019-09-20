#!/usr/bin/env python
# -*- coding:utf-8 -*-
from task.base import SaoDangFb
import  time,threading
import os,json

class eight(SaoDangFb):
    def __init__(self, level, user, passwd, num):
        super(eight, self).__init__(user, passwd, num)
        self.level = level
    def muster(self):
        #所有将领数量
        muster=self.action(c='muster', m='index',page= 1,perpage=999)['list']
        return muster
    def condition(self):
        #level 3 ['神黄权','神陆抗'] [['神卢植','神刘璋'],['神文丑','神董卓']]
        out=[u'神黄权',u'神陆抗'] #三重必须有其一
        b = [[u'神卢植',u'神刘璋',u'神袁尚',u'夏侯杰',u'神刘表'],[u'神文丑',u'神董卓',u'神刘表',u'神鲁肃',u'神袁尚'],
             [u'神文丑',u'神董卓',u'神卢植',u'神袁尚'],[u'神卢植',u'神刘璋',u'神文丑',u'神刘表']]
        conditions = [ (i,k[0],k[1],k[2],k[3]) for i in out for k in b]
        #print json.dumps(conditions)
        genral_info = self.matrix()
        genral_list = []
        for k,v in genral_info.items():
            genral_list.append(k)
        #print json.dumps(genral_list)
        for cond in conditions:
            if set(cond) <= set(genral_list):
                #print '三重',self.user,json.dumps(cond)
                return cond


    def reset(self):
        self.action(c='eight_diagram', m='reset_point')
        self.action(c='eight_diagram', m='level_index', level=self.level)  # level：八卦等级，分为1,2,3,4,5重

    def eight_index(self):
        now_level = self.action(c='eight_diagram', m='index')['now_level']
        level_index = self.action(c='eight_diagram', m='level_index', level=now_level)
        return level_index,now_level

    def pk(self):
        self.action(c='eight_diagram', m='pk', level=self.level)

    def matrix(self):
        #出征将领
        genral_dict = {}
        matrix_index = self.action(c='matrix', m='index')
        general = matrix_index['general']
        for k, v in general.items():
            name = v['name']
            genral_dict[name] = v['id']
        return genral_dict

    def use_matrix(self, mid=4,case=2):
        # boss固定4
        formdata = {
            "mid":mid,
            "case":case,
        }
        self.action(c='matrix', m='use_case',body=formdata)

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


def run(user,apass, addr,level):
    ei = eight(num=addr, user=user, passwd=apass, level=level)
    # # ei.use_matrix(4)  # 使用固定阵法
    # cond = ei.condition()
    # if not cond:
    #     #不符合三重条件
    #     exit(3)
    # ei.update_matrix(u'神甘宁',u'神刘璋',u'神袁尚',u'神刘表',u'神卢植',4)
    index,now_level = ei.eight_index()
    reset_times = int(index['reset_times'])
    point = index['cost']['point']
    print '%s 八卦等级 %s 当前位置%s 重置八卦次数%s'%(user,now_level,point,reset_times)
    # if point == '9' and reset_times == 1:
    #     ei.reset()
    # else:
    #     print '已经通关没有次数了'
    #     exit(1)
    for i in range(12):
        index, now_level = ei.eight_index()
        point = int(index['cost']['point'])
        if point == 1:#武将减低
            # 上谋士 u'神刘表'
            ei.use_matrix(mid=1,case=2)
            ei.pk()
            print '当前位置', point
        elif point == 2:#谋士降低
            ei.use_matrix(mid=2, case=2)
            ei.pk()
            print '当前位置', point
        elif point == 3:  # 谋士降低
            ei.use_matrix(mid=1, case=2)
            ei.pk()
            print '当前位置', point
        elif point == 4:  # 谋士降低
            print '当前位置', point
            ei.use_matrix(mid=2, case=2)
            ei.pk()
        else:  # 谋士降低
            print '当前位置', point
            ei.use_matrix(mid=1, case=1)
            ei.pk()
    ei.use_matrix(4)
if __name__ == '__main__':
    filepath = os.path.dirname(os.path.abspath(__file__))
    cont = ['five.txt']
    for t in cont:
        with open('%s/users/%s'%(filepath,t),'r') as f:
            for i in f:
                if i.strip() and not i.startswith('#'):
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    level = i.split()[3]
                    t1 = threading.Thread(target=run, args=(name, passwd, addr,level))
                    t1.start()