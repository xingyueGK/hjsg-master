# -*- coding:utf-8 -8-
import threading
import time
import json
import shujufenx
from shujufenx import fuben

"""每日不定期开展活动"""


def p(message):
    print json.dumps(message, ensure_ascii=False)


def userinfo(username, password, addr):
    act = shujufenx.fuben(username, password, addr)
    info = act.action(c='blackmarket', m='index')  # 获取黑市首页
    memberInfo = act.action(c='member', m='index')
    country = act.action(c='country', m='get_member_list')['country']
    if country:
        countryName = country['name']
    else:
        countryName = None
    name = memberInfo['nickname']  # 账号
    level = memberInfo['level']  # 等级
    act = memberInfo['act']  # 军令
    silver = memberInfo['silver']  # 银币
    gold = memberInfo['gold']  # 元宝
    vip = memberInfo['vip']
    reputation = memberInfo['reputation']  # 声望
    print '\n账号 %s 名字 %s 等级 %s vip %s 国家 %s 军令 %s 银币 %s 元宝 %s 黄宝石 %s 紫宝石 %s 声望 %s' % (
        username, name, level, vip, countryName, act, silver, gold, info['info']['get2'], info['info']['get3'],
        reputation)
    userlist = [username, name, level, vip, countryName, act, silver, gold, info['info']['get2'], info['info']['get3'],
                reputation]
    return userlist


