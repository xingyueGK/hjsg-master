#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/17 17:19
# @Author  : xingyue
# @File    : autocontrib.py

#从配置文件读取账号信息
#一次循环贡献退出
#调用审批函数 通过 调用执行函数  》

import threading
import os, time
from task.base import  SaoDangFb,MyLog

logger = MyLog().MyLog()

class contrib(SaoDangFb):
    def jioncountry(self, name):  # 加入国家
        logger.info(self.user+'申请加入国家')
        minfo = self.action(c='member', m='index')
        formdata = {
            "id":14900000000360,
            "page":1
        }
        result = self.action(c='country', m='apply', body=formdata)
        if result['status'] == 1:
            # 加入国家成功返回uid ,审批使用
            logger.info(self.user + '申请成功')
            return minfo['uid']
        else:
            logger.error(self.user + '申请失败,msg:%s'%result)
    def betray(self):  # 叛国
        logger.info(self.user+"退出国家")
        self.action(c='country', m='betray')

    def get_audit_list(self,uid):  # 国家审计同意
        audit = self.action(c='country', m='get_audit_list')
        """:type {1,2} 1同意，2 忽略"""
        self.p('get_audit_list',audit)
        logger.info('同意加入国家')
        self.action(c='country', m='audit', uid=uid, type=1)

    def gongxiang(self):  # 国家贡献
        memberInfo = self.action(c='member', m='index')
        self.action(c='country', m='get_member_list')
        self.action(c='country', m='storage')
        if int(memberInfo['level']) > 90:
            print '等级大于90'
            #回调执行函数
            return  None
        flag = 0
        donate = 0
        try:
            while True:
                if flag < 10:
                    result = self.action(c='country', m='donate', type=1)
                    status = result['status']
                    if status == 1:
                        donate += 10
                        print donate
                    else:
                        flag += 1
                else:
                    break
        except:
            time.sleep(60)
            self.betray()
            logger.info(result)

if __name__ == '__main__':
    s1 = threading.Semaphore(1)
    def act(user, apass, addr):
        s1.acquire()
        action = contrib(user, apass, addr)
        uid = action.jioncountry('光芒神殿')
        if uid:
            c = contrib('pock520','5553230',149)
            #审核通过
            c.get_audit_list(uid)
        action.gongxiang()
        action.betray()
        s1.release()

    filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # cont = ['21user.txt', 'autouser.txt','gmnewyear.txt', 'user.txt', 'alluser.txt']
    cont = ['149cnm.txt']
    for t in cont:
        with open('%s/users/%s' % (filepath, t), 'r') as f:
            for i in f:
                if i.strip() and not i.startswith('#'):
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    # addr = 147
                    t1 = threading.Thread(target=act, args=(name, passwd, addr))
                    t1.start()
