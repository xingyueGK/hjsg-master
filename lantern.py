#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/19 15:08
# @Author  : xingyue
# @File    : lantern.py


from task.base import SaoDangFb
import threading
import os,time
import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
_redis = redis.StrictRedis(connection_pool=pool)
lock = threading.RLock()

class task(SaoDangFb):

    def lantern_festival(self):
        try:
            answer = {
                "48": "c", "10": "c", "42": "a", "27": "b", "39": "b", "5": "d", "14": "c",
                "50": "d", "47": "c", "33": "b", "23": "d", "45": "b", "15": "b", "4": "d",
                "18": "c", "35": "d", "12": "b", "29": "c", "41": "a", "20": "b",
                "32": "a", "6": "d", "3": "d", "22": "a", "17": "a", "37": "a",
                "43": "a", "49": "d", "7": "a", "2": "a", "30": "a", "9": "a",
                "46": "b", "21": "c", "31": "b", "16": "d", "25": "b", "13": "d",
                "28": "a", "40": "c", "26": "a", "36": "b", "44": "b", "1": "c",
                "38": "b", "11": "b", "34": "c", "19": "d", "8": "d"
            }
            for i in range(1, 16):
                resutl = self.action(c='lantern_festival', m='question_index', position=i)
                questiont = resutl['question']
                id = questiont['id']
                anserresutl = self.action(c='lantern_festival', m='answer', position=i, answer=answer[id])
                if anserresutl['right_num'] >= "8":
                    return None
                if anserresutl['is_right'] == 0:
                    self.p(questiont)
        except:
            pass


if __name__ == '__main__':
    def act(user, apass, addr):
        action = task(user, apass, addr)
        action.lantern_festival()

    filepath = os.path.dirname(os.path.abspath(__file__))
    # cont = ['21user.txt', 'autouser.txt','gmnewyear.txt', 'user.txt', 'alluser.txt']
    cont = ['21user.txt']
    for t in cont:
        with open('%s/users/%s' % (filepath, t), 'r') as f:
            for i in f:
                if i.strip() and not i.startswith('#'):
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    #addr = 147
                    t1 = threading.Thread(target=act, args=(name, passwd, addr))
                    t1.start()
                    time.sleep(0.2)