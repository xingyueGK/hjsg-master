#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
'''获取武将成就信息'''

def wujian(self,uid):
    data = self.action(c = 'information', m = 'get_own_achievement' ,uid = uid)['achievement']
    zhili = 0
    tili = 0
    wuli = 0
    shangbi = 0
    baojilv = 0
    shipo = 0
    mingzhong = 0
    kangbjl = 0
    wuligj = 0
    wulify = 0
    clgj = 0
    clfy = 0
    shengming = 0
    shiqi = 0
    jingzhun = 0
    poji = 0
    kanpo = 0
    print '统计武将成就信息'
    print data
    for i in data:
        for count in range(1, 4):
            addtype = 'addtype' + str(count)
            addvalue = 'addvalue' + str(count)
            a1 = i[addtype]
            v1 = i[addvalue]
            v1 = int(v1.split('%')[0])
            print a1,'!!!!',v1
            if a1 == u'智力':
                zhili += v1
            elif a1 == u'武力':
                wuli += v1
            elif a1 == u'体力':
                tili += v1
            elif a1 == u'物防':
                wulify += v1
            elif a1 == u'物攻':
                wuligj += v1
            elif a1 == u'策攻':
                clgj += v1
            elif a1 == u'策防':
                clfy += v1
            elif a1 == u'暴击率':
                baojilv += v1
            elif a1 == u'扛暴击率':
                kangbjl += v1
            elif a1 == u'生命':
                shengming += v1
            elif a1 == u'初始士气':
                shiqi += v1
            elif a1 == u'精准':
                jingzhun += v1
            elif a1 == u'破击':  #
                poji += v1
            elif a1 == u'勘破':  #
                kanpo += v1
            elif a1 == u'命中':
                mingzhong += v1
            elif a1 == u'闪避':
                shangbi += v1
            elif a1 == u'识破':  #
                shipo += v1
            elif a1 == '0':
                pass
        info = '''
武力+%s           物理攻击+%s
智力+%s           物理防御+%s
体力+%s           策略攻击+%s
暴击率+%s%%         策略防御+%s   
识破+%s             生命值+%s
命中+%s%%           初始士气+%s
扛暴击率%s%%        精准+%s%%
闪避+%s%%           破击+%s%%   
勘破+%s%%         
        ''' % (
        wuli, wuligj, zhili, wulify, tili, clgj, baojilv, clfy,shipo , shengming, mingzhong, shiqi, kangbjl, jingzhun,shangbi,
        kanpo, poji, )
        print info