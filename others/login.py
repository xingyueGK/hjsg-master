#!/usr/bin/env python
#-*- coding:utf-8 -*-

import requests
import time
import json

headers = {
    'Connection':'keep-alive',
    'Upgrade-Insecure-Requests':'1',
    'Content-Type':'application/json',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
#账号登录信息
class login():
    def __init__(self,username, password):
        #初始化账号密码信息
        self.username = username
        self.password = password
        def get_html():
            # 获取首页html
            url = 'http://uc.game.hanjiangsanguo.com/index.php?&c=user&m=login&&token=&channel=150&lang=zh-cn&rand=150959328607564&u=%s&p=%s'%(self.username,self.password)
            r = requests.session()
            return r.get(url).text
        self.rand = str(int(time.time() * 1000))
        self.token_uid = '210000353508'
        self.addr_info = json.loads(get_html())['serverlist']
        for v in self.addr_info:
            #获取默认登录地址是多少
            if v['selected'] == 1:
                self.addr = v['addr']
                break
        def get_token():
            url = 'http://%s/index.php?v=0&c=login&&m=user&&token=&channel=150&lang=zh-cn&rand=150959405499450&u=%s&p=%s' % (
            self.addr, self.username, self.password)
            token = requests.session().get(url).text
            tokens = json.loads(token)
            return tokens['token']
        self.token = get_token()
    def post_url(self,data):
        #url拼接数据
        self.url = 'http://%s/index.php?&v=2017111501&channel=11&imei=NoDeviceId&platform=android&lang=zh-cn&token=%s&token_uid=%s&rand=%s&' % (self.addr,self.token, self.token_uid, self.rand)
        for k,v in data.items():
            self.url += '&%s=%s'%(k,v)
        r = requests.post(self.url,headers=headers)
        return r.text
    def action(self,**kwargs):
        """动作参数m={'index':'获取基础账号密码等信息',‘get_monster_list’：“获取副本怪物列表信息”}
        """
        self.action_data = kwargs
        self.serverinfo = self.post_url(self.action_data)
        #self.serverinfo
        try:
            return json.loads(self.serverinfo)
        except ValueError as e:
            print e
