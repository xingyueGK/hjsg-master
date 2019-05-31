# -*- coding:utf-8 -*-


import requests
import time
import json
import  sys
import  redis
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
postheaders = {
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Upgrade-Insecure-Requests':'1',
    'Content-Type':'application/x-www-form-urlencoded',
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
        url = 'http://s{num}.game.hanjiangsanguo.com/index.php?c=login&&m=user&u={user}&p={passwd}&v=2018083101&token=&channel=11&lang=zh-cn&rand=150959405499450'.format(
            num=num, user=user, passwd=passwd)
        pool = redis.ConnectionPool(host='localhost', port=6379,db=0)
        _redis = redis.StrictRedis(connection_pool=pool)
        try:
            if _redis.hget(num,user):
                token = _redis.hget(num,user)
                login = 'http://s{num}.game.hanjiangsanguo.com/index.php?c=member&m=index&v=0&token={token}&channel=150&lang=zh-cn&rand=150959405499450'.format(
                    num=num, token=token)
                r = requests.get(login)
                if r.text == '403':
                    raise TokenErr('token expire')
                else:
                    return token
            else:
                raise TokenErr('token expire')
        except TokenErr:
                try:
                    result= requests.get(url).json()
                    if result['status'] == 1:
                        token = result['token']
                        _redis.hset(num,user,token)
                        return token
                    else:
                        print user,'账号密码不对'
                        exit(2)
                except Exception as e:
                    print e

    def post_url(self,body,data):
        self.data = ''
        for k,v in data.items():
            self.data += '&%s=%s'%(k,v)
        self.url = 'http://s%s.game.hanjiangsanguo.com/index.php?%s&v=2017111501&v=2017111501&channel=11&imei=NoDeviceId&platform=android&lang=zh-cn&token=%s&token_uid=%s&rand=%s' % (
            self.num, self.data, self.token, self.token_uid, self.rand)
        keep_request = True
        while keep_request:
            try:
                if body:
                    r = requests.post(self.url, headers=postheaders,data=body,timeout=20)
                else:
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
    def action(self,body=0,**kwargs):
        """动作参数m={'index':'获取基础账号密码等信息',‘get_monster_list’：“获取副本怪物列表信息”}
        """
        action_data = kwargs
        serverinfo = self.post_url(body,action_data)
        if serverinfo == 403:
            print self.user,'账号异常'
            exit(4)
        return serverinfo
    def level(self):
        userinfo = self.action(c='member', m='index')
        level = int(userinfo['level'])
        return level
    def unlock(self, pwd):  # 解锁密码
        self.action(c='member', m='resource_unlock', token_uid=210000353508, pwd=pwd)
    @classmethod
    def p(cls,message):
        print json.dumps(message, ensure_ascii=False)
    def get_act(self):#角色信息
        print '角色信息'
        act_info = self.action(c='member', m='index')
        return act_info
    def getWeek(self):
        week = time.strftime("%w", time.localtime())
        return week
    def general_book(self):
        try:
            index = self.action(c='general_book', m='index',perpage=18)
            addition = index['addition']
            return addition
        except:
            return None
    def get_attribute(self):
        act_info = self.get_act()
        uid = act_info['uid']
        gid = act_info['gid']
        formdata = {
            "uid":uid,
        }
        a = self.action(c='information',m='index',body=formdata)
        wuli = int(a['list']['1']['wuliup'])
        zhili = int(a['list']['1']['zhiliup'])
        if wuli > zhili:
            return  wuli
        else:
            return zhili
if __name__ == '__main__':
    pass