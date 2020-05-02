# -*- coding:utf-8 -*-


import requests
import time
import json
import  sys,os
import  redis
from logging.handlers import RotatingFileHandler
import logging
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
        self.num = self.get_addr(num,user,passwd)
        self.user = user
        self.passwd = passwd
        self.rand = int(time.time()*1000)
        self.token_uid = ''
        self.token = self.get_token(self.num, self.user, self.passwd)
        #POST基础URL地址
        self.url = 'http://s{0}.game.hanjiangsanguo.com/index.php?{1}&v=0&channel=150&lang=zh-cn&token={2}&token_uid={3}&rand={4}'.format(self.num,'{data}',self.token,self.token_uid,self.rand)
    @staticmethod
    def get_addr(num,u,p):
        url = 'http://uc.game.hanjiangsanguo.com/index.php?&c=user&m=login&&token=&channel=150&lang=zh-cn&rand=157355135868932'
        if num:
           return num
        else:
            result = requests.post(url,data={"u":u,"p":p}).json()
            if result['status'] !=1:
                print(result['message'])
                exit(result['status'])
            else:
                for item in result['serverlist']:
                    if item['selected'] ==1:
                        return int(item['id'])
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
                        print(user,'账号密码不对')
                        exit(2)
                except Exception as e:
                    print(e)

    def post_url(self,body,data):
        self.data = ''
        for k,v in data.items():
            self.data += '&%s=%s'%(k,v)
        url =  self.url.format(data=self.data)
        keep_request = True
        while keep_request:
            try:
                if body:
                    r = requests.post(url, headers=postheaders,data=body,timeout=20)
                else:
                    r = requests.post(url,headers=headers,timeout=20)
                keep_request = False
                if r.status_code != 200:
                    r = requests.post(url, headers=headers,timeout=20)
                    r.encoding = 'utf-8'
                    return r.json(encoding="UTF-8")
                else:
                    return r.json( encoding="UTF-8")
            except Exception as e:
                print(e)
                time.sleep(0.3)
    def action(self,body=0,**kwargs):
        """动作参数m={'index':'获取基础账号密码等信息',‘get_monster_list’：“获取副本怪物列表信息”}
        """
        action_data = kwargs
        serverinfo = self.post_url(body,action_data)
        if serverinfo == 403:
            print(self.user,u'账号异常')
            return 403
        return serverinfo
    def level(self):
        userinfo = self.action(c='member', m='index')
        level = int(userinfo['level'])
        return level
    def unlock(self, pwd):  # 解锁密码
        self.action(c='member', m='resource_unlock', token_uid=210000353508, pwd=pwd)
    @classmethod
    def p(cls,message,c='cls'):
        msg = '方法：%s, json: %s'%(c ,json.dumps(message, ensure_ascii=False))
        print(msg)
        return msg
    def get_act(self):#角色信息
        act_info = self.action(c='member', m='index')
        return act_info
    def getWeek(self):
        week = time.strftime("%w", time.localtime())
        return week

    def get__function_name(self):
        import inspect
        '''获取正在运行函数(或方法)名称'''
        return inspect.stack()[1][3]
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
        formdata = {
            "uid":uid,
        }
        a = self.action(c='information',m='index',body=formdata)
        wuli = int(a['list']['1']['wuliup'])
        zhili = int(a['list']['1']['zhiliup'])
        if wuli > zhili:
            return  'wuli'
        else:
            return 'zhili'

import logging
class ContextFilter(logging.Filter):

    username = 'USER'
    addr = 'ADDR'

    def filter(self, record):

        record.addr = self.addr
        record.username = self.username
        return True

class MyLog(object):
    def my_listener(self,event):
        if event.exception:
            print('The job crashed :(') # or logger.fatal('The job crashed :(')
        else:
            print('The job worked :)')

    def MyLog(self,logpath=None,logname='mylog.log'):
        """
        :param logpath: dir
        :param logname: str(name)
        :return: logger
        """
        if logpath :
            if  not os.path.exists(logpath):
                os.makedirs(logpath)
                _log = os.path.join(logpath,logname)
            else:
                _log = os.path.join(logpath,logname)
        else:
            _log = logname

        format = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] [%(username)s:%(addr)s] %(levelname)s %(message)s')
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = RotatingFileHandler(_log,mode='a',maxBytes=1024*1024,backupCount=3,encoding='utf-8')
        handler.setLevel(logging.INFO)
        handler.setFormatter(format)
        logger.addHandler(handler)
        filter = ContextFilter()
        logger.addFilter(filter)
        return logger

