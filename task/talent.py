#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/21 10:18
# @Author  : xingyue
# @File    : talent.py

# 天赋卷轴碎片获取


class Talent(object):
    # 指定类型
    type_map = {
        'type1': 'wg',  # 物攻
        'type2': 'wf',  # 物防
        'type3': 'cg',  # 策攻
        'type4': 'cf',  # 策防
        'type5': 'sm',  # 生命
    }
    # 对应类型id值
    id_map = {
        'wg': 5,
        'wf': 6,
        'cg': 7,
        'cf': 8,
        'sm': 9,
    }

    def index(self):
        result = self.action(c='talent', m='index')
        return result

    def get_info(self, type):
        # 获取碎片npc48523
        result = self.action(c='talent', m='get_info', type=type)
        return result

    def sweep(self, type):
        # vip>3可以扫荡当前需要
        formdata = {
            'type': type
        }
        result = self.action(c='talent', m='sweep', body=formdata)
        formdata = {
            'type': type,
            'check': 1
        }
        result = self.action(c='talent', m='sweep', body=formdata)
        return result

    def map_mission(self, l, s, id):
        # 获取指定NPC详细信息
        formdata = {
            'l': l,
            's': s,
            'id': id
        }
        result = self.action(c='map', m='mission', body=formdata)
        return result

    def map_action(self, l, s, id, times):
        # 普通攻击
        formdata = {
            'l': l,
            's': s,
            'id': id
        }
        for i in range(times):
            result = self.action(c='map', m='action', body=formdata)

    def map_action_vip(self, l, s, id, times):
        # vip扫荡
        times = int(times)
        formdata = {
            'l': l,
            's': s,
            'id': id,
        }
        if times > 5 and times % 5 == 0:#如果大于5次并且是5的倍数直接扫荡
            formdata['times'] = times
            result = self.action(c='map', m='action', body=formdata)
            return result
        elif times > 5 and times % 5 != 0:#如果大于5次不是5的倍数扫荡指定次数，剩下普通攻击
            a = times % 5
            b = times - a
            formdata['times'] = b
            result = self.action(c='map', m='action', body=formdata)
            for i in range(a):
                self.action(c='map', m='action', body=formdata)

        else:
            #不足5次直接普通攻击
            for i in range(times):
                self.action(c='map', m='action', body=formdata)

    def talent_action(self, l,s,id):
        vip = int(self.get_act()['vip'])
        try:
            # 获取碎片npc
            times = int(self.map_mission(l, s, id)['info']['maxtimes'])
        except KeyError as e:
            print(e)
            return None
        if vip > 2:
            self.map_action_vip(l,s,id,times)
        else:
            self.map_action(l, s, id, times)

