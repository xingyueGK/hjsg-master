#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests

import sys
import re
import time
import json

reload(sys)
sys.setdefaultencoding('utf-8')
headers = {
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Host':'s148.game.hanjiangsanguo.com',
    'Upgrade-Insecure-Requests':'1',
    'Content-Type':'application/json',
    'DNT':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
def get_html():
    #获取首页html
    url = 'http://uc.game.hanjiangsanguo.com/index.php?&c=user&m=login&&token=&channel=150&lang=zh-cn&rand=150959328607564&u=xingyue123a&p=413728161'
    r = requests.session()
    return r.get(url).text
def get_token():
    url = 'http://s148.game.hanjiangsanguo.com/index.php?v=0&c=login&&m=user&&token=&channel=150&lang=zh-cn&rand=150959405499450&u=xingyue123a&p=413728161'
    token = requests.session().get(url).text
    tokens = json.loads(token)
    return tokens['token']

def get_info():
    token = get_token()
    rand = int(time.time()*1000)
    url='http://s148.game.hanjiangsanguo.com/index.php?v=0&c=member&&m=index&&token=%s&channel=150&lang=zh-cn&rand=%d'%(token,rand)
    info = requests.post(url,headers=headers).text
    return  json.loads(info)
class SaoDangFb(object):
    def  __init__(self):
        #随机请求参数
        self.rand = str(int(time.time()*1000))
        self.token_uid = '210000353508'
        self.token = get_token()
        #POST基础URL地址
        self.url = 'http://s148.game.hanjiangsanguo.com/index.php?v=0&channel=150&lang=zh-cn&token=%s&token_uid=%s&rand=%s&'%(self.token,self.token_uid,self.rand)

    def post_url(self,data):
        #url拼接数据
        self.url = 'http://s148.game.hanjiangsanguo.com/index.php?v=0&channel=150&lang=zh-cn&token=%s&token_uid=%s&rand=%s&' % (self.token, self.token_uid, self.rand)
        for k,v in data.items():
            self.url += '&%s=%s'%(k,v)
        #print self.url
        r = requests.post(self.url,headers=headers)
        return r.text
    def action(self,**kwargs):
        """动作参数m={'index':'获取基础账号密码等信息',‘get_monster_list’：“获取副本怪物列表信息”}
        """
        self.action_data = kwargs
        self.serverinfo = self.post_url(self.action_data)
        #print self.serverinfo
        return json.loads(self.serverinfo)
    def copies(self):
        # 扫荡副本需要传递的参数
        # id 是副本名字id ，self.role_info
        # diff_id是困难级别分别为1,2,3个级别
        # monster_id 是第几个怪物，1-10个，
        #times 扫荡的次数
        for  id  in range(1,4):
            #遍历三个副本，
            print '开始扫荡副本:%s'%id
            for  diff_id in range(1,4):
                print '开始扫关卡:%s' % diff_id
                #遍历三个难度，普通，困难，英雄
                for monster_id in range(1,11):
                    #遍历十次小兵
                    print  "开始扫荡小兵"
                    try:
                        times = self.action(c="copies",m="get_monster_info",id=id,diff_id=diff_id,monster_id=monster_id,d="newequip")['info']['free_times']
                    except Exception:
                        pass
                    if times != '0':

                        print self.action(c="copies",m="mop_up",id=id,diff_id=diff_id,monster_id=monster_id,d="newequip",times=int(times))
    def qiandao(self):#签到
        # 领取连续登陆15天奖励，id:15，c:logined，m:get_reward
        print self.action(c='logined',m='index')

        print self.action(c='logined',m='get_reward',id=15)
        #每日签到，所有动作就是c内容，m动作参数即可，包括领取vip工资，还有每日抽奖
        self.action(c='sign',m='sign_index')
        # c:vipwage，m:get_vip_wage，领取VIP每日奖励
        self.action(c='vipwage',m='get_vip_wage')

    def zhengshou(self):#征收
        cishu = self.action(c='city',m='index')#获取银币征收次数,m=impose,执行征收
        cishu_count = cishu['times']
        if cishu_count != '0':#判断征收次数是否为0，不为0则进行全部征收
            for count in range(1,int(cishu_count)+1):
                print '开始征收第 %d 次'%count
                time.sleep(0.5)
                print self.action(c='city',m='impose')
        else:
            print '次数为0次'

    def hitegg(self):#砸蛋
        hitegg_cd = self.action(c='hitegg',m='index')#获取砸蛋首页面
        for i in range(3):
            cd = hitegg_cd['list'][i]['cd']
            if cd == 0:
                print '砸蛋成功'
                _id = i+1
                self.action(c='hitegg',m='hit_egg',id=_id)

    def island(self):#金银洞活动
        #获取当前攻击的次数和金银守护者5的状态，是否为攻击过，如果为1则为可以攻击，为0 则表示不可以
        count = self.action(c='island',m='get_mission',id=85)['info']['act']
        id_open = self.action(c='island',m='index')['list'][4]['openstatus']
        if count <= 10 and id_open != 1:
            for i in range(81,86):#每日共计5次
                print self.action(c='island',m='pk',id=i) #共计金银洞
        id_open = self.action(c='island', m='index')['list'][4]['openstatus']
        if count <= 10 and id_open == 1:
            for i in range(5):
                print self.action(c='island', m='pk', id=85)#共计通过之后的最高金银洞5次
        else:
            print '今天已经攻击了10次不在攻打'
    def worldboss(self):#世界boss领取
        #银币鼓舞
        now_time = time.strftime('%H:%M:%S')
        if  '12:00:00' < now_time < '12:15:00' or '20:00:00' < now_time < '20:15:00':
            boss_info = self.action(c='worldboss',m='index')
            countdown = boss_info['countdown']
            powerup = boss_info['powerup']
            if powerup != 200:
                for i in range(10):
                    self.action(c='worldboss',m='powerup',gold=0)
            while countdown >0:
                #获取boss退出世界
                countdown = boss_info['countdown']
                self.action(c='worldboss',m='battle')
                time.sleep(61)
            if countdown == 0:
                self.action(c='worldboss',m='reward')#reward领取奖励
        else:
            print '世界boos未开始'
    def overseastrade(self):#海外贸易
        #购买粮食，花费银币的，id=1为粮食，id2-5为花费元宝的玛瑙等
        self.action(c='overseastrade',m='buy_item',id=1)
        # 组队 ，检查是否有对， 有则加入，没有则创建 ，开始贸易
        #1获取组队列表
        list_country = self.action(c='overseastrade',m='get_list_by_country',p=1)['list']
        if list_country:#如果列表不为空，说明有组
            #自动加组贸易
            for k,v in list_country.items():#判断第一个角色有值没有，有责加入第二个，没有则加入第一个#需要time_id
                if v['member1'] != '0':#如果不为0 则说明角色有人，加入另一个，
                    print '加入2'
                    self.id = v['id']
                    print self.action(c="overseastrade", m='join_team',id=self.id, place=int(k),site=2,page=1)
                else:
                    print '加入1'
                    self.id = v['id']
                    print self.action(c="overseastrade", m='join_team',id=self.id,place=int(k),site=1, page=1)
                #print list_country[k]['member1']
        else:
            #加入贸易队伍，每页有四个框，为place：1-4，每个框有两个位置site:1-2，页数为page:1-10默认为1即可，
            print self.action(c="overseastrade",m='join_team',id=0,place=4,site=2,page=1)
    def tower(self):#将魂星路
        #领取每日奖励
        self.action(c='tower',m='reward_info')
        self.action(c='tower',m='get_reward')
        #获取次数：
        self.tower_times = self.action(c='tower',m='get_mission_list',s=7)['times']
        print self.action(c='tower',m='mop_up',id=174,times=self.tower_times)

    def business(self):#
        #获取通商次数
        business_times = self.action(c='business',m='index')['times']
        print '可用通商次数 %s'%business_times
        for count in range(business_times):#执行通商次数
            #每次通商是需要输入通商id
            print '开始第 %s 次通商'%count
            business_id=self.action(c='business', m='index')['trader'][0]['id']
            self.action(c='business',m='go_business',id=business_id)
        print '通商完成'
    def generaltask(self):#每日神将
        self.number = self.action(c='generaltask',m='index')['number']#获取次数
        print '开始神将扫荡，共计 %s 次'%self.number
        #使用长孙无忌gid=210000353508
        #怪物id=255
        for count in range(int(self.number)):
             self.action(type=0,id=255,gid='210000398930',c='generaltask',m='action')
        print '神将10次扫荡完毕'
    def sanctum(self):
        #每日宝石领奖
        try:
            print '领取每日宝石奖励'
            self.action(c='sanctum',m='get_reward',type=1,multiple=0)
        except:
            print '已经领取宝石奖励'
        #扫荡宝石次数
        #获取次数
        print '开始扫荡宝石'
        numbers = self.action(c='sanctum',m='select_map',l=3)['times']
        if numbers != 0:
            self.action(c='sanctum',m='action',id=150,num=numbers)
        else:
            print '剩余次数为 %s 次'%numbers
        print '宝石扫荡结束'
    def lottery(self):#每日抽奖
        #c=lottery，m=action
        #获取每日抽奖次数
        self.numbers = self.action(c='lottery',m='index')['log']['info']['total_num']
        print '开始抽奖，剩余次数 %s' % self.numbers
        for num in range(self.numbers):
            self.action(c='lottery',m='action')
        print '抽奖结束'
    def herothrone(self):#
        self.action(c='herothrone',m='index')
        for i in range(3):
            print self.action(c='herothrone',m='start')#开始王座
            #攻击:
            while True:
                flag = self.action(c='herothrone', m='action')['status']
                print  '攻击王座副本'
                if flag == -2:
                    break
    def workshop(self):#玉石收集
        #收取
        for i in range(1,7):
            self.action(c='workshop',m='get_reward',s=i)
    def exploit_tree(self):#木材收集
        #gather收集,site:1,第一个框
        self.action(c='exploit_tree',m='gather',site=1)
        self.action(c='exploit_tree',m='action',site=1)
    def exploit_stone(self):#石头收集
        #exploit_stone，m:{gather收集,action，采集}site:1,第一个框,有三个
        for i in range(1,4):
            self.action(c='exploit_stone', m='gather', site=i)
            self.action(c='exploit_stone', m='action', site=i)
    def heaven(self):#通天塔每日奖励和扫荡
        #获取每日奖励
        self.action(c='heaven',m='get_reward')
        self.times = self.action(c='heaven',m='index')['times']
        if self.times:
            self.action(c='heaven',m='mop_up',id=90,times = self.times)
    def arena(self):#
        self.action(c='arena', m='index')
        self.action(c='arena',m='get_reward')
    def zimap(self):#获取图片
        #levev:7,11，14是红色sh关卡s:1-9，id:6
        #扫荡金色以上5-9
        #获取次数nowmaxtimes
        for level in range(8,11):#遍历每一个图
        #for level in range(14, 17):  # 遍历每一个图红色使用

            print '开始攻击第 %s 个图'%level
            site = len(self.action(c='map',m='get_scene_list',l=level)['list'])

            for i in range(site):#遍历关卡图次数
                print '攻击第 %s 个关卡' %(i+1)
                for id in range(5,10):  # 遍历5个小兵
                #for id in range(4,9):#遍历5个小兵红色使用
                    #判断当前次数是否为0次，如果为0 则不扫荡
                    if level==8 and id !=4:
                        continue
                    times = self.action(c='map',m='mission',l=level,s=i+1,id=id)['info']['nowmaxtimes']
                    #times = self.action(c='map', m='mission', l=level, s=i + 1, id=id)['info']['maxtimes']#红色天赋
                    print '剩余扫荡次数 %s' %times
                    if times !=0:
                        #print 'gongji',level,i+1,id,times
                        print self.action(c='map',m='action',l=level,s=i+1,id=id,times=times)
    def hongmap(self):#获取图片
        #levev:7,11，14是红色sh关卡s:1-9，id:6
        #扫荡金色以上5-9
        #获取次数nowmaxtimes
        #for level in range(8,11):#遍历每一个图
        for level in range(14, 17):  # 遍历每一个图红色使用

            print '开始攻击第 %s 个图'%level
            site = len(self.action(c='map',m='get_scene_list',l=level)['list'])

            for i in range(site):#遍历关卡图次数
                print '攻击第 %s 个关卡' %(i+1)
                #for id in range(5,10):  # 遍历5个小兵
                for id in range(4,9):#遍历5个小兵红色使用
                    #判断当前次数是否为0次，如果为0 则不扫荡
                    try:
                        print self.action(c='map',m='mission',l=level,s=i+1,id=id)['info']
                    except KeyError:
                        continue

                    times = self.action(c='map',m='mission',l=level,s=i+1,id=id)['info']['nowmaxtimes']
                    #times = self.action(c='map', m='mission', l=level, s=i + 1, id=id)['info']['maxtimes']#红色天赋
                    print '剩余扫荡次数 %s' %times
                    if times !=0:
                        #print 'gongji',level,i+1,id,times
                        print self.action(c='map',m='action',l=level,s=i+1,id=id,times=times)
    def guyu(self):#获取古玉购买
        print self.action(c='actguyu',m='reward_index',id=22,num=1)
    def mount_stone(self):
        self.action(c='mountstone_throne', m='index')
        for i in range(3):
            print self.action(c='mountstone_throne', m='start')  # 开始王座
            # 攻击:
            while True:
                flag = self.action(c='mountstone_throne', m='action')['status']
                print  '攻击符石副本'
                if flag == -2:
                    break
    def dice(self):
        for i in range(1,8):
            self.action(c='dice',m='shake_dice')
    def act_steadily(self):#节节高
        info = self.action(c='act_steadily', m='index')
        if info['reward']:
            status = info['status']
            reward_cd = info['reward_cd']
            t = info['reward']['time']
            if reward_cd == 0 and status == 1:
                self.action(c='act_steadily', m='get_online_reward', t=t)
            elif reward_cd == 0 and status != 1:
                status = 3
                return status
            else:
                print '%s分钟后领取,%s' % (reward_cd / 60, reward_cd)

                time.sleep(reward_cd + 1)
                self.action(c='act_steadily', m='get_online_reward', t=t)
        else:
            print '节节高领完奖励'
            status = 3
            return status
    def act_sword(self):#铸剑
        info = self.action(c='act_sword',m='index')
        print info
        need_nums  = int(info['need_nums'])
        nums = info['nums']
        print need_nums,nums
        #收获
        if need_nums == int(nums):
            self.action(c='act_sword', m='index')
            time.sleep(0.5)
            self.action(c='act_sword', m='get_cast_reward')
            time.sleep(0.5)
            self.action(c='act_sword', m='index')
            self.action(c='act_sword', m='start')
        else:
            slp = need_nums - int(nums)
            print slp
            time.sleep(slp*50)
        #print self.action(c='act_sword',m='battle',touid='260000484980')
    def beauty(self):#铜雀台互动
        status = 1
        while status == 1:
            status = self.action(c='beauty',m='active_action',beauty_id=2,type=1)['status']
    def country(self):#每日国家奖励
        self.action(c='country',m='get_salary')
    def countrysacrifice(self):#每日贡献
        self.action(c='countrysacrifice',m='action',id=1)

def main():
    action = SaoDangFb()
    action.arena()  # 获取每日演武奖
    action.qiandao()  # 每日签到
    action.overseastrade()#海外贸易
    action.hitegg()#砸蛋
   # action.heaven()#通天塔
    action.workshop()#玉石采集
    action.exploit_tree()#木材采集
    action.exploit_stone()#石头采集
    action.herothrone()#英雄王座
    action.sanctum()#每日宝石领奖
    action.generaltask()#
    action.business()#每日通商

   # action.tower()#将魂星路
    #action.island()#金银洞
    action.lottery()#每日抽奖
    action.worldboss()#世界boos
    action.copies()  # 扫荡副本
   # action.zimap()
   # action.hongmap()
    action.mount_stone()
    action.dice()
    action.beauty()
    action.countrysacrifice()
    action.country()
if __name__ == '__main__':
    a = SaoDangFb()
    status = 1
    while status == 1:
        status = a.act_steadily()

