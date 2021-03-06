#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/23 16:51
# @Author  : xingyue
# @File    : worldoverseastradexiaohao.py

from overseastrade import OverseaStrade

#所有的号都丛redis中去获取队列

import threading,os

import redis
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
_redis = redis.StrictRedis(connection_pool=pool)

teamvale = "teamid"


def main(user, apass, addr,lockpwd):
    print user,'kaishi'
    action = OverseaStrade(user, apass, addr)
    index = action.world_index()
    info = index['info']
    times = int(info['times'])
    if times == 0:
        print user,'剩余次数为零 '
        return  False
    print user,' 剩余次数为',times
    print '选择商船'
    action.renovate_ship()
    action.harbour_list()
    print '打开商店'
    world_goods_list = action.world_goods_list()
    if world_goods_list['status'] !=1:
        print world_goods_list['msg']
        return  False
    if world_goods_list['choose_status'] != 1:
        print '开始选择商品'
        """
        harbour 1 是银币 2 是紫石头 3是声望 4是战功
        quality 是商品的等级 3级别以上的才买
        """
        #目前设定 不买1 银币的东西
        harbour = [2,3,4]
        quality = 3
        action.unlock(lockpwd)
        id = ""
        #选先看是否为刷新过了商品意外退出
        for item in world_goods_list['list']:
            if int(item['quality']) > quality and int(item['harbour']) in harbour:
                action.log.info('console获取到了商品信息{name}'.format(name=item['name']))
                print 'console获取到了商品信息{name}'.format(name = item['name'])
                id = item['id']
                break
        if id:
            action.log.info('获取到了商品信息id {id}'.format(id=id))
            print '获取到了商品信息id {id}'.format(id=id)
            #表示获取到了设定的商品
            action.choose_world_goods(goods_id=id)
        else:#没有获取到设定的商品，只能获取最符合要求的
            print 'meiyougengfuhede'
            flag = True
            flush = 1
            while flag and flush <6:
                # 最多刷新6次
                print '第{num}刷新商品'.format(num=flush)
                renovate = action.renovate_world_goods()
                for item in renovate['list']:
                    print item['id'],item['name'],item['quality'],item['harbour']
                    if int(item['quality']) > quality and int(item['harbour']) in harbour:
                        print '刷新搞到了 65行出'
                        id = item['id']
                        flag = False
                        break
                flush +=1
            if id:
                print '获取到了合适的商品{id}'.format(id=id)
                action.log.info('获取到了商品信息')
                # 表示获取到了设定的商品
                action.choose_world_goods(goods_id=id)
            else:
                print '没有符合要求的'
                world_goods_list = action.world_goods_list()
                r = sorted(world_goods_list['list'], key=lambda k: k['quality'], reverse=True)
                for item in r :
                    if int(item['harbour']) in harbour:
                        id = item['id']
                        action.choose_world_goods(goods_id=id)
                        break
    else:
        for item in world_goods_list['list']:
            if item['status'] == 1:
                print '已经选择了商品%s'%item['name']
    print '开始组队'
    get_list_from_world = action.get_list_from_world()
    #如果redis 有key 则从redis 取，没有创建
    #判断大区是什么
    ip149 = [i for i in range(145,150) ]
    ip21 = [21,22,25,26,29,30]
    worldkey = 'set:worldstrade:{addr}'.format(addr=149)
    ip = int(addr)
    oip = None
    if ip in ip149:
        print '大区为149'
        oip = 149
        worldkey =  'set:worldstrade:{addr}'.format(addr=149)
    elif ip in ip21:
        print '大区为 21'
        oip = 21
        worldkey = 'set:worldstrade:{addr}'.format(addr=21)

    #查看是否有这个ID 有返回1 ，没有返回0
    r_teamlist = _redis.exists(worldkey)

    team_id = int(get_list_from_world['team_id'])
    if team_id == 0 and r_teamlist:
        #表示没有队伍，并且redis 有
        v = _redis.get(worldkey)
        print '没有队伍，获取redis 数据 %s' %v
        id = v.split(':')[0]
        s = int(v.split(':')[1])
        place = v.split(':')[2]
        page = v.split(':')[3]
        user = v.split(':')[4]
        addr = v.split(':')[5]
        passwd = v.split(':')[6]
        print '加入队伍'
        join_world_team = action.join_world_team(s+1,place,page,id)
        if join_world_team['status'] == 1:
            #第二个队友加入队伍后，调账号跑船
            print '组队成功'
            _redis.delete(worldkey)
            print 'teamid{oip}'.format(oip=oip), id
            OverseaStrade(user, passwd, addr).world_start()
            _redis.lpush('teamid{oip}'.format(oip=oip), id)
            #_redis.lpush('teamid{oip}'.format(oip=oip), team_id)
        else:
            print '组队失败'
            action.p(join_world_team)
            _redis.delete(worldkey)
            main(user, apass, addr,lockpwd)
    elif team_id == 0 and not r_teamlist:
        # 表示没有队伍，并且redis 也没有
        print '没有队伍， 没有已房间，创建新房间'
        num =1
        while True:
            print '进入循环创建房间 %s' %num
            join_world_team = action.join_world_team(1, 4, 10)
            if join_world_team['status'] ==1:
                team_id = join_world_team['team_id']
                status = join_world_team['status']
            else:
                action.p(join_world_team)
                join_world_team = action.join_world_team(1, 1, 10)
                #表示未选择货物
                team_id = join_world_team['team_id']
                status = join_world_team['status']
            if status == 1:
                v = "{id}:{site}:{place}:{page}:{username}:{addr}:{passwd}".format(id=team_id, site = 1, place=1, page = 10,username= user,addr=addr,passwd = apass)
                action.log.info('创建新房间成功，存入redis key:value %s'%v)
                print '创建成功'
                _redis.setnx(worldkey, v)
                break
            else:
                print '创建新房间失败，重新创建'
                action.log.error('创建新房间失败，重新创建')
                join_world_team = action.join_world_team(1, 1, 10)
                status = join_world_team['status']
                if status == 1:
                    v = "{id}:{site}:{place}:{page}:{username}:{addr}:{passwd}".format(id=team_id, site=1, place=1,
                                                                                       page=10, username=user,
                                                                                       addr=addr, passwd=apass)
                    action.log.info('创建新房间成功，存入redis key:value %s' % v)
                    print '创建新房间成功'
                    _redis.setnx(worldkey, v)
                    break
                else:
                    print '创建新房间失败'
                    num +=1
    else:
        action.quit()
        print '已经有队伍了,不在控制范围内，退出队伍'
        action.log.info('已经有队伍了,不在控制范围内，退出队伍')
        main(user, apass, addr,lockpwd)
if __name__ == '__main__':
    s1 = threading.Semaphore(1)
    def act(user, apass, addr,lockpwd):
        s1.acquire()
        main(user, apass, addr,lockpwd)
        s1.release()

    filepath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # cont = ['21user.txt', 'autouser.txt','gmnewyear.txt', 'user.txt', 'alluser.txt']
    cont = ['user.txt']
    for t in cont:
        with open('%s/users/%s' % (filepath, t), 'r') as f:
            for i in f:
                if i.strip() and not i.startswith('#'):
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    try:
                        lockpwd = i.split()[3]
                    except:
                        lockpwd = None
                    # addr = 147
                    t1 = threading.Thread(target=act, args=(name, passwd, addr,lockpwd))
                    t1.start()