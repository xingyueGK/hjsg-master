#-*- coding:utf-8 -8-
import os
import threading
import datetime
from utils.scheduler import schdeuler
from utils.mylog import MyLog


from task.base import  SaoDangFb
headers = {
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Upgrade-Insecure-Requests':'1',
    'Content-Type':'application/json',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

class zhujian(SaoDangFb):

    def index(self):
        #获取首页信息
        info = self.action(c='act_sword', m='index')
        '''{"status":1,"reward_right_button":0,"reward_left_button":0,"reward_right_cd":82255,"reward_left_cd":82255,"grab_list":[{"country":"\u8150\u8d25\u5929\u671d","nums":"38","level":"61","gender":"2","nickname":"\u957f\u6c5f6\u53f7","uid":"210008568318"},{"country":"\u8150\u8d25\u5929\u671d","nums":"39","level":"253","gender":"1","nickname":"\u5c0f\u9752","uid":"220002535321"},{"country":"\u608d\u5c06\u8981\u547d300","nums":"46","level":"419","gender":"1","nickname":"\u72ec\u5b64\u4ec7","uid":"280000556318"}],"rank_left":{"my_info":[],"rank":[{"uid":"280008303988","nickname":"\u5b64\u72ec\u4ec72","nums_temp":"48","rank":1,"type1":"76","num1":"6","value1":"6"},{"uid":"280000556318","nickname":"\u72ec\u5b64\u4ec7","nums_temp":"46","rank":2,"type1":"76","num1":"5","value1":"6"},{"uid":"280000186154","nickname":"\u6c34\u6676\u9f99","nums_temp":"43","rank":3,"type1":"76","num1":"4","value1":"6"},{"uid":"220002535321","nickname":"\u5c0f\u9752","nums_temp":"39","rank":4,"type1":"76","num1":"5","value1":"5"},{"uid":"210008568318","nickname":"\u957f\u6c5f6\u53f7","nums_temp":"38","rank":5,"type1":"76","num1":"4","value1":"5"},{"uid":"220000453005","nickname":"\u711a\u65e0\u5929","nums_temp":"38","rank":6,"type1":"76","num1":"3","value1":"5"},{"uid":"210008568315","nickname":"\u5173\u6000\u8776","nums_temp":"38","rank":7,"type1":"76","num1":"2","value1":"5"},{"uid":"210008568314","nickname":"\u957f\u6c5f1\u53f7","nums_temp":"38","rank":8,"type1":"76","num1":"1","value1":"5"},{"uid":"210008568606","nickname":"\u6613\u7eff\u771f","nums_temp":"38","rank":9,"type1":"76","num1":"9","value1":"4"},{"uid":"290000588739","nickname":"\u7c97\u72b7\u7684\u6e29\u67d4","nums_temp":"34","rank":10,"type1":"76","num1":"8","value1":"4"},{"uid":"280001230508","nickname":"\u90a3\u5e74\u590f\u5929","nums_temp":"24","rank":11,"type1":"76","num1":"7","value1":"4"},{"uid":"280000739666","nickname":"\u5982\u6653\u5578","nums_temp":"14","rank":12,"type1":"76","num1":"6","value1":"4"}]},"rank_right":{"my_info":[],"rank":[{"uid":"280001230508","nickname":"\u90a3\u5e74\u590f\u5929","grab_times":"7","rank":1,"type2":"4","num2":"1000","value2":"0"},{"uid":"280000556318","nickname":"\u72ec\u5b64\u4ec7","grab_times":"1","rank":2,"type2":"4","num2":"800","value2":"0"}]},"free_times":10,"times":2,"nums":0,"need_nums":"100","button_status":0,"cd_time":0,"date":"06.19-06.26","free_cost":100,"speed_cost":50}'''
        return info
    def get_reward(self):
        #获取排名奖励
        self.action(c='act_sword', m='get_rank_reward', type=0)
        self.action(c='act_sword', m='get_rank_reward', type=1)

    def act_sword(self,job,log):#铸剑
        info = self.index()
        button_status = int(info['button_status'])
        reward_right_button = info['reward_right_button']
        reward_left_button  = info['reward_left_button']
        if reward_left_button !=0 or reward_right_button != 0:
            #按键可以领取奖励
            self.get_reward()
            info = self.index()
        need_nums  = int(info['need_nums'])
        nums = int(info['nums'])
        reward_right_cd = int(info['reward_left_cd'])
        log.info('%s 需要数量%s,现有数量%s'%(self.user,need_nums,nums))
        if button_status == 0:
            #可能未开始铸剑,需要开始if
            start = self.action(c='act_sword', m='start')
            self.p(start)
            if start['status'] == 1:
                #如果状态不为1 表示不能开始继续下一步
                #小于表示时间没到领奖时间，大于表示领奖时间
                if int(start['need_nums']) > reward_right_cd /60:
                    return reward_right_cd / 60
                else:
                    return start['need_nums']

        # 如果 nums == need_nums 表示可以收获
        if need_nums == nums and reward_right_cd != 0 :
            self.p('get_cast_reward',self.action(c='act_sword', m='get_cast_reward'))
            start = self.action(c='act_sword', m='start')
            if start['status'] ==1:
                if int(start['need_nums']) > reward_right_cd / 60:
                    return reward_right_cd / 60
                else:
                    return start['need_nums']
        elif need_nums != nums and reward_right_cd != 0 :
            slp = need_nums - nums
            if int(slp) > reward_right_cd / 60:
                return reward_right_cd / 60
            else:
                return slp
        elif need_nums == nums and reward_right_cd == 0 :
            #CD为零 一天结束，领取奖励
            job_id = self.user + self.num
            self.action(c='act_sword',m='get_rank_reward',type=1)
            self.action(c='act_sword', m='get_rank_reward', type=0)
            self.action(c='act_sword', m='get_cast_reward')
            start = self.action(c='act_sword', m='start')
            if start['status'] == 1:
                if int(start['need_nums']) > reward_right_cd / 60:
                    return reward_right_cd / 60
                else:
                    return start['need_nums']
        elif need_nums != nums and reward_right_cd == 0:
            # CD为零 一天结束，领取奖励
            #移除原来的任务id
            print reward_right_cd
            job_id = self.user+self.num
            self.action(c='act_sword', m='get_rank_reward', type=1)
            self.action(c='act_sword', m='get_rank_reward', type=0)
            start = self.action(c='act_sword', m='start')
            if start['status'] == 1:
                if int(start['need_nums']) > reward_right_cd / 60:
                    return reward_right_cd / 60
                else:
                    return start['need_nums']

if __name__ == '__main__':
    s1 = threading.Semaphore(10)
    l = threading.Lock()
    log = MyLog(logpath='D:\hjsg\utils',logname='zhujian.log')
    schdeuler =schdeuler(log)
    def act(user, apass, addr,job,log):
        s1.acquire()
        action = zhujian(user, apass, addr)
        num = int(action.act_sword(job,log))
        job_id = user + addr
        #添加任务，循环调用act 函数，以便动态添加定时任务
        log.info(job.add_job(act,next_run_time=(datetime.datetime.now() + datetime.timedelta(minutes=num)),
                          args=(user,apass,addr,job,log),id=job_id))
        s1.release()
    filepath = os.path.dirname(os.path.abspath(__file__))
    cont = ['sunzi.txt']
    # cont = ['qingbing.txt']
    for t in cont:
        with open('%s/users/%s' % (filepath, t), 'r') as f:
            for i in f:
                if i.strip() and not i.startswith('#'):
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    # addr = 147
                    t1 = threading.Thread(target=act, args=(name, passwd, addr,schdeuler,log))
                    t1.start()
    schdeuler.start()
