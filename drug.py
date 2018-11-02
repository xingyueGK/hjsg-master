#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/10 10:37
# @Author  : xingyue
# @File    : task.py


from task.base import SaoDangFb
import  time,threading
import os,json
class task(SaoDangFb):
    def drugrefresh(self):#经脉刷新
        self.action(c='drug', m='refresh')
    def drug(self):#经脉
        try:
            print '经脉购买'
            index = self.action(c='drug', m='index')
            shop_index= self.action(c='drug', m='shop_index')
            remain_freetimes = shop_index['remain_freetimes']
            for i in range(remain_freetimes):
                for  item in shop_index['list']:
                    # sub_type 为1 使用元宝购买  goods_type 为 82 暂时用不到的金丹
                    if item['goods_type'] != "82" or item['sub_type'] != "1":
                        # 购买经脉
                        id = item['id']
                        reward_index=self.action(c='drug', m='reward_index', id=id)
                        print json.dumps(reward_index)
                self.drugrefresh()
        except Exception as e:
            print e
def run(user,apass, addr):
    action = task(user,apass, addr)
    action.drug()
if __name__ == '__main__':
    filepath = os.path.dirname(os.path.abspath(__file__))
    cont = ['user.txt']
    for t in cont:
        with open('%s/users/%s'%(filepath,t),'r') as f:
            for i in f:
                if i.strip() :
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    t1 = threading.Thread(target=run, args=(name, passwd, addr))
                    t1.start()
