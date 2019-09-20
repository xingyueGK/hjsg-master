#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/7 10:48
# @Author  : xingyue
# @File    : hero_soul.

#端午节活动

import  time,random

class DragonBoat(object):
    def index(self):
        reult = self.action(c='dragon_boat',m='index')
        return  reult
    def zongziindex(self):
        reult = self.action(c='dragon_boat',m='zongzi_index')
        return reult
    def take_knife(self,t,num):
        """领取元宝
        一般都是 type 3 num 1
        :param type:
        :param num:
        :return:
        """
        formdata = {
            'type':t,
            'num':num
        }
        reult = self.action(c='dragon_boat',m='take_knife',body=formdata)
        return reult
    def boat_index(self):
        #划龙舟首页
        reult = self.action(c='dragon_boat',m='boat_index')
        return reult


    def go_boat(self):
        #开始龙舟比赛 {"status":1,"direction":[2,3,1,3,4,2]}
        reult = self.action(c='dragon_boat',m='go_boat')
        return reult
    def rowing_boat(self,l):
        #开始龙舟比赛
        if isinstance(l,str):
            l = list(l)

        l = ",".join([str(i) for i in l])
        formdata = {
            'list':l
        }
        reult = self.action(c='dragon_boat',m='rowing_boat',body=formdata)
        print reult['status'],reult['msg']
        return reult

    def longzhou(self):
        self.index()
        index = self.zongziindex()
        if int(index['is_take']) != 0:
            self.p(self.take_knife(3,1))
        boat = self.boat_index()
        times = boat['times']
        print '%s剩余龙舟次数为 %s' %(self.user,times)
        for i in range(times):
            result = self.go_boat()
            time.sleep(3)
            self.p(result)
            if result['status'] !=1:
                self.p(result)
                return False
            direction = result['direction']
            for i in range(12):
                time.sleep(random.randint(1,3))
                print '开始步伐',direction
                try:
                    if int(result['status'])  == 13:
                        print result['msg']
                        break
                    elif int(result['status']) != 1:
                        print result['msg']
                        continue
                    direction = self.rowing_boat(direction)['direction']
                except:
                    break
                print '后面步法',direction
                self.boat_index()

class GoBoat(object):
    def sui(self):
        #随机报错
        a = (random.randint(1, 50))
        if a in [5]:
            return True
    def boat_index(self):
        resutl = self.action(c='go_boating',m='boat_index')
        return resutl

    def go_boat(self):
        # 开始龙舟比赛 {"status":1,"direction":[2,3,1,3,4,2]}
        reult = self.action(c='go_boating', m='go_boat')
        return reult

    def rowing_boat(self, l):
        # 开始龙舟比赛
        if isinstance(l, str):
            l = list(l)

        l = ",".join([str(i) for i in l])
        formdata = {
            'list': l
        }
        reult = self.action(c='go_boating', m='rowing_boat', body=formdata)
        print reult['status'], reult['msg']
        return reult
    def buytimes(self,num):
        bootindx = self.boat_index()
        cost = int(bootindx['cost'])
        butimes = cost /50 -1
        print '已经购买%s次,需要购买 %s 次，还需购买%s次'%(butimes,num, num -butimes)
        if butimes >= num:
            return
        else:
            for i in range(num -butimes):
                status = self.action(c='go_boating', m='buy_time')
                self.boat_index()
    def longzhou(self):
        boat = self.boat_index()
        times = boat['times']
        print '%s剩余龙舟次数为 %s' % (self.user, times)
        for i in range(times):
            result = self.go_boat()
            time.sleep(3)
            self.p(result)
            if result['status'] != 1:
                self.p(result)
                return False
            direction = result['direction']
            for i in range(12):
                time.sleep(random.randint(1, 3))
                try:
                    if int(result['status']) == 13:
                        print result['msg']
                        break
                    elif int(result['status']) != 1:
                        print result['msg']
                        continue
                    if self.sui():
                        num = random.randint(1,5)
                        if direction[num] == 4:
                            direction[num] = random.randint(1,3)
                        else:
                            direction[num] = direction[num]+1
                    print '开始步伐', direction
                    direction = self.rowing_boat(direction)['direction']
                except:
                    break
                print '后面步法', direction
                self.boat_index()
    def meter_reward(self):
        #获取奖励
        for i in range(1,11):
            formdata = {
                'id': i
            }
            self.action(c='go_boating',m='meter_reward',body=formdata)