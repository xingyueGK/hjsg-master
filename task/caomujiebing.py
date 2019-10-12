#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/23 15:48
# @Author  : xingyue
# @File    : caomujiebing.py

#草木接兵任务
#1、任务流程 获取 每日任务信息 get_today_schedule
#2、获取可以进入列表 get_enter_list
#3、进入指定的列表  enter
class Flag(object):
    def get_today_schedule(self):
        #获取
        """{"status":1,"data":{"enter_desc":[{"id":"1","type":"1","desc":"1.\u5728\u6bd4\u8d5b\u65e5\u5f53\u59298\u70b9\u524d\uff0c\u6240\u6709\u6709\u6bd4\u8d5b\u7684\u670d\u52a1\u5668\u524d\u6f14\u6b66\u699c\u524d100\u540d\u4e14\u4e3b\u516c\u7b49\u7ea7\u8fbe\u5230240\u7ea7\u7684\u73a9\u5bb6\u53ef\u4ee5\u624b\u52a8\u62a5\u540d\u53c2\u4e0e\u6d3b\u52a8"},{"id":"2","type":"1","desc":"2.\u65e0\u8bba\u5df1\u65b9\u670d\u52a1\u5668\u6709\u65e0\u6bd4\u8d5b\uff0c\u6f14\u6b66\u699c\u524d100\u540d\u73a9\u5bb6\u5747\u53ef\u62a5\u540d\u53c2\u4e0e\u5f00\u542f\u5916\u63f4\u7684\u670d\u52a1\u5668\u7684\u6218\u6597\uff08\u4e0d\u80fd\u53c2\u52a0\u5df1\u65b9\u654c\u5bf9\u670d\u52a1\u5668\uff09"},{"id":"3","type":"1","desc":"3.\u524d\u4e00\u5929\u6f14\u6b66\u699c\u524d\u4e24\u540d\u81ea\u52a8\u6210\u4e3a\u76df\u4e3b\u548c\u526f\u76df\u4e3b\u3002\u76df\u4e3b\u548c\u526f\u76df\u4e3b\u53ef\u4ee5\u5f00\u542f\u3001\u5173\u95ed\u5916\u63f4\u529f\u80fd\uff0c\u53ef\u4ee5\u8c03\u914d\u90e8\u961f\uff0c\u53ef\u4ee5\u8e22\u51fa\u73a9\u5bb6\uff0c\u53ef\u4ee5\u4fee\u6539\u516c\u544a\u5e76\u81ea\u52a8\u4eab\u6709\u6218\u573a\u6307\u6325\u529f\u80fd"},{"id":"4","type":"1","desc":"4.\u6bcf\u4e2a\u73a9\u5bb6\u540c\u65f6\u53ea\u80fd\u53c2\u52a0\u4e00\u4e2a\u670d\u52a1\u5668\u7684\u6218\u6597"}],"schedule":[{"id":"59","season":"1","round":"5","phase":"20190923","serverid1":"86","serverid2":"149","open1":0,"open2":"0","score1":"0","score2":"0","win":"0"},{"id":"60","season":"1","round":"5","phase":"20190923","serverid1":"66","serverid2":"3042","open1":"0","open2":"0","score1":"0","score2":"0","win":"0"},{"id":"61","season":"1","round":"5","phase":"20190923","serverid1":"3034","serverid2":"3029","open1":"0","open2":"0","score1":"0","score2":"0","win":"0"},{"id":"62","season":"1","round":"5","phase":"20190923","serverid1":"110","serverid2":"150","open1":"0","open2":"0","score1":"0","score2":"0","win":"0"},{"id":"63","season":"1","round":"5","phase":"20190923","serverid1":"3006","serverid2":"98","open1":"0","open2":"0","score1":"0","score2":"0","win":"0"},{"id":"64","season":"1","round":"5","phase":"20190923","serverid1":"20","serverid2":"46","open1":"0","open2":"0","score1":"0","score2":"0","win":"0"},{"id":"65","season":"1","round":"5","phase":"20190923","serverid1":"30","serverid2":"8","open1":"0","open2":"0","score1":"0","score2":"0","win":"0"}],"self_server":149,"enemy_server":"86","enter_server":0}}"""
        get_today_schedule =self.action(c='flag',m='get_today_schedule')
        return  get_today_schedule

    def get_enter_list(self,serverid):
        """{"status":1,"kick":0,"switch":0,"army_list":[{"enter":0,"limit":30,"list":[],"army":{"name":"\u6218\u6597\u90e8\u961f","desc":"\u51fb\u6740\u654c\u4eba\uff0c\u4fdd\u62a4\u5df1\u65b9\u593a\u65d7\u90e8\u961f","move":"3","alive":"1","recover":"3","fight":"1"}},{"enter":0,"limit":15,"list":[],"army":{"name":"\u5668\u68b0\u90e8\u961f","desc":"\u653b\u53d6\u636e\u70b9\uff0c\u64cd\u4f5c\u636e\u70b9\u5f00\u5173","move":"1","alive":"2","recover":"2","fight":"3"}},{"enter":0,"limit":5,"list":[],"army":{"name":"\u593a\u65d7\u90e8\u961f","desc":"\u593a\u53d6\u6218\u65d7\uff0c\u4fdd\u62a4\u6218\u65d7","move":"2","alive":"3","recover":"1","fight":"2"}}],"total_enter":0,"total_limit":50,"enter_soldier":0,"manager":0,"foreign":"0","announcement":"","enter_cd":16946}"""
        get_enter_list =self.action(c='flag',m='get_enter_list',serverid=serverid)
        return  get_enter_list
    def enter(self,serverid,soldier=1):
        """

        :param serverid:
        :param soldier:  战斗部队 1,2,3 ，默认加入战斗部队
        :return:
        """
        formdata = {
            "serverid":serverid,
            "soldier":soldier
        }
        enter =self.action(c='flag',m='enter',body=formdata)
        self.p(enter)