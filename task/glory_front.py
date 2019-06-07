#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/7 13:35
# @Author  : xingyue
# @File    : glory_front.


#每日荣耀战线

class glory_front(object):
    def index(self):
        # 加入战线 own_pk_info 不为空
        resutl = self.action(c='glory_front',m='index')
        return resutl
    def pvp_index(self,group):
        formdata = {
            'group':group
        }
        resutl = self.action(c='glory_front', m='pvp_index',body=formdata)
        return resutl

    def get_pk_list(self, group, page):
        formdata = {
            'group': group,
            'page': page
        }
        resutl = self.action(c='glory_front', m='get_pk_list', body=formdata)
        return resutl

    def pk(self,touid,page):
        formdata = {
            'touid':touid,
            'page':page
        }
        resutl = self.action(c='glory_front', m='pk',body=formdata)
        return resutl
    def pkinfo(self):
        index = self.index()
        pk_times = int(index['pk_times'])
        group = ''
        if index['own_pk_info']:
            group = index['own_pk_info']['group']
            print '已经加入战线 ', group
        elif self.general_book() == 'wuli':
            print '加入战线 东部'
            group = 2
        elif self.general_book() == 'zhili':
            print '加入战线 西部'
            group = 1
        pvp = self.pvp_index(group)
        self.p(pvp)
        all_page = pvp['all_page']
        page = int(pvp['page'])
        return group,all_page,page,pk_times
    def zhanxian(self):
        group, all_page, page,pk_times = self.pkinfo()
        while pk_times > 0:
            get_pk_list = self.get_pk_list(group,page-1)
            print '开始 PK，第 %s 梯队'%(page-1)
            for item in get_pk_list['list']:
                if int(item['is_pk']) == 1:
                    touid = item['uid']
                    pk = self.pk(touid,page-1)
                    pk_times = int(pk['pk_times'])
                    if pk['info']['win']> 0:
                        #pk胜利
                        print "pk 胜利，剩余次数",pk_times
                        page  = page -1 #胜利后次数减一页
                        break
                print "pk 失败，剩余次数",pk_times
