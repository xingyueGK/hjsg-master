#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/27 11:05
# @Author  : xingyue
# @File    : country_shop.py

#国家商店购买

"""
{"status":1,"shop_list":{"status":1,"list":[{"id":"1","type":"32","value":"1","limit_type":"2","num":0,"taxes":"5","openlevel":"30","is_open":1,"limit":"0","is_take":0,"times":0},{"id":"12","type":"28","value":"1","limit_type":"2","num":10,"taxes":"30","openlevel":"30","is_open":1,"limit":"10","is_take":1,"times":0},{"id":"23","type":"28","value":"10","limit_type":"1","num":8,"taxes":"290","openlevel":"30","is_open":1,"limit":"20","is_take":1,"times":12},{"id":"25","type":"28","value":"20","limit_type":"1","num":0,"taxes":"400","openlevel":"30","is_open":1,"limit":"5","is_take":0,"times":5},{"id":"11","type":"27","value":"5","limit_type":"2","num":10,"taxes":"30","openlevel":"30","is_open":1,"limit":"10","is_take":1,"times":0},{"id":"22","type":"27","value":"50","limit_type":"1","num":8,"taxes":"290","openlevel":"30","is_open":1,"limit":"20","is_take":1,"times":12},{"id":"24","type":"27","value":"100","limit_type":"1","num":0,"taxes":"10","openlevel":"30","is_open":1,"limit":"5","is_take":0,"times":5},{"id":"10","type":"16","value":"150","limit_type":"2","num":50,"taxes":"30","openlevel":"30","is_open":1,"limit":"50","is_take":1,"times":0},{"id":"21","type":"16","value":"1500","limit_type":"1","num":8,"taxes":"290","openlevel":"30","is_open":1,"limit":"20","is_take":1,"times":12},{"id":"9","type":"15","value":"2750","limit_type":"2","num":50,"taxes":"30","openlevel":"30","is_open":1,"limit":"50","is_take":1,"times":0},{"id":"20","type":"15","value":"27500","limit_type":"1","num":7,"taxes":"290","openlevel":"30","is_open":1,"limit":"20","is_take":1,"times":13},{"id":"8","type":"14","value":"120000","limit_type":"2","num":50,"taxes":"30","openlevel":"30","is_open":1,"limit":"50","is_take":1,"times":0},{"id":"19","type":"14","value":"1200000","limit_type":"1","num":10,"taxes":"290","openlevel":"30","is_open":1,"limit":"20","is_take":1,"times":10},{"id":"2","type":"11","value":"1000","limit_type":"2","num":20,"taxes":"65","openlevel":"30","is_open":1,"limit":"20","is_take":1,"times":0},{"id":"13","type":"11","value":"10000","limit_type":"1","num":11,"taxes":"640","openlevel":"30","is_open":1,"limit":"20","is_take":1,"times":9},{"id":"7","type":"9","value":"12000","limit_type":"2","num":20,"taxes":"30","openlevel":"30","is_open":1,"limit":"20","is_take":1,"times":0},{"id":"18","type":"9","value":"120000","limit_type":"1","num":14,"taxes":"290","openlevel":"30","is_open":1,"limit":"20","is_take":1,"times":6},{"id":"5","type":"7","value":"5000","limit_type":"2","num":20,"taxes":"400","openlevel":"30","is_open":1,"limit":"20","is_take":1,"times":0},{"id":"16","type":"7","value":"50000","limit_type":"1","num":8,"taxes":"1900","openlevel":"30","is_open":1,"limit":"20","is_take":1,"times":12},{"id":"6","type":"6","value":"900000","limit_type":"2","num":20,"taxes":"20","openlevel":"30","is_open":1,"limit":"20","is_take":1,"times":0},{"id":"17","type":"6","value":"9000000","limit_type":"1","num":16,"taxes":"190","openlevel":"30","is_open":1,"limit":"20","is_take":1,"times":4},{"id":"4","type":"4","value":"50","limit_type":"2","num":20,"taxes":"400","openlevel":"30","is_open":1,"limit":"20","is_take":1,"times":0},{"id":"15","type":"4","value":"500","limit_type":"1","num":12,"taxes":"1900","openlevel":"30","is_open":1,"limit":"20","is_take":1,"times":8},{"id":"3","type":"3","value":"500","limit_type":"2","num":20,"taxes":"130","openlevel":"30","is_open":1,"limit":"20","is_take":1,"times":0},{"id":"14","type":"3","value":"5000","limit_type":"1","num":6,"taxes":"1200","openlevel":"30","is_open":1,"limit":"20","is_take":1,"times":14}]},"member_info":{"status":1,"info":{"id":"14900000002061","uid":"14900004864052","country_id":"14900000000374","taxes":"51780","dateline":"1520571099","contribute":"41548","general":"9"}}}
"""
from task.base import SaoDangFb
from utils.mylog import MyLog

import threading
import os,time

class country_taxes_shop(SaoDangFb):
    def __init__(self,logger,*args):
        super(country_taxes_shop,self).__init__(*args)
        self.log = logger
    def index(self):
        index = self.action(c='country_taxes_shop',m='index')
        return index
    def buy(self):
        index = self.index()
        taxes = index['member_info']['info']['taxes']
        shop_list = index['shop_list']['list']
        #购买蓝宝石
        self.action(c='country_taxes_shop', m='buy', id=32, buy_number=5)
        for item in shop_list:
            if item['is_open'] == 1 and int(item['openlevel']) != 250:
                if item['id'] ==1:
                    continue
                else:
                    #如果 limit_type ==1 国家今日剩余次数
                    if int(item['limit_type']) == 1:
                        if int(item['is_take']) == 0:
                            print 'sold out'
                            continue
                        elif int(item['is_take']) == 1:
                            self.action(c='country_taxes_shop',m='buy',id=item['id'],buy_number=1)
                        elif int(item['is_take']) == 2:
                            self.log.info('your purchased ')
                    else:
                        self.log.info(item)
                        if int(item['is_take']) == 0:
                            self.log.info(self.user + 'sold out')
                            continue
                        elif int(item['is_take']) == 1:
                            self.action(c='country_taxes_shop',m='buy',id=item['id'],buy_number=int(item['num']))
            else:
                self.log.debug('国家等级达到{}级开启'.format(item['openlevel']))

def main(name, passwd, addr):
    log = MyLog(logname="country_shop")
    a = country_taxes_shop(log,name, passwd, addr)
    a.buy()

if __name__ == '__main__':

    filepath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # cont = ['21user.txt', 'autouser.txt','gmnewyear.txt', 'user.txt', 'alluser.txt']
    cont = ['countryshop.txt']
    for t in cont:
        with open('%s/users/%s' % (filepath, t), 'r') as f:
            for i in f:
                if i.strip() and not i.startswith('#'):
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    # addr = 147
                    t1 = threading.Thread(target=main, args=(name, passwd, addr))
                    t1.start()