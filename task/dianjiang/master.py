#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/23 17:55
# @Author  : xingyue
# @File    : master.py



class Master(object):
    #点将台
    def index(self):
        self.log.info('点将台')
        result = self.action(c='master',m=self.get__function_name())
        return  result

    def get_general_info(self,gid):
        self.log.info('获取武将信息')
        formdata = {
            "gid":gid,
            "token":self.token
        }
        result = self.action(c='master', m=self.get__function_name(),body=formdata)
        return result

    def go_battle(self,gid=0,name=None):
        index= self.index()
        d = index['list']
        if name:
            for k,v in d.items():
                if v['name'] == name:
                    gid = v['id']
        formdata = {
            "gid":gid,
            "confrim":0,
            "token":self.token
        }
        ginfo = self.get_general_info(gid)['info']
        name = ginfo['name']
        star = ginfo['star']
        level = ginfo['level']
        self.log.info('{star}星{level}级武将{name}出征'.format(star=star,level=level,name=name))
        result = self.action(c='master',m=self.get__function_name(),body=formdata)
        return  result

    def go_rest(self, gid):
        formdata = {
            "gid": gid,
            "confrim": 0,
            "token": self.token
        }
        ginfo = self.get_general_info(gid)['info']
        name = ginfo['name']
        star = ginfo['star']
        level = ginfo['level']
        self.log.info('{star}星{level}级武将{name}休息'.format(star=star, level=level, name=name))
        result = self.action(c='master', m=self.get__function_name(), body=formdata)
        return result

class case(object):
    #布阵
    """
    position1-9:0为开通，-1为未开通
    固定阵法方格位置
    ｜—— —— — -|
    ｜7  4   1 |
    ｜8  5   2 |
    ｜9  6   3 |
    - - - - - -
    """
    #固定阵法

    listmind = dict({
        "1","-1,{gid1},-1,{gid2},-1,{gid3},{gid4},-1,{gid5}",
        "2","-1,{gid1},-1,{gid2},-1,{gid3},{gid4},-1,{gid5}",
        "3","-1,{gid1},-1,{gid2},-1,{gid3},{gid4},-1,{gid5}",
        "4","{gid1},-1,{gid2},-1,{gid3},-1,{gid4},-1,{gid5}",
        "5","-1,{gid1},-1,{gid2},-1,{gid3},{gid4},-1,{gid5}",
    })
    midname = dict({
        "mid1":"锥形阵",#物理加成
        "mid2":"锋矢阵",#物理加成
        "mid3":"八卦阵",#策略加成
        "mid4":"七星阵",#策略加成
        "mid5":"鱼鳞阵",#物理防御
        "mid6":"",
        "mid7":"",
        "mid8":"锥形阵",
    })
    def case_index(self,case=1):
        self.use_case()
        formdata = {
            "case": case,
            "token": self.token
        }
        result = self.action(c='matrix',m=self.get__function_name(),body=formdata)
        return  result

    def use_matrix_case(self,
            gid1=0,
            gid2=0,
            gid3=0,
            gid4=0,
            gid5=0,
            mid=1,
            case=1):
        self.listmind[str(mid)].format(gid1=gid1,gid2=gid2,gid3=gid3,gid4=gid4,gid5=gid5)
        formdata = {
            "list":self.listmind,
            "mid":mid,
            "case":case,
            "token":self.token
        }
        result = self.action(c='master',m=self.get__function_name(),body=formdata)
        return  result

    def levelup(self,mid=4,case=1,level=5):
        self.log.info('阵法升级')
        formdata = {
            "case": case,
            "mid":mid,
            "token": self.token
        }
        info_case = self.get_info_case()
        case_level = int(info_case['case']['level'])
        self.log.info('当前{mid}阵法{level}级'.format(mid=mid,level=case_level))
        if case_level> level:
            return True
        else:
            for i in range(level - case_level):
                result = self.action(c='master',m=self.get__function_name(),body=formdata)
                case_level = result['info']['level']
                self.log.info('当前{mid}阵法{level}级'.format(mid=mid,level=case_level))

    def use_case(self,mid=4,case=1):
        formdata = {
            "case": case,
            "mid":mid,
            "token": self.token
        }
        result = self.action(c='master',m=self.get__function_name(),body=formdata)
        return  result

    def get_info_case(self,mid=4,case=1):
        formdata = {
            "case": case,
            "mid":mid,
            "token": self.token
        }
        result = self.action(c='master',m=self.get__function_name(),body=formdata)
        return  result

class practice(object):
    #训练
    def index(self):
        result = self.action(c='master',m=self.get__function_name())
        freetimes = result['freetimes']

        return  result
    def practice_stop(self,pid):
        self.action(c='practice', m=self.get__function_name(), pid=pid)

    def onekey_turn_index(self,gid):
        self.action(c='practice', m=self.get__function_name(), gid=gid)

    def onekey_turn(self,gid,type=4):
        #type 4 默认为最大转生 ，1是一次 2是五次 3是十次
        self.action(c='practice', m=self.get__function_name(), gid=gid,type=type)

    def practice_start(self,name=None,gid=0,pid=0):
        #首先确定是否训练中，如果给定的在训练中则退出
        index = self.index()
        place = index['place']
        l = index['index']
        for k,v in l.items():#查看给定的英雄是否在训练中
            if v['name'] == name and v['ispractice'] ==1:
                self.log.info('{name}已经在训练中'.format(name=name))
                return True
            elif v['name'] == name:#查找name对应的gid
                gid = v['id']
            else:
                self.log.error('训练失败，没有这个英雄')
                return False

        for k,v in place.items():#查找是否有空闲的槽位
            if int(v['gid']) == 0:
                pid = v['id']
        if pid:#如果没有强制停止第一个槽位
            self.log.error('没有空余槽位')
            pid = place['1']['id']
            self.practice_stop(pid)
        formdata = {
            "pid": pid,
            "gid":gid,
            "type":2,
            "token": self.token
        }
        result = self.action(c='master',m=self.get__function_name(),body=formdata)
        if result['status'] ==1:
            self.log.info('训练成功')
        else:
            self.log.info('训练失败{msg}'.format(msg=result))
        return  True
