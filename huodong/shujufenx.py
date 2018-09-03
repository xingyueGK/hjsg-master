# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import requests
import sys
import time
import json
import threading

reload(sys)
sys.setdefaultencoding('utf-8')
headers = {
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'close',
    # 'Host':'s148.game.hanjiangsanguo.com',
    'Upgrade-Insecure-Requests':'1',
    'Content-Type':'application/json',
    'DNT':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
class fuben(object):
    def __init__(self,username, password,addr):
        self.username = username
        self.password = password
        def get_html():
            # 获取首页html
            url = 'http://uc.game.hanjiangsanguo.com/index.php?&c=user&m=login&&token=&channel=150&lang=zh-cn&rand=150959328607564&u=%s&p=%s'%(self.username,self.password)
            r = requests.session()
            return r.get(url).text
        self.rand = int(time.time()*1000)
        self.token_uid = '210000353508'
        self.addr_info = json.loads(get_html())['serverlist']
        for v in self.addr_info:
            if v['selected'] == 1:
                self.addr = v['addr']
                break
        #自定义等级位置
        self.addr = "s%s.game.hanjiangsanguo.com"%addr
        def get_token():
            url = 'http://%s/index.php?v=0&c=login&&m=user&&token=&channel=150&lang=zh-cn&rand=150959405499450&u=%s&p=%s' % (
            self.addr, self.username, self.password)
            token = requests.session().get(url).text
            tokens = json.loads(token)
            return tokens['token']
        self.token = get_token()
    def post_url(self,data):
        # url拼接数据
        self.url = 'http://%s/index.php?v=2017111501&v=2017111501&channel=11&imei=NoDeviceId&platform=android&lang=zh-cn&token=%s&token_uid=%s&rand=%s&' % (
        self.addr, self.token, self.token_uid, self.rand)
        for k,v in data.items():
            self.url += '&%s=%s'%(k,v)
        keep_request = True
        while keep_request:
            try:
                r = requests.post(self.url,headers=headers,timeout=20)
                keep_request = False
                if r.status_code != 200:
                    r = requests.post(self.url, headers=headers,timeout=20)
                    return r.text
                else:
                    return r.text
            except Exception as e:
                print e
                time.sleep(0.3)
    def action(self,**kwargs):
        """动作参数m={'index':'获取基础账号密码等信息',‘get_monster_list’：“获取副本怪物列表信息”}
        """
        self.action_data = kwargs
        self.serverinfo = self.post_url(self.action_data)
        #self.serverinfo
        try:
            return json.loads(self.serverinfo)
        except Exception as e:
            print e

    def level(self):
        level = self.action(c='member', m='index')
        levelinfo = int(level['level'])
        return levelinfo
    def muster(self,level=40):#添加武将并出征
        # gid武将id，pid那个槽位训练获取
        caiid=''
        liaoid=''
        gid=''
        practtice_info = self.action(c='practice', m='index')
        # 初期都是两个训练槽位，
        pid = practtice_info['place']['1']['id']
        self.action(c = 'practice' , m = 'practice_stop ',pid = pid)#终止训练
        #获取武将
        self.action(c='levelgift',m='index')
        wujiang_index = self.action(c='muster',m='index',page=1,perpage=999)['list']
        for  k,v in wujiang_index.items():
            if v['name']=='蔡文姬':#蔡文姬
                print '蔡文姬出征'
                self.action(c='muster',m='go_battle',gid=v['id'])
                self.action(c='matrix',m='index')
                caiid =  v['id']
            elif v['name']=='廖化':
                self.action(c='muster', m='go_battle', gid=v['id'])
                liaoid = v['id']
            elif v['name'] == '张昭':
                print '找到张昭'
                gid=v['id']
        lists = '0,%s,0,%s,0,0,0,0,0'%(gid,caiid)
        print self.action(c='matrix',m='update_matrix',list=lists,mid=1)
        #队武将突飞
        status=1
        index_info = self.action(c='practice',m='index')
        #训练武将，
        self.action(c='practice',m='practice_start',gid= gid,pid=pid,type=2)
        freetimes = index_info['freetimes']#突飞卡
        isturn = index_info['list']['1']['isturn']#武将师是否到转生级别
        wjlevel = index_info['list']['1']['level']
        print '武将等级',wjlevel
        while status == 1 and freetimes != '0':#队伍将进行突飞
            if int(isturn) == 1 and int(wjlevel) <= level:
                print '武将转生'
                print self.action(c='practice',m='turn',gid=gid)
            self.action(c='practice', m='mop', times = 100,gid=gid)
            self.action(c='practice', m='mop', times=50, gid=gid)
            self.action(c='practice', m='mop', times=10, gid=gid)
            self.action(c='practice', m='mop', times=5, gid=gid)
            index_info = self.action(c='practice', m='index')
            freetimes = index_info['freetimes']
            info = self.action(c = 'practice',m='go_leap',gid=gid)#武将突飞一次
            status = info['status']
    def tufei(self,name,level):#对武将突飞
        gid = ''
        practtice_info = self.action(c='practice', m='index')
        # 初期都是两个训练槽位，
        pid = practtice_info['place']['1']['id']
        self.action(c='practice', m='practice_stop ', pid=pid)  # 终止训练
        wujiang_index = self.action(c='muster', m='index', page=1, perpage=999)['list']
        for k, v in wujiang_index.items():
            if v['name'] == name:  # 蔡文姬
                print u'武将出征',name
                result = self.action(c='muster', m='go_battle', gid=v['id'])
                print result['status']
                gid = v['id']
        status = 1
        index_info = self.action(c='practice', m='index')
        # 训练武将，
        self.action(c='practice', m='practice_start', gid=gid, pid=pid, type=2)
        freetimes = index_info['freetimes']  # 突飞卡
        for k,v  in index_info['list'].items():
            if v['name'] == name:
                isturn = v['isturn']  # 武将师是否到转生级别
                wjlevel = v['level']
        print '武将等级', wjlevel
        while status == 1 and freetimes != '0':  # 队伍将进行突飞
            if int(isturn) == 1 and int(wjlevel) <= level:
                print '武将转生'
                self.action(c='practice', m='turn', gid=gid)
            self.action(c='practice', m='mop', times=100, gid=gid)
            self.action(c='practice', m='mop', times=50, gid=gid)
            self.action(c='practice', m='mop', times=10, gid=gid)
            self.action(c='practice', m='mop', times=5, gid=gid)
            index_info = self.action(c='practice', m='index')
            freetimes = index_info['freetimes']
            info = self.action(c='practice', m='go_leap', gid=gid)  # 武将突飞一次
            status = info['status']
    def mapscene(self):#领取通关奖励
        self.action(c='map',m='get_scene_list',l=1,v=2018071801)
        self.action(c='map',m='get_newreward_index',levelid=1,v=2018071801)
        self.action(c='map',m='get_newreward',id=1,v=2018071801)
        self.action(c='map', m='get_newreward', id=2, v=2018071801)
        self.action(c='map', m='get_newreward', id=3, v=2018071801)
        self.action(c='map', m='get_newreward', id=4, v=2018071801)
    def zhengshou(self):#征收
        cishu = self.action(c='city',m='index')#获取银币征收次数,m=impose,执行征收
        cishu_count = cishu['times']
        if cishu_count != '0':#判断征收次数是否为0，不为0则进行全部征收
            for count in range(1,int(cishu_count)+1):
                print '开始征收第 %d 次'%count
                time.sleep(0.5)
                self.action(c='city',m='impose')
        else:
            print '次数为0次'
    def join(self):#申请加入你是学姐国家
        print self.action(c='country',m='search',name='%E6%98%AF%E4%BD%A0%E5%AD%A6%E5%A7%90')
        print self.action(c='country',m='apply',id=250000000286,page=1)
    def overseastrade(self):  # 海外贸易
        self.action(c='message',m='index')
        self.action(c='overseastrade',m='index')
        # 购买粮食，花费银币的，id=1为粮食，id2-5为花费元宝的玛瑙等
        self.action(c='overseastrade', m='buy_item', id=1)
        # 组队 ，检查是否有对， 有则加入，没有则创建 ，开始贸易
        # 1获取组队列表
        list_country = self.action(c='overseastrade', m='get_list_by_country', p=1)['list']
        if list_country:  # 如果列表不为空，说明有组
            # 自动加组贸易
            for k, v in list_country.items():  # 判断第一个角色有值没有，有责加入第二个，没有则加入第一个#需要time_id
                if v['member1'] != '0':  # 如果不为0 则说明角色有人，加入另一个，
                    print '加入2'
                    self.id = v['id']
                    print self.action(c="overseastrade", m='join_team', id=self.id, place=int(k), site=2, page=1)
                else:
                    print '加入1'
                    self.id = v['id']
                    print self.action(c="overseastrade", m='join_team', id=self.id, place=int(k), site=1, page=1)
                    # print list_country[k]['member1']
        else:
            # 加入贸易队伍，每页有四个框，为place：1-4，每个框有两个位置site:1-2，页数为page:1-10默认为1即可，
            print self.action(c="overseastrade", m='join_team', id=0, place=4, site=2, page=1)
    def general(self,type):#获取武将id和装备id,并返回输入获取的等级
        #装备信息栏
        info = self.action(c='general',m='index')
        gid = info['list']['1']['id']  # 武将id
        etype1 = self.action(c='general', m='get_info',gid=gid,etype=1)
        etype3 = self.action(c='general', m='get_info',gid=gid,etype=3)#获取披风
        etype2 = self.action(c='general', m='get_info', gid=gid, etype=2)#获取铠甲
        etype4 = self.action(c='general', m='get_info', gid=gid, etype=4)
        eid = []#装备列表
        if info['list']['1']['eid1'] == 0 or info['list']['1']['eid1'] == "0":
            #判断是否穿戴装备
            # for k,v in  etype1['equipments'].items():#初期获得最高级装备为2级别
            #     if v['needlevel'] == str(type) and v['etype']== 2:
            #         eid.append({"1":v['id']})
            #         break
            eid.append({"1": etype1['equipments']['1']['id']})#第一个就就是最好的装备
        else:
            eid.append({"1":info['list']['1']['eid1']['id']})
        if info['list']['1']['eid2'] == 0 or info['list']['1']['eid2'] == "0":
            # for k,v in  etype2['equipments'].items():#初期获得最高级装备为2级别
            #     if v['needlevel'] == str(type) and v['etype']== 2:
            #         eid.append({"2":v['id']})
            #         break
            eid.append({"2": etype2['equipments']['1']['id']})
        else:
            eid.append({"2":info['list']['1']['eid2']['id']})
        if info['list']['1']['eid3'] == 0 or info['list']['1']['eid3'] == "0":
            # for k, v in etype3['equipments'].items():  # 初期获得最高级装备为2级别
            #     if v['needlevel'] == str(type) and v['etype']== 3:
            #         eid.append({"3":v['id']})
            #         break
            eid.append({"3": etype3['equipments']['1']['id']})
        else:
            eid.append({"3":info['list']['1']['eid3']['id']})
        if info['list']['1']['eid4'] == 0 or info['list']['1']['eid4'] == "0":
            # for k, v in etype3['equipments'].items():  # 初期获得最高级装备为2级别
            #     if v['needlevel'] == str(type) and v['etype']== 3:
            #         eid.append({"3":v['id']})
            #         break
            eid.append({"4": etype4['equipments']['1']['id']})
        else:
            eid.append({"4":info['list']['1']['eid4']['id']})

        return gid,eid
    def get_general(self):#获取武将信息
        general_index=self.action(c='general',m='index')
        return general_index
    def strengthen(self,id):#强化装备
        levelinfo = self.level()
        self.action(c='general',m='index')
        self.action(c='strengthen',m='index')
        id_info = self.action(c='strengthen',m='strengthen_info',id=id)
        newlevel = id_info['info']['level']#获取当前装备的强化等级
        print '当前等级',newlevel
        try:
            while int(newlevel) < levelinfo :
                strenthinfo = self.action(c='strengthen', m='strengthen_start', id=id, ratetype=0)
                newlevel = strenthinfo['newlevel']
        except KeyError as e:
            print '已经强化到最高级',e
    def eqip(self,gid,eid,etype):#给武将穿戴装备
        self.action(c='general',m='equip',gid=gid,eid=eid,etype=etype)
    def levelgift(self,level):#获取等级奖励
        self.action(c = 'levelgift' , m = 'index')#打开奖励页面
        self.action(c='levelgift',m='get_reward',level=level)#获取30级奖励
    def saodang(self,num):#攻击小兵
        memberindex = self.action(c='member',m='index')
        missionlevel = memberindex['missionlevel']
        missionsite = memberindex['missionsite']
        missionstage = memberindex['missionstage']
        map = self.action(c='map',m='get_mission_list')
        exit_code = 1
        if exit_code == 1 :
            for level in range(missionlevel,12):#遍历每一个图
                print '开始攻击第 %s 个图'%level
                self.action(c='map',m='get_scene_list',l=level)
                site = len(self.action(c='map',m='get_scene_list',l=level)['list'])+1
                for i in range(missionstage,site):#遍历关卡图次数
                    print '关卡',i
                    status = 1
                    for id in range(1,11):  # 遍历10个小兵
                        try:
                            #获取首杀状态，1为首杀，-1为已经击杀
                            first = self.action(c='map', m='mission', l=level, s=i, id=id)['info']['first']
                        except KeyError as e :
                            continue
                        if first == 1 and status == 1:#
                            status = self.action(c='map',m='action',l=level,s=i,id=id)['status']
                            print status
                            if  first == 1 and status == -5:
                                print '退出'
                                exit_code = 2
                                return exit_code
                        else:
                            print '已经击杀'
        else:
            print 'dabuduole'
            return

    def act_steadily(self):#节节高
        info = self.action(c='act_steadily',m='index')
        status  = info['status']
        reward_cd = info['reward_cd']
        t = info['reward']['time']
        if reward_cd == 0 and status == 1:
            self.action(c='act_steadily',m='get_online_reward',t=t)
        elif reward_cd == 0 and status != 1:
            exit(2)
        else:
            print '%s分钟后领取,%s'%(reward_cd/60,reward_cd)

            time.sleep(reward_cd+1)
            self.action(c='act_steadily', m='get_online_reward', t=t)
    def morra(self):#节节高奖券
        status =1
        while status == 1:
            info=self.action(c='act_steadily',m='morra',type=1)
            status= info['status']
        #买突飞卡
        print self.action(c='act_steadily',m='get_score_reward',id=1)
    def mainquest(self):#领取所有活动奖励
            mainquest_info =self.action(c='mainquest',m='index')
            print '领奖'
            for i in mainquest_info['list']:
                if int(i['status'])==1:#获取奖励
                    self.action(c='mainquest',m='get_task_reward',id=i['task_id'])
                    print '领取奖励',i['task_id']
    def qiandao(self):#签到
        # 领取连续登陆15天奖励，id:15，c:logined，m:get_reward
        print self.action(c='logined',m='index')

        print self.action(c='logined',m='get_reward',id=15)
        #每日签到，所有动作就是c内容，m动作参数即可，包括领取vip工资，还有每日抽奖
        self.action(c='sign',m='sign_index')
        # c:vipwage，m:get_vip_wage，领取VIP每日奖励
        self.action(c='vipwage',m='get_vip_wage')
    def soul(self):#武将将魂
        site = [1, 2, 3, 4]
        sid = []
        gid=''
        soulindex=self.action(c='soul',m='index')
        for i in soulindex['pack']['list']:
            sid.append(int(i['id']))
        for k,v in soulindex['general'].items():
            if v['name'] == '张昭':
                gid = int(v['id'])
        for i in range(4):
            self.action(c='soul',m='equip',gid=gid,sid=sid[i],site=site[i])
    def tujian(self,user):#图鉴
        result = self.action(c='equip_book',m='get_level_up',id=75)#橙装策防
        resultwf = self.action(c='equip_book', m='get_level_up', id=74)  # 橙装物防

        print '账号',user,'披风等级',result['now']['level'],'铠甲等级',resultwf['now']['level']
        if result['now']['level'] < "8":
            print '升级图鉴'
            self.action(c='equip_book', m='level_up', id=75)#升级图鉴
        if resultwf['now']['level'] < "8":
            self.action(c='equip_book', m='level_up', id=74)#升级图鉴
    def mingjiang(self):#升级张昭成就
        self.action(c='general_book', m='index', perpage=999)
        self.action(c='general_book',m='get_achievement_list',v=2018071801)
        self.action(c='general_book',m='levelup',id=176,v=2018071801)
    def zuoji(self):#首次购买坐骑并穿戴
        self.action(c='studfarm',m='action',new=1,id=3)
        pass
    def mapinfo(self):
        memberindex = self.action(c='member',m='index')
        missionlevel = memberindex['missionlevel']#当前势力
        missionsite = memberindex['missionsite']#有多少个关卡
        missionstage = memberindex['missionstage']#当前关卡
        print '第 %s 个图，%s 节点 '%(missionlevel,missionstage)
        #print json.dumps(self.action(c='map', m='get_scene_list', l=missionlevel))
    def lottery(self):#每日抽奖
        #c=lottery，m=action
        #获取每日抽奖次数
        self.numbers = self.action(c='lottery',m='index')['log']['info']['total_num']
        print '开始抽奖，剩余次数 %s' % self.numbers
        for num in range(self.numbers):
            self.action(c='lottery',m='action')
        print '抽奖结束'
if __name__ == '__main__':
    def act(user,apass,addr):
            action = fuben(user,apass,addr)
            action.mapinfo()
            #action.general(1)
            #action.mingjiang()
            #action.saodang(9)
    with open('../users/149gmjrhy.txt', 'r') as f:
        for i in f:
            str = i.strip().split()[0]
            name = str
            passwd = i.strip().split()[1]
            addr = 149
            t1 = threading.Thread(target=act, args=(name,passwd,addr))
            t1.start()
            time.sleep(0.1)