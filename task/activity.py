#!/usr/bin/env python
#-*- coding:utf-8 -*-
import time

from base import SaoDangFb

class activity(SaoDangFb):
    """每日任务活动"""
    def qiandao(self):#签到
        # 领取连续登陆15天奖励，id:15，c:logined，m:get_reward
        self.action(c='logined',m='index')
        self.action(c='logined',m='get_reward',id=15)
        #每日签到，所有动作就是c内容，m动作参数即可，包括领取vip工资，还有每日抽奖
        self.action(c='sign',m='sign_index')
        # c:vipwage，m:get_vip_wage，领取VIP每日奖励
        self.action(c='vipwage',m='get_vip_wage')
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
                self.action(c='island',m='pk',id=i) #共计金银洞
        id_open = self.action(c='island', m='index')['list'][4]['openstatus']
        if count <= 10 and id_open == 1:
            for i in range(5):
                self.action(c='island', m='pk', id=85)#共计通过之后的最高金银洞5次
        else:
            print '今天已经攻击了10次不在攻打'
    def worldboss(self):#世界boss领取
        #银币鼓舞
        now_time = time.strftime('%H:%M:%S')
        if  '20:00:00' < now_time < '20:15:00':
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

    def overseastrade(self): #海运
        self.action(c='message', m='index')
        self.action(c='overseastrade', m='index')
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
                    self.action(c="overseastrade", m='join_team', id=self.id, place=int(k), site=1, page=1)
                    # print list_country[k]['member1']
        else:
            # 加入贸易队伍，每页有四个框，为place：1-4，每个框有两个位置site:1-2，页数为page:1-10默认为1即可，
            print self.action(c="overseastrade",m='join_team',id=0,place=4,site=2,page=1)
    def tower(self):#将魂星路
        #领取每日奖励
        self.action(c='tower',m='reward_info')
        self.action(c='tower',m='get_reward')
        self.action(c='tower',m='get_mission_list',s=7)
        #获取次数：
        self.tower_times = self.action(c='tower',m='get_mission_list',s=7)['times']
        self.action(c='tower',m='mop_up',id=174,times=self.tower_times)
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
        #使用魔张亮gid=251000020801
        #怪物id=255
        for count in range(int(self.number)):
             self.action(type=0,id=255,gid='251000020801',c='generaltask',m='action')
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
    def herothrone(self):#英雄王座
        self.action(c='herothrone',m='index')
        for i in range(3):
            self.action(c='herothrone',m='start')#开始王座
            #攻击:
            while True:
                flag = self.action(c='herothrone', m='action')['status']
                print  '攻击王座副本'
                if flag == -2:
                    break
    def heaven(self):#通天塔每日奖励和扫荡
        #获取每日奖励
        self.action(c='heaven',m='get_reward')
        times = self.action(c='heaven',m='index')['times']
        if times:
            self.action(c='heaven',m='mop_up',id=90,times = times)
    def arena(self):#竞技场奖励
        self.action(c='arena', m='index')
        self.action(c='arena',m='get_reward')
    def xinnian(self):#新年活动
        index = self.action(c='act_spring',m='sacrifice_index',v=2018021101)
        if index['price']['1']['1']< "60":
            self.action(c='act_spring', m='sacrifice', type=1, resource_type=1)
        if index['price']['2']['1']< "60":
            self.action(c='act_spring', m='sacrifice', type=2, resource_type=1)
        if index['price']['3']['1']< "60":
            self.action(c='act_spring', m='sacrifice', type=3, resource_type=1)
def main():
    action = activity(num=21,user='xingyue123',passwd='413728161')
    action.tower()
    action.overseastrade()
    action.business()
    action.worldboss()
    action.herothrone()
    action.island()
    action.qiandao()
    action.hitegg()
    action.arena()
    action.lottery()
    action.generaltask()
    action.sanctum()
    action.heaven()
if __name__ == '__main__':
    main()