class activity(fuben):
    def sanguo(self):  # 游历三国活动
        try:
            travelindex = self.action(c='act_travel', m='index')  # 获取活动
            details = self.action(c='act_travel', m='action_travel')['details']  # 开始活动
            print travelindex['info']['points']
            if travelindex['info']['free'] == 1:
                result = self.action(c='act_travel', m='action_dice')  # 掷骰子
            if travelindex['info']['points'] != 0:
                # #走路顺序list[4,2,3,5,8,9,10,11,12,13,14]
                plain = [1, 4, 2, 3, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                         28,
                         29,
                         30]
                num = plain.index(int(details['current'])) + 1
                stats = self.action(c='act_travel', m='plain', point=plain[num])
        except:
            pass

    def jingsu(self):  # 竞速奖励
        info = self.action(c='map', m='get_reward_list', channel=11, v=2017122401)
        print info
        for i in info['list']:
            if i['open_status'] == 0:
                print '%s 已通过未领取 ，元宝：%s' % (i['name'], i['gold'])
            elif i['open_status'] == 1:
                print '%s 未通过 ，元宝：%s' % (i['name'], i['gold'])
            elif i['open_status'] == 2:
                print '%s 已通过已领取 ，元宝：%s' % (i['name'], i['gold'])
        # self.action(c='map',m='get_mission_reward',id=120)

    def sign(self):  # 够买签到声望
        index = self.action(c='sign', m='sign_index')
        shop = self.action(c='sign', m='sale_shop')
        for i in shop['reward']:
            self.action(c='sign', m='get_reward', type=2, id=i['id'])

    def fuka(self, num):  # 福卡活动处理
        print '-' * 20
        flag = True
        status = 1
        while flag:
            qm_card = self.action(c='qm_card', m='index')
            index = self.action(c='qm_card', m='get_lottery')
            print '当前福卡', int(index['lottery_num']['score'])
            print '翻牌数', num
            if int(index['lottery_num']['score']) < int(num) and status == 1:
                print '本次花费: %s' % str(qm_card['cost'])
                print '剩余福卡: %s' % str(index['lottery_num']['score'])
                print '开始翻牌'
                if qm_card['cost'] < '50' and status == 1:
                    status = self.action(c='qm_card', m='draw ', v=2018061901)['status']  # 随机翻牌
                    qm_card = self.action(c='qm_card', m='index')
                elif qm_card['cost'] == '50' and qm_card['refresh_times'] != '0':
                    self.action(c='qm_card', m='refresh')  # 重制翻盘
                elif qm_card['cost'] == '50' and qm_card['refresh_times'] == '0':
                    print 'pangzishu:%d,shedingshuzhi:%s' % (int(index['lottery_num']['score']), num)
                    status = self.action(c='qm_card', m='draw ', v=2018061901)['status']  # 随机翻牌
                    qm_card = self.action(c='qm_card', m='index')
                else:
                    flag = False
            else:
                break

        qm_index = self.action(c='qm_card', m='get_lottery')  # 获取福卡商店首页
        qmindex = self.action(c='qm_card', m='action_lottery', id=4)  # 用福卡买1紫宝石,2突飞卡4 1150突飞
        while qmindex['status'] == 1:
            self.action(c='qm_card', m='action_lottery', id=4)
            qmindex = self.action(c='qm_card', m='action_lottery', id=1)  # 用福卡买紫宝石

    def guyu(self):  # 古玉换银币
        info = self.action(c='actguyu', m='index')
        reputation = int(info['reputation'])
        vip = int(info['vip'])
        purple_jade = int(info['purple_jade'])
        if info['vip'] == "1":
            if reputation / 220000 >= 2:
                self.action(c='actguyu', m='reward_index ', id=6, num=2)
            elif reputation / 220000 == 1:
                self.action(c='actguyu', m='reward_index ', id=6, num=1)
            info = self.action(c='actguyu', m='index')
            reputation = int(info['reputation'])
            if reputation / 55000 >= 2:
                self.action(c='actguyu', m='reward_index ', id=5, num=2)
            elif reputation / 55000 == 1:
                self.action(c='actguyu', m='reward_index ', id=5, num=1)
            info = self.action(c='actguyu', m='index')
            reputation = int(info['reputation'])
            if reputation / 11000 >= 2:
                self.action(c='actguyu', m='reward_index ', id=4, num=2)
            elif reputation / 11000 == 1:
                self.action(c='actguyu', m='reward_index ', id=4, num=1)
            self.action(c='actguyu', m='reward_index ', id=1, num=2)
            self.action(c='actguyu', m='reward_index ', id=2, num=2)
            self.action(c='actguyu', m='reward_index ', id=3, num=2)
        else:
            self.action(c='actguyu', m='reward_index ', id=1, num=1)
            self.action(c='actguyu', m='reward_index ', id=2, num=1)
            self.action(c='actguyu', m='reward_index ', id=3, num=1)
            self.action(c='actguyu', m='reward_index ', id=6, num=1)
            self.action(c='actguyu', m='reward_index ', id=5, num=1)
            self.action(c='actguyu', m='reward_index ', id=4, num=1)
            self.action(c='actguyu', m='reward_index ', id=7, num=1)
            self.action(c='actguyu', m='reward_index ', id=8, num=1)
            self.action(c='actguyu', m='reward_index ', id=9, num=1)
        # #所有 古玉够买声望
        info = self.action(c='actguyu', m='index')
        num = info['guyu']
        self.action(c='actguyu', m='reward_index', id=34, num=num)

    def mooncake(self):  # 活动吃月饼
        self.action(c='act_mooncake', m='action', type=1)
        self.action(c='act_mooncake', m='action', type=2)
        self.action(c='act_mooncake', m='action', type=3)

    def generalpool(self):  # 武将池
        self.action(c='act_generalpool', m='index')
        # 免费武将1谋士，2武将
        self.action(c='act_generalpool', m='lottery', type=1)
        self.action(c='act_generalpool', m='lottery', type=2)

    def messages(self):
        print  self.action(c='message', m='get_notice')

    def cuju(self):  # 蹴鞠首页
        try:
            index = self.action(c='act_kemari', m='index')
            for i in index['list']:
                if i['id'] == 2 and i['times'] != 0 and i['cd'] == 0:
                    self.action(c='act_kemari', m='action', type=2)
                elif i['id'] == 1 and i['times'] != 0 and i['cd'] == 0:
                    self.action(c='act_kemari', m='action', type=1)
        except:
            pass

    def gongxiang(self, num=1000):  # 国家贡献
        self.action(c='country', m='get_member_list')
        self.action(c='country', m='storage')
        flag = 0
        donate = 0
        try:
            for i in range(num):
                if flag < 10:
                    result = self.action(c='country', m='donate', type=1)
                    status = result['status']
                    if status == 1:
                        donate += 10
                        print donate
                    else:
                        flag += 1
        except:
            print result
            # self.action(c='country',m='get_member_list')
            # self.action(c='country',m='storage')
            # status = self.action(c='country',m='donate',type=1)['status']
            # while status != 1:
            #       status = self.action(c='country',m='donate',type=1)['status']

    def countrysacrifice(self):  # 国家每日贡献
        self.action(c='country', m='get_salary')
        self.action(c='countrysacrifice', m='action', id=1)

    def tes(self):  # 国家任务
        self.action(c='country', m='get_member_list')
        self.action(c='expostulation', m='support', id=251000004878)

    def business(self):  #
        # 获取通商次数
        business_times = self.action(c='business', m='index')['times']
        print '可用通商次数 %s' % business_times
        for count in range(business_times):  # 执行通商次数
            # 每次通商是需要输入通商id
            print '开始第 %s 次通商' % count
            business_id = self.action(c='business', m='index')['trader'][0]['id']
            self.action(c='business', m='go_business', id=business_id)
        print '通商完成'

    def jinyan(self):  # 国家谨言
        self.action(c='expostulation', m='get_reward', id=251000004881)

    def usebuff(self):
        self.action(c='country_taxes_shop', m='index')
        # buy = self.action(c='country_taxes_shop', m='buy', id=1)
        p(self.action(c='war_college', m='use_buff', need_general=1))

    def act_sword(self):  # 铸剑
        self.action(c='act_sword', m='start')
        # print self.action(c='act_sword', m='battle', touid='291000034922')
        info = self.action(c='act_sword', m='index')

        self.action(c='act_sword', m='get_rank_reward', type=1)
        self.action(c='act_sword', m='get_rank_reward', type=0)
        need_nums = int(info['need_nums'])
        nums = info['nums']
        print need_nums, nums
        # 收获
        if need_nums == int(nums):
            self.action(c='act_sword', m='index')
            time.sleep(0.5)
            print self.action(c='act_sword', m='get_cast_reward')
            time.sleep(0.5)
            self.action(c='act_sword', m='index')
            self.action(c='act_sword', m='start')
        else:
            slp = need_nums - int(nums)
            print slp
            time.sleep(slp * 50)

    def pack(self):  # 卖垃圾装备
        index1 = self.action(c='pack', m='index', type=1)  # 武器
        index3 = self.action(c='pack', m='index', type=3)  # 铠甲
        index4 = self.action(c='pack', m='index', type=4)  # 防御
        index5 = self.action(c='pack', m='index', type=5)  # 兵符
        for equ in index1['list']:  # 遍历未穿戴装备列表
            if equ['quality'] == "3" or equ['quality'] == "1" or equ['quality'] == "2":
                self.action(c='pack', m='sale', id=equ['id'])
        for equ in index3['list']:  # 遍历未穿戴装备列表
            if equ['quality'] == "3" or equ['quality'] == "1" or equ['quality'] == "2":
                self.action(c='pack', m='sale', id=equ['id'])
        for equ in index4['list']:  # 遍历未穿戴装备列表
            if equ['quality'] == "3" or equ['quality'] == "1" or equ['quality'] == "2":
                self.action(c='pack', m='sale', id=equ['id'])
        # c=pack&m=sale&id=291000378856 ,出售制定装备
        # print self.action(c='pack', m='open_box', id=5, num=40)

    def jisi(self):  # 新年活动
        self.action(c='act_spring', m='index')
        index = self.action(c='act_spring', m='sacrifice_index')
        if index['price']['3']['1'] < "50":
            self.action(c='act_spring', m='sacrifice', type=3, resource_type=1)
        if index['price']['1']['1'] < "50":
            self.action(c='act_spring', m='sacrifice', type=1, resource_type=1)
            self.action(c='act_spring', m='sacrifice', type=1, resource_type=2)
        if index['price']['2']['1'] < "50":
            self.action(c='act_spring', m='sacrifice', type=2, resource_type=1)
            self.action(c='act_spring', m='sacrifice', type=2, resource_type=2)

    def leigu(self):
        self.action(c='happy_guoqing', m='get_reward', type=1)

    def fubi(self):
        status = 1
        while status == 1:
            index = self.action(c='act_spring', m='exchange', id=23, v=2018021101)
            status = index['status']

    def jianghun(self):
        index = self.action(c='soul', m='index')
        info = index['pack']['list']
        memberInfo = self.action(c='member', m='index')
        name = memberInfo['nickname']  # 账号
        for i in info:
            if i['name'] in ['穷变战魂', '移山战魂', '形虚战魂']:
                print '账号 :%s ,%s' % (self.username, i['name'])

    def meiri(self):
        for i in range(1, 16):
            print self.action(c='logined', m='get_reward', id=1)

    def chicken(self):
        try:
            chenk = self.action(c='chicken', m='vip_index', v=2018021101)['reward']
            member = self.action(c='member', m='index')
            vip = member['vip']
            print json.dumps(chenk)
            for l in chenk:
                # print vip,l['vip']
                if int(l['vip']) == int(vip):
                    print self.action(c='chicken', m='get_vip_reward', id=l['id'])
                    break
        except:
            pass
        # print self.action(c='chicken', m='get_vip_reward', id=17)
        # print self.action(c='chicken', m='get_vip_reward', id=2)
        # print self.action(c='chicken', m='get_vip_reward', id=3)

    def holiday(self):
        print self.action(c='act_holiday', m='index', v=2018021101)
        print self.action(c='act_holiday', m='add_login_reward', v=2018021101)

    def signs(self):  # 每日福利签到购买
        self.action(c='sign', m='get_reward', type=2, id=95)

    def ivlist(self):  # 邀请好友
        print self.action(c='invitation', m='change', code='nifckpm', v=2018021101)

    def shenshu(self):  # 神树
        index = self.action(c='sacredtree', m='index')
        if int(index['time']) == 1:
            self.action(c='sacredtree', m='watering', type=1, v=2018021101)

    def yuanxiao(self):
        try:
            index = self.action(c='act_lantern', m='index', v=2018021101)
            if index['freetimes'] > 0:
                self.action(c='act_lantern', m='buy', lid=1, mid=1, v=2018021101)
                self.action(c='act_lantern', m='buy', lid=1, mid=2, v=2018021101)
                self.action(c='act_lantern', m='buy', lid=1, mid=3, v=2018021101)
        except:
            pass

    def message(self):
        index = self.action(c='message', m='get_notice')['status']
        for i in xrange(111):
            print self.action(c='worldarena', m='get_server_reward')

    def betray(self):  # 叛国
        self.action(c='country', m='betray')

    def jioncountry(self, name):  # 加入国家
        self.action(c='member', m='index')
        for i in range(1, 85):
            info = self.action(c='country', m='get_rank', page=i)
            for item in info["list"]:
                if item['name'] == name:
                    print item['name'], name
                    id = int(item['id'])
                    print id
                    self.action(c='country', m='apply', id=id)
                    exit(3)

    def gxinfo(self):  # 国家贡献
        self.action(c='country', m='get_member_list')
        info = self.action(c='country', m='storage')
        print  '名次\t昵称\t贡献'
        for i in range(5):
            item = info['list'][i]
            print '%s\t%s\t%s' % (info['list'].index(item), item['nickname'], item['contribute'])

    def actjubao(self):
        self.action(c='actjubao', m='index', v=2018042801)
        self.action(c='actjubao', m='action', type=1, v=2018042801)
        self.action(c='actjubao', m='reward_index', v=2018042801)
        self.action(c='actjubao', m='get_reward', id=1, v=2018042801)

    def jingcai(self):
        # 拍卖行竞拍，魔马超
        self.action(c='act_auction', m='auction', id=61, num=1)

    def wuxing(self, id1, id2):
        self.action(c='member', m='resource_unlock', token_uid=210000353508, pwd=413728)
        info = self.action(c='five_line_guess', m='guessing', guess_type_1=1, guess_id_1=id1, guess_type_2=2,
                           guess_id_2=id2, goods_type=7, num=2000, v=2018061101)
        return info

    def caikuang(self):
        mineinfo = self.action(c='mine', m='index')
        dateline = mineinfo['dateline']
        log = mineinfo['log']
        if log:
            log_dateline = log['dateline']
            lasttime = int(dateline) - int(log_dateline)
            print lasttime
            if lasttime > 14400:
                self.action(c='mine', m='give_up')
                print self.action(c='mine', m='get_silver', s=mineinfo['log']['site'])
                for i in range(1, 6):
                    mineinfo = self.action(c='mine', m='index', p=i)['list']
                    for l in mineinfo:
                        if l['status'] == 0:
                            self.action(c='mine', m='caikuang', p=i, id=l['id'], t=l['type'])
                            break
        else:
            for i in range(1, 6):
                mineinfo = self.action(c='mine', m='index', p=i)['list']
                for l in mineinfo:
                    if l['status'] == 0:
                        self.action(c='mine', m='caikuang', p=i, id=l['id'], t=l['type'])
                        break
                # 占矿

    def countrymine(self):
        try:
            mineinfo = self.action(c='countrymine', m='index')
            print mineinfo
            dateline = mineinfo['dateline']
            log = mineinfo['log']
            if log:
                log_dateline = log['dateline']
                lasttime = int(dateline) - int(log_dateline)
                print lasttime
                for i in range(8, 10):
                    mineinfo = self.action(c='countrymine', m='index', p=i)['list']
                    for l in mineinfo:
                        if l['status'] == 0:
                            self.action(c='countrymine', m='caikuang', p=i, id=l['id'], t=l['type'])
                            break
        except KeyError as e:
            print e, '没有加入国家，或是等级不够'

    def arena(self):  #
        self.action(c='arena', m='index')
        self.action(c='arena', m='get_reward')

    def role(self, name):  # 注册名字
        self.action(c='member', m='select_role', sex=2, name=name)

    def chat(self, ms):  # 获取聊天信息
        chat_index = self.action(c='chat', m='index')
        # for message in chat_index['list']:
        #     print u'%s' % message['nickname'] + ":" + u'%s' % message['message']
        print self.action(c='chat', m='send', message=ms)  # 发送消息

    def rob(self, name, user):  # 海运打劫
        # name 就是打劫的国家[list]
        robtimes = 1
        while robtimes > 0:
            index_result = self.action(c='overseastrade', m='index')
            try:
                robtimes = int(index_result['info']['robtimes'])  # 获取打劫次数
                print '剩余打劫次数{robtimes}'.format(robtimes=robtimes)
            except:
                pass
            try:
                refresh_result = self.action(c='overseastrade', m='refresh', p=1)['team']  # 获取刷新船信息
                if refresh_result['allpage'] > 1:  # 船页数大于1页需要遍历
                    for i in range(refresh_result['allpage']):
                        team_list = self.action(c='overseastrade', m='refresh', p=i + 1)['team']['list']
                        for team in team_list:
                            if team['country_name'] in name:
                                id = team['id']
                                rob_result = self.action(c='overseastrade', m='rob', id=id)
                                print json.dumps(rob_result)
                else:
                    team_list = self.action(c='overseastrade', m='refresh', p=1)['team']['list']
                    for team in team_list:
                        if team['country_name'] in name:
                            id = team['id']
                            rob_result = self.action(c='overseastrade', m='rob', id=id)
                            print json.dumps(rob_result)

            except Exception as e:
                pass

    def jierihaiyun(self, user):  # 节日海外贸易
        self.action(c='message', m='index')
        index = self.action(c='overseastrade', m='index')
        # 购买粮食，花费银币的，id=1为粮食，id2-5为花费元宝的玛瑙等
        if int(index['info']['times']) > 0:
            while True:
                try:
                    info = self.action(c='overseastrade', m='renew', v=2018061901)
                    print json.dumps(info)
                    if info['reward'] > '3':  # and info['renew'] < '880':#封顶200元宝，如果不限制元宝要注释renew
                        self.action(c='overseastrade', m='buy_item', id=int(info['reward']))
                        break
                #    elif  info['renew'] > '80':
                #        self.action(c='overseastrade', m='buy_item', id=int(info['reward']))
                #        break
                except Exception as e:
                    break
            # 组队 ，检查是否有对， 有则加入，没有则创建 ，开始贸易
            # 1获取组队列表
            list_country = self.action(c='overseastrade', m='get_list_by_country', p=1)['list']

            # 加入贸易队伍，每页有四个框，为place：1-4，每个框有两个位置site:1-2，页数为page:1-10默认为1即可，
            print self.action(c="overseastrade", m='join_team', id=0, place=4, site=2, page=5)
            self.action(c="overseastrade", m='trade', v=0)  # 开启
            time.sleep(0.2)
        index = self.action(c='overseastrade', m='index')
        print '{} 剩余贸易次数：{}'.format(user, index['info']['times'])

    def peiyang(self, name, attribute='wuliup'):
        """
        :param gid: 武将名字
        :param attribute: 培养属性 'zhiliup','wuliup'
        :return:
        """
        print '开始培养'
        index = self.action(c='cultivate', m='index')
        for k, v in index['list'].items():
            print v['name']
            if v['name'] == name:
                gid = v['id']
                limit = str(int(v['level']) + 20)  # 属性值上限
                initnum = v[attribute]  # 当前值
                print limit, initnum
                while int(initnum) < int(limit):
                    print '=' * 20
                    index = self.action(c='cultivate', m='roll', mode=1, gid=gid)
                    print json.dumps(index)
                    roll = index['info'][attribute]
                    print '智力值是：', initnum, limit
                    print '剩余银币', index['info']['silver']
                    print 'roll 值', roll
                    if int(roll) <= int(initnum):
                        print '放弃'
                        self.action(c='cultivate', m='giveup', gid=gid)  # 放弃
                    else:
                        result = self.action(c='cultivate', m='save', gid=gid)  # 保存
                        initnum = roll
                        print '保存'
                        print json.dumps(result)
                print 'name: %s  属性值 %s' % (name, initnum)

    def blackmarket(self):  # 黑市购买军令，突飞卡
        # buy_type 1 是银币  2 是元宝 5 是紫石头
        index = self.action(c='blackmarket', m='index')
        times = index['info']['times']

    def matrix(self):
        genral_dict = {}
        matrix_index = self.action(c='matrix', m='index')
        general = matrix_index['general']
        for k, v in general.items():
            name = v['name']
            genral_dict[name] = v['id']
        return genral_dict

    def update_matrix(self, mid=4):
        genral_info = self.matrix()
        if mid != 4:
            print '下全部将领'
            lists = '0,0,0,0,0,0,0,0,0'
        else:
            lists = '%s,-1,%s,-1,%s,-1,%s,-1,%s' % (
                genral_info[u'蔡文姬'], genral_info[u'神周仓'], 0, 0, 0)
        print self.action(c='matrix', m='update_matrix', list=lists, mid=4)
        print self.action(c='matrix', m='use_matrix', mid=4)

    def years_guard(self):  # 周年守护签到
        self.action(c='years_guard', m='des_index')
        self.action(c='years_guard', m='sign_index')

    def fukubukuro(self):  # 周年福矿签到
        self.action(c='fukubukuro', m='index')
        self.action(c='fukubukuro', m='sign', type=1)
        self.action(c='fukubukuro', m='get_general', gid=354)

    def zhounianfukuang(self, username):  # 周年矿
        self.action(c='fukubukuro', m='index')
        self.action(c='fukubukuro', m='get_mine_discription')
        mineinfo = self.action(c='fukubukuro', m='mine')
        dateline = mineinfo['dateline']
        log = mineinfo['log']
        times = log['times']
        fukuangstatus = log['site']  # 为空说明没有下矿，反之已经占领矿
        if times == '0' and fukuangstatus == '0':
            print username, '未占矿，剩余次数为0'
            exit(1)
        elif times == '0' and fukuangstatus != '0':
            # 收取占领的矿
            print '收货抢劫矿'
            log_dateline = log['jointime']
            lasttime = int(dateline) - int(log_dateline)
            print lasttime
            if lasttime > 3600:
                print self.action(c='fukubukuro', m='harvest_mine', s=mineinfo['log']['site'])
                print '退出'
                exit(2)
        elif times != "0" and fukuangstatus != '0':
            log_dateline = log['jointime']
            lasttime = int(dateline) - int(log_dateline)
            print lasttime
            if lasttime > 3600:
                print self.action(c='fukubukuro', m='harvest_mine', s=mineinfo['log']['site'])
                for i in range(10, 0, -1):
                    mineinfo = self.action(c='fukubukuro', m='mine', p=i)['list']
                    for l in mineinfo:
                        if l['status'] == 0:
                            status = self.action(c='fukubukuro', m='action_mine', p=i, id=l['id'], t=l['type'])
                            if status['status'] != 1:
                                continue
                            else:
                                print '占矿'
                    #             exit(3)
        else:
            for i in range(10, 0, -1):
                mineinfo = self.action(c='fukubukuro', m='mine', p=i)['list']
                for l in mineinfo:
                    if l['status'] == 0:
                        status = self.action(c='fukubukuro', m='action_mine', p=i, id=l['id'], t=l['type'])
                        if status['status'] != 1:

                            continue
                        else:
                            print '占矿'
                            exit(3)
                # 占矿

    def robfukuang(self, username, countryname):  # 打劫周年礦城
        self.action(c='fukubukuro', m='index')
        self.action(c='fukubukuro', m='get_mine_discription')
        mineinfo = self.action(c='fukubukuro', m='mine')
        robtimes = mineinfo['log']['robtimes']  # 打劫次数
        dateline = mineinfo['dateline']
        log = mineinfo['log']
        times = log['times']
        fukuangstatus = log['site']
        print '剩余打劫次数为{times}'.format(times=times)
        if robtimes == "0" and fukuangstatus == "0":

            exit(1)
        elif robtimes != "0" and fukuangstatus == "0":
            for page in range(10, 0, -1):
                try:
                    info = self.action(c='fukubukuro', m='mine', p=page)['list']
                    for item in info:
                        try:
                            if item['status'] == 1 and item['country'] in countryname:
                                print '打劫'
                                status = self.action(c='fukubukuro', m='loot_mine', p=item['page'], id=item['id'],
                                                     t=item['type'])
                                if status['status'] != 1:
                                    continue
                                else:
                                    exit(3)
                        except Exception as e:
                            print 'aaaaaaaaaaaaaa', e
                except Exception as e:
                    print 'wwwwwwwwwww', e
        else:
            print '收矿'
            self.zhounianfukuang(username)

    def fq(self):  # 打劫周年礦城
        self.action(c='fukubukuro', m='index')
        self.action(c='fukubukuro', m='get_mine_discription')
        mineinfo = self.action(c='fukubukuro', m='mine')
        self.action(c='fukubukuro', m='give_up')

    def fukuang(self):
        info = self.action(c='fukubukuro', m='index')
        print json.dumps(info)

    def springshop(self, name=u'聊得'):  # 武將商城
        spring = self.action(c='springshop', m='index')['list']
        self.action(c='springshop', m='buy', id=1)
        # self.action(c='springshop', m='buy', id=1)
        self.action(c='springshop', m='buy', id=3)
        self.action(c='springshop', m='buy', id=10)
        self.action(c='springshop', m='buy', id=17)
        # for item in spring:
        #     if item['name'] == name:
        #         self.action(c='springshop', m='buy',id=item['id'])

    def unlock(self, pwd):
        self.action(c='member', m='resource_unlock', token_uid=210000353508, pwd=pwd)

    def znhh(self):
        # 周年喊话
        result = self.action(c='act_halloween', m='index')
        hammer = result['hammer']
        for i in range(int(result['candy'])):
            self.action(c='act_halloween', m='action_candy')
        for i in range(10):
            for i in range(1, 10):
                self.action(c='act_halloween', m='action_pumpkin', id=i)

    def zhounianshop(self):
        medal = self.action(c='fukubukuro', m='index')['medal']
        print medal
        # self.action(c='fukubukuro', m='shop', type=1,)
        # self.action(c='fukubukuro', m='shop', type=2, )
        # self.action(c='fukubukuro',m='shop_buy',type=1,id=24)
        # self.action(c='fukubukuro', m='shop_buy', type=1, id=35)
        # self.action(c='fukubukuro', m='shop_buy', type=1, id=35)


