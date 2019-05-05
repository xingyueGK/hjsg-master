#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/8 18:09
# @Author  : xingyue
# @File    : mingjiang.py

import json, time

addtype = {
    "1": '武力',
    "2": '智力',
    "3": '体力',
    "4": '物理攻击',
    "5": '物理防御',
    "6": '策略攻击',
    "7": '策略防御',
    "8": '生命值',
    "9": '闪避',
    "10": '暴击率',
    "11": '识破',
    "12": '初始士气',
    "13": '命中',
    "14": '精准',
    "15": '抗暴击率',
    "16": '破击',
    "17": '勘破',
    "18": '最终伤害',
    "19": '最终减伤',
    "51": '坚韧',
    "50": '锋芒',
}

with open('../users/data.json') as f:
    json_data = json.load(f)

for i in json_data['achievement']:
    id = i['id'].strip()
    name = i['name'].strip()
    try:
        gid1name = i['gid1']['name'].strip()
    except:
        gid1name = ''

    try:
        gid2name = i['gid2']['name'].strip()
    except:
        gid2name = ''

    try:
        gid3name = i['gid3']['name'].strip()
    except:
        gid3name = ''
    try:
        gid4name = i['gid4']['name'].strip()
    except:
        gid4name = ''
    try:
        gid5name = i['gid5']['name'].strip()
    except:
        gid5name = ''
        # 升级类型
    paytype = i['paytype']
    context = u'{id}\t{name}\t{gid1name}\t{gid2name}\t{gid3name}\t{gid4name}\t{gid5name}\t{paytype}\t' \
        .format(id=id, name=name, gid1name=gid1name, gid2name=gid2name, gid3name=gid3name, gid4name=gid4name,
                gid5name=gid5name,paytype=paytype)
    #print context
    preview = i['preview']
    for item in preview:
        level = preview.index(item) + 1
        addtype1 = addtype[item['addtype1']]
        addtype2 = addtype[item['addtype2']]
        try:
            addtype3 = addtype[item['addtype3']]
        except:
            addtype3 =  ''
        addvalue1 = item['addvalue1']
        addvalue2 = item['addvalue2']
        addvalue3 = item['addvalue3']
        values = '{level}\t{addtype1}\t{addvalue1}\t{addtype2}\t{addvalue2}\t{addtype3}\t{addvalue3}'\
            .format(level=level,addtype1=addtype1,addvalue1=addvalue1,addtype2=addtype2,addvalue2=addvalue2,addtype3=addtype3,addvalue3=addvalue3)
        print context,values
    #


