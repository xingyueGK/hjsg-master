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
            return True
        else:
            return False
    def get_banquet_key(self):
        if self.num > 31:
            return  'coutnry:banquet:149'
        else:
            return 'coutnry:banquet:30'
    def jion_team(self,r,id=None):#每日任务国宴
        info = self.index
        bqk = self.get_banquet_key()
        if r.exists(bqk):
            if not self.is_team:
                if id:
                    print 'id not None'
                    index = self.action(c='banquet', m='jion_team', id=id)  # 首页
                    if index['status'] != 1:
                        return False
                    return index
                #如果没有加入宴会
                for item in info['list']:
                    print 'for item list '
                    self.p(item)
                    if int(item['type']) ==3 and item['now_number'] <10:
                        id_ = item['caption']
                        formdata = {
                            "id":id_
                        }
                        print  formdata
                        index=self.action(c='banquet',m='join_team',body=formdata)#首页
                        self.p(index)
                        if index['status'] !=1:
                            print 'jion False'
                            return False
                        else:
                            print 'jion success'
                            return index
                return  False
            else:
                print 'alredy jion team'
                return True
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
        bqk = self.get_banquet_key()
        if r.exists(bqk):
            #如果已经有创建的key 了则不再创建
            return True
        if self.is_team:
            return True
        formdata = {
            "id":id
        }
        status = self.action(c='banquet',m='create_team',body=formdata)
        if status['status'] ==1 :
            print 'create_team false'
            caption= status['team']['caption']
            if r.lpush('coutnry:banquet',caption):
                print 'create_team %s'%(status['team']['caption'])
                return status['team']['caption']
            else:
                #可能有其他创建好了队伍了，则取消自己创建的
                self.dismiss_team()
                return False
        else:
            return False
    def start(self):
        index = self.index
        if self.is_team:
            if int(index['team']['now_number']) == int(index['team']['number']):
                formdata = {
                    "type": 0
                }
                status = self.action(c='banquet', m='action', body=formdata)
                if status['status'] != 1:
                    return False
                return True
            else:
                #人数 不够
                print '人数不够'
                return False
        #没有队伍
        return None

