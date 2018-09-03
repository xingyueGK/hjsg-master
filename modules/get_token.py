#!/usr/bin/env python
#-*- condint:utf-8 -*-

import requests
import time
import json


headers = {
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Host':'game.hanjiangsanguo.com',
    'Upgrade-Insecure-Requests':'1',
    'Content-Type':'application/json',
    'DNT':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
def get_token(username,password,addr):
   username = username
   password = password
   addr = "s%s.game.hanjiangsanguo.com" % (addr)
   rand = int(time.time() * 1000)
   token_uid = '210000353508'
   url = 'http://%s/index.php?v=0&c=login&&m=user&&token=&channel=150&lang=zh-cn&rand=150959405499450&u=%s&p=%s' % (
       addr, username, password)
   token = requests.session().get(url,headers=headers).text
   tokens = json.loads(token)
   return tokens['token']

if __name__ == '__main':
    token = get_token()
