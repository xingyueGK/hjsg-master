# -*- coding:utf-8 -*-


import requests
import time
import json
import  sys
reload(sys)
sys.setdefaultencoding('utf-8')
import threading
headers = {
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Upgrade-Insecure-Requests':'1',
    'Content-Type':'application/json',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

class TokenErr(Exception):
    pass


class SaoDangFb(object):
    def  __init__(self,user,passwd,num):
        #随机请求参数
        self.num = num
        self.user = user
        self.passwd = passwd
        self.rand = int(time.time()*1000)
        self.token_uid = '210000353508'
        self.token = self.get_token(self.num, self.user, self.passwd)
        #POST基础URL地址
        self.url = 'http://s{0}.game.hanjiangsanguo.com/index.php?v=0&channel=150&lang=zh-cn&token={1}&token_uid={2}&rand={3}&'.format(self.num,self.token,self.token_uid,self.rand)
    @staticmethod
    def get_token(num, user, passwd):
        url = 'http://s{num}.game.hanjiangsanguo.com/index.php?u={user}&p={passwd}&v=0&c=login&&m=user&&token=&channel=150&lang=zh-cn&rand=150959405499450'.format(
            num=num, user=user, passwd=passwd)
        token_dict = {}
        try:
            with open("token.json", 'r') as f:
                json_dict = json.load(f)
                if user not in json_dict:
                    raise TokenErr
                token = json_dict[user]
                login = 'http://s{num}.game.hanjiangsanguo.com/index.php?c=member&m=index&v=0&token={token}&channel=150&lang=zh-cn&rand=150959405499450'.format(
                    num=num, token=token)
                r = requests.get(login)
                if r.text == '403':
                    raise TokenErr('token expire')
                else:
                    return token
        except IOError:
            with open("token.json", 'a') as f:
                token_dict[user] = requests.get(url).json()['token']
                json.dump(token_dict, f)
                return token_dict[user]
        except TokenErr:
            with open("token.json", 'r') as f:
                token_dict = json.load(f)
            with open("token.json", 'w') as f:
                print 'jishi'
                a = time.time()
                try:
                    token_dict[user] = requests.get(url).json()['token']
                    print time.time() -a
                    json.dump(token_dict, f)
                    return token_dict[user]
                except:
                    json.dump(token_dict,f)
    def post_url(self,data):
        self.data = ''
        for k,v in data.items():
            self.data += '&%s=%s'%(k,v)
        self.url = 'http://s%s.game.hanjiangsanguo.com/index.php?%s&v=2017111501&v=2017111501&channel=11&imei=NoDeviceId&platform=android&lang=zh-cn&token=%s&token_uid=%s&rand=%s' % (
            self.num, self.data, self.token, self.token_uid, self.rand)
        keep_request = True
        while keep_request:
            try:
                r = requests.post(self.url,headers=headers,timeout=20)
                keep_request = False
                if r.status_code != 200:
                    r = requests.post(self.url, headers=headers,timeout=20)
                    return r.json(encoding="UTF-8")
                else:
                    return r.json( encoding="UTF-8")
            except Exception as e:
                print e
                time.sleep(0.3)
    def action(self,**kwargs):
        """动作参数m={'index':'获取基础账号密码等信息',‘get_monster_list’：“获取副本怪物列表信息”}
        """
        action_data = kwargs
        serverinfo = self.post_url(action_data)
        return serverinfo
if __name__ == '__main__':
    pass