#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/26 9:56
# @Author  : xingyue
# @File    : autoCountryBanquet.py

#自动国宴贡献

class autoCountryBanquet(object):
    @property
    def index(self):
        formdata = {
            "type":1
        }
        index = self.action(c='banquet', m='index', body = formdata)
        return index

    @property
    def is_team(self):
        #查看是否有队伍
        info = self.index
        if info['team']:
            return info
        else:
            return False
    def get_banquet_key(self):
        if int(self.num) > 31:
            return  'country:banquet:149'
        else:
            return 'country:banquet:30'
    def join_team(self,id=None):#每日任务国宴
        info = self.index
        print 'jion_team '
        if not self.is_team:
            print 'start join banquet'
            max_priced_item = max(info['list'], key=lambda x: x['now_number'])
            formdata = {
                "id":max_priced_item['caption']
            }
            index = self.action(c='banquet', m='join_team', body=formdata)  # 首页
            if index['status'] != 1:
                print 'join False'
                return False
            print 'jion item %s'%id

            return index
        else:
            self.p(self.is_team,self.user)
            print '%s alredy jion team'%self.user
            return False
    def dismiss_team(self):
        formdata = {
            "id":1
        }
        self.action(c='banquet',m='dismiss_team',body=formdata)

    def create_team(self,r,id=3):
        """
        分为小 中 大 1 2 3
        :param id:
        :return: Ture 创建成功， False 创建失败
        """

        item = self.is_team
        if item:
            return  True
        formdata = {
            "id":id
        }
        status = self.action(c='banquet',m='create_team',body=formdata)
        print status
        if status['status'] ==1 :
            print 'create_team '
            return True
        else:
            return False
    def start(self,r):
        index = self.index
        if self.is_team:
            if int(index['team']['now_number']) == int(index['team']['number']):
                formdata = {
                    "type": 0
                }
                status = self.action(c='banquet', m='action', body=formdata)
                if status['status'] != 1:
                    return False
                bqk = self.get_banquet_key()
                print 'success'
                r.delete(bqk)
                return True
            else:
                #人数 不够
                print '人数不够'
                return False
        #没有队伍
        return None

