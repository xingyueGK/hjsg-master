#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/19 15:08
# @Author  : xingyue
# @File    : lantern.py


from task.base import SaoDangFb
import threading
import os, time
import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
_redis = redis.StrictRedis(connection_pool=pool)
lock = threading.RLock()


class task(SaoDangFb):

    def lantern_festival(self):
        try:
            answer = {
                "1": "a",
                "2": "b",
                "3": "c",
                "4": "d",
                "5": "b",
                "6": "d",
                "7": "d",
                "8": "d",
                "9": "d",
                "10": "a",
                "11": "a",
                "12": "a",
                "13": "b",
                "14": "b",
                "15": "a",
                "16": "c",
                "17": "b",
                "18": "d",
                "19": "a",
                "20": "c",
                "21": "c",
                "22": "a",
                "23": "d",
                "24": "a",
                "25": "a",
                "26": "c",
                "27": "a",
                "28": "b",
                "29": "a",
                "30": "a",
                "31": "a",
                "32": "b",
                "33": "b",
                "34": "b",
                "35": "c",
                "36": "c",
                "37": "d",
                "38": "d",
                "39": "c",
                "40": "b",
            }
            resutl = self.action(c='guess_lantern', m='answer_index')
            self.p(resutl['question'])
            total_num = int(resutl['total_num'])
            print total_num
            for i in range(total_num):
                questiont = resutl['question']
                id = questiont['id']
                try:
                    formdata = {
                        'right': answer[id]
                    }
                except KeyError as e:
                    print 'id error ,chaoguo xianzhi '
                    self.p(questiont,'id')
                    formdata = {
                        'right': 'a'
                    }
                resutl = self.action(c='guess_lantern', m='check', body=formdata)
                if resutl['stauts'] ==1:
                    if resutl['right'] == 0:
                        pass
                    else:
                        self.p(resutl,'check result')
                time.sleep(0.5)
        except KeyError as e:
            self.p(resutl)
            pass

    def get_reward(self):
        self.action(c='guess_lantern', m='get_reward', id=1)


if __name__ == '__main__':
    def act(user, apass, addr):
        action = task(user, apass, addr)
        action.lantern_festival()
        action.get_reward()


    filepath = os.path.dirname(os.path.abspath(__file__))
    # cont = ['21user.txt', 'autouser.txt','gmnewyear.txt', 'user.txt', 'alluser.txt']
    cont = ['user.txt']
    for t in cont:
        with open('%s/users/%s' % (filepath, t), 'r') as f:
            for i in f:
                if i.strip() and not i.startswith('#'):
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    # addr = 21
                    t1 = threading.Thread(target=act, args=(name, passwd, addr))
                    t1.start()
                    time.sleep(0.2)
