#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/23 11:50
# @Author  : xingyue
# @File    : redislist.py

#有序插入500W 数据 list：uid

import  redis,time

def get_redi_conn(host, port, passwd,db):
    """
    实例化连接 redis
    :param host: 主机地址
    :param port: 端口
    :param passwd: 密码
    :param db: 库
    :return: r
    """
    pool = redis.ConnectionPool(host=host,password=passwd,port=port, db=db)
    r = redis.Redis(connection_pool=pool)
    return r



def initvalue(r,keyname):
    """
    #初始值 如果redis “list:uid” 不存在 使用初始值，否则使用redis list key 最后一个值
    :param r: redis 连接实例化对象
    :param keyname: list Key
    :return: initvalue 插入的初始值
    """
    if r.exists(keyname) :
        initvalue = int(r.lindex(keyname,-1))
    else:
        initvalue = 1000000000
    return initvalue


def redis_push_pipe(r,keyname,value,splistnum):
    """
    使用redis 管道批量插入数据
    :param r:
    :param keyname:
    :param value:
    :param splistnum:
    :return:
    """
    starttime = time.time()
    #批量插入数据，一次 splistnum 个
    splistnum = splistnum
    # 将500W数据分成若干个list
    rlist = [[i + value for i in xrange(i, i + splistnum)] for i in xrange(1, 5000000, splistnum)]
    with r.pipeline(transaction=False) as p:
        # 批量插入数据，一次5000个
        for i in rlist:
            p.rpush(keyname, *i)
        p.execute()
    endtime = time.time()

    print('消耗时间%s' % (endtime - starttime))
def main():
    # 定义key
    keyname = 'list:uid'
    redis_host = 'localhost'
    redis_port = 6379
    redis_passwd = ''
    redis_db = 11
    #分成若干大小批量插入
    splistnum = 5000
    r = get_redi_conn(redis_host,redis_port,redis_passwd,redis_db)
    value = initvalue(r,keyname)
    redis_push_pipe(r,keyname,value,splistnum)

if __name__ == '__main__':
    main()