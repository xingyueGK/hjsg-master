# -*- coding:utf-8 -*-


import requests
import time
import json
import sys, os
import redis, random
from logging.handlers import RotatingFileHandler
import logging
import hashlib

reload(sys)
sys.setdefaultencoding('utf-8')
import threading

headers = {
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
postheaders = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://game.hjsg.zhanyougame.com",
    "Referer": "http://game.hjsg.zhanyougame.com/index.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
}


class TokenErr(Exception):
    pass


class SaoDangFb(object):
    def __init__(self, user, passwd, num):
        # 随机请求参数
        self.num = self.get_addr(num, user, passwd)
        self.user = user
        self.passwd = passwd
        self.token_uid = ''
        self.token = self.get_token(self.num, self.user, self.passwd)
        self.url = 'http://s{0}.game.hanjiangsanguo.com/index.php?{1}&v=0&channel=150&lang=zh-cn&token={2}&token_uid={3}&'

    @staticmethod
    def get_addr(num, u, p):
        url = 'http://uc.game.hanjiangsanguo.com/index.php?&c=user&m=login&&token=&channel=150&lang=zh-cn&rand=157355135868932'
        if num:
            return num
        else:
            result = requests.post(url, data={"u": u, "p": p}).json()
            if result['status'] != 1:
                print result['message']
                exit(result['status'])
            else:
                for item in result['serverlist']:
                    if item['selected'] == 1:
                        return int(item['id'])

    @staticmethod
    def get_token(num, user, passwd):
        pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        _redis = redis.StrictRedis(connection_pool=pool)
        try:
            if _redis.hget(num, user):
                token = _redis.hget(num, user)
                rand = str(int(time.time()))
                a = token + rand
                te = hashlib.md5(a).hexdigest()
                signature = hashlib.md5(te + "a4c13b9ecf81").hexdigest()
                login = 'http://s{num}.game.hanjiangsanguo.com/index.php?c=member&m=index&v=0&token={token}&channel=150&lang=zh-cn&rand={rand}&signature={signature}'.format(
                    num=num, token=token, rand=rand, signature=signature)

                r = requests.get(login)
                if r.text == '403':
                    raise TokenErr('token expire')
                elif r.ok:
                    return token
                else:
                    raise TokenErr('token expire')
            else:
                raise TokenErr('token expire')
        except TokenErr:
            try:
                rand = str(int(time.time()))
                a = "" + rand
                te = hashlib.md5(a).hexdigest()
                signature = hashlib.md5(te + "a4c13b9ecf81").hexdigest()
                url = 'http://s{num}.game.hanjiangsanguo.com/index.php?v=0&c=login&&m=user&&token=&channel=150&lang=zh-cn&rand={rand}&signature={signature}'.format(
                    num=num, rand=rand, signature=signature)
                formdata = {
                    "mac": "00:00:00:00:00:00",
                    "devicetoken": 000000,
                    "adid": "",
                    "u": user,
                    "p": passwd,
                    "channel": 150,
                }
                for i in range(5):
                    result = requests.post(url, headers=postheaders, data=formdata, timeout=20)
                    if result.status_code == 200:
                        if result.json()['status'] == 1:
                            print user,url
                            token = result.json()['token']
                            _redis.hset(num, user, token)
                            if token:
                                return token
                        else:
                            print user, '账号密码不对'
                            exit(2)

            except Exception as e:
                print user, e
                exit(401)
    def __get_http_session(self, pool_connections, pool_maxsize, max_retries):
        session = requests.Session()
        # 创建一个适配器，连接池的数量pool_connections, 最大数量pool_maxsize, 失败重试的次数max_retries
        adapter = requests.adapters.HTTPAdapter(pool_connections=pool_connections,
                                                pool_maxsize=pool_maxsize, max_retries=max_retries)
        # 告诉requests，http协议和https协议都使用这个适配器
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
    def post_url(self, body, data, token=None):
        rs = self.__get_http_session(pool_connections=3,pool_maxsize=10,max_retries=5)
        num = 0
        self.data = ''
        for k, v in data.items():
            self.data += '&%s=%s' % (k, v)
        self.rand = str(int(time.time()))
        # POST基础URL地址
        try:
            self.a = self.token + self.rand
        except:
            print '*' * 10, self.token
            exit(101)
        self.te = hashlib.md5(self.a).hexdigest()
        self.signature = hashlib.md5(self.te + "a4c13b9ecf81").hexdigest()
        self.urlf = self.url.format(self.num, self.data, self.token,
                                    self.token_uid) + 'rand={rand}&signature={signature}'.format(rand=self.rand,signature=self.signature)
        #postheaders['Host'] = 's{addr}.game.hanjiangsanguo.com'.format(addr=self.num)
        while num < 40:
            num += 1
            try:
                if body:
                    r = rs.post(self.urlf, headers=postheaders, data=body, timeout=20)
                else:
                    r = rs.get(self.urlf, headers=headers, timeout=20)
                if r.ok:
                    return r
                elif r.status_code >= 500:
                    pass
            except Exception as e:
                print 'post_url', e
                time.sleep(1)


    def action(self, body=0, **kwargs):
        """动作参数m={'index':'获取基础账号密码等信息',‘get_monster_list’：“获取副本怪物列表信息”}
        """
        action_data = kwargs
        try:
            postresult = self.post_url(body, action_data)
            serverinfo = postresult.json(encoding="UTF-8")
            if serverinfo == 403:
                time.sleep(3)
                # 重新初始化
                self.token = self.get_token(self.num, self.user, self.passwd)
                postresult = self.post_url(body, action_data)
                serverinfo = postresult.json(encoding="UTF-8")
            try:
                status = int(serverinfo['status'])
                if status == 1 or status == 0:
                    return serverinfo
                else:
                    print status,serverinfo['msg']
            except Exception as e:
                print e,self.p(serverinfo)
            return serverinfo
        except ValueError as e:
            print postresult.content, postresult.headers, postresult.raw, postresult.url

    def level(self):
        userinfo = self.action(c='member', m='index')
        level = int(userinfo['level'])
        return level

    def unlock(self, pwd):  # 解锁密码
        self.action(c='member', m='resource_unlock', token_uid=210000353508, pwd=pwd)

    @classmethod
    def p(cls, message, c='cls'):
        msg = '方法：%s, json: %s' % (c, json.dumps(message, ensure_ascii=False))
        print(msg)
        return msg

    def get_act(self):  # 角色信息
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
            index = self.action(c='general_book', m='index', perpage=18)
            addition = index['addition']
            return addition
        except:
            return None

    def get_attribute(self):
        act_info = self.get_act()
        uid = act_info['uid']
        formdata = {
            "uid": uid,
        }
        a = self.action(c='information', m='index', body=formdata)
        wuli = int(a['list']['1']['wuliup'])
        zhili = int(a['list']['1']['zhiliup'])
        if wuli > zhili:
            return 'wuli'
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
    def my_listener(self, event):
        if event.exception:
            print('The job crashed :(')  # or logger.fatal('The job crashed :(')
        else:
            print('The job worked :)')

    def MyLog(self, logpath=None, logname='mylog.log'):
        """
        :param logpath: dir
        :param logname: str(name)
        :return: logger
        """
        if logpath:
            if not os.path.exists(logpath):
                os.makedirs(logpath)
                _log = os.path.join(logpath, logname)
            else:
                _log = os.path.join(logpath, logname)
        else:
            _log = logname

        format = logging.Formatter(
            '%(asctime)s %(filename)s[line:%(lineno)d] [%(username)s:%(addr)s] %(levelname)s %(message)s')
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = RotatingFileHandler(_log, mode='a', maxBytes=1024 * 1024, backupCount=3, encoding='utf-8')
        handler.setLevel(logging.INFO)
        handler.setFormatter(format)
        logger.addHandler(handler)
        filter = ContextFilter()
        logger.addFilter(filter)
        return logger
