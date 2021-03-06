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
    def lanternIndex(self):
        stats = self.action(c='guess_lantern', m='index')
        if stats['status']== 1:
            print '开始答题'
        else:
            self.p(stats)
            exit(2)
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
                "41": "a",
                "42": "a",
                "44": "a",
                "45": "b",
                "46": "c",
                "48": "a",
                "49": "b",
                "50": "d",
                "51": "c",
                "52": "a",
                "54": "a",
                "55": "d",
                "56": "d",
                "58": "b",
                "59": "b",
                "61": "d",
                "62": "d",
                "63": "d",
                "67": "b",
                "68": "a",
                "69": "b",
                "71": "d",
                "73": "b",
                "74": "a",
                "75": "d",
                "76": "a",
                "77": "b",
                "78": "b",
                "43": "d",
                "47": "d",
                "53": "c",
                "57": "d",
                "60": "c",
                "64": "d",
                "65": "d",
                "66": "b",
                "70": "c",
                "72": "a",
                "79": "c",
                "80": "a",
                "81": "a",
                "82": "d",
                "83": "b",
                "84": "a",
                "85": "c",
                "86": "b",
                "87": "b",
                "88": "b",
                "89": "d",
                "90": "d",
                "91": "b",
                "92": "c",
                "93": "c",
                "94": "b",
                "95": "c",
                "96": "a",
                "97": "d",
                "98": "d",
                "99": "a",
                "100": "c",
                "101": "c",
                "102": "a",
                "103": "b",
                "104": "a",
                "105": "c",
                "106": "a",
                "107": "a",
                "108": "b",
                "109": "c",
                "110": "b",
                "111": "d",
                "112": "b",
                "113": "d",
                "114": "b",
                "115": "a",
                "116": "a",
                "117": "b",
                "118": "b",
                "119": "c",
                "120": "d",
            }
            resutl = self.action(c='guess_lantern', m='answer_index')
            time.sleep(0.5)
            total_num = int(resutl['total_num'])
            for i in range(total_num):
                questiont = resutl['question']
                id = questiont['id']
                try:
                    formdata = {
                        'right': answer[id]
                    }
                except KeyError as e:
                    print 'id error ,chaoguo xianzhi '
                    self.p(questiont, 'iderror')
                    formdata = {
                        'right': 'a'
                    }
                resutl = self.action(c='guess_lantern', m='check', body=formdata)
                self.p(resutl,'resieeeeeeee')
                while True:
                    if resutl['status'] == 1:
                        if resutl['right'] == 1:
                            time.sleep(2)
                            break
                        else:
                            self.p(resutl, 'check result')
                            print formdata
                            break
                    elif resutl['status'] == -10:
                        time.sleep(5)
                        resutl = self.action(c='guess_lantern', m='check', body=formdata)
        except KeyError as e:
            self.p(resutl, 'error')
            print 'eeeee',e

    def get_reward(self):
        self.action(c='guess_lantern', m='get_reward', id=1)


if __name__ == '__main__':
    def act(user, apass, addr):
        action = task(user, apass, addr)
        action.lanternIndex()#开始答题
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
