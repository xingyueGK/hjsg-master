#-*- coding:utf-8 -*-
from shujufenx import  fuben
import  threading
import time


def act(user, apass):
    action = fuben(user, apass)
    gid,uid = action.general()
    print gid,uid
    for i in uid:
        print uid
        action.strengthen(i)
        action.eqip(gid,i)
    action.saodang()




with open('C:\Users\Administrator\Desktop\user.txt', 'r') as f:
    for i in f:
        str = i.strip()
        name = str + 'yue123a'
        t1 = threading.Thread(target=act, args=(name, '413728161'))
        t1.start()
        time.sleep(0.5)

