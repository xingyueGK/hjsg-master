#-*- coding:utf-8 -8-
import threading
import time
import requests

headers = {
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Upgrade-Insecure-Requests':'1',
    'Content-Type':'application/json',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

class SaoDangFb(object):
    def  __init__(self,user,passwd,num):
        #随机请求参数
        self.num = num
        self.user = user
        self.passwd = passwd
        self.rand = str(int(time.time()*1000))
        self.token_uid = '210000353508'
        self.token = self.get_token(self.num,self.user,self.passwd)#账号密码
        #POST基础URL地址
        self.url = 'http://s{}.game.hanjiangsanguo.com/index.php?v=0&channel=150&lang=zh-cn&token={}&token_uid={}&rand={}&'.format(self.num,self.token,self.token_uid,self.rand)
    @staticmethod
    def get_token(num, user, passwd):
        url = 'http://s{num}.game.hanjiangsanguo.com/index.php?u={user}&p={passwd}&v=0&c=login&&m=user&&token=&channel=150&lang=zh-cn&rand=150959405499450'.format(
            num=num, user=user, passwd=passwd)
        token = requests.session().get(url).json()
        return token['token']

    def post_url(self,data):
        for k,v in data.items():
            self.url += '&%s=%s'%(k,v)
        try:
            r = requests.post(self.url,headers=headers)
        except Exception:
            pass
        if r.status_code != 200:
            print r.status_code
            exit(2)
        else:
            return r.json( encoding="UTF-8")
    def action(self,**kwargs):
        """动作参数m={'index':'获取基础账号密码等信息',‘get_monster_list’：“获取副本怪物列表信息”}
        """
        action_data = kwargs
        serverinfo = self.post_url(action_data)
        return serverinfo
    def act_sword(self):#铸剑
        self.action(c='act_sword', m='start')
        #print self.action(c='act_sword', m='battle', touid='291000034922')
        info = self.action(c='act_sword',m='index')

        self.action(c='act_sword',m='get_rank_reward',type=1)
        self.action(c='act_sword', m='get_rank_reward', type=0)
        need_nums  = int(info['need_nums'])
        nums = info['nums']
        print need_nums,nums
        #收获
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
            time.sleep(slp*50)
if __name__ == '__main__':
    def act(user,apass,addr):
        action = SaoDangFb(user,apass,addr)
        action.act_sword()
    with open('../users/alluser.txt', 'r') as f:
        for i in f:
            name = i.split()[0]+'yue123a'
            passwd =  i.split()[1]
            addr=21
            t1 = threading.Thread(target=act, args=(name,passwd,addr))
            t1.start()