# 周年比购物

# def wx():#五行竞猜刷数据
# for i in range(100):
# id1 = random.randint(1, 5)
# id2 = random.randint(1, 12)
# sum = 0
# jin = 0
# mu = 0
# shui = 0
# huo = 0
# tu = 0
# for i in range(5):
#     infos = action.wuxing(id1,id2)
#     if infos['five_line']['id'] == "1":
#         jin += 1
#     elif infos['five_line']['id'] == "2":
#         mu += 1
#     elif infos['five_line']['id'] == "3":
#         shui += 1
#     elif infos['five_line']['id'] == "4":
#         huo += 1
#     elif infos['five_line']['id'] == "5":
#         tu += 1
#     sum +=infos['reward_num']
#     print infos['reward_num']
# print id1, id2
# print '共计：',sum - 10000
# print jin,mu,shui,huo,tu
# action.generalpool()
# action.fuka()
# action.messages()
if __name__ == '__main__':
    def act(user, apass, addr):
        action = activity(user, apass, addr)
        # action.pack()
        # action.mooncake()
        action.leigu()
        # action.peiyang('张昭')
        # action.generalpool()#
        # action.cuju()
        action.shenshu()
        # action.fuka()
        # action.caikuang()
        # action.chenk()
        action.jisi()


    def task(user, apass, addr):  # 节节高买突飞
        action = activity(user, apass, addr)
        # action.actjubao()
        # action.morra()
        # action.gongxiang()
        # action.lottery()#抽奖
        # action.actjubao()
        # action.leigu()
        action.shenshu()
        # action.qiandao()
        # action.actjubao()
        # action.jisi()
        # action.guyu()
        # action.gongxiang()
        # action.usebuff()
        # action.sign()
        # action.fuka(15)
        # action.fukubukuro()
        # action.holiday()
        # action.chicken()
        # action.years_guard()


    def zhujian(user, apass, addr):
        while True:
            action = activity(user, apass, addr)
            # action.unlock(413728)
            action.act_steadily()


    def xinnain(user, apass, addr):
        action = activity(user, apass, addr)
        # action.leigu()
        # action.shenshu()
        action.actjubao()


    def fanpai(user, apass, addr):
        action = activity(user, apass, addr)
        action.fuka(15)


    def haiyun(user, apass, add):
        action = activity(user, apass, add)
        # action.jierihaiyun(user)
        action.overseastrade()
        # action.countrymine()


    def jion(user, apass, addr):  # 加入腐败天朝
        action = activity(user, apass, addr)
        action.jioncountry('光芒神殿')


    def gongxian(user, apass, addr):
        action = activity(user, apass, addr)
        action.gongxiang()


    def panguo(user, apass, addr):
        action = activity(user, apass, addr)
        action.betray()


    def dajie(user, apass, addr):
        action = activity(user, apass, addr)
        action.rob(['体检了', '8523', '英雄', '是你学姐', '杰克傻bi'], user)


    def jianghun(user, apass, addr):
        action = activity(user, apass, addr)
        action.jianghun()


    def buff(user, apass, addr):
        action = activity(user, apass, addr)
        action.usebuff()


    def ylsanguo(user, apass, addr):
        action = activity(user, apass, addr)
        action.sanguo()


    def chat(user, apass, addr):
        action = activity(user, apass, addr)
        # action.gxinfo()
        action.chat(u"悍将三国六周年快乐")


    def upmatrix(user, apass, addr):  # 更新出征武将
        action = activity(user, apass, addr)
        action.update_matrix(mid=4)


    def guyuyinbi(user, apass, addr):  # 换古玉买银币
        action = activity(user, apass, addr)
        action.sign()  # 购买签到声望
        action.guyu()


    def rolename(user, apass, addr, name):  # 更新出征武将
        action = activity(user, apass, addr)
        action.role(name)


    def zhouniankuang(user, apass, addr):  # 更新出征武将
        action = activity(user, apass, addr)
        action.zhounianfukuang(user)


    def robfu(user, apass, addr):  # 更新出征武将
        action = activity(user, apass, addr)
        action.robfukuang(user, ['体检了', '杰克吃翔', '杰克喝尿', '悍龙', '梦', '炎黄天都', '杰克喝sui'])


    def znshop(user, apass, addr):  # 周年福矿商店
        action = activity(user, apass, addr)
        action.jingcai()


    def practice(user, apass, addr):  # 周年福矿商店
        action = activity(user, apass, addr)
        action.tufei(u'神周仓', 100)


    def equip_strengthen(user, apass, addr):  # 强化，穿戴装备
        action = activity(user, apass, addr)
        gid, uid = action.general()  # 获取三级装备，再次强化，并给武将穿戴上
        for i in uid:
            for etype, v in i.items():
                # action.strengthen(v)
                action.equip(gid, v, etype)


    def chuan():
        with open('../users/alluser.txt', 'r') as f:
            # with open('../users/duguyi.txt', 'r') as f:
            for i in f:
                if i.strip():
                    name = i.split()[0]
                    # name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    addr = 21
                    t1 = threading.Thread(target=userinfo, args=(name, passwd, addr))
                    t1.start()
                    # t1.join()
                    # time.sleep(0.2)


    def ck():
        cont = ['149cnm.txt', '149dgj.txt', '149gx1.txt', '149xx.txt', '149xb.txt', '149lwzs.txt']
        for t in cont:
            with open('../users/%s' % t, 'r') as f:
                for i in f:
                    if i.strip():
                        user = i.split()[0]
                        passwd = i.split()[1]
                        addr = 149
                        t1 = threading.Thread(target=guyuyinbi, args=(user, passwd, addr))
                        t1.start()
                        time.sleep(0.1)

    def dg():
        cont = ['150.txt', '150num.txt', '150nm.txt']
        for t in cont:
            with open('../users/%s' % t, 'r') as f:
                for i in f:
                    if i.strip():
                        user = i.split()[0]
                        passwd = i.split()[1]
                        addr = 150
                        t1 = threading.Thread(target=guyuyinbi, args=(user, passwd, addr))
                        t1.start()


    # chat('xingyue123a',413728161,148)
    #ck()
    dg()
    #chuan()
