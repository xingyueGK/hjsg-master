#-*- coding:utf-8 -*-

import requests
import threading
import time,json
class TokenErr(Exception):
    pass

token_dict ={}
lock = threading.Lock()


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
            token_dict[user] = requests.get(url).json()['token']
            json.dump(token_dict, f)
            return token_dict[user]
with open('../users/149gmjrhy.txt', 'r') as f:
    for i in f:
        if i.strip():
            str = i.strip().split()[0]
            name = str
            passwd = i.split()[1]
            addr = 148
            threading.Thread(target=get_token,args=( addr,name,passwd)).start()
            time.sleep(1)
# while 1:#阻塞主进程确保任务生成
#     if threading.activeCount() == 1:
#         break